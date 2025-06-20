import pytest
from notebooks.tools.prompt_builder import PromptBuilder


def test_generate_contents_basic(tmp_path):
    builder = PromptBuilder.__new__(PromptBuilder)
    builder.generate = lambda target: ("start <|image_0|> middle <|image_1|> end", [str(tmp_path/"a.jpg"), str(tmp_path/"b.jpg")])
    builder._make_image_part = lambda p: {"path": p}
    parts = builder.generate_contents(None)
    assert parts == [
        "start ",
        {"path": str(tmp_path/"a.jpg")},
        " middle ",
        {"path": str(tmp_path/"b.jpg")},
        " end",
    ]


def test_generate_contents_invalid_index(tmp_path):
    builder = PromptBuilder.__new__(PromptBuilder)
    builder.generate = lambda target: ("<|image_1|>", [str(tmp_path/"a.jpg")])
    builder._make_image_part = lambda p: {"path": p}
    with pytest.raises(ValueError):
        builder.generate_contents(None)


def test_make_image_part(tmp_path):
    img = tmp_path/"img.jpg"
    img.write_bytes(b"data")
    builder = PromptBuilder.__new__(PromptBuilder)
    part = builder._make_image_part(str(img))
    assert part["mime_type"] == "image/jpeg"
    assert part["data"] == b"data"
