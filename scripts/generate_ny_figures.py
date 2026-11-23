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
    headline(fig, "Một lệnh short Silver Bullet diễn ra thế nào?", "Dữ liệu mô phỏng · Không phải backtest · nến 5 phút")

    candles = [
        (99.80, 99.95, 99.60, 99.90),
        (99.90, 100.10, 99.75, 100.05),
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
    xs = [x - 2 for x in range(len(candles))]
    swept_high, entry, target = 100.56, 100.20, 99.60

    ax.hlines(100.42, -0.5, 5.5, color=MUTED, lw=1.4, ls="--")
    ax.text(-0.4, 100.44, "Đỉnh gần nhất (thanh khoản)", color=MUTED, fontsize=13, va="bottom")
    ax.hlines(99.60, -2.5, 12.6, color=MUTED, lw=1.4, ls="--")
    ax.text(9.6, 99.54, "Đáy gần nhất (thanh khoản đối diện)", color=MUTED, fontsize=13, va="top")

    ax.add_patch(Rectangle((6.6, 100.15), 2.9, 0.10, fc=FVG_FILL, ec=PURPLE, lw=1.5, zorder=2))
    ax.text(8.05, 100.31, "FVG (khoảng trống giá)", color=PURPLE, fontsize=13, ha="center", va="bottom")

    ax.hlines(swept_high + 0.04, 5.5, 12.6, color=RED, lw=1.4, ls="--")
    ax.text(12.8, swept_high + 0.04, "Dừng lỗ", color=RED, fontsize=14, va="center")
    ax.hlines(entry, 9.5, 12.6, color=BLUE, lw=1.4, ls="--")
    ax.text(12.8, entry, "Vào short", color=BLUE, fontsize=14, va="center")
    ax.hlines(target, 11.5, 12.6, color=TEAL, lw=1.4, ls="--")
    ax.text(12.8, target, "Mục tiêu", color=TEAL, fontsize=14, va="center")

    candlesticks(ax, xs, candles)
    label_event(ax, "1. Quét thanh khoản\n(Judas Swing)", (5, 100.56), (4.4, 100.85), RED)
    label_event(ax, "2. Displacement\nđể lại FVG", (7, 99.95), (6.2, 99.62), PURPLE)
    label_event(ax, "3. Hồi về FVG\n→ vào lệnh", (10, entry), (10.7, 100.42), BLUE)

    ax.set(xlim=(-2.6, 14.6), ylim=(99.45, 101.0))
    ax.set_xticks([-2, 0, 4, 8, 12], ["09:30", "09:40", "10:00", "10:20", "10:40"])
    ax.set_yticks([99.6, 100, 100.4, 100.8], ["99,6", "100,0", "100,4", "100,8"])
    clean_axis(ax, "y")
    save(fig, "ny-silver-bullet-co-che")


def range_forex():
    fig, ax = plt.subplots(figsize=(10.7, 5.2))
    fig.subplots_adjust(left=0.09, right=0.86, bottom=0.17, top=0.82)
    headline(fig, "Setup range 8:00–9:30 trên Forex", "Dữ liệu mô phỏng (kiểu EURUSD) · Không phải backtest · nến 15 phút")

    candles = [
        (1.0820, 1.0835, 1.0810, 1.0830),
        (1.0830, 1.0842, 1.0822, 1.0826),
        (1.0826, 1.0850, 1.0800, 1.0835),
        (1.0835, 1.0844, 1.0820, 1.0828),
        (1.0828, 1.0840, 1.0818, 1.0836),
        (1.0836, 1.0845, 1.0825, 1.0842),
        (1.0842, 1.0848, 1.0828, 1.0840),
        (1.0840, 1.0846, 1.0825, 1.0830),
        (1.0830, 1.0868, 1.0828, 1.0865),
        (1.0865, 1.0882, 1.0860, 1.0878),
        (1.0878, 1.0900, 1.0875, 1.0896),
        (1.0896, 1.0915, 1.0890, 1.0912),
        (1.0912, 1.0930, 1.0905, 1.0926),
        (1.0926, 1.0948, 1.0920, 1.0945),
        (1.0945, 1.0952, 1.0938, 1.0946),
    ]
    xs = list(range(len(candles)))
    range_lo, range_hi, mid = 1.0800, 1.0850, 1.0825
    entry, target = 1.0865, 1.0945

    ax.add_patch(Rectangle((-0.4, range_lo), 5.9, range_hi - range_lo, fc=OR_FILL, ec=BLUE, lw=1.5, zorder=1))
    ax.text(2.5, range_lo - 0.0006, "Range 8:00–9:30 (gồm nến tin 8:30)", color=BLUE, fontsize=13, ha="center", va="top")
    ax.hlines(mid, -0.4, 14.5, color=RED, lw=1.3, ls=":")
    ax.text(14.7, mid, "Dừng lỗ\n(giữa range)", color=RED, fontsize=12, va="center")
    ax.hlines(entry, 8.0, 14.5, color=BLUE, lw=1.4, ls="--")
    ax.text(14.7, entry, "Vào lệnh", color=BLUE, fontsize=14, va="center")
    ax.hlines(target, 12.5, 14.5, color=TEAL, lw=1.4, ls="--")
    ax.text(14.7, target, "Mục tiêu 2R", color=TEAL, fontsize=14, va="center")

    candlesticks(ax, xs, candles)
    label_event(ax, "Nến 15 phút đóng\nngoài range → vào", (8, 1.0868), (7.6, 1.0910), BLUE)

    ax.set(xlim=(-0.7, 16.6), ylim=(1.0780, 1.0960))
    ax.set_xticks([0, 2, 6, 10, 14], ["08:00", "08:30", "09:30", "10:30", "11:30"])
    ax.set_yticks([1.0800, 1.0850, 1.0900, 1.0950], ["1,0800", "1,0850", "1,0900", "1,0950"])
    clean_axis(ax, "y")
    save(fig, "ny-range-forex")


def initial_balance():
    fig, ax = plt.subplots(figsize=(10.7, 5.2))
    fig.subplots_adjust(left=0.08, right=0.86, bottom=0.17, top=0.82)
    headline(fig, "Initial Balance: range giờ đầu phiên (9:30–10:30)", "Dữ liệu mô phỏng · Không phải backtest · nến 10 phút")

    candles = [
        (100.00, 100.15, 99.90, 100.10),
        (100.10, 100.30, 100.05, 100.25),
        (100.25, 100.40, 100.18, 100.22),
        (100.22, 100.30, 100.00, 100.05),
        (100.05, 100.18, 99.95, 100.12),
        (100.12, 100.35, 100.10, 100.30),
        (100.30, 100.38, 100.15, 100.20),
        (100.20, 100.32, 100.10, 100.15),
        (100.15, 100.55, 100.12, 100.50),
        (100.50, 100.68, 100.42, 100.62),
        (100.62, 100.80, 100.55, 100.75),
        (100.75, 100.92, 100.70, 100.88),
        (100.88, 100.95, 100.72, 100.78),
        (100.78, 100.85, 100.60, 100.65),
        (100.65, 100.90, 100.62, 100.88),
        (100.88, 101.05, 100.85, 101.00),
        (101.00, 101.15, 100.95, 101.10),
        (101.10, 101.22, 101.02, 101.18),
        (101.18, 101.28, 101.08, 101.12),
        (101.12, 101.20, 101.00, 101.06),
    ]
    xs = list(range(len(candles)))
    ib_lo, ib_hi = 99.90, 100.40

    ax.add_patch(Rectangle((-0.4, ib_lo), 6.0, ib_hi - ib_lo, fc=OR_FILL, ec=BLUE, lw=1.5, zorder=1))
    ax.text(2.6, ib_hi + 0.05, "Initial Balance 9:30–10:30", color=BLUE, fontsize=13, ha="center")
    ax.hlines(ib_hi, 5.6, 19.5, color=MUTED, lw=1.2, ls=":")
    ax.hlines(ib_lo, 5.6, 19.5, color=MUTED, lw=1.2, ls=":")
    ax.text(19.7, ib_hi, "Đỉnh IB", color=MUTED, fontsize=13, va="center")
    ax.text(19.7, ib_lo, "Đáy IB", color=MUTED, fontsize=13, va="center")

    candlesticks(ax, xs, candles)
    label_event(ax, "Phá lên khỏi IB\n→ ngày có xu hướng", (8, 100.55), (7.2, 101.15), TEAL)
    ax.text(14, 99.62, "Giá quay lại trong IB thì coi là ngày đi ngang (không minh họa)", color=MUTED, fontsize=13, ha="center")

    ax.set(xlim=(-0.7, 21.6), ylim=(99.55, 101.5))
    ax.set_xticks([0, 6, 12, 18], ["09:30", "10:30", "11:30", "12:30"])
    ax.set_yticks([99.9, 100.4, 100.9, 101.4], ["99,9", "100,4", "100,9", "101,4"])
    clean_axis(ax, "y")
    save(fig, "ny-initial-balance")


def vwap():
    fig, ax = plt.subplots(figsize=(10.7, 5.2))
    fig.subplots_adjust(left=0.08, right=0.86, bottom=0.17, top=0.82)
    headline(fig, "Giá so với VWAP trong phiên", "Dữ liệu mô phỏng · Không phải backtest · nến 5 phút")

    closes = [
        100.00, 100.06, 100.12, 100.10, 100.18, 100.24, 100.30, 100.28, 100.36, 100.42,
        100.48, 100.46, 100.52, 100.55, 100.53, 100.50, 100.42, 100.30, 100.16, 100.08,
        100.05, 100.09, 100.11, 100.08, 100.10, 100.12, 100.09, 100.10, 100.11, 100.09,
    ]
    vols = [
        100, 110, 120, 105, 130, 140, 150, 120, 160, 170,
        175, 140, 180, 185, 160, 200, 320, 380, 340, 260,
        140, 110, 95, 85, 90, 95, 80, 85, 90, 80,
    ]
    candles = []
    prev = closes[0] - 0.03
    for i, c in enumerate(closes):
        o = prev
        h = max(o, c) + 0.04
        low = min(o, c) - 0.04
        candles.append((o, h, low, c))
        prev = c
    xs = list(range(len(candles)))

    vwap_line, num, den = [], 0.0, 0.0
    for c, v in zip(closes, vols, strict=True):
        num += c * v
        den += v
        vwap_line.append(num / den)

    candlesticks(ax, xs, candles)
    ax.plot(xs, vwap_line, color=PURPLE, lw=2.4, zorder=5)
    ax.text(29.8, vwap_line[-1], "VWAP", color=PURPLE, fontsize=14, va="center", fontweight="bold")

    label_event(ax, "Giá giữ trên VWAP\n→ theo xu hướng", (10, 100.30), (9.0, 99.94), TEAL)
    label_event(ax, "Cắt mạnh xuống VWAP\n→ cảnh báo đảo chiều", (18, 100.32), (20.5, 100.62), RED)

    ax.set(xlim=(-0.7, 32.0), ylim=(99.85, 100.72))
    ax.set_xticks([0, 6, 12, 18, 24], ["09:30", "10:00", "10:30", "11:00", "11:30"])
    ax.set_yticks([99.9, 100.1, 100.3, 100.5, 100.7], ["99,9", "100,1", "100,3", "100,5", "100,7"])
    clean_axis(ax, "y")
    save(fig, "ny-vwap")


def news_830():
    fig, ax = plt.subplots(figsize=(10.7, 5.2))
    fig.subplots_adjust(left=0.08, right=0.88, bottom=0.17, top=0.82)
    headline(fig, "Tin kinh tế Mỹ lúc 8:30", "Dữ liệu mô phỏng · Không phải backtest · nến 5 phút")

    candles = [
        (100.00, 100.05, 99.97, 100.02),
        (100.02, 100.06, 99.98, 100.04),
        (100.04, 100.08, 100.00, 100.05),
        (100.05, 100.80, 99.40, 100.25),
        (100.25, 100.45, 100.10, 100.15),
        (100.15, 100.30, 100.00, 100.22),
        (100.22, 100.28, 100.05, 100.10),
        (100.10, 100.15, 99.85, 99.90),
        (99.90, 99.95, 99.65, 99.70),
        (99.70, 99.78, 99.55, 99.60),
        (99.60, 99.68, 99.48, 99.52),
        (99.52, 99.60, 99.40, 99.45),
    ]
    xs = list(range(len(candles)))

    ax.hlines(100.08, -0.5, 2.6, color=MUTED, lw=1.2, ls=":")
    ax.hlines(99.97, -0.5, 2.6, color=MUTED, lw=1.2, ls=":")
    ax.text(1.0, 100.12, "Range trước tin", color=MUTED, fontsize=13, ha="center", va="bottom")

    candlesticks(ax, xs, candles)
    label_event(ax, "Nến tin 8:30:\ngiãn mạnh hai phía,\nspread nới rộng", (3, 100.80), (4.4, 100.90), RED)
    label_event(ax, "Chờ giá ổn định", (5.5, 100.15), (5.0, 100.62), MUTED)
    label_event(ax, "Theo hướng đã chọn\nsau khi ổn định", (9.3, 99.60), (10.8, 99.86), BLUE)

    ax.set(xlim=(-0.7, 12.6), ylim=(99.30, 101.05))
    ax.set_xticks([0, 3, 6, 9], ["08:15", "08:30", "08:45", "09:00"])
    ax.set_yticks([99.4, 99.7, 100.0, 100.3, 100.6, 100.9], ["99,4", "99,7", "100,0", "100,3", "100,6", "100,9"])
    clean_axis(ax, "y")
    save(fig, "ny-tin-830")


def london_fix():
    fig, ax = plt.subplots(figsize=(10.7, 5.2))
    fig.subplots_adjust(left=0.09, right=0.88, bottom=0.17, top=0.82)
    headline(fig, "Dòng tiền quanh London Fix (11:00 New York)", "Dữ liệu mô phỏng (kiểu EURUSD) · Không phải backtest · nến 5 phút")

    candles = [
        (1.0800, 1.0810, 1.0795, 1.0806),
        (1.0806, 1.0815, 1.0800, 1.0810),
        (1.0810, 1.0820, 1.0805, 1.0815),
        (1.0815, 1.0825, 1.0810, 1.0820),
        (1.0820, 1.0828, 1.0814, 1.0818),
        (1.0818, 1.0826, 1.0812, 1.0822),
        (1.0822, 1.0830, 1.0818, 1.0828),
        (1.0828, 1.0838, 1.0824, 1.0834),
        (1.0834, 1.0842, 1.0830, 1.0840),
        (1.0840, 1.0848, 1.0836, 1.0845),
        (1.0845, 1.0852, 1.0840, 1.0850),
        (1.0850, 1.0858, 1.0844, 1.0855),
        (1.0855, 1.0862, 1.0848, 1.0852),
        (1.0852, 1.0856, 1.0840, 1.0844),
        (1.0844, 1.0848, 1.0830, 1.0834),
        (1.0834, 1.0838, 1.0822, 1.0826),
        (1.0826, 1.0830, 1.0815, 1.0818),
        (1.0818, 1.0824, 1.0810, 1.0814),
        (1.0814, 1.0818, 1.0804, 1.0808),
        (1.0808, 1.0814, 1.0800, 1.0804),
        (1.0804, 1.0810, 1.0798, 1.0802),
        (1.0802, 1.0808, 1.0796, 1.0800),
    ]
    xs = list(range(len(candles)))

    ax.axvline(12, color=PURPLE, lw=1.6, ls="--", zorder=2)
    ax.text(12, 1.0874, "London Fix 11:00\n(16:00 giờ London)", color=PURPLE, fontsize=13, ha="center", va="bottom", fontweight="bold")

    candlesticks(ax, xs, candles)
    label_event(ax, "Dòng tiền tái cân bằng\nquanh Fix → đảo chiều", (14.5, 1.0828), (18.0, 1.0852), PURPLE)

    ax.set(xlim=(-0.7, 22.6), ylim=(1.0792, 1.0900))
    ax.set_xticks([0, 6, 12, 18], ["10:00", "10:30", "11:00", "11:30"])
    ax.set_yticks([1.0800, 1.0825, 1.0850, 1.0875], ["1,0800", "1,0825", "1,0850", "1,0875"])
    clean_axis(ax, "y")
    save(fig, "ny-london-fix")


def judas_swing():
    fig, ax = plt.subplots(figsize=(10.7, 5.2))
    fig.subplots_adjust(left=0.08, right=0.88, bottom=0.17, top=0.82)
    headline(fig, "Judas Swing: nhịp chạy sai hướng quanh giờ mở cửa", "Dữ liệu mô phỏng · Không phải backtest · nến 5 phút")

    candles = [
        (99.95, 100.00, 99.85, 99.88),
        (99.88, 99.90, 99.78, 99.80),
        (99.80, 99.84, 99.72, 99.74),
        (99.74, 99.78, 99.70, 99.72),
        (99.72, 99.85, 99.70, 99.82),
        (99.82, 99.95, 99.80, 99.92),
        (99.92, 100.02, 99.90, 100.00),
        (100.00, 100.10, 99.98, 100.08),
        (100.08, 100.12, 100.00, 100.04),
        (100.04, 100.05, 99.75, 99.78),
        (99.78, 99.80, 99.50, 99.55),
        (99.55, 99.85, 99.52, 99.82),
        (99.82, 100.05, 99.80, 100.02),
        (100.02, 100.25, 100.00, 100.22),
        (100.22, 100.40, 100.20, 100.38),
        (100.38, 100.55, 100.35, 100.52),
        (100.52, 100.62, 100.45, 100.58),
        (100.58, 100.75, 100.56, 100.72),
        (100.72, 100.85, 100.68, 100.82),
        (100.82, 100.90, 100.78, 100.86),
    ]
    xs = list(range(len(candles)))

    ax.hlines(99.70, -0.5, 12.5, color=MUTED, lw=1.4, ls="--")
    ax.text(-0.4, 99.66, "Đáy buổi sáng (thanh khoản)", color=MUTED, fontsize=13, va="top")
    ax.axvline(6, color=MUTED, lw=1, ls=":", zorder=1)
    ax.text(6, 100.97, "Mở cửa 9:30", color=MUTED, ha="center", va="bottom", fontsize=13)

    candlesticks(ax, xs, candles)
    label_event(ax, "Judas Swing:\nquét stop dưới đáy", (10, 99.50), (9.6, 99.32), RED)
    label_event(ax, "Đảo chiều đi\ntheo hướng thật", (16, 100.60), (14.6, 100.92), TEAL)

    ax.set(xlim=(-0.7, 20.6), ylim=(99.18, 101.15))
    ax.set_xticks([0, 6, 12, 18], ["09:00", "09:30", "10:00", "10:30"])
    ax.set_yticks([99.4, 99.7, 100.0, 100.3, 100.6, 100.9], ["99,4", "99,7", "100,0", "100,3", "100,6", "100,9"])
    clean_axis(ax, "y")
    save(fig, "ny-judas-swing")


def silver_bullet_long():
    fig, ax = plt.subplots(figsize=(10.7, 5.2))
    fig.subplots_adjust(left=0.08, right=0.86, bottom=0.17, top=0.82)
    headline(fig, "Một lệnh mua Silver Bullet diễn ra thế nào?", "Dữ liệu mô phỏng · Không phải backtest · nến 5 phút")

    candles = [
        (100.40, 100.55, 100.35, 100.42),
        (100.42, 100.45, 100.20, 100.25),
        (100.25, 100.30, 100.00, 100.05),
        (100.05, 100.10, 99.60, 99.68),
        (99.68, 99.85, 99.62, 99.80),
        (99.80, 99.90, 99.70, 99.75),
        (99.75, 99.78, 99.42, 99.48),
        (99.48, 100.02, 99.45, 99.98),
        (99.98, 100.15, 99.90, 100.12),
        (100.12, 100.20, 100.00, 100.05),
        (100.05, 100.10, 99.82, 99.88),
        (99.88, 100.10, 99.85, 100.05),
        (100.05, 100.30, 100.00, 100.28),
        (100.28, 100.45, 100.25, 100.42),
        (100.42, 100.56, 100.38, 100.52),
    ]
    xs = list(range(len(candles)))
    swept_low, entry, target = 99.38, 99.90, 100.55

    ax.hlines(100.55, -0.5, 7.5, color=MUTED, lw=1.4, ls="--")
    ax.text(-0.4, 100.57, "Đỉnh gần nhất (thanh khoản đối diện)", color=MUTED, fontsize=13, va="bottom")
    ax.hlines(99.60, -0.5, 6.5, color=MUTED, lw=1.4, ls="--")
    ax.text(-0.4, 99.56, "Đáy gần nhất (thanh khoản)", color=MUTED, fontsize=13, va="top")

    ax.add_patch(Rectangle((7.4, 99.78), 3.0, 0.12, fc=FVG_FILL, ec=PURPLE, lw=1.5, zorder=2))
    ax.text(8.9, 99.74, "FVG", color=PURPLE, fontsize=13, ha="center", va="top")

    ax.hlines(swept_low, 4.5, 14.6, color=RED, lw=1.4, ls="--")
    ax.text(14.8, swept_low, "Dừng lỗ", color=RED, fontsize=14, va="center")
    ax.hlines(entry, 10.0, 14.6, color=BLUE, lw=1.4, ls="--")
    ax.text(14.8, entry, "Vào lệnh mua", color=BLUE, fontsize=14, va="center")
    ax.hlines(target, 13.5, 14.6, color=TEAL, lw=1.4, ls="--")
    ax.text(14.8, target, "Mục tiêu", color=TEAL, fontsize=14, va="center")

    candlesticks(ax, xs, candles)
    label_event(ax, "1. Quét thanh khoản\n(Judas Swing)", (6, 99.42), (6.4, 99.16), RED)
    label_event(ax, "2. Displacement\nđể lại FVG", (7, 100.02), (6.3, 100.30), PURPLE)
    label_event(ax, "3. Hồi về FVG\n→ vào lệnh", (10, 99.88), (11.0, 99.55), BLUE)

    ax.set(xlim=(-0.7, 16.6), ylim=(99.08, 100.82))
    ax.set_xticks([0, 5, 10, 13], ["09:55", "10:20", "10:45", "11:00"])
    ax.set_yticks([99.4, 99.8, 100.2, 100.6], ["99,4", "99,8", "100,2", "100,6"])
    clean_axis(ax, "y")
    save(fig, "ny-silver-bullet-long")


def macro_windows():
    fig, ax = plt.subplots(figsize=(12.8, 5.4))
    fig.subplots_adjust(left=0.11, right=0.98, bottom=0.20, top=0.80)
    headline(
        fig,
        "8 khung Macro đối chiếu các Killzone trong ngày",
        "Giờ New York (dòng trên) · Giờ Việt Nam mùa đông (dòng dưới)",
    )

    killzones = [
        ("NY PM", 1.3, 37.5, 40.0),
        ("London Close", 2.1, 34.0, 36.0),
        ("NY AM", 2.9, 32.5, 35.0),
        ("London", 3.7, 26.0, 29.0),
        ("Asia", 4.5, 20.0, 24.0),
    ]
    for name, y, start, end in killzones:
        ax.add_patch(Rectangle((start, y - 0.22), end - start, 0.44, fc=OR_FILL, ec=BLUE, lw=1.3))
        ax.text((start + end) / 2, y, f"{fmt(start % 24)}–{fmt(end % 24)}", color=BLUE, ha="center", va="center", fontsize=12, fontweight="bold")

    macros = [
        (26.55, 27.00),
        (28.05, 28.50),
        (32.83, 33.17),
        (33.83, 34.17),
        (34.83, 35.17),
        (35.83, 36.17),
        (37.17, 37.67),
        (39.25, 39.75),
    ]
    for i, (start, end) in enumerate(macros):
        ax.add_patch(Rectangle((start, 0.08), end - start, 0.44, fc=PURPLE, ec=PURPLE))
        mid = (start + end) / 2
        y_label = -0.22 if i % 2 == 0 else -0.50
        ax.text(mid, y_label, f"{fmt(start % 24)}–{fmt(end % 24)}", color=PURPLE, ha="center", va="top", fontsize=11.5)

    ticks = list(range(20, 41, 2))
    ax.set_xticks(ticks, [f"{fmt(t % 24)}\n{vn(t % 24)}" for t in ticks], fontsize=11.5)
    ax.set_yticks([0.3, 1.3, 2.1, 2.9, 3.7, 4.5], ["Macro", "NY PM", "London\nClose", "NY AM", "London", "Asia"], fontsize=13)
    ax.set(xlim=(19.0, 40.4), ylim=(-0.95, 5.05))
    clean_axis(ax, "x")
    save(fig, "ny-macro-windows")


if __name__ == "__main__":
    OUTPUT.mkdir(parents=True, exist_ok=True)
    timeline()
    silver_bullet()
    range_forex()
    initial_balance()
    vwap()
    news_830()
    london_fix()
    judas_swing()
    silver_bullet_long()
    macro_windows()
