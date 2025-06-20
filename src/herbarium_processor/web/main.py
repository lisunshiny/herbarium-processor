from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from uuid import uuid4
from pathlib import Path
from typing import List
import threading
import io
import sys
from contextlib import redirect_stdout

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

job_logs: dict[str, list[str]] = {}
job_status: dict[str, str] = {}


class LogCapture(io.StringIO):
    def __init__(self, job_id: str, orig_stdout):
        super().__init__()
        self.job_id = job_id
        self.orig = orig_stdout

    def write(self, s: str):
        self.orig.write(s)
        job_logs.setdefault(self.job_id, []).append(s)

    def flush(self):
        self.orig.flush()


def process_job(job_id: str, files_data: list[tuple[str, bytes]]):
    job_status[job_id] = "processing"
    job_dir = TMP_DIR / f"job_{job_id}"
    images_dir = job_dir / "images"
    images_dir.mkdir(parents=True, exist_ok=True)

    with redirect_stdout(LogCapture(job_id, sys.stdout)):
        ocr = OcrClient()
        targets: List[SpecimenLabel] = []
        for fname, data in files_data:
            dest = images_dir / fname
            dest.write_bytes(data)
            rel_path = dest.relative_to(ROOT_DIR)
            ocr.extract_text_json(str(rel_path))
            ocr_json = TMP_DIR / f"ocr_ai_input_{dest.stem}.json"
            targets.append(
                SpecimenLabel(
                    id=dest.stem,
                    img_path=str(rel_path),
                    ocr_path=str(ocr_json.relative_to(ROOT_DIR)),
                )
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

        try:
            runner.run()
            job_status[job_id] = "complete"
        except Exception as e:
            job_logs.setdefault(job_id, []).append(f"Error: {e}\n")
            job_status[job_id] = "error"


@app.get("/", response_class=HTMLResponse)
async def index():
    return (STATIC_DIR / "index.html").read_text()

@app.post("/upload")
async def upload(files: List[UploadFile] = File(...)):
    if not files or len(files) > MAX_FILES:
        raise HTTPException(status_code=400, detail=f"Upload between 1 and {MAX_FILES} images")

    job_id = str(uuid4())
    file_data = []
    for f in files:
        file_data.append((f.filename, await f.read()))

    thread = threading.Thread(target=process_job, args=(job_id, file_data))
    thread.start()

    return {"job_id": job_id}

@app.get("/download/{job_id}")
async def download(job_id: str):
    csv_path = TMP_DIR / f"job_{job_id}" / "results.csv"
    if not csv_path.exists():
        raise HTTPException(status_code=404, detail="Results not found")
    return FileResponse(csv_path, media_type="text/csv", filename="results.csv")


@app.get("/logs/{job_id}")
async def logs(job_id: str):
    return {
        "logs": "".join(job_logs.get(job_id, [])),
        "status": job_status.get(job_id, "unknown"),
    }

