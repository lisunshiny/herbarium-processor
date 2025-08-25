from pathlib import Path
import os
from dotenv import load_dotenv

# Load environment variables from .env file (if present)
load_dotenv()

# Project root (2 levels up from this file: src/herbarium_processor/config.py)
ROOT_DIR = Path(__file__).resolve().parents[2]


def resolve_path(p: str | Path) -> Path:
    p = Path(p)
    return p if p.is_absolute() else ROOT_DIR / p


# Directory paths

# data paths
DATA_DIR = ROOT_DIR / "data"
CS_IMG_DIR = ROOT_DIR / "data" / "cs"

# storage paths
STORAGE_DIR = resolve_path(os.getenv("STORAGE_DIR", ROOT_DIR / "storage"))


# Create storage dir if it doesn't exist
STORAGE_DIR.mkdir(parents=True, exist_ok=True)

# Environment (dev/test/prod)
ENV = os.getenv("ENV", "dev")
DEBUG = ENV == "dev"

# # Image processing defaults
# DEFAULT_IMAGE_FORMAT = "jpg"
# MAX_IMAGE_SIZE = 1024

# # External services
# GOOGLE_VISION_API_KEY = os.getenv("GOOGLE_VISION_API_KEY")
# GOOGLE_APPLICATION_CREDENTIALS = os.getenv(
#     "GOOGLE_APPLICATION_CREDENTIALS",
#     str(Path.home() / ".secrets" / "vision-key.json")
# )
