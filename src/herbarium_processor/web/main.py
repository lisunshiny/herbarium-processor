from fastapi import FastAPI, UploadFile, File, HTTPException, Body
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from uuid import uuid4
from pathlib import Path
from typing import List, Dict
import shutil
import csv

from herbarium_processor.config import ROOT_DIR, TMP_DIR
from herbarium_processor.core.ocr.ocr_client import OcrClient
from herbarium_processor.core.inference import create_prompt_builder_from_yaml
from herbarium_processor.core.inference.label_extraction_batch_runner import LabelExtractionBatchRunner
from herbarium_processor.core.types.specimen_label import SpecimenLabel


app = FastAPI(title="Herbarium Processor Web")

STATIC_DIR = Path(__file__).parent / "static"
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
app.mount("/tmp", StaticFiles(directory=TMP_DIR), name="tmp")

MAX_FILES = 10


@app.get("/", response_class=HTMLResponse)
async def index():
    return (STATIC_DIR / "index.html").read_text()

@app.post("/upload")
async def upload(files: List[UploadFile] = File(...)):
    if not files or len(files) > MAX_FILES:
        raise HTTPException(status_code=400, detail=f"Upload between 1 and {MAX_FILES} images")

    job_id = str(uuid4())
    job_dir = TMP_DIR / f"job_{job_id}"
    images_dir = job_dir / "images"
    images_dir.mkdir(parents=True, exist_ok=True)

    ocr = OcrClient()
    targets: List[SpecimenLabel] = []
    for f in files:
        dest = images_dir / f.filename
        dest.write_bytes(await f.read())
        rel_path = dest.relative_to(ROOT_DIR)
        ocr.extract_text_json(str(rel_path))
        bound_src = TMP_DIR / f"ocr_bounding_{dest.stem}.jpg"
        if bound_src.exists():
            shutil.copy(bound_src, job_dir / bound_src.name)
        ocr_json = TMP_DIR / f"ocr_ai_input_{dest.stem}.json"
        targets.append(
            SpecimenLabel(id=dest.stem, img_path=str(rel_path), ocr_path=str(ocr_json.relative_to(ROOT_DIR)))
        )

    builder = create_prompt_builder_from_yaml("prompts/configs/web_prompt.yaml")

    csv_rel = (job_dir / "results.csv").relative_to(ROOT_DIR)
    runner = LabelExtractionBatchRunner(
        output_csv_path=str(csv_rel),
        output_dir=str(job_dir.relative_to(ROOT_DIR)),
        prompt_builder=builder,
        targets=targets,
    )

    # TODO: Offload this work to a background task queue like Celery
    runner.run()

    return {"job_id": job_id}


@app.get("/results/{job_id}")
async def get_results(job_id: str):
    job_dir = TMP_DIR / f"job_{job_id}"
    csv_path = job_dir / "results.csv"
    if not csv_path.exists():
        raise HTTPException(status_code=404, detail="Results not found")
    with open(csv_path, newline="") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        fieldnames = reader.fieldnames or []
    for row in rows:
        row["ocr_image"] = f"/tmp/job_{job_id}/ocr_bounding_{row['id']}.jpg"
    return {"fieldnames": fieldnames, "rows": rows}


@app.post("/finalize/{job_id}")
async def finalize(job_id: str, rows: List[Dict[str, str]] = Body(...)):
    job_dir = TMP_DIR / f"job_{job_id}"
    if not job_dir.exists():
        raise HTTPException(status_code=404, detail="Job not found")
    final_csv = job_dir / "final.csv"
    if not rows:
        raise HTTPException(status_code=400, detail="No data provided")
    fieldnames = list(rows[0].keys())
    with open(final_csv, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    return {"status": "ok"}

@app.get("/download/{job_id}")
async def download(job_id: str):
    job_dir = TMP_DIR / f"job_{job_id}"
    csv_path = job_dir / "final.csv"
    if not csv_path.exists():
        csv_path = job_dir / "results.csv"
    if not csv_path.exists():
        raise HTTPException(status_code=404, detail="Results not found")
    return FileResponse(csv_path, media_type="text/csv", filename=csv_path.name)

