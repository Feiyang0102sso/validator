import os
from PIL import Image, UnidentifiedImageError
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
import argparse
import time

# 项目路径和数据集路径
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
DATASET_DIR = os.path.join(PROJECT_DIR, "imagenette2")
# imagenette2
REPORT_FILE = os.path.join(DATASET_DIR, "validation_report.md")

def find_valid_structure_dirs(root_dir):
    found_dirs = []

    train_dir = None
    val_test_candidates = []

    for item in os.listdir(root_dir):
        lower_item = item.lower()
        path = os.path.join(root_dir, item)
        if os.path.isdir(path):
            if "train" in lower_item:
                train_dir = ("train", path)
            elif "val" in lower_item or "validation" in lower_item or "test" in lower_item:
                val_test_candidates.append((lower_item, path))

    if train_dir:
        found_dirs.append(train_dir)
    else:
        print("缺少 train 目录")
        found_dirs.append(("train", "缺失"))

    if val_test_candidates:
        # 按字母顺序选取第一个
        val_test_candidates.sort()
        selected = val_test_candidates[0]
        selected_name = os.path.basename(selected[1])
        # 在返回的 keyword 中直接加注优先选择信息
        found_dirs.append((f"val/validation/test (已优先选择 {selected_name})", selected[1]))
        # print(found_dirs)
    else:
        print("缺少 val/validation/test 目录")
        found_dirs.append(("val/validation/test", "缺失"))

    return found_dirs


def is_image_corrupt(file_path):
    try:
        with Image.open(file_path) as img:
            img.verify()
        return None
    except (UnidentifiedImageError, IOError, SyntaxError):
        return file_path

def check_images(root_dir, max_workers=8):
    image_files = []
    for dirpath, _, filenames in os.walk(root_dir):
        for f in filenames:
            if f.lower().endswith(('.png', '.jpg', '.jpeg')):
                image_files.append(os.path.join(dirpath, f))

    corrupt_files = []
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_file = {executor.submit(is_image_corrupt, file_path): file_path for file_path in image_files}
        for future in as_completed(future_to_file):
            result = future.result()
            if result:
                corrupt_files.append(result)
    return corrupt_files

def analyze_balance(train_path, corrupt_files):
    class_counts = defaultdict(int)
    corrupt_counts = defaultdict(int)

    if not os.path.exists(train_path):
        return class_counts, corrupt_counts

    for class_name in os.listdir(train_path):
        class_dir = os.path.join(train_path, class_name)
        if os.path.isdir(class_dir):
            for f in os.listdir(class_dir):
                if f.lower().endswith(('.png', '.jpg', '.jpeg')):
                    class_counts[class_name] += 1
                    file_path = os.path.join(class_dir, f)
                    if file_path in corrupt_files:
                        corrupt_counts[class_name] += 1
    return class_counts, corrupt_counts

def generate_report(found_dirs, corrupt_files, class_counts, corrupt_counts, elapsed_time, workers):

    lines = []
    lines.append("# 数据集校验报告\n")

    lines.append(f"\n## 性能信息")
    lines.append(f"- 使用并行线程数: {workers}")
    lines.append(f"- 校验总耗时: {elapsed_time:.2f} 秒")

    lines.append("## 检测到的结构目录\n")
    if found_dirs:
        for keyword, path in found_dirs:
            lines.append(f"-  发现含有关键词 `{keyword}` 的目录：{path}")
    else:
        lines.append("未发现任何有效目录结构（train / validation / test / val 等）")

    lines.append("\n## 损坏图片检查\n")
    if corrupt_files:
        lines.append(f"共发现 {len(corrupt_files)} 张损坏图片：")
        for path in corrupt_files:
            lines.append(f"  - {path}")
    else:
        lines.append("所有图片均可正常读取")

    lines.append("\n训练集类别样本数量\n")
    if class_counts:
        for cls in sorted(class_counts):
            count = class_counts[cls]
            corrupt = corrupt_counts.get(cls, 0)
            if corrupt > 0:
                lines.append(f"- {cls}: {count} 张图片（其中 {corrupt} 张损坏）")
            else:
                lines.append(f"- {cls}: {count} 张图片")
    else:
        lines.append("未找到训练集类别文件夹或其为空")

    with open(REPORT_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print("\n".join(lines))
    print(f"\n报告已生成：{REPORT_FILE}")

def parse_args():
    parser = argparse.ArgumentParser(description="Validate image dataset structure and integrity.")
    parser.add_argument("--workers", type=int, default=8, help="Number of worker threads for parallel image checking.")
    return parser.parse_args()

def main():
    found_dirs = find_valid_structure_dirs(DATASET_DIR)
    start_time = time.time()
    # corrupt_files = check_images(DATASET_DIR)

    args = parse_args()
    corrupt_files = check_images(DATASET_DIR, max_workers=args.workers)

    print(f"正在校验数据集路径：{DATASET_DIR}")
    print(f"使用并行线程数: {args.workers}")

    train_dir = None
    for keyword, path in found_dirs:
        if "train" in keyword:
            train_dir = path
            break

    class_counts, corrupt_counts = analyze_balance(train_dir, corrupt_files) if train_dir else ({}, {})

    end_time = time.time()
    elapsed_time = end_time - start_time

    generate_report(found_dirs, corrupt_files, class_counts,
                     corrupt_counts,  elapsed_time, args.workers)

if __name__ == "__main__":
    main()
    print()
