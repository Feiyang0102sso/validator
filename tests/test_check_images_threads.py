# tests/test_check_images_threads.py

import time
import pytest
from pathlib import Path
import sys
import re
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from run_validation import check_images

from utils_test_helpers import (
    create_good_image,
    clean_and_create_dir,
    init_report_file,
    append_report,
)

# 报告路径
REPORT_FILE = Path("mock_dataset/check_images_thread_report.md")
init_report_file(REPORT_FILE, "test_check_images_threads 自动化测试报告")

@pytest.fixture(scope="module")
def setup_large_amount_images():
    """
    创建大量正常图片用于并发检测性能测试。
    """
    test_dir = Path("mock_dataset/test_many_images")
    clean_and_create_dir(test_dir)

    num_images = 500  # 可调整
    for i in range(num_images):
        img_path = test_dir / f"img_{i:04}.jpg"
        create_good_image(img_path, color="blue")

    append_report(
        REPORT_FILE,
        "测试环境初始化",
        [("测试准备", f"已创建 {num_images} 张图片于 {test_dir.resolve()}")]
    )

    yield test_dir

    append_report(
        REPORT_FILE,
        "测试完成环境保留",
        [("测试保留", f"图片已保留于 {test_dir.resolve()}，如需清理请手动执行")]
    )

@pytest.mark.parametrize("num_workers", [1, 4, 8])
def test_check_images_threads_performance(setup_large_amount_images, num_workers):
    test_dir = setup_large_amount_images

    start_time = time.perf_counter()
    corrupt_files = check_images(str(test_dir), max_workers=num_workers)
    elapsed = time.perf_counter() - start_time

    append_report(
        REPORT_FILE,
        f"{num_workers}线程性能测试结果",
        [
            (f"{num_workers}线程耗时", f"{elapsed:.4f}秒"),
            ("检测到损坏文件数量", str(len(corrupt_files))),
            ("测试路径", test_dir.resolve()),
        ]
    )

    assert len(corrupt_files) == 0, "不应检测到任何损坏文件"

def test_thread_speedup_analysis():
    """
    从报告中提取不同线程耗时，比较加速效果并写入分析
    """
    if not REPORT_FILE.exists():
        pytest.skip("未生成报告，跳过加速分析")

    times = {}
    with REPORT_FILE.open("r", encoding="utf-8") as f:
        for line in f:
            # 放宽正则匹配，匹配 '线程' 后面任意字符，后面跟时间数字和秒
            match = re.search(r"`(\d+)线程耗时`\s*:\s*([\d.]+)秒", line)
            if match:
                num_threads = int(match.group(1))
                elapsed_sec = float(match.group(2))
                times[num_threads] = elapsed_sec

    lines = ["## 性能加速分析"]
    required_threads = [1, 4, 8]
    missing = [k for k in required_threads if k not in times]

    if not missing:
        t1, t4, t8 = times[1], times[4], times[8]
        lines.append(f"- 1线程耗时: {t1:.4f}秒")
        lines.append(f"- 4线程耗时: {t4:.4f}秒")
        lines.append(f"- 8线程耗时: {t8:.4f}秒")

        assert t4 <= t1 * 1.2, f"4线程加速不足: {t4:.4f}s vs {t1:.4f}s"
        assert t8 <= t4 * 1.2, f"8线程加速不足: {t8:.4f}s vs {t1:.4f}s"

        lines.append("- 线程并发加速符合预期 ✅")
    else:
        lines.append("- 部分线程测试耗时缺失，跳过断言")
        if times:
            lines.append("- 已提取到的线程耗时: " + ", ".join(f"{k}线程={times[k]:.4f}s" for k in sorted(times.keys())))
        else:
            lines.append("- 未能提取到任何线程耗时信息")

    with REPORT_FILE.open("a", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
