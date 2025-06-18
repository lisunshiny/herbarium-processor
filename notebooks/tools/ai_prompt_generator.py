import pandas as pd
import json
import os
from jinja2 import Environment, FileSystemLoader

def load_csv(csv_path):
    return pd.read_csv(csv_path, dtype={"id": str})

def load_ocr_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def load_output_json(df, id_, field_list):
    row = df[df["id"] == id_].iloc[0].to_dict()

    output = {}
    for key in field_list:
        if key == "sources":
            if "sources" in row and row["sources"]:
                output["sources"] = json.loads(row["sources"])
            else:
                output["sources"] = {}
        else:
            output[key] = row.get(key, None)

    return output
def generate_prompt(
    csv_path: str,
    field_list: list[str],
    shot_data: list[dict],   # each: {"id", "img_path", "ocr_path"}
    target_data: dict,       # same structure
    template_path: str       # path to Jinja2 .j2 file
) -> str:
    df = load_csv(csv_path)

    # Load and compile the template
    template_dir, template_file = os.path.split(template_path)
    env = Environment(loader=FileSystemLoader(template_dir))
    tmpl = env.get_template(template_file)

    # Build shots
    shots = []
    for s in shot_data:
        shots.append({
            "image_path": s["img_path"],
            "ocr_json": load_ocr_json(s["ocr_path"]),
            "output_json": load_output_json(df, s["id"], field_list)
        })

    # Build target
    target = {
        "image_path": target_data["img_path"],
        "ocr_json": load_ocr_json(target_data["ocr_path"])
    }

    return tmpl.render(field_list=field_list, shots=shots, target=target)
