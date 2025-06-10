import pandas as pd
import re
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.backends.backend_pdf import PdfPages


def normalize(val: str) -> str:
    """Normalize string values for comparison."""
    if pd.isna(val):
        return ""
    val = str(val).strip()
    val = re.sub(r"\bfeet\b", "ft", val)
    return val


def compare_fields(val1, val2) -> bool:
    return normalize(val1) == normalize(val2)


def _parse_prompt(prompt_text: str, image_paths):
    """Yield ('text', text) or ('image', path) parts parsed from prompt."""
    pattern = re.compile(r"<\|image_(\d+)\|>")
    pos = 0
    for match in pattern.finditer(prompt_text):
        start, end = match.span()
        if start > pos:
            yield "text", prompt_text[pos:start]
        idx = int(match.group(1))
        if idx < len(image_paths):
            yield "image", image_paths[idx]
        pos = end
    if pos < len(prompt_text):
        yield "text", prompt_text[pos:]


def add_text_page(pdf: PdfPages, title: str, text: str):
    fig, ax = plt.subplots(figsize=(8.5, 11))
    ax.axis("off")
    y = 0.95
    if title:
        ax.text(0.05, y, title, fontsize=14, weight="bold", va="top")
        y -= 0.05
    for line in text.splitlines():
        ax.text(0.05, y, line, fontsize=10, va="top")
        y -= 0.04
    pdf.savefig(fig)
    plt.close(fig)


def add_prompt_page(pdf: PdfPages, prompt_text: str, image_paths):
    parts = list(_parse_prompt(prompt_text, image_paths))
    fig, ax = plt.subplots(figsize=(8.5, 11))
    ax.axis("off")
    y = 0.95
    for kind, content in parts:
        if kind == "text":
            for line in content.splitlines():
                ax.text(0.05, y, line, fontsize=10, va="top")
                y -= 0.04
        else:
            img = plt.imread(content)
            aspect = img.shape[0] / img.shape[1]
            height = 0.25
            ax.imshow(img, extent=[0.05, 0.55, y-height, y], aspect='auto')
            y -= height + 0.02
    pdf.savefig(fig)
    plt.close(fig)


def generate_pdf_report(canonical_csv_path: str,
                         test_csv_path: str,
                         pdf_path: str,
                         system_instructions_path: str | None = None,
                         few_shot_prompt_path: str | None = None,
                         few_shot_image_paths=None):
    """Generate a PDF report comparing test CSV to canonical CSV."""
    few_shot_image_paths = few_shot_image_paths or []

    canonical_csv = pd.read_csv(canonical_csv_path).sort_values(by="id").reset_index(drop=True)
    test_csv = pd.read_csv(test_csv_path).sort_values(by="id").reset_index(drop=True)

    common_columns = test_csv.columns
    canonical_csv = canonical_csv[common_columns]

    comparison_columns = [c for c in common_columns if c != "id"]
    total_rows = len(test_csv)
    row_correct_counts = [0] * total_rows
    accuracy_report = {}
    total_correct = 0

    for column in comparison_columns:
        correct = 0
        diffs = []
        for i in range(total_rows):
            val1 = canonical_csv[column][i]
            val2 = test_csv[column][i]
            match = compare_fields(val1, val2)
            if match:
                correct += 1
                row_correct_counts[i] += 1
            elif len(diffs) < 5:
                diffs.append({
                    "id": test_csv["id"][i],
                    "original": normalize(val1),
                    "test": normalize(val2),
                })
        total_correct += correct
        accuracy_report[column] = {
            "correct": correct,
            "total": total_rows,
            "accuracy": round(correct / total_rows, 3),
            "examples": diffs,
        }

    total_fields = total_rows * len(comparison_columns)
    total_accuracy = round(total_correct / total_fields, 3)
    summary_df = pd.DataFrame.from_dict({c: {"accuracy": v["accuracy"]} for c, v in accuracy_report.items()}, orient="index")
    row_accuracy = pd.DataFrame({
        "id": test_csv["id"],
        "correct_fields": row_correct_counts,
        "total_fields": len(comparison_columns),
        "row_accuracy": [round(c/len(comparison_columns), 3) for c in row_correct_counts],
    })

    with PdfPages(pdf_path) as pdf:
        if system_instructions_path:
            with open(system_instructions_path) as f:
                instr = f.read()
            add_text_page(pdf, "System Instructions", instr)

        if few_shot_prompt_path:
            with open(few_shot_prompt_path) as f:
                prompt_text = f.read()
            add_prompt_page(pdf, prompt_text, few_shot_image_paths)

        fig, ax = plt.subplots(figsize=(8.5, 11))
        ax.axis("off")
        title = f"Model Accuracy Summary\nTotal Accuracy: {total_accuracy*100:.1f}%"
        ax.text(0.05, 0.95, title, fontsize=14, weight="bold", va="top")
        table = plt.table(cellText=np.round(summary_df["accuracy"].to_frame().values, 3),
                          rowLabels=summary_df.index,
                          colLabels=["accuracy"],
                          colColours=["#CCCCCC"],
                          rowColours=["#EEEEEE"] * len(summary_df),
                          cellLoc='center',
                          loc="center")
        table.scale(1, 1.5)
        pdf.savefig(fig)
        plt.close(fig)

        plt.figure()
        sns.barplot(x=summary_df.index, y=summary_df["accuracy"])
        plt.title("Model Accuracy by Field")
        plt.ylabel("Accuracy")
        plt.xlabel("Field")
        plt.ylim(0, 1)
        plt.xticks(rotation=45)
        plt.tight_layout()
        pdf.savefig()
        plt.close()

        plt.figure()
        sns.histplot(row_accuracy["row_accuracy"], bins=10, kde=True)
        plt.title("Distribution of Accuracy per Record")
        plt.xlabel("Row Accuracy")
        plt.ylabel("Number of Records")
        plt.xlim(0, 1)
        plt.tight_layout()
        pdf.savefig()
        plt.close()

        for col, data in accuracy_report.items():
            if not data["examples"]:
                continue
            fig, ax = plt.subplots(figsize=(8.5, len(data["examples"])*0.4 + 1.5))
            ax.axis("off")
            ax.text(0.05, 0.95, f"Sample Mismatches in Column: {col}", fontsize=12, weight="bold", va="top")
            table_data = [[d["id"], d["original"], d["test"]] for d in data["examples"]]
            table = plt.table(cellText=table_data,
                              colLabels=["id", "original", "test"],
                              cellLoc='center',
                              colColours=["#CCCCCC"]*3,
                              loc="center")
            table.scale(1, 1.5)
            pdf.savefig(fig)
            plt.close(fig)

    return {
        "total_accuracy": total_accuracy,
        "per_field": summary_df,
    }
