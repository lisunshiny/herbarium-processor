import json
from types import SimpleNamespace

import pytest

from notebooks.herbarium_label_extractor import HerbariumLabelExtractor


def test_build_contents_basic():
    extractor = HerbariumLabelExtractor.__new__(HerbariumLabelExtractor)
    prompt = "start <|image_0|> middle <|image_1|> end"
    parts = extractor._build_contents(prompt, [{"id": 0}, {"id": 1}])
    assert parts == ["start ", {"id": 0}, " middle ", {"id": 1}, " end"]


def test_build_contents_invalid_index():
    extractor = HerbariumLabelExtractor.__new__(HerbariumLabelExtractor)
    with pytest.raises(ValueError):
        extractor._build_contents("<|image_1|>", [{}])


def test_make_image_part(tmp_path):
    img_file = tmp_path / "img.jpg"
    img_file.write_bytes(b"data")
    extractor = HerbariumLabelExtractor.__new__(HerbariumLabelExtractor)
    part = extractor._make_image_part(str(img_file))
    assert part["mime_type"] == "image/jpeg"
    assert part["data"] == b"data"


def test_classify_creates_output(tmp_path):
    extractor = HerbariumLabelExtractor.__new__(HerbariumLabelExtractor)
    extractor.system_instructions = "sys"
    extractor.few_shot_prompt = "prompt <|image_0|>"
    extractor.example_parts = [{"ex": True}]
    extractor.output_dir = str(tmp_path)
    extractor.session_timestamp = 123
    extractor.model = SimpleNamespace()

    def fake_make_image_part(path):
        return {"mime_type": "image/jpeg", "data": b"x", "path": path}

    extractor._make_image_part = fake_make_image_part

    def fake_generate_content(contents):
        return SimpleNamespace(candidates=[
            SimpleNamespace(content=SimpleNamespace(parts=[
                SimpleNamespace(text="```json\n{\"result\": 1}\n```")
            ]))
        ])

    extractor.model.generate_content = fake_generate_content

    result = extractor.classify("foo.jpg")
    assert result == {"result": 1}
    output_files = list(tmp_path.glob("herbarium_processed_output_123_foo.json"))
    assert len(output_files) == 1
    with open(output_files[0]) as f:
        assert json.load(f) == {"result": 1}
