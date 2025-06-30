# tests/test_analyze_balance.py

import pytest
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).parent.parent.resolve()))
from run_validation import analyze_balance

from utils_test_helpers import (
    create_good_image,
    create_bad_image,
    clean_and_create_dir,
    init_report_file,
    append_report
)

REPORT_FILE = Path("mock_dataset/test_check_balance.md")
init_report_file(REPORT_FILE, "test_check_balance 自动化测试报告")

@pytest.fixture(scope="function")
def prepare_train_dataset(request):
    test_name = request.node.originalname.replace("test_", "")
    test_dir = Path(f"mock_dataset/train_{test_name}")
    clean_and_create_dir(test_dir)
    yield test_dir
    append_report(REPORT_FILE, f"{test_name} 数据集保留", [("保留路径", str(test_dir.resolve()))])

def format_class_counts(class_counts, corrupt_counts):
    lines = []
    for cls in sorted(class_counts.keys()):
        count = class_counts[cls]
        corrupt = corrupt_counts.get(cls, 0)
        if corrupt > 0:
            lines.append((cls, f"{count} 张（其中 {corrupt} 张损坏）"))
        else:
            lines.append((cls, f"{count} 张"))
    return lines

def test_analyze_balance_no_corrupt(prepare_train_dataset):
    test_dir = prepare_train_dataset
    for cls in ["10000", "10001"]:
        cls_dir = test_dir / cls
        cls_dir.mkdir()
        for i in range(5):
            create_good_image(cls_dir / f"{i}.jpg")

    class_counts, corrupt_counts = analyze_balance(str(test_dir), [])
    append_report(REPORT_FILE, "analyze_balance_no_corrupt", format_class_counts(class_counts, corrupt_counts))

    assert all(v == 5 for v in class_counts.values())
    assert all(v == 0 for v in corrupt_counts.values())

def test_analyze_balance_with_corrupt(prepare_train_dataset):
    test_dir = prepare_train_dataset
    corrupt_files = []

    for cls in ["10002", "10003"]:
        cls_dir = test_dir / cls
        cls_dir.mkdir()
        for i in range(5):
            img_path = cls_dir / f"{i}.jpg"
            if i == 2:
                create_bad_image(img_path)
                corrupt_files.append(str(img_path))
            else:
                create_good_image(img_path)

    class_counts, corrupt_counts = analyze_balance(str(test_dir), corrupt_files)
    append_report(REPORT_FILE, "analyze_balance_with_corrupt", format_class_counts(class_counts, corrupt_counts))

    assert all(v == 5 for v in class_counts.values())
    assert all(v == 1 for v in corrupt_counts.values())

def test_analyze_balance_all_corrupt(prepare_train_dataset):
    test_dir = prepare_train_dataset
    corrupt_files = []
    cls_dir = test_dir / "10004"
    cls_dir.mkdir()
    for i in range(3):
        img_path = cls_dir / f"{i}.jpg"
        create_bad_image(img_path)
        corrupt_files.append(str(img_path))

    class_counts, corrupt_counts = analyze_balance(str(test_dir), corrupt_files)
    append_report(REPORT_FILE, "analyze_balance_all_corrupt", format_class_counts(class_counts, corrupt_counts))

    assert list(class_counts.values())[0] == 3
    assert list(corrupt_counts.values())[0] == 3

def test_analyze_balance_class_no_images(prepare_train_dataset):
    test_dir = prepare_train_dataset
    for cls in ["10005", "10006"]:
        (test_dir / cls).mkdir()

    class_counts, corrupt_counts = analyze_balance(str(test_dir), [])
    append_report(REPORT_FILE, "analyze_balance_class_no_images", format_class_counts(class_counts, corrupt_counts))

    assert all(v == 0 for v in class_counts.values())
    assert all(v == 0 for v in corrupt_counts.values())
