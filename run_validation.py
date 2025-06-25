import os
from PIL import Image, UnidentifiedImageError
from collections import defaultdict

# 项目路径和数据集路径
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
DATASET_DIR = os.path.join(PROJECT_DIR, "imagenette2")
REPORT_FILE = os.path.join(DATASET_DIR, "validation_report.md")

def find_valid_structure_dirs(root_dir):
    found_dirs = []
    valid_keywords = ["train", "val", "validation", "test"]

    for keyword in valid_keywords:
        for item in os.listdir(root_dir):
            if keyword in item.lower():
                path = os.path.join(root_dir, item)
                if os.path.isdir(path):
                    found_dirs.append((keyword, path))
    return found_dirs

def check_images(root_dir):
    corrupt_files = []
    for dirpath, _, filenames in os.walk(root_dir):
        for f in filenames:
            if f.lower().endswith(('.png', '.jpg', '.jpeg')):
                file_path = os.path.join(dirpath, f)
                try:
                    with Image.open(file_path) as img:
                        img.verify()
                except (UnidentifiedImageError, IOError, SyntaxError):
                    corrupt_files.append(file_path)
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

def generate_report(found_dirs, corrupt_files, class_counts, corrupt_counts):
    lines = []
    lines.append("# 数据集校验报告\n")

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

def main():
    print(f"正在校验数据集路径：{DATASET_DIR}")

    found_dirs = find_valid_structure_dirs(DATASET_DIR)
    corrupt_files = check_images(DATASET_DIR)

    train_dir = None
    for keyword, path in found_dirs:
        if "train" in keyword:
            train_dir = path
            break

    class_counts, corrupt_counts = analyze_balance(train_dir, corrupt_files) if train_dir else ({}, {})

    generate_report(found_dirs, corrupt_files, class_counts, corrupt_counts)

if __name__ == "__main__":
    main()
