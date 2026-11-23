from io import StringIO
from pathlib import Path
from random import Random

import matplotlib as mpl

mpl.use("Agg")

import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

OUTPUT = Path(__file__).resolve().parents[1] / "docs" / "assets" / "orb"
INK = "#14263c"
MUTED = "#43566f"
BLUE = "#2459a9"
TEAL = "#157358"
RED = "#aa3f44"
PURPLE = "#65429b"
GRID = "#dce4ed"
OR_FILL = "#eaf2fc"

mpl.rcdefaults()
mpl.rcParams.update(
    {
        "font.family": "DejaVu Sans",
        "font.size": 15,
        "text.color": INK,
        "axes.labelcolor": MUTED,
        "xtick.color": MUTED,
        "ytick.color": MUTED,
        "svg.hashsalt": "trader-research-orb",
    }
)


def save(fig, name):
    svg = StringIO()
    fig.savefig(svg, format="svg", facecolor="white", metadata={"Date": None})
    lines = (line.rstrip() for line in svg.getvalue().splitlines())
    (OUTPUT / f"{name}.svg").write_text("\n".join(lines) + "\n", encoding="utf-8")
    plt.close(fig)


def headline(fig, title, footer):
    fig.text(0.035, 0.95, title, fontsize=24, fontweight="bold", va="top")
    fig.text(0.035, 0.045, footer, fontsize=14, color=MUTED)


def clean_axis(ax, grid_axis):
    ax.set_axisbelow(True)
    ax.grid(axis=grid_axis, color=GRID)
    ax.tick_params(length=0)
    for spine in ax.spines.values():
        spine.set_visible(False)


def candlesticks(ax, xs, ohlc):
    for x, (open_, high, low, close) in zip(xs, ohlc, strict=True):
        color = TEAL if close >= open_ else RED
        ax.vlines(x, low, high, color=color, linewidth=1.8, zorder=3)
        ax.add_patch(
            Rectangle(
                (x - 0.26, min(open_, close)),
                width=0.52,
                height=max(abs(close - open_), 0.003),
                facecolor=color,
                zorder=4,
            )
        )


def label_event(ax, text, xy, xytext, color):
    ax.annotate(
        text,
        xy=xy,
        xytext=xytext,
        color=color,
        fontsize=15,
        fontweight="bold",
        ha="center",
        arrowprops={"arrowstyle": "->", "color": color, "lw": 1.5},
        zorder=6,
    )


def mechanics():
    fig, ax = plt.subplots(figsize=(10.7, 5.2))
    fig.subplots_adjust(left=0.09, right=0.97, bottom=0.20, top=0.83)
    headline(fig, "Một lệnh long ORB diễn ra thế nào?", "Dữ liệu mô phỏng · Không phải backtest")

    rng = Random(17)
    path = [(100.55, 100.69), (100.69, 100.64), (100.64, 100.78), (100.78, 100.74)]
    later = [
        (o, max(o, c) + rng.uniform(0.02, 0.06), min(o, c) - rng.uniform(0.02, 0.06), c)
        for o, c in path
    ]
    candles = [
        (100.12, 100.27, 100.00, 100.23),
        (100.23, 100.28, 100.10, 100.16),
        (100.16, 100.32, 100.13, 100.28),
        (100.28, 100.40, 100.24, 100.35),
        (100.35, 100.38, 100.22, 100.29),
        (100.29, 100.37, 100.22, 100.34),
        (100.34, 100.60, 100.31, 100.55),
        *later,
        (100.71, 100.82, 100.68, 100.76),
        (100.76, 100.89, 100.69, 100.72),
    ]
    xs = [*range(11), 12.4, 13.4]
    stop, or_high, entry = 100.00, 100.40, 100.55
    target = entry + (entry - stop)
    ax.add_patch(Rectangle((-0.46, stop), 4.92, or_high - stop, fc=OR_FILL, ec=BLUE, lw=1.5))
    ax.text(1.95, 100.57, "Vùng OR 5 phút", color=BLUE, fontweight="bold", ha="center")
    ax.text(0, 100.415, "Đỉnh OR", color=BLUE, va="bottom", fontsize=14)
    ax.text(0, 99.98, "Đáy OR", color=BLUE, va="top", fontsize=14)
    ax.axvline(11.25, color=MUTED, lw=1, ls=":")
    for y, name, color in [(target, "Mục tiêu +1R", TEAL), (entry, "Giá vào", BLUE), (stop, "Dừng lỗ", RED)]:
        ax.hlines(y, 6, 14.05, color=color, lw=1.4, ls="--")
        ax.text(15.35, y, name, color=color, fontsize=14, ha="center", va="center")
    ax.annotate(
        "",
        xy=(14.2, entry),
        xytext=(14.2, stop),
        arrowprops={"arrowstyle": "<->", "color": PURPLE, "lw": 1.8},
    )
    ax.text(14.4, (entry + stop) / 2, "1R mỗi cổ phiếu\n= vào − stop", color=PURPLE, va="center", fontsize=14)
    candlesticks(ax, xs, candles)
    ax.scatter([6, 13.4], [entry, candles[-1][-1]], color=[BLUE, PURPLE], s=62, zorder=5)
    label_event(ax, "Vào long khi\nnến đóng ngoài OR", (6, entry), (6.8, 100.85), BLUE)
    label_event(ax, "Thoát cuối phiên", (13.4, candles[-1][-1]), (13.15, 100.98), PURPLE)
    ax.set(xlim=(-0.55, 17.1), ylim=(99.83, 101.25))
    ax.set_xticks([0, 4, 6, 11.25, 13.4], ["09:30", "09:34", "09:36", "…", "15:59"])
    ax.set_yticks([100, 100.5, 101], ["100,00", "100,50", "101,00"])
    ax.set_xlabel("Giờ mở nến 1 phút (ET) · Lược đoạn giữa phiên", labelpad=8)
    clean_axis(ax, "y")
    save(fig, "orb-co-che")


def short_example():
    fig, ax = plt.subplots(figsize=(10.7, 5.2))
    fig.subplots_adjust(left=0.09, right=0.97, bottom=0.20, top=0.83)
    headline(fig, "Một lệnh short ORB diễn ra thế nào?", "Dữ liệu mô phỏng · Không phải backtest")

    candles = [
        (100.12, 100.27, 100.00, 100.23),
        (100.23, 100.28, 100.10, 100.16),
        (100.16, 100.32, 100.13, 100.28),
        (100.28, 100.40, 100.24, 100.35),
        (100.35, 100.38, 100.22, 100.29),
        (100.29, 100.37, 100.22, 100.34),
        (100.34, 100.36, 99.80, 99.85),
        (99.85, 99.90, 99.62, 99.65),
        (99.65, 99.70, 99.42, 99.48),
        (99.48, 99.55, 99.26, 99.32),
        (99.32, 99.45, 99.25, 99.40),
    ]
    xs = range(11)
    or_high, entry, target = 100.40, 99.85, 99.30
    ax.add_patch(Rectangle((-0.46, 100.00), 4.92, or_high - 100.00, fc=OR_FILL, ec=BLUE, lw=1.5))
    ax.text(1.95, 100.57, "Vùng OR 5 phút", color=BLUE, fontweight="bold", ha="center")
    ax.text(0, 100.415, "Đỉnh OR", color=BLUE, va="bottom", fontsize=14)
    ax.text(0, 99.98, "Đáy OR", color=BLUE, va="top", fontsize=14)
    for y, name, color in [(or_high, "Dừng lỗ", RED), (entry, "Giá vào", BLUE), (target, "Mục tiêu +1R", TEAL)]:
        ax.hlines(y, 6, 12.6, color=color, lw=1.4, ls="--")
        ax.text(13.4, y, name, color=color, fontsize=14, ha="center", va="center")
    ax.annotate(
        "",
        xy=(11.4, or_high),
        xytext=(11.4, entry),
        arrowprops={"arrowstyle": "<->", "color": PURPLE, "lw": 1.8},
    )
    ax.text(11.6, (or_high + entry) / 2, "1R = stop − vào", color=PURPLE, va="center", fontsize=14)
    candlesticks(ax, xs, candles)
    ax.scatter([6, 9], [entry, target], color=[BLUE, TEAL], s=62, zorder=5)
    label_event(ax, "Vào short khi\nnến đóng dưới đáy OR", (6, entry), (7.2, 100.62), BLUE)
    label_event(ax, "Chạm mục tiêu\n→ chốt lời", (9, target), (10.4, 99.05), TEAL)
    ax.set(xlim=(-0.55, 15.1), ylim=(98.95, 100.75))
    ax.set_xticks([0, 4, 6, 9], ["09:30", "09:34", "09:36", "09:39"])
    ax.set_yticks([99.0, 99.5, 100.0, 100.5], ["99,00", "99,50", "100,00", "100,50"])
    ax.set_xlabel("Giờ mở nến 1 phút (ET)", labelpad=8)
    clean_axis(ax, "y")
    save(fig, "orb-lenh-short")


def or_candle_color():
    fig, axes = plt.subplots(1, 3, figsize=(10.7, 4.4))
    fig.subplots_adjust(left=0.06, right=0.97, bottom=0.26, top=0.74, wspace=0.3)
    headline(fig, "Màu nến OR quyết định chiều lệnh chờ (bài [1])", "Dữ liệu mô phỏng · Không phải backtest")

    cases = [
        ((100.00, 100.55, 99.90, 100.40), "Nến OR xanh", 100.55, "Mua chờ tại đỉnh OR", BLUE),
        ((100.40, 100.55, 99.90, 100.00), "Nến OR đỏ", 99.90, "Bán chờ tại đáy OR", RED),
        ((100.20, 100.55, 99.90, 100.20), "Nến OR doji", None, "Không đặt lệnh", MUTED),
    ]
    for ax, (candle, title, trigger, note, color) in zip(axes, cases, strict=True):
        ax.set_title(title, loc="left", fontsize=17, fontweight="bold", pad=12)
        ax.axvspan(-0.48, 0.48, color=OR_FILL, zorder=0)
        candlesticks(ax, [0], [candle])
        if trigger is not None:
            ax.axhline(trigger, color=color, lw=1.5, ls="--")
        ax.text(0, 99.55, note, color=color, fontsize=15, fontweight="bold", ha="center")
        ax.set(xlim=(-1.1, 1.1), ylim=(99.4, 100.9))
        ax.set_xticks([0], ["Nến OR\n09:30–09:35"])
        ax.set_yticks([])
        clean_axis(ax, "x")
    save(fig, "orb-mau-nen-or")


def rvol():
    fig, ax = plt.subplots(figsize=(10.7, 4.6))
    fig.subplots_adjust(left=0.09, right=0.97, bottom=0.20, top=0.80)
    headline(fig, "RVOL: hôm nay so với trung bình 14 phiên", "Dữ liệu mô phỏng · Không phải backtest")

    vols = [95, 110, 88, 102, 97, 120, 90, 105, 99, 112, 86, 104, 98, 101]
    avg = sum(vols) / len(vols)
    today = 200
    colors = [MUTED] * len(vols) + [BLUE]
    ax.bar(range(len(vols) + 1), vols + [today], color=colors, width=0.6)
    ax.axhline(avg, color=RED, lw=1.4, ls="--")
    ax.text(5.5, 140, "Trung bình 14 phiên cùng khung giờ", color=RED, fontsize=13, ha="center")
    ax.annotate(
        "Hôm nay ≈ 2× trung bình\n→ RVOL ≈ 2",
        xy=(14, today), xytext=(12.8, 248), color=BLUE,
        fontsize=15, fontweight="bold", ha="center",
        arrowprops={"arrowstyle": "->", "color": BLUE, "lw": 1.5},
    )
    ax.set(xlim=(-0.7, 15.6), ylim=(0, 290))
    ax.set_xticks([6.5, 14], ["14 phiên trước (cùng khung giờ)", "Hôm nay"])
    ax.set_yticks([0, 100, 200], ["0", "100.000", "200.000"])
    ax.set_ylabel("Khối lượng 5 phút đầu (cổ phiếu)", labelpad=8)
    clean_axis(ax, "y")
    save(fig, "orb-rvol")


def range_narrow_vs_wide():
    fig, axes = plt.subplots(1, 2, figsize=(10.7, 4.9), sharey=True)
    fig.subplots_adjust(left=0.08, right=0.97, bottom=0.20, top=0.76, wspace=0.22)
    headline(fig, "Cùng một phiên, hai độ dài vùng khác nhau", "Dữ liệu mô phỏng · Không phải backtest · nến 1 phút")

    candles = [
        (100.10, 100.30, 100.00, 100.25),
        (100.25, 100.40, 100.18, 100.32),
        (100.32, 100.36, 100.15, 100.20),
        (100.20, 100.28, 100.08, 100.15),
        (100.15, 100.35, 100.12, 100.30),
        (100.30, 100.38, 100.25, 100.35),
        (100.35, 100.50, 100.32, 100.46),
        (100.46, 100.48, 100.33, 100.46),
        (100.46, 100.52, 100.38, 100.42),
        (100.42, 100.45, 100.30, 100.33),
        (100.33, 100.50, 100.25, 100.42),
        (100.42, 100.48, 100.20, 100.28),
        (100.28, 100.30, 99.90, 99.98),
        (99.98, 100.10, 99.85, 100.05),
        (100.05, 100.15, 99.95, 100.10),
        (100.10, 100.30, 100.05, 100.26),
        (100.26, 100.58, 100.22, 100.54),
        (100.54, 100.58, 100.40, 100.56),
        (100.56, 100.70, 100.52, 100.66),
        (100.66, 100.78, 100.60, 100.74),
    ]
    ors = [(4, 100.00, 100.40, 6, 100.46, "Tín hiệu nến thứ 7\n(dừng lỗ gần)", 10.0),
           (14, 99.85, 100.52, 16, 100.54, "Tín hiệu nến thứ 17\n(dừng lỗ xa hơn)", 13.6)]
    for ax, (last, lo, hi, sig_x, sig_y, note, note_x), title in zip(
        axes, ors, ("Vùng 5 phút", "Vùng 15 phút"), strict=True
    ):
        ax.set_title(title, loc="left", fontsize=17, fontweight="bold", pad=12)
        ax.add_patch(Rectangle((-0.46, lo), last + 0.92, hi - lo, fc=OR_FILL, ec=BLUE, lw=1.5))
        candlesticks(ax, range(len(candles)), candles)
        ax.axhline(hi, color=BLUE, lw=1.3, ls="--")
        ax.axhline(lo, color=BLUE, lw=1.3, ls="--")
        ax.scatter([sig_x], [sig_y], color=TEAL, s=62, zorder=5)
        label_event(ax, note, (sig_x, sig_y), (note_x, 100.88), TEAL)
        ax.set(xlim=(-0.55, 20.6), ylim=(99.6, 101.05))
        ax.set_xticks([0, 9, 19], ["09:30", "09:39", "09:49"])
        ax.set_yticks([99.8, 100.2, 100.6, 101.0], ["99,8", "100,2", "100,6", "101,0"])
        clean_axis(ax, "y")
    save(fig, "orb-vung-ngan-vs-dai")


def entries():
    fig, axes = plt.subplots(1, 2, figsize=(10.7, 5), sharey=True)
    fig.subplots_adjust(left=0.08, right=0.97, bottom=0.26, top=0.78, wspace=0.22)
    headline(fig, "Chạm biên khác với đóng nến ngoài biên", "Cùng dữ liệu mô phỏng · Không phải backtest")
    candles = [
        (100.13, 100.40, 100.04, 100.29),
        (100.29, 100.52, 100.24, 100.34),
        (100.34, 100.39, 100.27, 100.31),
        (100.31, 100.73, 100.28, 100.62),
    ]
    edge = candles[0][1]
    for ax, title in zip(axes, ("Lệnh stop theo bài [1]", "Classic: chờ đóng nến"), strict=True):
        ax.set_title(title, loc="left", fontsize=17, fontweight="bold", pad=12)
        ax.axvspan(-0.48, 0.48, color=OR_FILL, zorder=0)
        ax.axhline(edge, color=BLUE, lw=1.5, ls="--")
        candlesticks(ax, range(4), candles)
        ax.text(-0.42, edge + 0.017, "Đỉnh OR", color=BLUE, fontsize=13, va="bottom")
        ax.set(xlim=(-0.53, 3.65), ylim=(99.97, 100.97))
        ax.set_xticks([0, 1, 3], ["Nến OR\n09:30–09:35", "Quét râu", "Đóng ngoài"])
        ax.set_yticks([100.0, 100.4, 100.8], ["100,0", "100,4", "100,8"])
        clean_axis(ax, "y")
    axes[0].scatter(1, edge, color=BLUE, s=62, zorder=5)
    label_event(axes[0], "Chạm → kích hoạt\nở đỉnh OR", (1, edge), (1.47, 100.82), BLUE)
    axes[1].scatter(3, candles[-1][-1], color=TEAL, s=62, zorder=5)
    label_event(axes[1], "Quét râu:\nkhông vào", (1, candles[1][1]), (0.90, 100.82), RED)
    label_event(axes[1], "Đóng ngoài:\nvào long", (3, candles[-1][-1]), (2.85, 100.82), TEAL)
    fig.text(0.08, 0.105, "Bài [1]: OR xanh → long; OR đỏ → short; OR doji → bỏ qua.", fontsize=15)
    save(fig, "orb-cham-bien-vs-dong-nen")


def bars(ax, labels, values, colors, value_labels, *, limits, title):
    ax.set_title(title, loc="left", fontsize=17, fontweight="bold", pad=13)
    ax.barh(labels, values, color=colors, height=0.56)
    ax.invert_yaxis()
    ax.set_xlim(*limits)
    ax.set_xticks([])
    ax.axvline(0, color=MUTED, lw=1, zorder=0)
    offset = (limits[1] - limits[0]) * 0.03
    for i, (value, value_label) in enumerate(zip(values, value_labels, strict=True)):
        ax.text(max(value, 0) + offset, i, value_label, ha="left", va="center", fontweight="bold")
    clean_axis(ax, "x")


def research_paper():
    fig, axes = plt.subplots(1, 2, figsize=(10.7, 4.4), gridspec_kw={"width_ratios": [1.2, 1]})
    fig.subplots_adjust(left=0.16, right=0.95, bottom=0.16, top=0.76, wspace=0.58)
    headline(fig, "Độ dài vùng và RVOL trong nghiên cứu [1]", "Nguồn: Zarattini, Barbon & Aziz [1] · Bảng 3 và Hình 4")
    bars(
        axes[0],
        ["5 phút", "15 phút", "30 phút", "60 phút", "COMBO"],
        [2.81, 1.43, 0.21, 0.40, 1.99],
        BLUE,
        ["2,81", "1,43", "0,21", "0,40", "1,99"],
        limits=(0, 3.55),
        title="Sharpe · ORB có lọc RVOL",
    )
    bars(
        axes[1],
        ["RVOL < 1", "RVOL > 1"],
        [-0.02, 0.08],
        [RED, TEAL],
        ["−0,02R", "+0,08R"],
        limits=(-0.066, 0.132),
        title="P&L/lệnh · ORB 5 phút",
    )
    save(fig, "orb-ket-qua-zarattini")


def orb_setups():
    fig, axes = plt.subplots(1, 2, figsize=(10.7, 4.4))
    fig.subplots_adjust(left=0.12, right=0.96, bottom=0.26, top=0.76, wspace=0.43)
    headline(fig, "Tỷ lệ thắng cao hơn chưa chắc lãi hơn", "Nguồn: ORB Setups [2] · Số liệu backtest do nhà cung cấp công bố")
    bars(
        axes[0],
        ["5 phút", "15 phút", "30 phút"],
        [53.78, 50.97, 49.38],
        BLUE,
        ["53,78%", "50,97%", "49,38%"],
        limits=(0, 74),
        title="Tỷ lệ thắng tổng hợp",
    )
    bars(
        axes[1],
        ["5 phút", "15 phút"],
        [0.018, 0.044],
        TEAL,
        ["0,018", "0,044"],
        limits=(0, 0.061),
        title="P&L/lệnh (USD) · Hai ví dụ",
    )
    axes[1].text(
        0, -0.12, "Mục tiêu / dừng lỗ theo bề rộng OR:\n5 phút: 0,5× / 1×  ·  15 phút: 1× / 1×",
        transform=axes[1].transAxes, fontsize=13, va="top", color=MUTED,
    )
    save(fig, "orb-ket-qua-setups")


def retest():
    fig, ax = plt.subplots(figsize=(10.7, 5.2))
    fig.subplots_adjust(left=0.08, right=0.86, bottom=0.17, top=0.82)
    headline(fig, "ORB Retest: chờ giá thử lại biên", "Dữ liệu mô phỏng · Không phải backtest · nến 1 phút")

    candles = [
        (100.12, 100.27, 100.00, 100.23),
        (100.23, 100.28, 100.10, 100.16),
        (100.16, 100.32, 100.13, 100.28),
        (100.28, 100.40, 100.24, 100.35),
        (100.35, 100.38, 100.22, 100.29),
        (100.29, 100.50, 100.27, 100.47),
        (100.47, 100.68, 100.45, 100.62),
        (100.62, 100.75, 100.58, 100.70),
        (100.70, 100.72, 100.50, 100.55),
        (100.55, 100.56, 100.36, 100.44),
        (100.44, 100.58, 100.42, 100.55),
        (100.55, 100.78, 100.52, 100.72),
        (100.72, 100.85, 100.68, 100.80),
        (100.80, 100.92, 100.75, 100.88),
    ]
    xs = list(range(len(candles)))
    or_hi, retest_low, entry, target = 100.40, 100.36, 100.55, 100.74

    ax.add_patch(Rectangle((-0.46, 100.00), 4.92, or_hi - 100.00, fc=OR_FILL, ec=BLUE, lw=1.5))
    ax.text(1.95, 99.90, "Vùng OR 5 phút", color=BLUE, fontweight="bold", ha="center", va="top")
    ax.hlines(or_hi, 4.5, 14.6, color=BLUE, lw=1.3, ls=":")
    ax.hlines(retest_low, 9.5, 14.6, color=RED, lw=1.4, ls="--")
    ax.text(14.8, retest_low, "Dừng lỗ\n(dưới nến thử lại)", color=RED, fontsize=12, va="center")
    ax.hlines(entry, 10.5, 14.6, color=BLUE, lw=1.4, ls="--")
    ax.text(14.8, entry, "Vào lệnh", color=BLUE, fontsize=14, va="center")
    ax.hlines(target, 11.5, 14.6, color=TEAL, lw=1.4, ls="--")
    ax.text(14.8, target, "Mục tiêu", color=TEAL, fontsize=14, va="center")

    candlesticks(ax, xs, candles)
    ax.scatter([10], [entry], color=BLUE, s=62, zorder=5)
    label_event(ax, "Phá vùng:\nchưa vào, chờ thử lại", (6, 100.68), (5.6, 100.92), MUTED)
    label_event(ax, "Giá thử lại\nđỉnh OR", (9, retest_low), (8.9, 100.06), PURPLE)
    label_event(ax, "Nến xác nhận\n→ vào lệnh", (10, entry), (11.9, 100.20), BLUE)

    ax.set(xlim=(-0.7, 16.8), ylim=(99.85, 101.0))
    ax.set_xticks([0, 4, 9, 13], ["09:30", "09:34", "09:39", "09:43"])
    ax.set_yticks([99.9, 100.2, 100.5, 100.8], ["99,9", "100,2", "100,5", "100,8"])
    clean_axis(ax, "y")
    save(fig, "orb-retest")


def trend_filter():
    fig, axes = plt.subplots(1, 2, figsize=(10.7, 4.9), sharey=True)
    fig.subplots_adjust(left=0.08, right=0.97, bottom=0.20, top=0.76, wspace=0.22)
    headline(fig, "Lọc theo EMA: cú phá vùng cùng hướng mới được vào", "Dữ liệu mô phỏng · Không phải backtest · nến 15 phút")

    up = [
        (100.10, 100.30, 100.05, 100.25),
        (100.25, 100.38, 100.20, 100.32),
        (100.32, 100.40, 100.24, 100.28),
        (100.28, 100.36, 100.20, 100.33),
        (100.33, 100.42, 100.26, 100.38),
        (100.38, 100.55, 100.36, 100.52),
        (100.52, 100.68, 100.48, 100.62),
        (100.62, 100.75, 100.58, 100.70),
    ]
    ema_up = [99.95, 100.00, 100.06, 100.12, 100.18, 100.26, 100.34, 100.42]
    down = [
        (100.30, 100.35, 100.10, 100.15),
        (100.15, 100.20, 99.98, 100.02),
        (100.02, 100.10, 99.90, 99.95),
        (99.95, 100.05, 99.88, 100.00),
        (100.00, 100.12, 99.95, 100.08),
        (100.08, 100.28, 100.05, 100.24),
        (100.24, 100.45, 100.22, 100.42),
        (100.42, 100.50, 100.30, 100.38),
        (100.38, 100.42, 100.15, 100.20),
    ]
    ema_down = [100.60, 100.55, 100.50, 100.46, 100.42, 100.38, 100.34, 100.30, 100.26]
    ors = [(100.05, 100.42), (99.88, 100.35)]

    for ax, candles, ema, (lo, hi), title in zip(
        axes, (up, down), (ema_up, ema_down), ors,
        ("Giá trên EMA tăng → được vào", "Giá dưới EMA giảm → bỏ qua"), strict=True,
    ):
        ax.set_title(title, loc="left", fontsize=16, fontweight="bold", pad=12)
        ax.add_patch(Rectangle((-0.46, lo), 4.92, hi - lo, fc=OR_FILL, ec=BLUE, lw=1.5))
        candlesticks(ax, range(len(candles)), candles)
        ax.plot(range(len(ema)), ema, color=PURPLE, lw=2.2, zorder=5)
        ax.axhline(hi, color=BLUE, lw=1.3, ls="--")
        ax.set(xlim=(-0.55, len(candles) - 0.35), ylim=(99.5, 101.05))
        ax.set_xticks([0, 4, len(candles) - 1])
        ax.set_yticks([99.8, 100.2, 100.6, 101.0], ["99,8", "100,2", "100,6", "101,0"])
        clean_axis(ax, "y")

    axes[0].set_xticklabels(["09:30", "10:30", "11:15"])
    axes[1].set_xticklabels(["09:30", "10:30", "11:30"])
    axes[0].text(0.3, 99.72, "EMA", color=PURPLE, fontsize=13, fontweight="bold")
    axes[1].text(0.3, 100.63, "EMA", color=PURPLE, fontsize=13, fontweight="bold")
    axes[0].scatter([5], [100.52], color=TEAL, s=62, zorder=6)
    label_event(axes[0], "Phá vùng cùng\nEMA → vào", (5, 100.52), (6.0, 100.85), TEAL)
    label_event(axes[1], "Phá đỉnh OR nhưng\nngược EMA → bỏ qua", (6, 100.45), (6.4, 100.80), RED)
    save(fig, "orb-loc-xu-huong")


def gap_and_go():
    fig, ax = plt.subplots(figsize=(10.7, 5.2))
    fig.subplots_adjust(left=0.08, right=0.88, bottom=0.17, top=0.82)
    headline(fig, "Gap-and-Go: phá vùng cùng hướng khoảng trống", "Dữ liệu mô phỏng · Không phải backtest · nến 1 phút")

    candles = [
        (101.10, 101.35, 101.05, 101.28),
        (101.28, 101.45, 101.20, 101.38),
        (101.38, 101.50, 101.25, 101.30),
        (101.30, 101.42, 101.18, 101.24),
        (101.24, 101.48, 101.20, 101.40),
        (101.40, 101.68, 101.38, 101.62),
        (101.62, 101.80, 101.55, 101.72),
        (101.72, 101.85, 101.65, 101.80),
        (101.80, 101.95, 101.72, 101.90),
    ]
    xs = list(range(len(candles)))
    prev_close, or_hi = 100.00, 101.50

    ax.hlines(prev_close, -0.5, 9.5, color=MUTED, lw=1.4, ls=":")
    ax.text(4.5, 99.94, "Đóng cửa hôm trước", color=MUTED, fontsize=13, ha="center", va="top")
    ax.annotate(
        "", xy=(-0.2, 101.10), xytext=(-0.2, prev_close),
        arrowprops={"arrowstyle": "<->", "color": PURPLE, "lw": 1.8},
    )
    ax.text(0.4, 100.55, "Khoảng trống\nqua đêm > ATR", color=PURPLE, fontsize=13, va="center")

    ax.add_patch(Rectangle((-0.46, 101.05), 4.92, or_hi - 101.05, fc=OR_FILL, ec=BLUE, lw=1.5))
    ax.text(1.95, 101.68, "Vùng OR 5 phút", color=BLUE, fontweight="bold", ha="center", va="bottom")
    ax.hlines(or_hi, 4.5, 10.0, color=BLUE, lw=1.3, ls="--")
    ax.text(10.45, or_hi, "Đỉnh OR", color=BLUE, fontsize=13, va="center")

    candlesticks(ax, xs, candles)
    ax.scatter([5], [101.62], color=TEAL, s=62, zorder=5)
    label_event(ax, "Phá vùng cùng\nhướng gap → vào", (5, 101.62), (6.4, 102.05), TEAL)
    ax.text(4.5, 100.28, "Nếu giá lấp khoảng trống sớm, bỏ qua tín hiệu đi tiếp (không minh họa)",
            color=MUTED, fontsize=13, ha="center")

    ax.set(xlim=(-0.7, 11.5), ylim=(99.75, 102.25))
    ax.set_xticks([0, 4, 8], ["09:30", "09:34", "09:38"])
    ax.set_yticks([100.0, 100.5, 101.0, 101.5, 102.0], ["100,0", "100,5", "101,0", "101,5", "102,0"])
    clean_axis(ax, "y")
    save(fig, "orb-gap-and-go")


def failed_orb():
    fig, ax = plt.subplots(figsize=(10.7, 5.2))
    fig.subplots_adjust(left=0.08, right=0.88, bottom=0.17, top=0.82)
    headline(fig, "Failed ORB: nến đóng trở lại trong vùng", "Dữ liệu mô phỏng · Không phải backtest · nến 1 phút")

    candles = [
        (100.12, 100.27, 100.00, 100.23),
        (100.23, 100.28, 100.10, 100.16),
        (100.16, 100.32, 100.13, 100.28),
        (100.28, 100.40, 100.24, 100.35),
        (100.35, 100.38, 100.22, 100.29),
        (100.29, 100.52, 100.28, 100.48),
        (100.48, 100.55, 100.40, 100.45),
        (100.45, 100.46, 100.22, 100.28),
        (100.28, 100.32, 100.05, 100.10),
        (100.10, 100.15, 99.92, 99.96),
        (99.96, 100.05, 99.80, 99.85),
        (99.85, 99.95, 99.70, 99.78),
    ]
    xs = list(range(len(candles)))
    or_lo, or_hi, entry = 100.00, 100.40, 100.48

    ax.add_patch(Rectangle((-0.46, or_lo), 4.92, or_hi - or_lo, fc=OR_FILL, ec=BLUE, lw=1.5))
    ax.text(1.95, 100.57, "Vùng OR 5 phút", color=BLUE, fontweight="bold", ha="center")
    ax.hlines(or_hi, 4.5, 12.5, color=BLUE, lw=1.3, ls=":")
    ax.hlines(or_lo, 4.5, 12.5, color=BLUE, lw=1.3, ls=":")
    ax.hlines(entry, 5.0, 8.0, color=BLUE, lw=1.4, ls="--")

    candlesticks(ax, xs, candles)
    ax.scatter([5, 7], [entry, 100.28], color=[BLUE, RED], s=62, zorder=5)
    label_event(ax, "Đóng trên đỉnh\n→ vào long", (5, entry), (5.6, 100.78), BLUE)
    label_event(ax, "Đóng lại trong vùng\n→ thoát", (7, 100.28), (8.2, 100.62), RED)
    label_event(ax, "Biên đối diện:\ntín hiệu riêng nếu\nvào ngược", (11, 99.78), (11.6, 100.18), PURPLE)

    ax.set(xlim=(-0.7, 13.8), ylim=(99.45, 100.95))
    ax.set_xticks([0, 4, 7, 11], ["09:30", "09:34", "09:37", "09:41"])
    ax.set_yticks([99.6, 99.8, 100.0, 100.2, 100.4, 100.6, 100.8],
                  ["99,6", "99,8", "100,0", "100,2", "100,4", "100,6", "100,8"])
    clean_axis(ax, "y")
    save(fig, "orb-pha-vo-that-bai")


if __name__ == "__main__":
    OUTPUT.mkdir(parents=True, exist_ok=True)
    mechanics()
    short_example()
    entries()
    or_candle_color()
    rvol()
    range_narrow_vs_wide()
    research_paper()
    orb_setups()
    retest()
    trend_filter()
    gap_and_go()
    failed_orb()
