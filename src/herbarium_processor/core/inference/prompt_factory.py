import yaml
from pathlib import Path

from .prompt_builder import PromptBuilder
from herbarium_processor.config import ROOT_DIR
from herbarium_processor.core.types.specimen_label import SpecimenLabel


def create_prompt_builder_from_yaml(config_path: str) -> PromptBuilder:
    """Create a PromptBuilder using settings loaded from a YAML file.

    Args:
        config_path: Path to a YAML configuration file relative to the project
            root directory.

    Returns:
        PromptBuilder: An initialized PromptBuilder instance.
    """
    config_file = ROOT_DIR / config_path
    with open(config_file, "r", encoding="utf-8") as f:
        cfg = yaml.safe_load(f)

    shot_data = [SpecimenLabel(**shot) for shot in cfg.get("shot_data", [])]

    return PromptBuilder(
        csv_path=cfg["csv_path"],
        field_list=cfg["field_list"],
        shot_data=shot_data,
        template_path=cfg["template_path"],
    )
