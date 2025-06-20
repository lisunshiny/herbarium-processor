import os
from typing import Optional

from PIL import Image, ExifTags
import pytesseract
import pillow_heif

from herbarium_processor.config import ROOT_DIR, resolve_path

# Configuration constants
TARGET_MAX_DIMENSION = 1000  # Resize long edge to 1000px
TARGET_DPI = (300, 300)

# Mapping EXIF orientation to rotation angle
EXIF_ORIENTATION_TAG = next(
    (k for k, v in ExifTags.TAGS.items() if v == "Orientation"), None
)
EXIF_ROTATION_MAP = {
    3: 180,
    6: 270,
    8: 90
}

def remove_alpha(image: Image.Image) -> Image.Image:
    """Remove alpha channel if present."""
    if image.mode in ("RGBA", "LA"):
        return image.convert("RGB")
    return image

def resize_image(image: Image.Image, label: str = "") -> Image.Image:
    """Resize image if its largest dimension exceeds the target."""
    width, height = image.size
    max_dim = max(width, height)

    if max_dim > TARGET_MAX_DIMENSION:
        scale = TARGET_MAX_DIMENSION / max_dim
        new_size = (int(width * scale), int(height * scale))
        image = image.resize(new_size, Image.LANCZOS)
        print(f"[{label}] Resized to: {new_size}")
    else:
        print(f"[{label}] No resize needed.")

    return image

def preprocess_image(image: Image.Image, label: str = "") -> Image.Image:
    """Full image preprocessing pipeline."""
    print(f"[{label}] Original size: {image.size}")
    image = remove_alpha(image)
    image = resize_image(image, label=label)
    return image

def rotate_image_if_needed(image: Image.Image, label: str = "") -> Image.Image:
    """Detect and correct image rotation based on OCR and EXIF, and strip EXIF."""
    try:
        # Rotate based on EXIF orientation first (if exists)
        exif = image._getexif()
        if exif and EXIF_ORIENTATION_TAG in exif:
            orientation = exif[EXIF_ORIENTATION_TAG]
            if orientation in EXIF_ROTATION_MAP:
                angle = EXIF_ROTATION_MAP[orientation]
                image = image.rotate(angle, expand=True)
                print(f"[{label}] Rotated from EXIF orientation: {angle}°")
    except Exception as e:
        print(f"[{label}] Failed EXIF orientation check: {e}")

    try:
        osd = pytesseract.image_to_osd(image)
        rotation_line = next(line for line in osd.splitlines() if "Rotate" in line)
        angle = int(rotation_line.split(":")[1].strip())

        if angle != 0:
            image = image.rotate(-angle, expand=True)
            print(f"[{label}] Rotated from OCR detection: {-angle}°")
        else:
            print(f"[{label}] No rotation needed from OCR.")
    except Exception as e:
        print(f"[{label}] OCR rotation detection failed: {e}")

    # Remove EXIF data to ensure external OCR gets correct orientation
    image = image.copy()
    image.info.pop("exif", None)

    return image

def auto_rotate_text_image(image_path: str, save_path: Optional[str] = None) -> None:
    image_path = resolve_path(image_path)
    save_path = resolve_path(save_path) if save_path else None
    """Auto-rotate and preprocess image, then save it."""
    label = os.path.basename(image_path)
    try:
        image = Image.open(image_path)
        image = rotate_image_if_needed(image, label)
        image = preprocess_image(image, label)

        save_path = save_path or image_path
        image.save(save_path, "JPEG", dpi=TARGET_DPI)
        print(f"[{label}] Saved corrected image to {save_path}")
    except Exception as e:
        print(f"[{label}] Failed to process image: {e}")

def convert_heic_to_jpg(path: str) -> Optional[str]:
    path = resolve_path(path)
    """Convert HEIC file to JPEG, delete original, and return new path."""
    try:
        heif_file = pillow_heif.read_heif(path)
        image = Image.frombytes(
            heif_file.mode,
            heif_file.size,
            heif_file.data,
            "raw"
        )
        image = preprocess_image(image, label=os.path.basename(path))
        jpg_path = os.path.splitext(path)[0] + ".jpg"
        image.save(jpg_path, "JPEG", dpi=TARGET_DPI)
        os.remove(path)
        print(f"[{os.path.basename(path)}] Converted and deleted original HEIC file")
        return jpg_path
    except Exception as e:
        print(f"[{os.path.basename(path)}] HEIC conversion failed: {e}")
        return None

def process_directory(directory: str) -> None:
    directory = resolve_path(directory)
    """Process all images in the given directory."""
    for filename in os.listdir(directory):
        path = os.path.join(directory, filename)

        if filename.lower().endswith(".heic"):
            new_path = convert_heic_to_jpg(path)
            if new_path:
                auto_rotate_text_image(new_path)
        else:
            auto_rotate_text_image(path)
