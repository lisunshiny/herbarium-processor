from dataclasses import dataclass

from herbarium_processor.config import ROOT_DIR

@dataclass
class SpecimenLabel:
    id: str
    img_path: str
    ocr_path: str

    def __post_init__(self):
        self.img_path = ROOT_DIR / self.img_path
        self.ocr_path = ROOT_DIR / self.ocr_path
