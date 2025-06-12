import pandas as pd
import numpy as np
import re
from difflib import SequenceMatcher, ndiff
import matplotlib.pyplot as plt
import seaborn as sns
from IPython.display import display, HTML


class ModelOutputComparator:
    """
    Compare the accuracy of ML model outputs against a canonical CSV.

    Usage:
        comparator = ModelOutputComparator(
            canonical_csv_path="path/to/canonical.csv",
            test_csv_path="path/to/test.csv"
        )
        comparator.evaluate()
        comparator.visualize()
        comparator.display_sample_diffs()
        comparator.display_diff_view()
    """

    def __init__(self, canonical_csv_path: str, test_csv_path: str):
        self.canonical_csv_path = canonical_csv_path
        self.test_csv_path = test_csv_path
        self.canonical_csv = pd.read_csv(canonical_csv_path).sort_values(by="id").reset_index(drop=True)
        self.test_csv = pd.read_csv(test_csv_path).sort_values(by="id").reset_index(drop=True)
        self.comparison_columns = [col for col in self.test_csv.columns if col != "id"]
        self.canonical_csv = self.canonical_csv[self.test_csv.columns]  # Align columns
        self.row_correct_counts = [0] * len(self.test_csv)
        self.accuracy_report = {}
        self.total_correct = 0

    def normalize(self, val):
        if pd.isna(val):
            return ""
        val = str(val).strip()
        val = re.sub(r'\bfeet\b', 'ft', val)
        return val

    def compare_fields(self, val1, val2):
        return self.normalize(val1) == self.normalize(val2)

    def evaluate(self):
        total_rows = len(self.test_csv)
        for column in self.comparison_columns:
            correct = 0
            diffs = []
            for i in range(total_rows):
                val1 = self.canonical_csv[column][i]
                val2 = self.test_csv[column][i]
                match = self.compare_fields(val1, val2)
                if match:
                    correct += 1
                    self.row_correct_counts[i] += 1
                elif len(diffs) < 5:
                    diffs.append({
                        "id": self.test_csv["id"][i],
                        "original": self.normalize(val1),
                        "test": self.normalize(val2)
                    })
            self.total_correct += correct
            self.accuracy_report[column] = {
                "correct": correct,
                "total": total_rows,
                "accuracy": round(correct / total_rows, 3),
                "examples": diffs
            }
        total_fields = total_rows * len(self.comparison_columns)
        self.total_accuracy = round(self.total_correct / total_fields, 3)
        print(f"\n🧠 Model Accuracy Summary")
        print(f"✅ Total Accuracy Across All Fields: {self.total_accuracy * 100:.1f}%\n")
        summary_df = pd.DataFrame.from_dict(
            {col: {"accuracy": v["accuracy"]} for col, v in self.accuracy_report.items()},
            orient="index"
        )
        print("📊 Per-Field Accuracy:")
        display(summary_df)

    def visualize(self):
      summary_df = pd.DataFrame.from_dict(
        {col: {"accuracy": v["accuracy"]} for col, v in self.accuracy_report.items()},
        orient="index"
      )

      # Per-column accuracy
      plt.figure(figsize=(6, 4))  # Reduced width
      sns.barplot(x=summary_df.index, y=summary_df["accuracy"])
      plt.title("Model Accuracy by Field")
      plt.ylabel("Accuracy")
      plt.xlabel("Field")
      plt.ylim(0, 1)
      plt.xticks(rotation=45)
      plt.tight_layout()
      plt.show()

      # Row-wise accuracy
      row_accuracy = pd.DataFrame({
        "id": self.test_csv["id"],
        "correct_fields": self.row_correct_counts,
        "row_accuracy": [round(c / len(self.comparison_columns), 3) for c in self.row_correct_counts]
      })
      plt.figure(figsize=(6, 4))  # Reduced width
      sns.histplot(row_accuracy["row_accuracy"], bins=10, kde=True)
      plt.title("Distribution of Accuracy per Record")
      plt.xlabel("Row Accuracy")
      plt.ylabel("Number of Records")
      plt.xlim(0, 1)
      plt.tight_layout()
      plt.show()

    def display_sample_diffs(self):
        for col, data in self.accuracy_report.items():
            if data["examples"]:
                print(f"\n❌ Sample Mismatches in Column: {col}")
                display(pd.DataFrame(data["examples"]))

    def similarity(self, a, b):
        return SequenceMatcher(None, self.normalize(a), self.normalize(b)).ratio()

    def inline_diff(self, a, b):
        a = self.normalize(a)
        b = self.normalize(b)
        diff = list(ndiff(a, b))
        result = ""
        for part in diff:
            if part.startswith("-"):
                result += f'<span style="background-color:#ffcccc">{part[2:]}</span>'
            elif part.startswith("+"):
                result += f'<span style="background-color:#ccffcc">{part[2:]}</span>'
            elif part.startswith(" "):
                result += part[2:]
        return result

    def highlight_diffs(self, row):
        styled = []
        for col in self.comparison_columns:
            test_val = self.test_csv.at[row.name, col]
            canon_val = self.canonical_csv.at[row.name, col]
            test_val_norm = "" if pd.isna(test_val) else test_val
            canon_val_norm = "" if pd.isna(canon_val) else canon_val
            sim = self.similarity(test_val, canon_val)
            if sim == 1:
                style = "background-color: #e6ffe6; color: #000; padding: 4px;"
                display_val = test_val_norm
            else:
                red = int((1 - sim) * 255)
                color = f"#{255:02x}{255 - red:02x}{128:02x}"
                style = f"background-color: {color}; color: #000; font-weight: bold; padding: 4px;"
                arrow_view = f"{test_val_norm}<br><small><i>→ {canon_val_norm}</i></small>"
                diff_view = self.inline_diff(test_val, canon_val)
                display_val = f"<span class='arrow-view'>{arrow_view}</span>"
                display_val += f"<span class='diff-view' style='display:none'>{diff_view}<br><small><i>→ {canon_val_norm}</i></small></span>"
            styled.append(f'<td style="{style}">{display_val}</td>')
        return f'<tr><td style="padding: 4px;"><b>{row["id"]}</b></td>' + ''.join(styled) + '</tr>'

    def display_diff_view(self):
        html = '''<button onclick="toggleDiffView()">Toggle Diff View</button>
<script>
function toggleDiffView() {
    const arrow = document.querySelectorAll('.arrow-view');
    const diff = document.querySelectorAll('.diff-view');
    for (let i = 0; i < arrow.length; i++) {
        if (arrow[i].style.display === 'none') {
            arrow[i].style.display = 'inline';
            diff[i].style.display = 'none';
        } else {
            arrow[i].style.display = 'none';
            diff[i].style.display = 'inline';
        }
    }
}
</script>
'''
        html += '<table border="1" style="border-collapse: collapse; font-family: sans-serif; font-size: 14px;">'
        html += '<tr><th style="padding: 6px;">ID</th>' + ''.join([f'<th style="padding: 6px;">{col}</th>' for col in self.comparison_columns]) + '</tr>'
        html += '\n'.join(self.test_csv.apply(self.highlight_diffs, axis=1))
        html += '</table>'
        display(HTML(html))
