import os
import re
import json
import time
from dotenv import load_dotenv
import google.generativeai as genai

from herbarium_processor.config import ROOT_DIR

class GeminiLabelExtractor:
    """
    A reusable Gemini-based extractor for structured data from label images.

    This class uses a provided prompt builder and system instructions to extract
    structured JSON data from label images efficiently.

    Initialization requires system instructions and a prompt builder object.
    The extractor loads the Gemini model once and can be used to process multiple images.

    Example usage:

    ```python
    from prompt_builder import PromptBuilder, LabelTarget

    # Load system instructions
    with open('prompts/system_instructions_no_ocr.md') as f:
        sys_instr = f.read()

    # Prepare your prompt builder (see PromptBuilder docs for details)
    prompt_builder = PromptBuilder(
        csv_path="data/labels.csv",
        field_list=["field1", "field2", "sources"],
        shot_data=[...],  # List of LabelTarget
        template_path="templates/prompt_template.j2"
    )

    extractor = GeminiLabelExtractor(
        system_instructions=sys_instr,
        prompt_builder=prompt_builder,
        output_dir='../tmp'
    )

    for target in [LabelTarget(id="3", img_path="../img/IMG_2712.jpg", ocr_path="../ocr/IMG_2712.json")]:
        result = extractor.classify(target)
        print(result)
    ```
    """

    def __init__(self, system_instructions, prompt_builder, output_dir="tmp/", model_name="gemini-2.5-pro-preview-05-06"):
        load_dotenv()
        genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))

        self.system_instructions = system_instructions
        self.prompt_builder = prompt_builder
        self.session_timestamp = int(time.time())

        self.model = genai.GenerativeModel(
            model_name,
            system_instruction=self.system_instructions
        )
        self.output_dir = ROOT_DIR / output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def classify(self, target):
        """
        Extract structured data from a new label image using Gemini.

        This method is reusable and safe to call multiple times after initializing the extractor.

        Args:
            target: An object with at least an 'img_path' attribute.

        Returns:
            dict: JSON result with extracted fields.
        """
        image_basename = os.path.splitext(os.path.basename(target.img_path))[0]
        contents = self.prompt_builder.generate_contents(target)
        response = self.model.generate_content(contents=contents)
        raw = response.candidates[0].content.parts[0].text.strip()
        json_text = re.sub(r'^```json\s*|```$', '', raw)

        try:
            result = json.loads(json_text)
        except json.JSONDecodeError:
            raise ValueError("Failed to parse model output as JSON:\n" + json_text)

        output_path = self.output_dir / f"processed_output_{self.session_timestamp}_{image_basename}.json"
        with open(output_path, "w") as f:
            json.dump(result, f, indent=2)

        print(f"Saved output to {output_path}")
        return result
    