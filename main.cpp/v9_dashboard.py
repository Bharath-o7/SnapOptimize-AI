import tkinter as tk
import subprocess
import sys
import os
import threading
import time
import math


# ============================================================
# SNAPOPTIMIZE AI - V9 OCEAN UI
# ============================================================

root = tk.Tk()

root.title("⚡ SnapOptimize AI - V9")
root.geometry("1000x720")
root.resizable(False, False)


# ============================================================
# COLORS
# ============================================================

OCEAN_TOP = "#DDF8FF"
OCEAN_MIDDLE = "#65D9F2"
OCEAN_BOTTOM = "#05B9E8"

DARK_BLUE = "#062B5C"
BLUE = "#0878D1"
BUTTON_BLUE = "#0569B5"

CARD = "#F5FCFF"
CARD_BORDER = "#B9E8F5"
WHITE = "#FFFFFF"


# ============================================================
# VARIABLES
# ============================================================

status_var = tk.StringVar(
    value="Ready to analyze AI workload"
)

baseline_var = tk.StringVar(value="--")
optimized_var = tk.StringVar(value="--")
improvement_var = tk.StringVar(value="--")
throughput_var = tk.StringVar(value="--")


# ============================================================
# OCEAN BACKGROUND
# ============================================================

canvas = tk.Canvas(
    root,
    width=1000,
    height=720,
    highlightthickness=0
)

canvas.place(x=0, y=0)


def draw_ocean():

    # Sky / water gradient
    steps = 100

    for i in range(steps):

        ratio = i / (steps - 1)

        if ratio < 0.42:

            # Light sky
            r = int(221 + (101 - 221) * (ratio / 0.42))
            g = int(248 + (217 - 248) * (ratio / 0.42))
            b = int(255 + (242 - 255) * (ratio / 0.42))

        else:

            # Deep ocean
            local = (ratio - 0.42) / 0.58

            r = int(101 + (5 - 101) * local)
            g = int(217 + (185 - 217) * local)
            b = int(242 + (232 - 242) * local)

        color = "#{:02x}{:02x}{:02x}".format(
            r, g, b
        )

        y1 = int(i * 720 / steps)
        y2 = int((i + 1) * 720 / steps)

        canvas.create_rectangle(
            0,
            y1,
            1000,
            y2,
            fill=color,
            outline=color
        )

    # Horizon
    canvas.create_line(
        0,
        305,
        1000,
        305,
        fill="#B5F3FF",
        width=2
    )

    # Ocean waves
    for wave in range(12):

        y = 350 + wave * 32

        points = []

        for x in range(0, 1001, 10):

            wave_y = (
                y
                + math.sin(x / 55 + wave) * 5
            )

            points.extend([x, wave_y])

        canvas.create_line(
            *points,
            fill="#72E5F6",
            width=2
        )

    # Small water highlights
    for x in range(40, 1000, 120):

        y = 390 + (x % 90)

        canvas.create_line(
            x,
            y,
            x + 55,
            y,
            fill="#A9F2FA",
            width=2
        )


draw_ocean()


# ============================================================
# TITLE
# ============================================================

title = tk.Label(
    root,
    text="⚡ SnapOptimize AI",
    font=("Segoe UI", 30, "bold"),
    fg=DARK_BLUE,
    bg=OCEAN_TOP
)

title.place(
    x=0,
    y=45,
    width=1000,
    height=45
)


subtitle = tk.Label(
    root,
    text="AI Workload Performance Optimization",
    font=("Segoe UI", 15),
    fg=DARK_BLUE,
    bg=OCEAN_TOP
)

subtitle.place(
    x=0,
    y=92,
    width=1000,
    height=30
)


# ============================================================
# STATUS
# ============================================================

status = tk.Label(
    root,
    textvariable=status_var,
    font=("Segoe UI", 12),
    fg=DARK_BLUE,
    bg=OCEAN_TOP
)

status.place(
    x=0,
    y=135,
    width=1000,
    height=30
)


# ============================================================
# RUN BUTTON
# ============================================================

run_button = tk.Button(
    root,
    text="▶  RUN AI ANALYSIS",
    command=lambda: run_analysis(),
    font=("Segoe UI", 15, "bold"),
    fg=WHITE,
    bg=BUTTON_BLUE,
    activebackground="#075B99",
    activeforeground=WHITE,
    relief="flat",
    cursor="hand2",
    padx=35,
    pady=12
)

run_button.place(
    x=340,
    y=175,
    width=320,
    height=65
)


# ============================================================
# RESULT CARDS
# ============================================================

def create_card(
    title,
    variable,
    x_position,
    icon
):

    frame = tk.Frame(
        root,
        bg=CARD,
        highlightbackground=CARD_BORDER,
        highlightthickness=2
    )

    frame.place(
        x=x_position,
        y=275,
        width=215,
        height=145
    )

    icon_label = tk.Label(
        frame,
        text=icon,
        font=("Segoe UI", 20),
        fg=BLUE,
        bg=CARD
    )

    icon_label.pack(
        pady=(12, 0)
    )

    title_label = tk.Label(
        frame,
        text=title,
        font=("Segoe UI", 11, "bold"),
        fg=DARK_BLUE,
        bg=CARD
    )

    title_label.pack()

    value_label = tk.Label(
        frame,
        textvariable=variable,
        font=("Segoe UI", 20, "bold"),
        fg=DARK_BLUE,
        bg=CARD
    )

    value_label.pack(
        pady=(8, 0)
    )


create_card(
    "Baseline",
    baseline_var,
    35,
    "◉"
)

create_card(
    "Optimized",
    optimized_var,
    270,
    "🚀"
)

create_card(
    "Latency Reduction",
    improvement_var,
    505,
    "↘"
)

create_card(
    "Throughput Gain",
    throughput_var,
    740,
    "↗"
)


# ============================================================
# AI WORKLOAD PANEL
# ============================================================

workload_frame = tk.Frame(
    root,
    bg=CARD,
    highlightbackground=CARD_BORDER,
    highlightthickness=2
)

workload_frame.place(
    x=60,
    y=450,
    width=880,
    height=125
)


workload_title = tk.Label(
    workload_frame,
    text="⚙  AI Workload",
    font=("Segoe UI", 14, "bold"),
    fg=DARK_BLUE,
    bg=CARD
)

workload_title.pack(
    anchor="w",
    padx=25,
    pady=(15, 8)
)


workload_text = tk.Label(
    workload_frame,
    text=(
        "Model: SqueezeNet        |        "
        "Task: Image Classification        |        "
        "Input: 224 × 224        |        "
        "Execution: ONNX Runtime CPU"
    ),
    font=("Segoe UI", 11),
    fg=DARK_BLUE,
    bg=CARD
)

workload_text.pack(
    pady=8
)


# ============================================================
# FOOTER
# ============================================================

footer = tk.Label(
    root,
    text=(
        "🌊  Prototype: Snapdragon deployment can be evaluated "
        "on supported Qualcomm hardware.  🌊"
    ),
    font=("Segoe UI", 10),
    fg=DARK_BLUE,
    bg="#5DD8EF"
)

footer.place(
    x=0,
    y=650,
    width=1000,
    height=35
)


# ============================================================
# ANALYSIS FUNCTIONS
# ============================================================

def run_analysis():

    run_button.config(
        state="disabled"
    )

    status_var.set(
        "Starting AI workload analysis..."
    )

    baseline_var.set("--")
    optimized_var.set("--")
    improvement_var.set("--")
    throughput_var.set("--")

    thread = threading.Thread(
        target=analysis_process
    )

    thread.daemon = True
    thread.start()


def analysis_process():

    steps = [

        "Loading SqueezeNet AI model...",

        "Preparing test input...",

        "Running baseline benchmark...",

        "Analyzing AI workload...",

        "Applying ONNX Runtime optimization...",

        "Running optimized benchmark...",

        "Comparing performance..."

    ]

    for step in steps:

        root.after(
            0,
            lambda s=step:
            status_var.set(s)
        )

        time.sleep(0.8)


    # --------------------------------------------------------
    # Project paths
    # --------------------------------------------------------

    project_root = os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            ".."
        )
    )

    v8_file = os.path.join(
        os.path.dirname(__file__),
        "ai_inference.py"
    )


    try:

        result = subprocess.run(
            [
                sys.executable,
                v8_file
            ],

            cwd=project_root,

            capture_output=True,

            text=True
        )


        output = result.stdout


        # ----------------------------------------------------
        # Extract benchmark values
        # ----------------------------------------------------

        baseline = extract_value(
            output,
            "Baseline latency:"
        )

        optimized = extract_value(
            output,
            "Optimized latency:"
        )

        improvement = extract_value(
            output,
            "Latency improvement:"
        )

        throughput = extract_value(
            output,
            "Throughput improvement:"
        )


        # ----------------------------------------------------
        # Show results
        # ----------------------------------------------------

        root.after(
            0,
            lambda:
            show_results(
                baseline,
                optimized,
                improvement,
                throughput
            )
        )


    except Exception as e:

        root.after(
            0,
            lambda:
            status_var.set(
                "Error: " + str(e)
            )
        )

        root.after(
            0,
            lambda:
            run_button.config(
                state="normal"
            )
        )


# ============================================================
# EXTRACT VALUES
# ============================================================

def extract_value(
    text,
    label
):

    for line in text.splitlines():

        if label in line:

            value = line.split(
                label
            )[1].strip()

            return value

    return "N/A"


# ============================================================
# SHOW RESULTS
# ============================================================

def show_results(
    baseline,
    optimized,
    improvement,
    throughput
):

    # FIXED: no duplicate "ms"
    baseline_var.set(
        baseline
    )

    optimized_var.set(
        optimized
    )

    improvement_var.set(
        improvement
    )

    throughput_var.set(
        throughput
    )

    status_var.set(
        "Analysis complete — optimization detected"
    )

    run_button.config(
        state="normal"
    )


# ============================================================
# START APPLICATION
# ============================================================

root.mainloop()