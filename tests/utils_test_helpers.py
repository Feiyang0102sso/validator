# tests/utils_test_helpers.py

import os
import random
import shutil
from pathlib import Path
from PIL import Image

# mock data总路径
MOCK_DATA_ROOT = Path(__file__).parent / "mock_dataset"

def init_report_file(report_path: Path, title: str):
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(f"# {title}\n", encoding="utf-8")

def append_report(report_path: Path, section: str, items):
    lines = [f"\n## {section}\n"]
    for k, v in items:
        lines.append(f"- `{k}` : {v}")
    lines.append("\n")
    with open(report_path, "a", encoding="utf-8") as f:
        f.write("\n".join(lines))

def create_good_image(path: Path, color="red"):
    img = Image.new('RGB', (10, 10), color=color)
    img.save(path, format='JPEG')

def create_bad_image(path: Path):
    with open(path, "wb") as f:
        f.write(b"This is not a valid image file")

def clean_and_create_dir(path: Path):
    if path.exists():
        shutil.rmtree(path)
    path.mkdir(parents=True, exist_ok=True)

