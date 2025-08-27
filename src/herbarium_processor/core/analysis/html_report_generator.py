"""
HTMLReportGenerator
==================

This script defines the `HTMLReportGenerator` class, which compares two CSV files
(canonical and test outputs), generates visual diffs, and writes a comprehensive HTML
report. The report includes:

- Run metadata (date, CSV paths)
- Model accuracy summary and visualizations
- Sample mismatches with GitHub-style highlighting
- Full diff views
- Optionally, the prompt and system instructions used for the model run

Usage:
------
from html_report_generator import HTMLReportGenerator

scorer = HTMLReportGenerator(
    canonical_csv_path="path/to/canonical.csv",
    test_csv_path="path/to/test.csv",
    html_output_path="path/to/output.html",              # Required
    prompt_builder=your_prompt_builder,                  # Optional: to render the prompt for the report
    system_instructions_path="path/to/instructions.md"   # Optional: to include system instructions in the report
)

scorer.run_all()

This will:
- Compare the two CSVs
- Display visualizations and diffs in the notebook or terminal
- Generate an HTML report with all relevant metadata, prompt, and instructions

Dependencies:
-------------
- Assumes availability of a `CsvComparator` class in `notebooks.tools.csv_comparator`
- Optionally uses a `PromptBuilder` for generating prompts
"""

import datetime
import os

from herbarium_processor.config import ROOT_DIR
from herbarium_processor.core.analysis.csv_comparator import CsvComparator


class HTMLReportGenerator:
    def __init__(
        self,
        canonical_csv_path,
        test_csv_path,
        html_output_path,
        prompt_builder=None,
        system_instructions_path=None,
    ):
        self.canonical_csv_path = ROOT_DIR / canonical_csv_path
        self.test_csv_path = ROOT_DIR / test_csv_path
        self.prompt_builder = prompt_builder
        if system_instructions_path is not None:
            self.system_instructions_path = ROOT_DIR / system_instructions_path
        else:
            self.system_instructions_path = None
        self.html_output_path = ROOT_DIR / html_output_path
        self.comparator = CsvComparator(
            canonical_csv_path=self.canonical_csv_path, test_csv_path=self.test_csv_path
        )

    def run_all(self):
        self.comparator.evaluate()
        self.comparator.visualize()
        self.comparator.display_sample_diffs()
        self.comparator.display_diff_view()
        self.write_html_report()

    def write_html_report(self):
        html_parts = []
        run_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        html_parts.append("<h2>Model Scorer Report</h2>")
        html_parts.append(f"<b>Date run:</b> {run_date}<br>")
        html_parts.append(f"<b>Canonical CSV:</b> {self.canonical_csv_path}<br>")
        html_parts.append(f"<b>Test CSV:</b> {self.test_csv_path}<br><hr>")

        html_parts += self.comparator.calculate_html_parts()

        if self.prompt_builder:
            prompt_text = self.prompt_builder.generate_debug_prompt()
            html_parts.append(f"<h2>Prompt</h2><pre>{prompt_text}</pre>")
        if self.system_instructions_path and os.path.exists(
            self.system_instructions_path
        ):
            with open(self.system_instructions_path, "r", encoding="utf-8") as f:
                sys_instr_text = f.read()
            html_parts.append(
                f"<h2>System Instructions</h2><pre>{sys_instr_text}</pre>"
            )

        with open(self.html_output_path, "w", encoding="utf-8") as f:
            f.write("<html><body>" + "\n".join(html_parts) + "</body></html>")
