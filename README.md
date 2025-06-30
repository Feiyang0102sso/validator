# Validator Readme

一个用于自动化检查图像分类数据集结构、图像有效性与类别分布的命令行工具，助力保障 AI 训练数据质量。

---

## 项目背景

本工具旨在对图像分类数据集执行以下自动化检查：

- 目录结构是否合法（是否包含如 `train`、`val`、`validation`、`test` 等子文件夹）；
-  图像文件是否完整、可读（排查损坏图片）；
- 训练集各类别图片数量是否平衡；
-  自动生成结构化校验报告 `validation_report.md`，便于开发者快速定位问题。
-   支持 `--workers` 参数多线程加速
-  配合 `pytest` 可进行批量自动化验证

---

## 项目结构

```yaml
validator/
├── run_validation.py              # 校验主程序 (支持 --workers)
├── requirements.txt               # 项目依赖
├── README.md                      # 本说明文件
├── tests/
│   ├── test_check_images.py       # 检查图像完整性测试
│   ├── test_check_images_threads.py # 多线程性能测试
│   ├── test_find_structure.py     # 目录结构检测测试
│   ├── test_analyze_balance.py    # 类别分布检测测试
│	├── utils_test_helpers.py          # 测试辅助工具
│   └── mockdata_sets/  #测试数据集，包含生成的测试文档，可清理
└── imagenette2/           # 数据集，包含自动生成的校验报告

```

##  环境要求

- Python 3.10 或更高版本

### 安装依赖

使用 pip 安装依赖：

```bash
pip install -r requirements.txt
```

## 使用方法

### 运行基础校验

```bash
python run_validation.py
```

默认使用 `imagenette2/` 下的数据集进行校验，结果生成在：

```bash
imagenette2/validation_report.md
```

------

### 使用多线程加速校验

在包含大量图片的情况下，通过 `--workers` 参数加速检测，默认为8，可选参数1-8：

```bash
python run_validation.py --workers 8
```

可显著加快检查大型数据集损坏图片的速度。

## 使用 pytest 自动化验证

### 一次性测试

执行自动化测试：

```bash
pytest -sv tests
```

这些测试共计15个包含：

- **结构校验测试**
- **损坏图片检测**
- **类别分布校验**
- **多线程性能测试并验证加速效果**

### 每个文件依次执行

也可以选择每个文件依次执行

``` bash
cd tests
pytest -sv test_analyze_balance.py
pytest -sv test_check_images_threads.py
pytest -sv test_check_images.py
pytest -sv test_find_structure.py
```

会自动生成详细的 Markdown 报告在 `mock_dataset/` 下供回顾。

### 清理mock数据

运行 clean.bat将自动清空mock_dataset下除了报告外的所有文件

## 上传到git

``` bash
git status
#检测当前状态
git add --all
# 上传到本地的一个预备区
git commit -m "更新"
# 上传到本地仓库
git push
# 上传到网络上的github
```



## 更新记录

| 版本号 | 日期       | 更新内容摘要                       |
| :----- | ---------- | ---------------------------------- |
| v1.0.0 | 2025-06-25 | initial push                       |
| v1.1.0 | 2025-07-1  | 实现多线程读取<br />新增pytest测试 |
|        |            |                                    |
|        |            |                                    |

