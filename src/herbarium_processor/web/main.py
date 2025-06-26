from fastapi import FastAPI, UploadFile, File, HTTPException, Body
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from uuid import uuid4
from pathlib import Path
from typing import List, Dict
from pydantic import BaseModel
import shutil
import csv

from herbarium_processor.config import ROOT_DIR, TMP_DIR
from herbarium_processor.core.ocr.ocr_client import OcrClient
from herbarium_processor.core.inference import create_prompt_builder_from_yaml
from herbarium_processor.core.inference.label_extraction_batch_runner import (
    LabelExtractionBatchRunner,
)
from herbarium_processor.core.types.specimen_label import SpecimenLabel
from herbarium_processor.core.image.image_utils import (
    convert_heic_to_jpg_no_resize,
    preprocess_image_file_no_resize,
    crop_rotate_and_resize,
)


app = FastAPI(title="Herbarium Processor Web")

STATIC_DIR = Path(__file__).parent / "static"
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
app.mount("/tmp", StaticFiles(directory=TMP_DIR), name="tmp")

MAX_FILES = 10


class CropOperation(BaseModel):
    filename: str
    x: float = 0.0
    y: float = 0.0
    width: float = 0.0
    height: float = 0.0
    rotate: float = 0.0


@app.get("/", response_class=HTMLResponse)
async def index():
    return (STATIC_DIR / "index.html").read_text()


@app.get("/edit/{job_id}", response_class=HTMLResponse)
async def edit(job_id: str):
    return (STATIC_DIR / "index.html").read_text()


@app.post("/upload")
async def upload(files: List[UploadFile] = File(...)):
    if not files or len(files) > MAX_FILES:
        raise HTTPException(
            status_code=400, detail=f"Upload between 1 and {MAX_FILES} images"
        )

    job_id = str(uuid4())
    job_dir = TMP_DIR / f"job_{job_id}"
    images_dir = job_dir / "images"
    images_dir.mkdir(parents=True, exist_ok=True)

    images = []
    for f in files:
        dest = images_dir / f.filename
        dest.write_bytes(await f.read())
        if dest.suffix.lower() == ".heic":
            new_path = convert_heic_to_jpg_no_resize(dest)
            if new_path:
                dest = Path(new_path)
        preprocess_image_file_no_resize(dest)
        images.append(f"/tmp/job_{job_id}/images/{dest.name}")
    return {"job_id": job_id, "images": images}


@app.post("/sanitize/{job_id}")
async def sanitize(job_id: str, ops: List[CropOperation] = Body(...)):
    job_dir = TMP_DIR / f"job_{job_id}"
    images_dir = job_dir / "images"
    if not images_dir.exists():
        raise HTTPException(status_code=404, detail="Job not found")

    ocr = OcrClient()
    targets: List[SpecimenLabel] = []
    for op in ops:
        path = images_dir / op.filename
        crop = (op.x, op.y, op.width, op.height)
        angle = op.rotate
        crop_rotate_and_resize(path, crop, angle)
        rel_path = path.relative_to(ROOT_DIR)
        ocr.extract_text_json(str(rel_path))
        bound_src = TMP_DIR / f"ocr_bounding_{path.stem}.jpg"
        if bound_src.exists():
            shutil.copy(bound_src, job_dir / bound_src.name)
        ocr_json = TMP_DIR / f"ocr_ai_input_{path.stem}.json"
        targets.append(
            SpecimenLabel(
                id=path.stem,
                img_path=str(rel_path),
                ocr_path=str(ocr_json.relative_to(ROOT_DIR)),
            )
        )

    builder = create_prompt_builder_from_yaml("prompts/configs/default_prompt.yaml")

    csv_rel = (job_dir / "results.csv").relative_to(ROOT_DIR)
    runner = LabelExtractionBatchRunner(
        output_csv_path=str(csv_rel),
        output_dir=str(job_dir.relative_to(ROOT_DIR)),
        system_instructions_path="prompts/ocr_system_instructions_no_citations.md",
        prompt_builder=builder,
        targets=targets,
    )

    runner.run()

    return {"status": "ok"}


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
