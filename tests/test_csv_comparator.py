import pandas as pd
import tempfile
import os
from herbarium_processor.core.analysis.csv_comparator import CsvComparator

def make_csv(path, rows):
    pd.DataFrame(rows).to_csv(path, index=False)

def test_csv_comparator_basic(tmp_path):
    
    canonical = [
        {"id": "1", "taxon": "A", "date": "2020-01-01"},
        {"id": "2", "taxon": "B", "date": "2020-01-02"},
    ]
    test = [
        {"id": "1", "taxon": "A", "date": "2020-01-01"},
        {"id": "2", "taxon": "C", "date": "2020-01-03"},
    ]
    canonical_path = tmp_path / "canonical.csv"
    test_path = tmp_path / "test.csv"
    make_csv(canonical_path, canonical)
    make_csv(test_path, test)

    comp = CsvComparator(str(canonical_path), str(test_path))
    comp.evaluate()
    assert comp.accuracy_report["taxon"]["correct"] == 1
    assert comp.accuracy_report["date"]["correct"] == 1
    assert comp.total_accuracy == 0.5

    # Test similarity
    assert comp.similarity("foo", "foo") == 1.0
    assert 0 <= comp.similarity("foo", "bar") < 1.0

    # Test inline_diff
    diff_html = comp.inline_diff("foo", "fob")
    assert "span" in diff_html

    # Test highlight_diffs returns HTML row
    row = pd.Series({"id": "1"})
    row.name = 0
    html_row = comp.highlight_diffs(row)
    assert "<td" in html_row

    # Test display_diff_view does not error (visual test)
    comp.display_diff_view()

def test_normalize_and_compare_fields():
    comp = CsvComparator.__new__(CsvComparator)
    assert comp.normalize(" feet ") == "ft"
    assert comp.compare_fields(" feet ", "ft")