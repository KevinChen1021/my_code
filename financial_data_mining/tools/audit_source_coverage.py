import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "Code" / "python_financial_coding.py"
REPORT = ROOT / "Notebooks" / "source_code_coverage.md"


RECONCILED_MODULES = [
    ("19-45", "Package inspection; annuities; delayed perpetuity; NPV and IRR", "Chapters 2-3", "Integrated"),
    ("48-107", "Data download workflow; returns; ticker column; CSV/pickle; missing values; aggregation; t-tests; histogram", "Chapter 4", "Integrated"),
    ("110-207", "Effective rates; APR conversion; continuous compounding; credit spreads; term structure; bond price; YTM; duration; stock valuation", "Chapter 5", "Integrated"),
    ("210-292", "CAPM; linregress; OLS; regression chart; joins; adjusted prices; t distribution", "Chapters 6 and 8", "Integrated"),
    ("295-474", "Fama-French regression; F distribution; rolling beta; Sharpe; Treynor; LPSD", "Chapter 7", "Integrated"),
    ("475-673", "Confidence intervals; F/Levene/t tests; Durbin-Watson; bidirectional Granger; interpolation; January effect", "Chapter 8", "Integrated"),
    ("680-848", "Portfolio variance, constrained optimization, and maximum-Sharpe portfolios", "Chapter 7 extension / later portfolio chapter", "Core Sharpe optimization integrated; full portfolio theory reserved"),
    ("849-1065", "Option payoffs, Black-Scholes, implied volatility, FX futures, Greeks, volatility smile", "Later options chapter; Assignment 3 previews", "Not part of Chapters 1-8"),
    ("1067-1115", "SQLite joins", "Later database topic; Assignment 3", "Assignment example integrated"),
    ("1117-1380", "Parametric, historical, modified VaR, expected shortfall, and portfolio volatility", "Later risk-management chapter", "Not part of Chapters 1-8"),
    ("1381-1580", "Monte Carlo, stock paths, option simulation, barrier option, simulation VaR", "Later simulation chapter", "Not part of Chapters 1-8"),
    ("1582-end", "Long-horizon arithmetic/geometric return comparison", "Later forecasting topic", "Not part of Chapters 1-8"),
]


CHAPTER_RULES = [
    (1, ["python basics", "lambda function"]),
    (2, ["showing the functions", "module"]),
    (3, ["time value", "annuity", "perpetuity", "npv and irr"]),
    (4, ["download data", "daily return", "monthly return", "annual return", "t-test", "return distribution"]),
    (5, ["bond and stock", "effective rate", "credit rate", "term structure", "zero coupon", "ytm", "duration", "pricing a stock"]),
    (6, ["capm", "linear regression", "join", "close and adj close", "rolling annual beta"]),
    (7, ["multivariable", "fama french", "performance measures", "sharpe", "treynor", "lpsd"]),
    (8, ["hypotehsis", "hypothesis", "normal distribution", "equal variances", "equal means", "time-series", "granger", "interpolation", "january effect"]),
]


LATER_RULES = [
    ("Later: Portfolio Theory", ["porfolio theory", "portfolio theory", "2-stock variance", "optimization", "n-stock performance"]),
    ("Later: Options and Futures", ["options and futures", "call options", "put options", "black-scholes", "implied volatility", "exchange rate", "option greeks", "volatility smile"]),
    ("Later: Databases", ["sqlite basics"]),
    ("Later: Risk Management", ["var", "expected shortfall", "modified var", "normality test"]),
    ("Later: Monte Carlo Simulation", ["monte carlo", "roll a dice", "terminal price", "call simulation", "stock price change", "correlated random", "up and out"]),
]


def clean(text):
    return " ".join(text.replace("\ufeff", "").split())


def extract_blocks(text):
    pattern = re.compile(r"(?P<quote>'''|\"\"\")(?P<body>.*?)(?P=quote)", re.DOTALL)
    matches = list(pattern.finditer(text))
    blocks = []
    for index, match in enumerate(matches):
        heading = clean(match.group("body"))
        if not heading or len(heading) > 240:
            continue
        start = text.count("\n", 0, match.start()) + 1
        next_start = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        code_after = text[match.end():next_start].strip()
        if not code_after and len(heading) < 4:
            continue
        blocks.append({"line": start, "heading": heading, "code": code_after[:500]})
    return blocks


def classify(heading):
    normalized = heading.lower()
    for chapter, keywords in CHAPTER_RULES:
        if any(keyword in normalized for keyword in keywords):
            return f"Chapter {chapter}"
    for destination, keywords in LATER_RULES:
        if any(keyword in normalized for keyword in keywords):
            return destination
    return "Manual review"


def notebook_text():
    text = ""
    for path in sorted((ROOT / "Notebooks").glob("chapter_[1-8].ipynb")):
        data = json.loads(path.read_text(encoding="utf-8"))
        for cell in data["cells"]:
            source = cell.get("source", "")
            text += "\n" + ("".join(source) if isinstance(source, list) else source)
    return text.lower()


def covered(heading, notebooks):
    words = [
        word for word in re.findall(r"[a-zA-Z][a-zA-Z0-9_-]+", heading.lower())
        if len(word) >= 4 and word not in {"this", "that", "using", "calculate", "example", "method"}
    ]
    return bool(words) and sum(word in notebooks for word in words[:5]) >= min(2, len(words))


def main():
    source_text = SOURCE.read_text(encoding="utf-8", errors="replace")
    notebooks = notebook_text()
    blocks = extract_blocks(source_text)
    rows = []
    for block in blocks:
        destination = classify(block["heading"])
        status = "Covered" if covered(block["heading"], notebooks) else "Review/Add"
        rows.append((block["line"], block["heading"], destination, status))

    lines = [
        "# Source Code Coverage Matrix",
        "",
        "This audit treats the instructor's classroom script as an independent source, not merely an appendix to the slides.",
        "",
        "## Reconciled Major Modules",
        "",
        "| Source lines | Classroom code family | Destination | Reconciliation |",
        "|---|---|---|---|",
    ]
    for source_lines, topic, destination, status in RECONCILED_MODULES:
        lines.append(f"| {source_lines} | {topic} | {destination} | {status} |")

    lines.extend([
        "",
        "## Raw Labeled-Block Inventory",
        "",
        "The table below is an automated fine-grained inventory. Short inline comments may be flagged separately even when their surrounding module is integrated; use the reconciled table above for chapter-level coverage.",
        "",
        "| Source line | Classroom topic | Destination | Status before detailed reconciliation |",
        "|---:|---|---|---|",
    ])
    for line, heading, destination, status in rows:
        safe_heading = heading.replace("|", "\\|")
        lines.append(f"| {line} | {safe_heading} | {destination} | {status} |")

    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Extracted {len(rows)} labeled source blocks")
    print(f"Wrote {REPORT}")
    for destination in sorted({row[2] for row in rows}):
        count = sum(row[2] == destination for row in rows)
        missing = sum(row[2] == destination and row[3] == "Review/Add" for row in rows)
        print(f"{destination}: {count} blocks, {missing} flagged")


if __name__ == "__main__":
    main()
