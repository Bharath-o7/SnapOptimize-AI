import tkinter as tk
from tkinter import ttk
import time


# ==========================================================
# SNAPOPTIMIZE AI - FINAL DASHBOARD
# ==========================================================

BASELINE_LATENCY = 198
OPTIMIZED_LATENCY = 177

BASELINE_MEMORY = 29.25
OPTIMIZED_MEMORY = 29.68

QUANT_BASELINE = 205
QUANT_OPTIMIZED = 193

IMPROVEMENT = ((BASELINE_LATENCY - OPTIMIZED_LATENCY)
               / BASELINE_LATENCY) * 100


# ==========================================================
# WINDOW
# ==========================================================

root = tk.Tk()
root.title("SnapOptimize AI - Qualcomm AI Performance Analyzer")
root.geometry("1150x780")
root.configure(bg="#071522")
root.resizable(False, False)


# ==========================================================
# COLORS
# ==========================================================

BG = "#071522"
PANEL = "#0D2233"
CARD = "#102B40"
TEXT = "#EAF6FF"
MUTED = "#8FA9BA"
GREEN = "#39E58C"
BLUE = "#35B6FF"
ORANGE = "#FFB454"
WHITE = "#FFFFFF"


# ==========================================================
# HEADER
# ==========================================================

header = tk.Frame(root, bg=BG)
header.pack(fill="x", padx=35, pady=(25, 5))

title = tk.Label(
    header,
    text="SNAPOPTIMIZE AI",
    font=("Segoe UI", 28, "bold"),
    fg=WHITE,
    bg=BG
)
title.pack(anchor="w")

subtitle = tk.Label(
    header,
    text="Adaptive AI Workload Optimization & Snapdragon Performance Analysis",
    font=("Segoe UI", 12),
    fg=MUTED,
    bg=BG
)
subtitle.pack(anchor="w", pady=(2, 0))


# ==========================================================
# TARGET BAR
# ==========================================================

target = tk.Frame(root, bg=PANEL)
target.pack(fill="x", padx=35, pady=18)

tk.Label(
    target,
    text="MODEL",
    font=("Segoe UI", 9, "bold"),
    fg=MUTED,
    bg=PANEL
).pack(side="left", padx=(20, 5), pady=15)

tk.Label(
    target,
    text="SqueezeNet ONNX",
    font=("Segoe UI", 11, "bold"),
    fg=TEXT,
    bg=PANEL
).pack(side="left", padx=(0, 35))

tk.Label(
    target,
    text="TARGET",
    font=("Segoe UI", 9, "bold"),
    fg=MUTED,
    bg=PANEL
).pack(side="left", padx=(10, 5))

tk.Label(
    target,
    text="Snapdragon X Elite",
    font=("Segoe UI", 11, "bold"),
    fg=BLUE,
    bg=PANEL
).pack(side="left")


# ==========================================================
# METRIC CARDS
# ==========================================================

cards = tk.Frame(root, bg=BG)
cards.pack(fill="x", padx=35)


def make_card(parent, title_text, value_text, color, subtitle_text):
    card = tk.Frame(
        parent,
        bg=CARD,
        width=245,
        height=135
    )
    card.pack(side="left", expand=True, fill="both", padx=7)
    card.pack_propagate(False)

    tk.Label(
        card,
        text=title_text,
        font=("Segoe UI", 10, "bold"),
        fg=MUTED,
        bg=CARD
    ).pack(anchor="w", padx=18, pady=(15, 0))

    tk.Label(
        card,
        text=value_text,
        font=("Segoe UI", 25, "bold"),
        fg=color,
        bg=CARD
    ).pack(anchor="w", padx=18, pady=(5, 0))

    tk.Label(
        card,
        text=subtitle_text,
        font=("Segoe UI", 9),
        fg=MUTED,
        bg=CARD
    ).pack(anchor="w", padx=18)

    return card


make_card(
    cards,
    "BASELINE LATENCY",
    "198 µs",
    ORANGE,
    "AI Hub estimated inference"
)

make_card(
    cards,
    "OPTIMIZED LATENCY",
    "177 µs",
    GREEN,
    "Compiled configuration"
)

make_card(
    cards,
    "LATENCY IMPROVEMENT",
    f"{IMPROVEMENT:.2f}%",
    GREEN,
    "Lower estimated latency"
)

make_card(
    cards,
    "PEAK MEMORY",
    "29.68 MiB",
    BLUE,
    "Optimized configuration"
)


# ==========================================================
# BEFORE / AFTER
# ==========================================================

comparison = tk.Frame(root, bg=PANEL)
comparison.pack(fill="x", padx=42, pady=25)

tk.Label(
    comparison,
    text="BEFORE vs AFTER",
    font=("Segoe UI", 14, "bold"),
    fg=WHITE,
    bg=PANEL
).pack(anchor="w", padx=20, pady=(15, 10))


def progress_row(parent, label, value, maximum, color):

    row = tk.Frame(parent, bg=PANEL)
    row.pack(fill="x", padx=20, pady=7)

    tk.Label(
        row,
        text=label,
        width=16,
        anchor="w",
        font=("Segoe UI", 10, "bold"),
        fg=TEXT,
        bg=PANEL
    ).pack(side="left")

    bar_bg = tk.Frame(
        row,
        bg="#18384E",
        height=20
    )
    bar_bg.pack(
        side="left",
        fill="x",
        expand=True,
        padx=10
    )

    width = int((value / maximum) * 600)

    bar = tk.Frame(
        bar_bg,
        bg=color,
        height=20,
        width=width
    )
    bar.pack(side="left")

    tk.Label(
        row,
        text=f"{value} µs",
        width=10,
        anchor="e",
        font=("Segoe UI", 10, "bold"),
        fg=color,
        bg=PANEL
    ).pack(side="right")


progress_row(
    comparison,
    "Baseline",
    BASELINE_LATENCY,
    BASELINE_LATENCY,
    ORANGE
)

progress_row(
    comparison,
    "Optimized",
    OPTIMIZED_LATENCY,
    BASELINE_LATENCY,
    GREEN
)


# ==========================================================
# OPTIMIZATION OBSERVATION
# ==========================================================

observation = tk.Frame(root, bg=CARD)
observation.pack(fill="x", padx=42, pady=5)

tk.Label(
    observation,
    text="OPTIMIZATION OBSERVATION",
    font=("Segoe UI", 12, "bold"),
    fg=WHITE,
    bg=CARD
).pack(anchor="w", padx=20, pady=(14, 5))

tk.Label(
    observation,
    text=(
        "QuantizeLinear operation: "
        f"{QUANT_BASELINE} µs → {QUANT_OPTIMIZED} µs"
    ),
    font=("Segoe UI", 11, "bold"),
    fg=ORANGE,
    bg=CARD
).pack(anchor="w", padx=20)

tk.Label(
    observation,
    text=(
        "The operation remained CPU-executed in the profiled configuration. "
        "The comparison does not attribute the total improvement to this "
        "operation alone."
    ),
    font=("Segoe UI", 9),
    fg=MUTED,
    bg=CARD,
    wraplength=1000,
    justify="left"
).pack(anchor="w", padx=20, pady=(3, 14))


# ==========================================================
# PIPELINE
# ==========================================================

pipeline = tk.Frame(root, bg=BG)
pipeline.pack(fill="x", padx=42, pady=15)

steps = [
    ("AI MODEL", BLUE),
    ("PROFILE", BLUE),
    ("ANALYZE", BLUE),
    ("COMPILE", GREEN),
    ("COMPARE", GREEN)
]

for i, (text, color) in enumerate(steps):

    tk.Label(
        pipeline,
        text=text,
        font=("Segoe UI", 10, "bold"),
        fg=color,
        bg=BG
    ).pack(side="left", expand=True)

    if i < len(steps) - 1:
        tk.Label(
            pipeline,
            text="→",
            font=("Segoe UI", 16, "bold"),
            fg=MUTED,
            bg=BG
        ).pack(side="left")


# ==========================================================
# FOOTER
# ==========================================================

footer = tk.Label(
    root,
    text=(
        "SnapOptimize AI | Qualcomm AI Hub profile comparison | "
        "SqueezeNet ONNX | Snapdragon X Elite"
    ),
    font=("Segoe UI", 9),
    fg=MUTED,
    bg=BG
)

footer.pack(side="bottom", pady=12)


# ==========================================================
# START
# ==========================================================

root.mainloop()