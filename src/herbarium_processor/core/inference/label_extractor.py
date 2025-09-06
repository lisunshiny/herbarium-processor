import json
import os
import re
import time

from herbarium_processor.config import ROOT_DIR
from .llm_api import BaseLLMAPI


class LabelExtractor:
    """Generic label extractor powered by an LLM backend."""

    def __init__(self, llm_api: BaseLLMAPI, prompt_builder, output_dir: str = "tmp/"):
        self.llm_api = llm_api
        self.prompt_builder = prompt_builder
        self.session_timestamp = int(time.time())
        self.output_dir = ROOT_DIR / output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    async def classify(self, target):
        """Extract structured data from a new label image."""
        image_basename = os.path.splitext(os.path.basename(target.img_path))[0]
        contents = self.prompt_builder.generate_contents(target)
        raw = await self.llm_api.generate_content(contents)
        json_text = re.sub(r"^```json\s*|```$", "", raw)

        try:
            result = json.loads(json_text)
        except json.JSONDecodeError as exc:
            raise ValueError(
                "Failed to parse model output as JSON:\n" + json_text
            ) from exc

        output_path = (
            self.output_dir
            / f"processed_output_{self.session_timestamp}_{image_basename}.json"
        )
        with open(output_path, "w") as f:
            json.dump(result, f, indent=2)

        print(f"Saved output to {output_path}")
        return result
