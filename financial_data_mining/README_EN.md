# Financial Data Mining Course Atlas

[中文版](README.md)

## Overview

This project transforms course slides, classroom Python code, and programming assignments from a Financial Data Mining course into a structured collection of Jupyter Notebooks.

It is more than a direct conversion of slides and scripts. The materials are reorganized into:

- **Concept notes:** English explanations of concepts, formulas, use cases, and financial meaning.
- **Independent code modules:** Every code cell imports its own dependencies and can run independently.
- **Exam-oriented comments:** Chinese comments highlight formulas, loops, conditions, and likely code-completion questions.
- **Result interpretation:** Each module explains the economic or statistical meaning of its output.
- **Visual results:** Important charts are embedded in the result Markdown sections.
- **Coverage auditing:** Both the slides and the instructor's classroom script are reviewed to reduce omitted topics.

The first eight chapters and three programming assignments are currently available.

## Notebook Guide

| File | Main Topics |
|---|---|
| `chapter_1.ipynb` | Python basics, variables, data types, functions, lambda expressions, introductory PV and FV |
| `chapter_2.ipynb` | Modules, import styles, package inspection, NumPy arrays, modular Black-Scholes example |
| `chapter_3.ipynb` | Time value of money, annuities, perpetuities, NPV, IRR, payback, and NPV profiles |
| `chapter_4.ipynb` | Open financial data, CSV, returns, missing values, frequency conversion, storage, and t-tests |
| `chapter_5.ipynb` | Rate conversion, bond pricing, YTM, duration, credit spreads, and stock valuation |
| `chapter_6.ipynb` | CAPM, linear regression, joins, beta significance, rolling beta, and portfolio beta |
| `chapter_7.ipynb` | Fama-French models, multifactor regression, performance measures, LPSD, and Sharpe optimization |
| `chapter_8.ipynb` | Probability distributions, hypothesis testing, confidence intervals, autocorrelation, Granger causality, and calendar effects |
| `assignment_1.ipynb` | Environment checks, multi-stock returns, Sharpe ratios, and cumulative wealth |
| `assignment_2.ipynb` | Bond price and duration, CAPM beta estimation |
| `assignment_3.ipynb` | Gamma, SQL left joins, and implied volatility |

## Repository Structure

```text
financial_data_mining/
├── Assignments/        # Original programming assignments
├── Code/               # Instructor's classroom Python script
├── Notebooks/          # Structured chapter and assignment notebooks
├── Slides/             # Original slides and extracted slide text
├── tools/              # Build, execution, visualization, and audit utilities
├── requirements.txt    # Python dependencies
├── README.md           # Chinese documentation
└── README_EN.md        # English documentation
```

### `Assignments/`

Contains the original assignment materials. The reorganized versions are stored as `Notebooks/assignment_x.ipynb`.

### `Code/`

Contains the Python code demonstrated by the instructor in class. Some classroom examples do not appear in the slides, so this directory is treated as an independent source of course knowledge.

### `Slides/`

Contains the original PDF slides and extracted text. The chapter structure, formulas, and theoretical explanations are mainly derived from these materials.

### `Notebooks/`

This is the main project output. A typical topic is organized as:

1. English concept explanation
2. Structured revision notes
3. Independently runnable code with Chinese comments
4. English result interpretation
5. A chart when visual explanation is useful

`source_code_coverage.md` maps the classroom script to the notebook chapters. It also identifies later-course topics such as options, VaR, portfolio theory, and Monte Carlo simulation.

### `tools/`

Project maintenance utilities include:

- `build_chapters_1_3.py`: builds Chapters 1-3.
- `build_chapters_4_8_and_assignments.py`: builds Chapters 4-8 and the assignments.
- `execute_notebooks.py`: executes code cells and writes results back to the notebooks.
- `embed_visualizations.py`: generates and embeds result charts.
- `audit_source_coverage.py`: creates the classroom-code coverage matrix.
- `inspect_source_materials.py`: inspects assignments and extracts slide text.

## Design Principles

- Notebook titles, prose, and filenames are written in English.
- Code explanations and exam hints are written as Chinese comments.
- Every code module imports only the dependencies it needs.
- Online market-data examples are generally replaced with seeded financial simulations for reliable offline execution.
- Simulated data represents meaningful financial scenarios rather than unexplained random values.
- Visualizations are placed in result Markdown sections; code outputs focus on numerical results.
- Bulk imports and `os.chdir` are not treated as standalone knowledge topics.
- Topic boundaries are based on both the slides and the classroom source code.

## Installation and Usage

Python 3.11 or later is recommended. Create a virtual environment and install the dependencies:

```bash
python -m venv .venv
```

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Launch Jupyter:

```bash
jupyter lab
```

Open a notebook from `Notebooks/` and run its cells in order. Since each module is designed to be independent, individual topics may also be executed separately.

## Current Status

- 8 chapter notebooks
- 3 assignment notebooks
- 65 independent code modules
- 15 embedded result charts
- All current code modules have passed execution checks

Additional chapters can be added with the same structure when the remaining course slides become available.

## Notice

This project is intended for course learning, revision, and code reuse. Copyright in the original slides, assignments, and instructor-provided classroom code remains with their respective authors.

