import csv
import os
import random
import importlib
from .herbarium_label_extractor import HerbariumLabelExtractor
import concurrent.futures


class GeminiBatchRunner:
    def __init__(self,
                 num_to_sample=None,
                 path_to_sample_from=None,
                 sampled_paths=None,
                 output_csv_path=None,
                 system_instructions_path='prompts/system_instructions_no_ocr.md',
                 output_dir='../tmp',
                 prompt_builder=None,
                 targets=[]):

        # todo deprecate num_to_sample and path_to_sample_from
        self.num_to_sample = num_to_sample
        self.path_to_sample_from = path_to_sample_from
        self.sampled_paths = sampled_paths or []
        self.output_csv_path = output_csv_path
        self.system_instructions_path = system_instructions_path
        self.output_dir = output_dir
        self.prompt_builder = prompt_builder
        self.targets = targets
        self.results = []

    def sample_images(self):
        if not self.sampled_paths:
            all_files = [
                f for f in os.listdir(self.path_to_sample_from)
                if f.lower().endswith(('.jpg', '.jpeg'))
            ]
            sampled_files = random.sample(all_files, min(self.num_to_sample, len(all_files)))
            self.sampled_paths = [os.path.join(self.path_to_sample_from, f) for f in sampled_files]
        print("Will generate CSV based on sampled files:")
        print(self.sampled_paths)

    def load_prompts(self):
        with open(self.system_instructions_path) as f:
            self.sys_instr = f.read()

    def run_extraction(self):
        extractor = HerbariumLabelExtractor(
            system_instructions=self.sys_instr,
            prompt_builder=self.prompt_builder,
            output_dir=self.output_dir
        )

        def classify_and_tag(target):
            print(f"Processing image: {target.img_path}")
            result = extractor.classify(target)
            print(f"Done classifying image: {target.img_path}")
            result['id'] = os.path.splitext(os.path.basename(target.img_path))[0]
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
        fieldnames = list(all_keys)

        with open(self.output_csv_path, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for row in self.results:
                writer.writerow(row)
        print(f"Saved CSV to {self.output_csv_path}")

    def run(self):
        self.sample_images()
        self.load_prompts()
        self.run_extraction()
        self.save_csv()
