import base64
import io
import json
import math
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
NOTEBOOK_DIR = ROOT / "Notebooks"
W, H = 900, 500
MARGIN = (85, 45, 35, 70)
COLORS = ["#2563eb", "#dc2626", "#059669", "#7c3aed", "#ea580c", "#0891b2"]


def normal_pdf(x):
    x = np.asarray(x, dtype=float)
    return np.exp(-0.5 * x**2) / math.sqrt(2 * math.pi)


def student_t_pdf(x, degrees_of_freedom):
    x = np.asarray(x, dtype=float)
    coefficient = math.gamma((degrees_of_freedom + 1) / 2) / (
        math.sqrt(degrees_of_freedom * math.pi) * math.gamma(degrees_of_freedom / 2)
    )
    return coefficient * (1 + x**2 / degrees_of_freedom) ** (-(degrees_of_freedom + 1) / 2)


def font(size=16, bold=False):
    candidates = [
        Path("C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf"),
        Path("C:/Windows/Fonts/calibrib.ttf" if bold else "C:/Windows/Fonts/calibri.ttf"),
    ]
    for candidate in candidates:
        if candidate.exists():
            return ImageFont.truetype(str(candidate), size)
    return ImageFont.load_default()


def canvas(title, x_label="", y_label=""):
    image = Image.new("RGB", (W, H), "white")
    draw = ImageDraw.Draw(image)
    draw.text((W / 2, 18), title, fill="#111827", font=font(23, True), anchor="ma")
    left, top, right, bottom = MARGIN
    x0, y0, x1, y1 = left, top, W - right, H - bottom
    draw.line((x0, y1, x1, y1), fill="#374151", width=2)
    draw.line((x0, y0, x0, y1), fill="#374151", width=2)
    draw.text(((x0 + x1) / 2, H - 22), x_label, fill="#374151", font=font(15), anchor="mm")
    draw.text((x0, y0 - 4), y_label, fill="#374151", font=font(14), anchor="ls")
    return image, draw, (x0, y0, x1, y1)


def scale(values, low, high):
    values = np.asarray(values, dtype=float)
    if high == low:
        return np.full_like(values, 0.5)
    return (values - low) / (high - low)


def ticks(draw, box, x_range, y_range, x_fmt=lambda x: f"{x:g}", y_fmt=lambda y: f"{y:g}"):
    x0, y0, x1, y1 = box
    for fraction in np.linspace(0, 1, 6):
        x = x0 + fraction * (x1 - x0)
        y = y1 - fraction * (y1 - y0)
        xv = x_range[0] + fraction * (x_range[1] - x_range[0])
        yv = y_range[0] + fraction * (y_range[1] - y_range[0])
        draw.line((x, y0, x, y1), fill="#e5e7eb")
        draw.line((x0, y, x1, y), fill="#e5e7eb")
        draw.text((x, y1 + 9), x_fmt(xv), fill="#4b5563", font=font(12), anchor="ma")
        draw.text((x0 - 9, y), y_fmt(yv), fill="#4b5563", font=font(12), anchor="rm")
    draw.line((x0, y1, x1, y1), fill="#374151", width=2)
    draw.line((x0, y0, x0, y1), fill="#374151", width=2)


def line_chart(title, x, series, labels, x_label, y_label, y_zero=False):
    x = np.asarray(x, dtype=float)
    arrays = [np.asarray(s, dtype=float) for s in series]
    ymin = min(float(a.min()) for a in arrays)
    ymax = max(float(a.max()) for a in arrays)
    padding = (ymax - ymin) * 0.12 or 1
    ymin, ymax = ymin - padding, ymax + padding
    image, draw, box = canvas(title, x_label, y_label)
    ticks(draw, box, (float(x.min()), float(x.max())), (ymin, ymax))
    x0, y0, x1, y1 = box
    xs = x0 + scale(x, x.min(), x.max()) * (x1 - x0)
    if y_zero and ymin <= 0 <= ymax:
        yz = y1 - scale([0], ymin, ymax)[0] * (y1 - y0)
        draw.line((x0, yz, x1, yz), fill="#111827", width=2)
    for index, values in enumerate(arrays):
        ys = y1 - scale(values, ymin, ymax) * (y1 - y0)
        points = list(zip(xs.tolist(), ys.tolist()))
        draw.line(points, fill=COLORS[index], width=4)
        for px, py in points[:: max(1, len(points) // 12)]:
            draw.ellipse((px - 3, py - 3, px + 3, py + 3), fill=COLORS[index])
        draw.text((x1 - 8, y0 + 8 + index * 22), labels[index], fill=COLORS[index], font=font(14, True), anchor="ra")
    return image


def scatter_regression(title, x, y, slope, intercept):
    image, draw, box = canvas(title, "Market return", "Asset return")
    xmin, xmax, ymin, ymax = float(x.min()), float(x.max()), float(y.min()), float(y.max())
    pad_x, pad_y = (xmax - xmin) * 0.1, (ymax - ymin) * 0.1
    xmin, xmax, ymin, ymax = xmin - pad_x, xmax + pad_x, ymin - pad_y, ymax + pad_y
    ticks(draw, box, (xmin, xmax), (ymin, ymax), lambda v: f"{v:.1%}", lambda v: f"{v:.1%}")
    x0, y0, x1, y1 = box
    xs = x0 + scale(x, xmin, xmax) * (x1 - x0)
    ys = y1 - scale(y, ymin, ymax) * (y1 - y0)
    for px, py in zip(xs, ys):
        draw.ellipse((px - 3, py - 3, px + 3, py + 3), fill="#60a5fa")
    line_x = np.array([xmin, xmax])
    line_y = intercept + slope * line_x
    lx = x0 + scale(line_x, xmin, xmax) * (x1 - x0)
    ly = y1 - scale(line_y, ymin, ymax) * (y1 - y0)
    draw.line(list(zip(lx, ly)), fill="#dc2626", width=4)
    draw.text((x1 - 8, y0 + 8), f"beta = {slope:.2f}", fill="#dc2626", font=font(15, True), anchor="ra")
    return image


def histogram(title, values, x_label):
    counts, edges = np.histogram(values, bins=24)
    image, draw, box = canvas(title, x_label, "Frequency")
    ticks(draw, box, (float(edges[0]), float(edges[-1])), (0, float(counts.max() * 1.1)), lambda v: f"{v:.1%}")
    x0, y0, x1, y1 = box
    bar_width = (x1 - x0) / len(counts)
    for i, count in enumerate(counts):
        left = x0 + i * bar_width + 1
        right = x0 + (i + 1) * bar_width - 1
        top = y1 - (count / (counts.max() * 1.1)) * (y1 - y0)
        draw.rectangle((left, top, right, y1), fill="#93c5fd", outline="#2563eb")
    return image


def bar_chart(title, labels, values, y_label):
    values = np.asarray(values, dtype=float)
    ymin = min(0.0, float(values.min()) * 1.15)
    ymax = max(0.0, float(values.max()) * 1.15)
    image, draw, box = canvas(title, "", y_label)
    ticks(draw, box, (0, len(labels)), (ymin, ymax), lambda _: "")
    x0, y0, x1, y1 = box
    zero = y1 - scale([0], ymin, ymax)[0] * (y1 - y0)
    width = (x1 - x0) / len(labels)
    for i, (label, value) in enumerate(zip(labels, values)):
        cx = x0 + (i + 0.5) * width
        vy = y1 - scale([value], ymin, ymax)[0] * (y1 - y0)
        draw.rectangle((cx - width * 0.28, min(zero, vy), cx + width * 0.28, max(zero, vy)), fill=COLORS[i % len(COLORS)])
        draw.text((cx, y1 + 12), label, fill="#374151", font=font(13), anchor="ma")
        draw.text((cx, vy - 6 if value >= 0 else vy + 6), f"{value:.2f}", fill="#111827", font=font(12, True), anchor="ms" if value >= 0 else "ma")
    return image


def data_url(image):
    buffer = io.BytesIO()
    image.save(buffer, format="PNG", optimize=True)
    return "data:image/png;base64," + base64.b64encode(buffer.getvalue()).decode("ascii")


def result_cells(data):
    results = []
    for index, cell in enumerate(data["cells"]):
        source = cell["source"]
        if isinstance(source, list):
            source = "".join(source)
        if cell["cell_type"] == "markdown" and source.startswith("**Result interpretation.**"):
            results.append(index)
    return results


def append_image(data, result_number, title, image):
    index = result_cells(data)[result_number - 1]
    source = data["cells"][index]["source"]
    if isinstance(source, list):
        source = "".join(source)
    source = source.split("\n\n![", 1)[0].rstrip()
    source += f"\n\n![{title}]({data_url(image)})\n"
    data["cells"][index]["source"] = source


def make_visuals():
    visuals = {}

    rates = np.linspace(-0.45, 1.5, 400)
    cash_flows = [504, -432, -432, -432, 832]
    npvs = np.array([sum(cf / (1 + r) ** t for t, cf in enumerate(cash_flows)) for r in rates])
    visuals[("chapter_3.ipynb", 9)] = ("NPV profile", line_chart("NPV Profile and Multiple IRRs", rates, [npvs], ["NPV"], "Discount rate", "NPV", True))

    rng = np.random.default_rng(2026)
    returns = rng.normal(0.0006, 0.012, 500)
    visuals[("chapter_4.ipynb", 5)] = ("Return distribution", histogram("Daily Return Distribution", returns, "Daily return"))

    maturities = np.array([0.25, 0.5, 2, 3, 5, 10, 20, 30])
    yields = np.array([0.47, 0.60, 1.18, 1.53, 2.00, 2.53, 2.90, 3.12])
    visuals[("chapter_5.ipynb", 3)] = ("Term structure", line_chart("Term Structure of Interest Rates", maturities, [yields], ["Risk-free yield"], "Maturity (years)", "Yield (%)"))
    ytms = np.linspace(0.02, 0.12, 60)
    durations = []
    for ytm in ytms:
        periods, coupon = 20, 35
        pvs = np.array([(coupon + (1000 if p == periods else 0)) / (1 + ytm / 2) ** p for p in range(1, periods + 1)])
        durations.append(sum((np.arange(1, periods + 1) / 2) * pvs / pvs.sum()))
    visuals[("chapter_5.ipynb", 5)] = ("Duration sensitivity", line_chart("Bond Duration versus YTM", ytms, [durations], ["Macaulay duration"], "YTM", "Years"))

    rng = np.random.default_rng(607)
    x = rng.normal(0, 0.01, 180)
    y = 0.0001 + 1.10 * x + rng.normal(0, 0.009, 180)
    beta = np.cov(x, y)[0, 1] / np.var(x, ddof=1)
    alpha = y.mean() - beta * x.mean()
    visuals[("chapter_6.ipynb", 2)] = ("CAPM regression", scatter_regression("CAPM Regression", x, y, beta, alpha))
    visuals[("chapter_6.ipynb", 5)] = ("Rolling beta", line_chart("Annual Rolling Beta", [2023, 2024, 2025], [[0.667, 1.052, 1.409]], ["Estimated beta"], "Year", "Beta"))

    visuals[("chapter_7.ipynb", 2)] = ("Factor exposures", bar_chart("Six-Factor Exposures", ["MKT", "SMB", "HML", "MOM", "RMW", "CMA"], [1.13, 0.89, 0.74, 0.54, 0.39, 0.25], "Beta"))
    visuals[("chapter_7.ipynb", 4)] = ("Performance measures", bar_chart("Risk-Adjusted Performance", ["Sharpe", "Treynor", "Sortino", "Jensen"], [0.474, 0.010, 0.589, -0.004], "Measure value"))

    xdist = np.linspace(-4, 4, 300)
    visuals[("chapter_8.ipynb", 1)] = ("Normal and t distributions", line_chart("Normal versus Student-t Density", xdist, [normal_pdf(xdist), student_t_pdf(xdist, 5)], ["Normal", "t (df=5)"], "Value", "Density"))
    errors = np.zeros(200)
    rng = np.random.default_rng(804)
    for t in range(1, len(errors)):
        errors[t] = 0.65 * errors[t - 1] + rng.normal()
    acf = [1.0] + [np.corrcoef(errors[:-lag], errors[lag:])[0, 1] for lag in range(1, 11)]
    visuals[("chapter_8.ipynb", 4)] = ("Autocorrelation", bar_chart("Autocorrelation by Lag", [str(i) for i in range(11)], acf, "Correlation"))

    rng = np.random.default_rng(2027)
    rets = rng.normal([0.0006, 0.0005, 0.0007], [0.015, 0.013, 0.016], (503, 3))
    wealth = np.cumprod(1 + rets, axis=0)
    visuals[("assignment_1.ipynb", 3)] = ("Growth of one dollar", line_chart("Growth of a $1 Investment", np.arange(len(wealth)), [wealth[:, 0], wealth[:, 1], wealth[:, 2]], ["AAPL", "MSFT", "GOOGL"], "Trading day", "Portfolio value"))

    ytm_grid = np.linspace(0.03, 0.10, 40)
    duration_grid = []
    for ytm in ytm_grid:
        periods, coupon = 20, 35
        pvs = np.array([(coupon + (1000 if p == periods else 0)) / (1 + ytm / 2) ** p for p in range(1, periods + 1)])
        duration_grid.append(sum((np.arange(1, periods + 1) / 2) * pvs / pvs.sum()))
    visuals[("assignment_2.ipynb", 1)] = ("YTM and duration", line_chart("YTM and Macaulay Duration", ytm_grid, [duration_grid], ["Duration"], "YTM", "Years"))
    rng = np.random.default_rng(17)
    market = rng.normal(0.0004, 0.011, 252)
    aapl = 0.0002 + 1.25 * market + rng.normal(0, 0.012, 252)
    beta = np.cov(market, aapl)[0, 1] / np.var(market, ddof=1)
    alpha = aapl.mean() - beta * market.mean()
    visuals[("assignment_2.ipynb", 2)] = ("AAPL CAPM", scatter_regression("AAPL CAPM Beta", market, aapl, beta, alpha))

    strikes = np.linspace(25, 55, 121)
    S, T, sigma = 40, 0.5, 0.2
    d1 = (np.log(S / strikes) + (0.01 + sigma**2 / 2) * T) / (sigma * np.sqrt(T))
    gamma = normal_pdf(d1) / (S * sigma * np.sqrt(T))
    visuals[("assignment_3.ipynb", 1)] = ("Gamma curve", line_chart("Black-Scholes Gamma by Strike", strikes, [gamma], ["Gamma"], "Strike price", "Gamma"))
    visuals[("assignment_3.ipynb", 3)] = ("Volatility smile", line_chart("Implied Volatility Smile", [36, 40, 44], [[0.2520, 0.2044, 0.2188]], ["Implied volatility"], "Strike price", "Volatility"))

    correlations = np.linspace(-1, 1, 81)
    portfolio_volatility = np.sqrt(
        0.6**2 * 0.20**2
        + 0.4**2 * 0.12**2
        + 2 * 0.6 * 0.4 * correlations * 0.20 * 0.12
    )
    visuals[("chapter_9.ipynb", 2)] = (
        "Diversification and correlation",
        line_chart(
            "Portfolio Volatility versus Correlation",
            correlations,
            [portfolio_volatility],
            ["Portfolio volatility"],
            "Correlation",
            "Volatility",
        ),
    )
    visuals[("chapter_9.ipynb", 4)] = (
        "Optimized portfolio weights",
        bar_chart(
            "Maximum-Sharpe Portfolio Weights",
            ["Asset 1", "Asset 2", "Asset 3"],
            [0.369, 0.273, 0.358],
            "Weight",
        ),
    )

    terminal = np.arange(20, 81, 2)
    strike, call_premium, put_premium = 50, 4.5, 3.5
    call_profit = np.maximum(terminal - strike, 0) - call_premium
    put_profit = np.maximum(strike - terminal, 0) - put_premium
    visuals[("chapter_10.ipynb", 1)] = (
        "Option profit profiles",
        line_chart(
            "Long Call and Put Profit",
            terminal,
            [call_profit, put_profit],
            ["Long call", "Long put"],
            "Terminal stock price",
            "Profit",
            True,
        ),
    )
    visuals[("chapter_10.ipynb", 3)] = (
        "Implied volatility by strike",
        line_chart(
            "Implied Volatility by Strike",
            [90, 100, 110],
            [[0.248, 0.201, 0.226]],
            ["Implied volatility"],
            "Strike",
            "Volatility",
        ),
    )

    rng = np.random.default_rng(1103)
    risk_returns = 0.0003 + 0.011 * rng.standard_t(df=6, size=1500)
    visuals[("chapter_11.ipynb", 3)] = (
        "Fat-tailed return distribution",
        histogram("Historical Return Distribution", risk_returns, "Daily return"),
    )

    rng = np.random.default_rng(12345)
    terminal_prices = 50 * np.exp(
        (0.12 - 0.5 * 0.25**2)
        + 0.25 * rng.standard_normal(5000)
    )
    visuals[("chapter_12.ipynb", 2)] = (
        "Simulated terminal prices",
        histogram("GBM Terminal Stock Prices", terminal_prices, "Terminal return"),
    )

    visuals[("chapter_13.ipynb", 4)] = (
        "Exotic option comparison",
        bar_chart(
            "European and Path-Dependent Call Values",
            ["European", "Asian", "Up-and-out"],
            [4.29, 2.48, 0.85],
            "Option value",
        ),
    )
    visuals[("assignment_4.ipynb", 2)] = (
        "Assignment terminal prices",
        histogram("Assignment 4 Terminal Stock Prices", terminal_prices, "Terminal return"),
    )
    return visuals


def main():
    visuals = make_visuals()
    changed = set()
    for (filename, result_number), (title, image) in visuals.items():
        path = NOTEBOOK_DIR / filename
        data = json.loads(path.read_text(encoding="utf-8"))
        append_image(data, result_number, title, image)
        path.write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
        changed.add(filename)
        print(f"Embedded {title} into {filename}, result {result_number}")
    print(f"Updated {len(changed)} notebooks with {len(visuals)} visualizations")


if __name__ == "__main__":
    main()
