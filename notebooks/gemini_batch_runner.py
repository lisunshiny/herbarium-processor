import sys
import os
sys.path.append(os.path.abspath(".."))

import csv
import random
import importlib
from notebooks.herbarium_label_extractor import HerbariumLabelExtractor
import concurrent.futures


class GeminiBatchRunner:
    def __init__(self,
                 num_to_sample=None,
                 path_to_sample_from=None,
                 sampled_paths=None,
                 output_csv_path=None,
                 system_instructions_path='prompts/system_instructions_no_ocr.md',
                 few_shot_prompt_path='prompts/few_shot_prompt_no_ocr.md',
                 few_shot_image_paths=None,
                 output_dir='../tmp'):

        self.num_to_sample = num_to_sample
        self.path_to_sample_from = path_to_sample_from
        self.sampled_paths = sampled_paths or []
        self.output_csv_path = output_csv_path
        self.system_instructions_path = system_instructions_path
        self.few_shot_prompt_path = few_shot_prompt_path
        self.few_shot_image_paths = few_shot_image_paths or ['../img/IMG_2708.jpg']
        self.output_dir = output_dir
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
        with open(self.few_shot_prompt_path) as f:
            self.few_shot = f.read()

    def run_extraction(self):
        extractor = HerbariumLabelExtractor(
            system_instructions=self.sys_instr,
            few_shot_prompt=self.few_shot,
            few_shot_image_paths=self.few_shot_image_paths,
            output_dir=self.output_dir
        )

        def classify_and_tag(img_path):
            print(f"Processing image: {img_path}")
            result = extractor.classify(img_path)
            print(f"Done classifying image: {img_path}")
            result['id'] = os.path.splitext(os.path.basename(img_path))[0]
            return result
        # run gemini calls in parallel. note that there is a 150rpm limit.
        print("Running classification in parallel...")
        with concurrent.futures.ThreadPoolExecutor() as executor:
            results = list(executor.map(classify_and_tag, self.sampled_paths))
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
