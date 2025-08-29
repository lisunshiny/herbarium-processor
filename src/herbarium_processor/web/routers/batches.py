from fastapi import APIRouter, UploadFile, File, HTTPException
from typing import List
from herbarium_processor.config import ROOT_DIR, TMP_DIR
from uuid import uuid4
from pathlib import Path

from herbarium_processor.core.image.image_utils import (
    convert_heic_to_jpg_no_resize,
    crop_rotate_and_resize,
    preprocess_image_file_no_resize,
)

router = APIRouter(prefix="/batches", tags=["batches"])
MAX_FILES = 20


@router.post("", status_code=201)
async def create_batch(files: List[UploadFile] = File(...)):
    if not files or len(files) > MAX_FILES:
        raise HTTPException(status_code=400, detail=f"Upload 1..{MAX_FILES} images")
    batch_id = str(uuid4())
    job_dir = TMP_DIR / f"batch_{batch_id}"
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
        images.append(f"/tmp/batch_{batch_id}/images/{dest.name}")
    return {"batch_id": batch_id, "images": images}


@router.get("/{batch_id}")
def get_batch(batch_id: str):
    images_dir = TMP_DIR / f"batch_{batch_id}" / "images"
    if not images_dir.exists():
        raise HTTPException(status_code=404, detail="Batch not found")
    images = [
        {"url": f"/tmp/batch_{batch_id}/images/{img.name}", "name": img.name}
        for img in images_dir.iterdir()
        if img.is_file()
    ]
    return {"batch_id": batch_id, "images": images}
