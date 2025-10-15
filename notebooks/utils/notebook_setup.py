def setup_project():
    import os
    from pathlib import Path
    import sys

    root = Path(__file__).resolve().parents[2]
    os.chdir(root)
    sys.path.insert(0, str(root))  # Now 'scripts/', 'notebooks/', etc. are importable
    sys.path.insert(0, str(root / "src"))  # Still support 'herbarium_processor'

    print(f"Notebook root set to {root}")
