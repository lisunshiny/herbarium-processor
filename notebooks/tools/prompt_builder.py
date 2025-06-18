"""
PromptBuilder

This module defines a PromptBuilder class that loads example data and a Jinja2 template,
then renders a few-shot prompt for use with a language model (e.g., Gemini).

Usage Example:
--------------
from prompt_builder import PromptBuilder, SpecimenLabel

labels = [
    SpecimenLabel(id="1", img_path="/path/to/image1.jpg", ocr_path="/path/to/ocr1.json"),
    SpecimenLabel(id="2", img_path="/path/to/image2.jpg", ocr_path="/path/to/ocr2.json")
]

target_example = SpecimenLabel(id="3", img_path="/path/to/image3.jpg", ocr_path="/path/to/ocr3.json")

builder = PromptBuilder(
    csv_path="data/labels.csv",
    field_list=["scientific_name", "field_collectors", "sources"],
    shot_data=labels,
    target_data=target_example,
    template_path="templates/prompt_template.j2"
)

prompt, image_paths = builder.generate()

# `prompt` is a string containing the rendered prompt
# `image_paths` is a list of image file paths referenced in the prompt
"""

import pandas as pd
import json
import os
from jinja2 import Environment, FileSystemLoader
from typing import List, Dict, Tuple
from dataclasses import dataclass


@dataclass
class SpecimenLabel:
    id: str
    img_path: str
    ocr_path: str


class PromptBuilder:
    def __init__(
        self,
        csv_path: str,
        field_list: List[str],
        shot_data: List[SpecimenLabel],
        target_data: SpecimenLabel,
        template_path: str
    ):
        self.csv_path = csv_path
        self.field_list = field_list
        self.shot_data = shot_data
        self.target_data = target_data
        self.template_path = template_path

        self.df = pd.read_csv(self.csv_path, dtype={"id": str})
        template_dir, template_file = os.path.split(self.template_path)
        self.env = Environment(loader=FileSystemLoader(template_dir))
        self.template = self.env.get_template(template_file)

    def _load_ocr_json(self, path: str) -> Dict:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    def _load_output_json(self, id_: str) -> Dict:
        row = self.df[self.df["id"] == id_].iloc[0].to_dict()
        output = {}
        for key in self.field_list:
            if key == "sources":
                output["sources"] = json.loads(row["sources"]) if row.get("sources") else {}
            else:
                output[key] = row.get(key, None)
        return output

    def generate(self) -> Tuple[str, List[str]]:
        shots = [
            {
                "image_path": shot.img_path,
                "ocr_json": self._load_ocr_json(shot.ocr_path),
                "output_json": self._load_output_json(shot.id),
            }
            for shot in self.shot_data
        ]

        target = {
            "image_path": self.target_data.img_path,
            "ocr_json": self._load_ocr_json(self.target_data.ocr_path),
        }

        prompt = self.template.render(field_list=self.field_list, shots=shots, target=target)

        image_paths = [shot.img_path for shot in self.shot_data]
        image_paths.append(self.target_data.img_path)

        return prompt, image_paths
