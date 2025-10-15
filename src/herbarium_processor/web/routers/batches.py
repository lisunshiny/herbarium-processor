import csv
from datetime import datetime
import json
from pathlib import Path
import shutil
from typing import Any, Dict, List, Optional
from uuid import uuid4

from anyio import to_thread
from fastapi import APIRouter, File, HTTPException, UploadFile
from fastapi.responses import FileResponse
from pydantic import BaseModel

from herbarium_processor.config import TMP_DIR
from herbarium_processor.core.image.image_utils import (
    convert_heic_to_jpg_no_resize,
    crop_rotate_and_resize,
    preprocess_image_file_no_resize,
)
from herbarium_processor.core.inference import create_prompt_builder_from_yaml
from herbarium_processor.core.inference.label_extraction_batch_runner import (
    LabelExtractionBatchRunner,
)
from herbarium_processor.core.ocr.ocr_client import OcrClient
from herbarium_processor.core.types.specimen_label import SpecimenLabel


class CropOperation(BaseModel):
    x: float = 0.0
    y: float = 0.0
    width: float = 0.0
    height: float = 0.0
    rotate: float = 0.0


class ImageInfo(BaseModel):
    # deprecated
    url: str
    # somewhat processed after upload (e.g. converted from heic), but before cropping
    pre_crop_url: str = ""
    # post cropped, pre-OCR
    post_crop_url: str = ""
    # has OCR bounding boxes drawn on it
    ocr_bounding_url: str = ""
    # the original filename
    name: str
    # the uuid I assigned to this image (i.e. the filename)
    id: str
    # json object of the llm output
    llm_output: Optional[Dict[str, Any]] = None
    # user saved fields of the llm output
    user_edited_llm_output: Any = None


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
        image_id = str(uuid4())
        image_subdir = images_dir / image_id
        image_subdir.mkdir(parents=True, exist_ok=True)

        # Save original/preprocessed image as pre_crop.jpg
        pre_crop_path = image_subdir / "pre_crop.jpg"
        pre_crop_path.write_bytes(await f.read())
        if pre_crop_path.suffix.lower() == ".heic":
            new_path = convert_heic_to_jpg_no_resize(pre_crop_path)
            if new_path:
                pre_crop_path = Path(new_path)
        preprocess_image_file_no_resize(pre_crop_path)

        # Save info.json
        info = {
            "id": image_id,
            "original_name": f.filename,
        }
        info_path = image_subdir / "info.json"
        info_path.write_text(json.dumps(info))

        images.append(f"/tmp/batch_{batch_id}/images/{image_id}/pre_crop.jpg")
    return {"batch_id": batch_id, "images": images}


@router.get("/{batch_id}")
def get_batch(batch_id: str):
    images_dir = TMP_DIR / f"batch_{batch_id}" / "images"
    if not images_dir.exists():
        raise HTTPException(status_code=404, detail="Batch not found")
    images = []
    for subdir in images_dir.iterdir():
        if subdir.is_dir():
            info_path = subdir / "info.json"
            if not info_path.exists():
                continue
            info = json.loads(info_path.read_text())
            fields = {
                "id": info.get("id", subdir.name),
                "name": info.get("original_name", "pre_crop.jpg"),
            }

            # Standardized image URLs
            pre_crop_path = subdir / "pre_crop.jpg"
            if pre_crop_path.exists():
                fields["pre_crop_url"] = (
                    f"/tmp/batch_{batch_id}/images/{subdir.name}/pre_crop.jpg"
                )
                fields["url"] = fields["pre_crop_url"]

            post_crop_path = subdir / "post_crop.jpg"
            if post_crop_path.exists():
                fields["post_crop_url"] = (
                    f"/tmp/batch_{batch_id}/images/{subdir.name}/post_crop.jpg"
                )

            ocr_bounding_path = subdir / "ocr_bounding.jpg"
            if ocr_bounding_path.exists():
                fields["ocr_bounding_url"] = (
                    f"/tmp/batch_{batch_id}/images/{subdir.name}/ocr_bounding.jpg"
                )

            llm_output_path = subdir / "llm_output.json"
            if llm_output_path.exists():
                with open(llm_output_path, "r") as f_json:
                    fields["llm_output"] = json.load(f_json)

            user_edited_llm_output_path = subdir / "user_edited_llm_output.json"
            if user_edited_llm_output_path.exists():
                with open(user_edited_llm_output_path, "r") as f_json:
                    fields["user_edited_llm_output"] = json.load(f_json)

            images.append(ImageInfo(**fields))
    return {"batch_id": batch_id, "images": images}


@router.post("/{batch_id}/crop_and_infer/{image_id}")
async def crop_and_infer(batch_id: str, image_id: str, ops: CropOperation):
    job_dir = TMP_DIR / f"batch_{batch_id}"
    images_dir = job_dir / "images"
    if not images_dir.exists():
        raise HTTPException(status_code=404, detail="Batch not found")

    image_dir = images_dir / image_id
    if not image_dir.exists():
        raise HTTPException(status_code=404, detail="Image not found")

    path = image_dir / "pre_crop.jpg"
    if not path.exists():
        raise HTTPException(status_code=404, detail="Pre-crop image not found")

    # Crop and rotate
    crop = (ops.x, ops.y, ops.width, ops.height)
    # the rotation angle is in degrees clockwise, but our function expects counterclockwise
    angle = (360 - ops.rotate) % 360
    post_crop_path = image_dir / "post_crop.jpg"
    crop_rotate_and_resize(path, crop, angle, post_crop_path)
    print("test 1")
    if not post_crop_path.exists():
        print("test 123")
        raise HTTPException(status_code=500, detail="Post-crop image not found")

    ocr = OcrClient()
    preprocessed_path = image_dir / "post_ocr.jpg"
    ocr_annotated_path = image_dir / "ocr_bounding.jpg"
    llm_json_path = image_dir / "llm_input.json"
    await to_thread.run_sync(
        ocr.extract_text_json,
        str(post_crop_path),
        preprocessed_path,
        ocr_annotated_path,
        llm_json_path,
    )
    print("test 2")
    targets = [
        SpecimenLabel(
            id=path.stem,
            img_path=str(post_crop_path),
            ocr_path=str(llm_json_path),
        )
    ]
    # Run batch runner
    builder = create_prompt_builder_from_yaml("prompts/configs/default_prompt.yaml")
    csv_rel = image_dir / "result.csv"
    runner = LabelExtractionBatchRunner(
        output_csv_path=str(csv_rel),
        output_dir=str(image_dir),
        system_instructions_path="prompts/ocr_system_instructions_no_citations.md",
        prompt_builder=builder,
        targets=targets,
        max_inflight=60,  # tune for cost/throughput
        rpm_limit=140,
    )
    await runner.run_async()

    # find the first file that starts with "processed_output"
    src = next((p for p in image_dir.glob("processed_output*") if p.is_file()), None)

    dest = image_dir / "llm_output.json"
    llm_output = None

    if src and src.exists():
        print("exists:", src)
        # copy to a canonical name
        shutil.copyfile(src, dest)

        # read the canonical file
        try:
            with dest.open("r", encoding="utf-8") as f:
                llm_output = json.load(f)
        except json.JSONDecodeError:
            # leave llm_output = None if the file isn't valid JSON
            print(f"Warning: {dest} is not valid JSON")

    # add user_edited_llm_output if it exists
    user_edited_llm_output = None
    user_edited_path = image_dir / "user_edited_llm_output.json"
    if user_edited_path.exists():
        try:
            with user_edited_path.open("r", encoding="utf-8") as f:
                user_edited_llm_output = json.load(f)
        except json.JSONDecodeError:
            print(f"Warning: {user_edited_path} is not valid JSON")

    # Build updated image info
    info_path = image_dir / "info.json"
    info = json.loads(info_path.read_text()) if info_path.exists() else {}
    fields = {
        "id": info.get("id", image_id),
        "name": info.get("original_name", "pre_crop.jpg"),
        "pre_crop_url": f"/tmp/batch_{batch_id}/images/{image_id}/pre_crop.jpg",
        "url": f"/tmp/batch_{batch_id}/images/{image_id}/pre_crop.jpg",
        "post_crop_url": f"/tmp/batch_{batch_id}/images/{image_id}/post_crop.jpg",
        "ocr_bounding_url": (
            f"/tmp/batch_{batch_id}/images/{image_id}/ocr_bounding.jpg"
            if (image_dir / "ocr_bounding.jpg").exists()
            else ""
        ),
        "llm_output": llm_output,
        "user_edited_llm_output": user_edited_llm_output,
    }

    return fields


@router.get("/{batch_id}/get_csv")
async def get_csv(batch_id: str):
    job_dir = TMP_DIR / f"batch_{batch_id}"
    images_dir = job_dir / "images"
    if not images_dir.exists():
        raise HTTPException(status_code=404, detail="Batch not found")

    rows: List[Dict[str, Any]] = []
    fieldnames: set[str] = set()
    for subdir in images_dir.iterdir():
        if not subdir.is_dir():
            continue
        user_json = subdir / "user_edited_llm_output.json"
        if user_json.exists():
            try:
                with user_json.open("r", encoding="utf-8") as f:
                    data = json.load(f)
                rows.append(data)
                fieldnames.update(data.keys())
            except json.JSONDecodeError:
                continue

    if not rows:
        raise HTTPException(status_code=404, detail="No label data found")

    field_list = sorted(fieldnames)
    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    num_specimens = len(rows)
    filename = f"parsely_export_{num_specimens}_{timestamp}.csv"
    csv_path = job_dir / filename

    with csv_path.open("w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=field_list)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)

    return FileResponse(csv_path, media_type="text/csv", filename=filename)


@router.post("/{batch_id}/save_label_edits/{image_id}")
async def save_label_edits(batch_id: str, image_id: str, labels: Dict[str, Any]):
    job_dir = TMP_DIR / f"batch_{batch_id}"
    images_dir = job_dir / "images"
    if not images_dir.exists():
        raise HTTPException(status_code=404, detail="Batch not found")

    image_dir = images_dir / image_id
    if not image_dir.exists():
        raise HTTPException(status_code=404, detail="Image not found")
    print("liann 1")
    llm_json_path = image_dir / "llm_output.json"
    user_edited_llm_json_path = image_dir / "user_edited_llm_output.json"
    user_edited_llm_json_path.write_text(json.dumps(labels, indent=2))
    print("liann 2")
    # Build updated image info
    info_path = image_dir / "info.json"
    info = json.loads(info_path.read_text()) if info_path.exists() else {}
    llm_json = json.loads(llm_json_path.read_text()) if llm_json_path.exists() else None
    user_edited_llm_json = (
        json.loads(user_edited_llm_json_path.read_text())
        if user_edited_llm_json_path.exists()
        else None
    )
    fields = {
        "id": info.get("id", image_id),
        "name": info.get("original_name", "pre_crop.jpg"),
        "pre_crop_url": f"/tmp/batch_{batch_id}/images/{image_id}/pre_crop.jpg",
        "url": f"/tmp/batch_{batch_id}/images/{image_id}/pre_crop.jpg",
        "post_crop_url": f"/tmp/batch_{batch_id}/images/{image_id}/post_crop.jpg",
        "ocr_bounding_url": (
            f"/tmp/batch_{batch_id}/images/{image_id}/ocr_bounding.jpg"
            if (image_dir / "ocr_bounding.jpg").exists()
            else ""
        ),
        "llm_output": llm_json,
        "user_edited_llm_output": user_edited_llm_json,
    }

    return fields
