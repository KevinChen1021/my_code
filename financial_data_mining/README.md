# 金融数据挖掘课程图鉴

[English Version](README_EN.md)

## 项目简介

本项目将金融数据挖掘课程的课件、课堂 Python 代码和编程作业整理为一套结构化的 Jupyter Notebook 复习资料。

项目的目标不是简单搬运 PPT 或源代码，而是将分散的课程材料重新组织为：

- **知识点讲解**：用英文整理概念、公式、适用场景和金融含义。
- **独立代码模块**：每个代码单元自行导入依赖，可单独运行。
- **考试导向注释**：代码块使用中文注释，重点标记公式、循环、判断和常见代码填空位置。
- **结果解释**：每个模块说明输出结果的经济或统计含义。
- **可视化展示**：重要图表以内嵌图片放在结果 Markdown 中。
- **覆盖审计**：同时核对 PPT 和老师课堂展示的源代码，减少知识点遗漏。

目前已整理课程前八章和三次编程作业。

## Notebook 内容

| 文件 | 主要内容 |
|---|---|
| `chapter_1.ipynb` | Python 基础、变量、数据类型、函数、Lambda、现值与终值入门 |
| `chapter_2.ipynb` | Python 模块、导入方式、包检查、NumPy 数组、Black-Scholes 模块化示例 |
| `chapter_3.ipynb` | 货币时间价值、年金、永续年金、NPV、IRR、回收期和 NPV 曲线 |
| `chapter_4.ipynb` | 开放金融数据、CSV、收益率、缺失值、频率转换、数据保存和 t 检验 |
| `chapter_5.ipynb` | 利率转换、债券定价、YTM、久期、信用利差和股票估值 |
| `chapter_6.ipynb` | CAPM、线性回归、数据连接、Beta 显著性、滚动 Beta 和组合 Beta |
| `chapter_7.ipynb` | Fama-French 模型、多因子回归、绩效指标、LPSD 和 Sharpe Ratio 优化 |
| `chapter_8.ipynb` | 概率分布、假设检验、置信区间、自相关、Granger 因果和日历效应 |
| `assignment_1.ipynb` | 环境检查、多股票收益率处理、Sharpe Ratio 和累计财富 |
| `assignment_2.ipynb` | 债券价格与久期、CAPM Beta 估计 |
| `assignment_3.ipynb` | Gamma、SQL Left Join 和隐含波动率 |

## 目录结构

```text
financial_data_mining/
├── Assignments/        # 用户原始编程作业
├── Code/               # 老师课堂展示的 Python 汇总代码
├── Notebooks/          # 整理后的章节图鉴和作业 Notebook
├── Slides/             # 原始课程课件及提取的课件文本
├── tools/              # Notebook 生成、执行、可视化和覆盖审计工具
├── requirements.txt    # Python 依赖
├── README.md           # 中文项目说明
└── README_EN.md        # 英文项目说明
```

### `Assignments/`

保存原始作业材料。整理后的版本位于 `Notebooks/assignment_x.ipynb`。

### `Code/`

保存老师上课展示的 Python 源代码。部分课堂代码并未出现在 PPT 中，因此该目录也是知识点整理的重要来源。

### `Slides/`

保存原始 PDF 课件和提取后的文本。章节框架、公式和理论说明主要依据这里的材料。

### `Notebooks/`

项目的主要成果。每个知识点通常按照以下顺序组织：

1. 英文 Markdown 知识点讲解
2. 结构化复习要点
3. 中文注释的独立代码模块
4. 英文结果解释
5. 必要的图表展示

`source_code_coverage.md` 记录课堂源代码与 Notebook 章节之间的映射，也标出了属于后续课程的期权、VaR、投资组合理论和 Monte Carlo 等主题。

### `tools/`

包含项目维护脚本：

- `build_chapters_1_3.py`：生成前三章。
- `build_chapters_4_8_and_assignments.py`：生成第 4 至第 8 章和三个作业。
- `execute_notebooks.py`：执行代码单元并将结果写回 Notebook。
- `embed_visualizations.py`：生成并嵌入结果图表。
- `audit_source_coverage.py`：生成课堂源代码覆盖矩阵。
- `inspect_source_materials.py`：检查作业和提取课件文本。

## 设计原则

- Notebook 正文、标题和文件名使用英文。
- 代码解释和考试提示使用中文注释。
- 每个代码模块按需导入依赖，不依赖其他代码单元的全局状态。
- 在线金融数据示例尽量改为固定种子的金融模拟数据，保证离线复现。
- 模拟数据保留明确的金融含义，不使用无解释的随机数字。
- 可视化放在结果 Markdown 中，代码输出区主要保留数值结果。
- 不将批量导入或 `os.chdir` 作为独立知识点。
- 同时依据课件和课堂源代码划分知识点。

## 安装与运行

建议使用 Python 3.11 或更高版本，并在虚拟环境中安装依赖：

```bash
python -m venv .venv
```

Windows PowerShell：

```powershell
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

然后启动 Jupyter：

```bash
jupyter lab
```

打开 `Notebooks/` 中的目标文件，并按顺序运行代码单元。由于每个模块设计为独立运行，也可以只运行需要复习的知识点。

## 当前状态

- 8 个章节 Notebook
- 3 个作业 Notebook
- 65 个独立代码模块
- 15 张内嵌结果图
- 所有当前代码模块均已完成执行检查

后续课程 PPT 发布后，可继续按照相同结构补充新章节。

## 说明

本项目用于课程学习、复习和代码复用。课程课件、原始作业和教师课堂代码的版权归其原作者所有。

