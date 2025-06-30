# test_find_structure.py

import os
import sys
import pytest
from pathlib import Path
from utils_test_helpers import init_report_file, append_report, clean_and_create_dir

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from run_validation import find_valid_structure_dirs, check_images, analyze_balance

REPORT_FILE = Path("mock_dataset/find_valid_structure_report.md")
init_report_file(REPORT_FILE, "find_valid_structure_dirs 自动化测试报告")

@pytest.mark.parametrize("folder_name, subdirs, section", [
    ("test1", ["train"], "only train available  "),
    ("test2", ["val"], "only val available"),
    ("test3", ["train", "validation", "val", "test"], "train, validation, val, test all available, priority test"),
    ("test4", [], "train, val/validation/test both missing"),
    ("test5", ["Train", "VALidation"], "sensitive test"),
])

def test_find_valid_structure_dirs(folder_name, subdirs, section):
    test_dir = Path(f"mock_dataset/{folder_name}")
    clean_and_create_dir(test_dir)
    for sd in subdirs:
        (test_dir / sd).mkdir()

    found_dirs = find_valid_structure_dirs(str(test_dir))
    append_report(REPORT_FILE, section, found_dirs)

    if "train" in section:
        if "missing" in section:
            # 预期应检测到 train 缺失 missing
            assert any("train" in k and "缺失" in p for k, p in found_dirs)
        else:
            # 预期不应检测到缺失 missing
            assert any("train" in k and "缺失" not in p for k, p in found_dirs)
