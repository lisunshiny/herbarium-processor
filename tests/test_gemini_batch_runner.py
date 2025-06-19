import os
import csv
import random
from types import SimpleNamespace
from herbarium.gemini_batch_runner import GeminiBatchRunner


def create_images(directory, names):
    for name in names:
        path = directory / name
        path.write_text("x")


def test_sample_images_random_selection(tmp_path):
    image_names = [f"img{i}.jpg" for i in range(5)]
    other = tmp_path / "note.txt"
    other.write_text("ignore")
    create_images(tmp_path, image_names)

    random.seed(0)
    runner = GeminiBatchRunner(num_to_sample=3, path_to_sample_from=str(tmp_path))
    runner.sample_images()

    assert len(runner.sampled_paths) == 3
    for p in runner.sampled_paths:
        assert p.startswith(str(tmp_path))
        assert os.path.basename(p) in image_names
    assert len(set(runner.sampled_paths)) == 3


def test_sample_images_uses_provided_paths(tmp_path):
    paths = []
    for name in ["a.jpg", "b.jpg"]:
        p = tmp_path / name
        p.write_text("x")
        paths.append(str(p))

    runner = GeminiBatchRunner(num_to_sample=1, path_to_sample_from=str(tmp_path), sampled_paths=list(paths))
    runner.sample_images()

    assert runner.sampled_paths == paths


def test_load_prompts(tmp_path):
    sys_path = tmp_path / "sys.txt"
    sys_path.write_text("SYS")
    runner = GeminiBatchRunner(
        num_to_sample=1,
        path_to_sample_from=str(tmp_path),
        system_instructions_path=str(sys_path),
    )
    runner.load_prompts()
    assert runner.sys_instr == "SYS"


def test_run_extraction(monkeypatch, tmp_path):
    calls = []

    class FakeExtractor:
        def __init__(self, system_instructions, prompt_builder, output_dir):
            self.system_instructions = system_instructions
            self.prompt_builder = prompt_builder
            self.output_dir = output_dir

        def classify(self, path):
            calls.append(path.img_path)
            return {"value": path.img_path}

    monkeypatch.setattr("herbarium.gemini_batch_runner.HerbariumLabelExtractor", FakeExtractor)
    monkeypatch.setattr("importlib.reload", lambda mod: mod)

    runner = GeminiBatchRunner(num_to_sample=1, path_to_sample_from=str(tmp_path), output_dir=str(tmp_path))
    runner.targets = [SimpleNamespace(img_path=str(tmp_path / "a.jpg")), SimpleNamespace(img_path=str(tmp_path / "b.jpg"))]
    runner.sys_instr = "SYS"
    runner.run_extraction()

    expected_paths = [t.img_path for t in runner.targets]
    assert calls == expected_paths
    assert [r["value"] for r in runner.results] == expected_paths
    assert [r["id"] for r in runner.results] == ["a", "b"]


def test_save_csv(tmp_path):
    csv_path = tmp_path / "out.csv"
    runner = GeminiBatchRunner(output_csv_path=str(csv_path))
    runner.results = [{"id": "1", "a": "x"}, {"id": "2", "b": "y"}]
    runner.save_csv()

    with open(csv_path, newline="") as f:
        rows = list(csv.DictReader(f))
    assert len(rows) == 2
    ids = {row["id"] for row in rows}
    assert ids == {"1", "2"}


def test_run_calls_all_methods(monkeypatch):
    order = []
    runner = GeminiBatchRunner(num_to_sample=1, path_to_sample_from=".")
    monkeypatch.setattr(runner, "sample_images", lambda: order.append("sample"))
    monkeypatch.setattr(runner, "load_prompts", lambda: order.append("load"))
    monkeypatch.setattr(runner, "run_extraction", lambda: order.append("extract"))
    monkeypatch.setattr(runner, "save_csv", lambda: order.append("save"))
    runner.run()
    assert order == ["sample", "load", "extract", "save"]
