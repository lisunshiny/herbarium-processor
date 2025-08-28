import concurrent.futures
import csv
import os
import random

from herbarium_processor.config import ROOT_DIR, TMP_DIR
from herbarium_processor.core.inference.gemini_label_extractor import (
    GeminiLabelExtractor,
)


class LabelExtractionBatchRunner:
    """
    Batch runner for extracting structured label data from a set of images using an LLM-based extractor.

    This class manages the workflow for sampling images, loading system instructions,
    running label extraction in parallel, and saving results to a CSV file.
    It is designed to be general-purpose and can be adapted to different LLM extractors
    by modifying the extractor instantiation in `run_extraction`.

    Args:
        num_to_sample (int, optional): Number of images to sample from a directory.
        path_to_sample_from (str, optional): Directory to sample images from.
        sampled_paths (list, optional): List of image paths to process.
        output_csv_path (str, optional): Path to save the output CSV.
        system_instructions_path (str, optional): Path to system instructions for the LLM.
        output_dir (str, optional): Directory to save intermediate outputs.
        prompt_builder (object, optional): Prompt builder for constructing LLM prompts.
        targets (list, optional): List of label target objects to process.

    Methods:
        sample_images(): Samples images from a directory if not provided.
        load_prompts(): Loads system instructions for the LLM.
        run_extraction(): Runs label extraction in parallel for all targets.
        save_csv(): Saves the extracted results to a CSV file.
        run(): Executes the full batch extraction workflow.

    Example usage:
        ```python
        from herbarium_processor.core.llm.label_extraction_batch_runner import LabelExtractionBatchRunner
        from herbarium_processor.core.llm.prompt_builder import PromptBuilder, LabelTarget

        # Prepare prompt builder and targets
        prompt_builder = PromptBuilder(
            csv_path="data/labels.csv",
            field_list=["field1", "field2", "sources"],
            shot_data=[...],  # List of LabelTarget
            template_path="templates/prompt_template.j2"
        )
        targets = [
            LabelTarget(id="3", img_path="../img/IMG_2712.jpg", ocr_path="../ocr/IMG_2712.json"),
            # ... more targets ...
        ]

        runner = LabelExtractionBatchRunner(
            output_csv_path="output/results.csv",
            system_instructions_path="prompts/system_instructions_no_ocr.md",
            output_dir="../tmp",
            prompt_builder=prompt_builder,
            targets=targets
        )
        runner.run()
        ```
    """

    def __init__(
        self,
        output_csv_path=None,
        system_instructions_path="prompts/system_instructions_no_ocr.md",
        output_dir=None,
        prompt_builder=None,
        targets=[],
    ):
        self.output_csv_path = ROOT_DIR / output_csv_path
        self.system_instructions_path = ROOT_DIR / system_instructions_path
        self.output_dir = ROOT_DIR / output_dir if output_dir else TMP_DIR

        self.prompt_builder = prompt_builder
        self.targets = targets
        self.results = []

    def load_prompts(self):
        with open(self.system_instructions_path) as f:
            self.sys_instr = f.read()

    def run_extraction(self):
        extractor = GeminiLabelExtractor(
            system_instructions=self.sys_instr,
            prompt_builder=self.prompt_builder,
            output_dir=self.output_dir,
        )

        def classify_and_tag(target):
            print(f"Processing image: {target.img_path}")
            result = extractor.classify(target)
            print(f"Done classifying image: {target.img_path}")
            result["id"] = os.path.splitext(os.path.basename(target.img_path))[0]
            return result

        # run gemini calls in parallel. note that there is a 150rpm limit.
        print("Running classification in parallel...")
        with concurrent.futures.ThreadPoolExecutor() as executor:
            results = list(executor.map(classify_and_tag, self.targets))
        self.results = results

    def save_csv(self):
        all_keys = set()
        for r in self.results:
            all_keys.update(r.keys())

        # preserve the order defined by the prompt configuration
        ordered = ["id"]
        if self.prompt_builder is not None:
            ordered += [f for f in self.prompt_builder.field_list if f not in ordered]

        # append any additional keys in sorted order for determinism
        remaining = [k for k in all_keys if k not in ordered]
        ordered += sorted(remaining)
        fieldnames = ordered

        with open(self.output_csv_path, "w", newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for row in self.results:
                writer.writerow(row)
        print(f"Saved CSV to {self.output_csv_path}")

    def run(self):
        self.load_prompts()
        self.run_extraction()
        self.save_csv()
