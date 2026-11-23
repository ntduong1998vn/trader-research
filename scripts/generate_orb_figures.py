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


if __name__ == "__main__":
    OUTPUT.mkdir(parents=True, exist_ok=True)
    mechanics()
    entries()
    research_paper()
    orb_setups()
