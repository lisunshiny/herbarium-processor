import os
import re
import json
import time
from dotenv import load_dotenv
import google.generativeai as genai

class HerbariumLabelExtractor:
    """
    A reusable Gemini-based extractor for herbarium specimen label images.

    This class loads prompts and reference examples once and can be used
    to extract structured JSON data from many different label images efficiently.

    Example usage:

    ```python
    with open('prompts/system_instructions_no_ocr.md') as f:
        sys_instr = f.read()
    with open('prompts/few_shot_prompt_no_ocr.md') as f:
        few_shot = f.read()

    extractor = HerbariumLabelExtractor(
        system_instructions=sys_instr,
        few_shot_prompt=few_shot,
        few_shot_image_paths=[
            '../img/IMG_2708.jpg',
        ],
        output_dir='../tmp'
    )

    for img_path in ["../img/IMG_2712.jpg", "../img/IMG_2713.jpg"]:
        result = extractor.classify(img_path)
        print(result)
    ```
    """

    def __init__(self, system_instructions, few_shot_prompt, few_shot_image_paths, output_dir="../tmp", model_name="gemini-2.5-pro-preview-05-06"):
        load_dotenv()
        genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))

        self.system_instructions = system_instructions
        self.few_shot_prompt = few_shot_prompt
        self.session_timestamp = int(time.time())

        self.model = genai.GenerativeModel(
            model_name,
            system_instruction=self.system_instructions
        )
        self.example_parts = [self._make_image_part(p) for p in few_shot_image_paths]
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def _build_contents(self, prompt_text, image_parts):
        """Return content parts with images inserted where referenced."""
        parts = []
        pattern = re.compile(r"image:(\d+)")
        pos = 0
        for match in pattern.finditer(prompt_text):
            start, end = match.span()
            if start > pos:
                parts.append(prompt_text[pos:start])
            idx = int(match.group(1))
            if idx >= len(image_parts):
                raise ValueError(f"Image index {idx} out of range")
            parts.append(image_parts[idx])
            pos = end
        if pos < len(prompt_text):
            parts.append(prompt_text[pos:])
        return parts

    def _make_image_part(self, image_path):
        with open(image_path, "rb") as img_file:
            img_bytes = img_file.read()
        return {
            "mime_type": "image/jpeg",
            "data": img_bytes,
        }

    def classify(self, image_path):
        """
        Extract structured data from a new herbarium label image using Gemini.

        This method is reusable and safe to call multiple times after initializing the extractor.

        Args:
            image_path (str): Full path to the image file (e.g. '../img/IMG_2712.jpg')

        Returns:
            dict: JSON result with extracted fields.
        """
        image_basename = os.path.splitext(os.path.basename(image_path))[0]
        classify_part = self._make_image_part(image_path)

        image_parts = self.example_parts + [classify_part]
        contents = self._build_contents(self.few_shot_prompt, image_parts)
        response = self.model.generate_content(contents=contents)
        raw = response.candidates[0].content.parts[0].text.strip()
        json_text = re.sub(r'^```json\s*|```$', '', raw)

        try:
            result = json.loads(json_text)
        except json.JSONDecodeError:
            raise ValueError("Failed to parse model output as JSON:\n" + json_text)

        output_path = os.path.join(self.output_dir, f"herbarium_processed_output_{self.session_timestamp}_{image_basename}.json")
        with open(output_path, "w") as f:
            json.dump(result, f, indent=2)

        print(f"Saved output to {output_path}")
        return result
