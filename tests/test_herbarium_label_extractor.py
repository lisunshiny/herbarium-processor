import json
from types import SimpleNamespace
from types import SimpleNamespace as SN

import pytest

from herbarium_processor.core.inference.gemini_label_extractor import GeminiLabelExtractor


class DummyBuilder:
    def __init__(self, contents):
        self.contents = contents
        self.called_with = None

    def generate_contents(self, target):
        self.called_with = target
        return self.contents


def make_fake_response(data):
    return SN(candidates=[SN(content=SN(parts=[SN(text=data)]))])


def test_classify_creates_output(tmp_path):
    builder = DummyBuilder(["text part"])
    extractor = GeminiLabelExtractor.__new__(GeminiLabelExtractor)
    extractor.system_instructions = "sys"
    extractor.prompt_builder = builder
    extractor.output_dir = tmp_path
    extractor.session_timestamp = 123
    extractor.model = SimpleNamespace(generate_content=lambda *args, **kwargs: make_fake_response("```json\n{\"result\": 1}\n```"))

    target = SimpleNamespace(id="foo", img_path="foo.jpg", ocr_path="foo.json")
    result = extractor.classify(target)

    assert builder.called_with is target
    assert result == {"result": 1}

    output_files = list(tmp_path.glob("processed_output_123_foo.json"))
    assert len(output_files) == 1
    with open(output_files[0]) as f:
        assert json.load(f) == {"result": 1}
