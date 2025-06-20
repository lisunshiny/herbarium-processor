from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from uuid import uuid4
from pathlib import Path
from typing import List

from herbarium_processor.config import ROOT_DIR, TMP_DIR
from herbarium_processor.core.ocr.ocr_client import OcrClient
from herbarium_processor.core.inference.prompt_builder import PromptBuilder
from herbarium_processor.core.inference.label_extraction_batch_runner import LabelExtractionBatchRunner
from herbarium_processor.core.types.specimen_label import SpecimenLabel

FIELD_LIST = ["taxon", "locality", "coordinates", "date", "elevation", "id", "substrate"]

app = FastAPI(title="Herbarium Processor Web")

STATIC_DIR = Path(__file__).parent / "static"
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

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
        ocr_json = TMP_DIR / f"ocr_ai_input_{dest.stem}.json"
        targets.append(
            SpecimenLabel(id=dest.stem, img_path=str(rel_path), ocr_path=str(ocr_json.relative_to(ROOT_DIR)))
        )

    builder = PromptBuilder(
        csv_path="data/csv/fake_canonical.csv",
        field_list=FIELD_LIST,
        shot_data=[],
        template_path="prompts/templates/herbarium_prompt.j2",
    )

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

@app.get("/download/{job_id}")
async def download(job_id: str):
    csv_path = TMP_DIR / f"job_{job_id}" / "results.csv"
    if not csv_path.exists():
        raise HTTPException(status_code=404, detail="Results not found")
    return FileResponse(csv_path, media_type="text/csv", filename="results.csv")

