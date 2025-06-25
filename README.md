# Validator Readme

一个用于自动化检查图像分类数据集结构、图像有效性与类别分布的命令行工具，助力保障 AI 训练数据质量。

---

## 项目背景

本工具旨在对图像分类数据集执行以下自动化检查：

- 目录结构是否合法（是否包含如 `train`、`val`、`validation`、`test` 等子文件夹）；
-  图像文件是否完整、可读（排查损坏图片）；
- 训练集各类别图片数量是否平衡；
-  自动生成结构化校验报告 `validation_report.md`，便于开发者快速定位问题。

---

## 项目结构

```yaml
validator/
├── imagenette2/                # 数据集
│   ├── train/
│   │   ├── class1/
│   │   ├── class2/
│   ├── val/
│   │   ├── class1/
│   │   ├── class2/
│   └── validation_report.md 校验报告
├── run_validation.py           # 校验主程序
├── requirements.txt            # 项目依赖库
├── README.md                   # 本说明文件
```

## 安装与配置

###  环境要求

- Python 3.10 或更高版本

### 安装依赖

使用 pip 安装依赖：

```bash
pip install -r requirements.txt
```

## 测试与运行

### 异常检测测试

validator/imagenette2/train/n03888257/ 目录下放置一个伪造的 .jpg 文件: error_testing.jpg，用于检测程序是否能检测图片异常

### 命令行运行方式

进入 `validator/` 项目目录下，打开终端（或 PowerShell）运行：

```bash
python run_validation.py
```

### 更新记录

| 版本号 | 日期       | 更新内容摘要 |
| :----- | ---------- | ------------ |
| v1.0.0 | 2025-06-25 | initial push |
|        |            |              |
|        |            |              |
|        |            |              |

