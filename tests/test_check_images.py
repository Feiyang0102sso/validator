# tests/test_check_images.py

import pytest
from pathlib import Path
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from run_validation import check_images, is_image_corrupt

from utils_test_helpers import (
    create_good_image,
    create_bad_image,
    clean_and_create_dir,
    init_report_file,
    append_report,
)

# 报告路径
REPORT_FILE = Path("mock_dataset/check_images_report.md")
init_report_file(REPORT_FILE, "check_images 自动化测试报告")

@pytest.fixture(scope="module")
def setup_test_images():
    """
    自动创建用于 is_image_corrupt 和 check_images 测试的 mock 数据。
    每次运行前清理，运行后保留以便检查。
    """
    test_dir = Path("mock_dataset/test_corrupt")
    clean_and_create_dir(test_dir)

    good_img = test_dir / "good.jpg"
    bad_img = test_dir / "bad.jpg"
    nested_dir = test_dir / "nested"
    nested_dir.mkdir()
    nested_good_img = nested_dir / "nested_good.jpg"

    create_good_image(good_img)
    create_bad_image(bad_img)
    create_good_image(nested_good_img)

    print(f"\n已创建测试文件:\n- {good_img.resolve()}\n- {bad_img.resolve()}\n- {nested_good_img.resolve()}")

    yield test_dir

    print(f"\n测试完成，已保留测试文件夹供检查: {test_dir.resolve()}")

def test_is_image_corrupt_good_and_bad(setup_test_images):
    test_dir = setup_test_images
    good_path = test_dir / "good.jpg"
    bad_path = test_dir / "bad.jpg"

    # 检查正常图片应返回 None
    assert is_image_corrupt(good_path) is None, "正常图片应返回 None"

    # 检查损坏图片应返回自身路径
    result = is_image_corrupt(bad_path)
    assert os.path.normpath(str(result)) == os.path.normpath(str(bad_path)), "损坏图片应返回文件路径"

    append_report(
        REPORT_FILE,
        "测试 is_image_corrupt",
        [
            ("Good image path", good_path.resolve()),
            ("Bad image path", bad_path.resolve()),
            ("检测结果", result.resolve() if hasattr(result, "resolve") else result),
        ],
    )

def test_check_images_detect_corrupt(setup_test_images):
    test_dir = setup_test_images
    corrupt_files = check_images(str(test_dir), max_workers=4)
    corrupt_files_resolved = [Path(f).resolve() for f in corrupt_files]

    append_report(
        REPORT_FILE,
        "检测 check_images 检测到的损坏图片",
        [("检测到的损坏文件数量", len(corrupt_files))] +
        [(f"Corrupt file {i+1}", p) for i, p in enumerate(corrupt_files_resolved)]
    )

    # 正确检测到损坏文件
    assert (test_dir / "bad.jpg").resolve() in corrupt_files_resolved, "应检测到损坏文件"

    # 不应误判正常文件
    assert (test_dir / "good.jpg").resolve() not in corrupt_files_resolved, "不应误判正常文件"
    assert (test_dir / "nested/nested_good.jpg").resolve() not in corrupt_files_resolved, "不应误判嵌套正常文件"
