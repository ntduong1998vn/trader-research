from io import StringIO
from pathlib import Path

import matplotlib as mpl

mpl.use("Agg")

import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

OUTPUT = Path(__file__).resolve().parents[1] / "docs" / "assets" / "ny"
INK = "#14263c"
MUTED = "#43566f"
BLUE = "#2459a9"
TEAL = "#157358"
RED = "#aa3f44"
PURPLE = "#65429b"
GRID = "#dce4ed"
OR_FILL = "#eaf2fc"
FVG_FILL = "#f3ecfa"
LUNCH_FILL = "#f8e3e4"

mpl.rcdefaults()
mpl.rcParams.update(
    {
        "font.family": "DejaVu Sans",
        "font.size": 15,
        "text.color": INK,
        "axes.labelcolor": MUTED,
        "xtick.color": MUTED,
        "ytick.color": MUTED,
        "svg.hashsalt": "trader-research-ny",
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


def fmt(h):
    return f"{int(h):02d}:{int(round((h % 1) * 60)):02d}"


def vn(h):
    return f"{int(h + 12) % 24:02d}:{int(round((h % 1) * 60)):02d}"


def timeline():
    fig, ax = plt.subplots(figsize=(10.7, 4.9))
    fig.subplots_adjust(left=0.17, right=0.97, bottom=0.24, top=0.80)
    headline(
        fig,
        "Các khung ICT chồng lên nhau trong phiên New York",
        "Giờ New York · Dòng phụ là giờ Việt Nam mùa đông (NY + 12)",
    )

    ax.axvspan(11.5, 13.5, color=LUNCH_FILL, zorder=0)
    ax.text(12.5, 3.9, "Giờ trưa: nên tránh", color=RED, ha="center", fontsize=14)

    bars = [
        ("Killzone NY AM", 8.5, 11.0, OR_FILL, BLUE, 2.15),
        ("Silver Bullet", 10.0, 11.0, BLUE, BLUE, 1.15),
    ]
    for name, start, end, fc, ec, y in bars:
        ax.add_patch(Rectangle((start, y - 0.3), end - start, 0.6, fc=fc, ec=ec, lw=1.5))
    ax.text(9.72, 2.15, "8:30–11:00", color=BLUE, ha="center", va="center", fontweight="bold")
    ax.text(10.5, 1.55, "10:00–11:00", color=BLUE, ha="center", va="center", fontsize=14)

    for start, end in [(9.833, 10.167), (10.833, 11.167)]:
        ax.add_patch(Rectangle((start, -0.15), end - start, 0.6, fc=PURPLE, ec=PURPLE))
    ax.text(9.75, 0.15, "9:50–10:10", color=PURPLE, ha="right", va="center", fontsize=14)
    ax.text(11.25, 0.15, "10:50–11:10", color=PURPLE, ha="left", va="center", fontsize=14)
    ax.text(13.75, 0.15, "Macro (20–30 phút)", color=PURPLE, fontsize=14, va="center")

    for x, name in [(8.5, "Tin Mỹ"), (9.5, "Mở cửa\nchứng khoán")]:
        ax.axvline(x, color=MUTED, lw=1, ls=":", zorder=1)
        ax.text(x, 3.55, name, color=MUTED, ha="center", va="bottom", fontsize=13)

    ticks = [7, 8.5, 9.5, 11, 12, 13.5, 15, 16]
    ax.set_xticks(ticks, [f"{fmt(t)}\n{vn(t)}" for t in ticks])
    ax.set_yticks([0.15, 1.15, 2.15], ["Macro", "Silver Bullet", "Killzone NY AM"])
    ax.set(xlim=(7, 16), ylim=(-0.7, 4.4))
    ax.set_xlabel("Giờ NY (dòng trên) · Giờ VN mùa đông (dòng dưới)", labelpad=8)
    clean_axis(ax, "x")
    save(fig, "ny-khung-gio")


def silver_bullet():
    fig, ax = plt.subplots(figsize=(10.7, 5.2))
    fig.subplots_adjust(left=0.07, right=0.86, bottom=0.17, top=0.82)
    headline(fig, "Một lệnh short Silver Bullet diễn ra thế nào?", "Dữ liệu mô phỏng · Không phải backtest")

    candles = [
        (100.05, 100.15, 100.00, 100.10),
        (100.10, 100.42, 100.08, 100.38),
        (100.38, 100.40, 100.25, 100.30),
        (100.30, 100.35, 100.22, 100.28),
        (100.28, 100.38, 100.24, 100.33),
        (100.32, 100.56, 100.30, 100.34),
        (100.34, 100.36, 100.25, 100.28),
        (100.28, 100.29, 99.95, 99.98),
        (99.98, 100.15, 99.90, 100.05),
        (100.05, 100.18, 100.00, 100.16),
        (100.16, 100.22, 100.10, 100.12),
        (100.12, 100.14, 99.80, 99.85),
        (99.85, 99.88, 99.60, 99.65),
    ]
    swept_high, entry, target = 100.56, 100.20, 99.60

    ax.hlines(100.42, -0.5, 5.5, color=MUTED, lw=1.4, ls="--")
    ax.text(-0.4, 100.44, "Đỉnh gần nhất (thanh khoản)", color=MUTED, fontsize=13, va="bottom")
    ax.hlines(99.60, 9.5, 12.6, color=MUTED, lw=1.4, ls="--")
    ax.text(9.6, 99.54, "Đáy gần nhất (thanh khoản đối diện)", color=MUTED, fontsize=13, va="top")

    ax.add_patch(Rectangle((6.6, 100.15), 2.9, 0.10, fc=FVG_FILL, ec=PURPLE, lw=1.5, zorder=2))
    ax.text(8.05, 100.31, "FVG (khoảng trống giá)", color=PURPLE, fontsize=13, ha="center", va="bottom")

    ax.hlines(swept_high + 0.04, 5.5, 12.6, color=RED, lw=1.4, ls="--")
    ax.text(12.8, swept_high + 0.04, "Dừng lỗ", color=RED, fontsize=14, va="center")
    ax.hlines(entry, 9.5, 12.6, color=BLUE, lw=1.4, ls="--")
    ax.text(12.8, entry, "Vào short", color=BLUE, fontsize=14, va="center")
    ax.hlines(target, 11.5, 12.6, color=TEAL, lw=1.4, ls="--")
    ax.text(12.8, target, "Mục tiêu", color=TEAL, fontsize=14, va="center")

    candlesticks(ax, range(13), candles)
    label_event(ax, "1. Quét thanh khoản\n(Judas Swing)", (5, 100.56), (3.4, 100.85), RED)
    label_event(ax, "2. Displacement\nđể lại FVG", (7, 99.95), (6.2, 99.62), PURPLE)
    label_event(ax, "3. Hồi về FVG\n→ vào lệnh", (10, entry), (10.7, 100.42), BLUE)

    ax.set(xlim=(-0.55, 14.6), ylim=(99.45, 101.0))
    ax.set_xticks([0, 5, 7, 10, 12], ["09:50", "10:00", "10:15", "10:40", "10:55"])
    ax.set_yticks([99.6, 100, 100.4, 100.8], ["99,6", "100,0", "100,4", "100,8"])
    ax.set_xlabel("Giờ NY · nến 5 phút", labelpad=8)
    clean_axis(ax, "y")
    save(fig, "ny-silver-bullet-co-che")


if __name__ == "__main__":
    OUTPUT.mkdir(parents=True, exist_ok=True)
    timeline()
    silver_bullet()
