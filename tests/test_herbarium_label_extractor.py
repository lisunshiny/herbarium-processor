import json
from types import SimpleNamespace
from herbarium.herbarium_label_extractor import HerbariumLabelExtractor


def test_classify_creates_output(tmp_path):
    extractor = HerbariumLabelExtractor.__new__(HerbariumLabelExtractor)
    extractor.system_instructions = "sys"
    extractor.prompt_builder = SimpleNamespace(generate_contents=lambda target: ["foo"])
    extractor.output_dir = str(tmp_path)
    extractor.session_timestamp = 123
    extractor.model = SimpleNamespace()

    def fake_generate_content(contents):
        return SimpleNamespace(candidates=[
            SimpleNamespace(content=SimpleNamespace(parts=[
                SimpleNamespace(text="```json\n{\"result\": 1}\n```")
            ]))
        ])

    extractor.model.generate_content = fake_generate_content

    Target = SimpleNamespace(img_path="foo.jpg")
    result = extractor.classify(Target)
    assert result == {"result": 1}
    output_files = list(tmp_path.glob("herbarium_processed_output_123_foo.json"))
    assert len(output_files) == 1
    with open(output_files[0]) as f:
        assert json.load(f) == {"result": 1}
