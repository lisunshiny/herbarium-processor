import json
from types import SimpleNamespace

import pytest

from herbarium_processor.core.inference.label_extractor import LabelExtractor


class DummyBuilder:
    def __init__(self, contents):
        self.contents = contents
        self.called_with = None

    def generate_contents(self, target):
        self.called_with = target
        return self.contents


class DummyAPI:
    def generate_content(self, contents):
        return '```json\n{"result": 1}\n```'


def test_classify_creates_output(tmp_path):
    builder = DummyBuilder(["text part"])
    api = DummyAPI()
    extractor = LabelExtractor(llm_api=api, prompt_builder=builder, output_dir=tmp_path)
    extractor.session_timestamp = 123

    target = SimpleNamespace(id="foo", img_path="foo.jpg", ocr_path="foo.json")
    result = extractor.classify(target)

    assert builder.called_with is target
    assert result == {"result": 1}

    output_files = list(tmp_path.glob("processed_output_123_foo.json"))
    assert len(output_files) == 1
    with open(output_files[0]) as f:
        assert json.load(f) == {"result": 1}
