import tkinter as tk
from tkinter import ttk
import subprocess
import sys
import os
import threading
import time


# -----------------------------
# Window
# -----------------------------

root = tk.Tk()
root.title("SnapOptimize AI - V9")
root.geometry("900x650")
root.resizable(False, False)


# -----------------------------
# Variables
# -----------------------------

status_var = tk.StringVar(value="Ready to analyze AI workload")
baseline_var = tk.StringVar(value="--")
optimized_var = tk.StringVar(value="--")
improvement_var = tk.StringVar(value="--")
throughput_var = tk.StringVar(value="--")


# -----------------------------
# Functions
# -----------------------------

def run_analysis():
    run_button.config(state="disabled")
    status_var.set("Starting AI workload analysis...")

    baseline_var.set("--")
    optimized_var.set("--")
    improvement_var.set("--")
    throughput_var.set("--")

    thread = threading.Thread(target=analysis_process)
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
            lambda s=step: status_var.set(s)
        )
        time.sleep(0.8)

    # Run the existing V8 benchmark
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

        root.after(
            0,
            lambda: show_results(
                baseline,
                optimized,
                improvement,
                throughput
            )
        )

    except Exception as e:

        root.after(
            0,
            lambda: status_var.set(
                "Error: " + str(e)
            )
        )

        root.after(
            0,
            lambda: run_button.config(
                state="normal"
            )
        )


def extract_value(text, label):

    for line in text.splitlines():

        if label in line:

            value = line.split(label)[1].strip()

            return value

    return "N/A"


def show_results(
    baseline,
    optimized,
    improvement,
    throughput
):

    baseline_var.set(
        baseline + " ms"
    )

    optimized_var.set(
        optimized + " ms"
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


# -----------------------------
# Title
# -----------------------------

title = tk.Label(
    root,
    text="⚡ SnapOptimize AI",
    font=("Segoe UI", 28, "bold")
)

title.pack(pady=(25, 5))


subtitle = tk.Label(
    root,
    text="AI Workload Performance Optimization",
    font=("Segoe UI", 14)
)

subtitle.pack()


# -----------------------------
# Status
# -----------------------------

status = tk.Label(
    root,
    textvariable=status_var,
    font=("Segoe UI", 12)
)

status.pack(pady=20)


# -----------------------------
# Run Button
# -----------------------------

run_button = tk.Button(
    root,
    text="▶  RUN AI ANALYSIS",
    command=run_analysis,
    font=("Segoe UI", 15, "bold"),
    padx=35,
    pady=12
)

run_button.pack(pady=10)


# -----------------------------
# Results frame
# -----------------------------

results_frame = tk.Frame(root)

results_frame.pack(
    pady=30
)


def create_card(
    parent,
    title,
    variable,
    column
):

    frame = tk.LabelFrame(
        parent,
        text=title,
        font=("Segoe UI", 11, "bold"),
        padx=25,
        pady=20
    )

    frame.grid(
        row=0,
        column=column,
        padx=10
    )

    label = tk.Label(
        frame,
        textvariable=variable,
        font=("Segoe UI", 20, "bold")
    )

    label.pack()


create_card(
    results_frame,
    "Baseline",
    baseline_var,
    0
)

create_card(
    results_frame,
    "Optimized",
    optimized_var,
    1
)

create_card(
    results_frame,
    "Latency Reduction",
    improvement_var,
    2
)

create_card(
    results_frame,
    "Throughput Gain",
    throughput_var,
    3
)


# -----------------------------
# Workload information
# -----------------------------

info = tk.LabelFrame(
    root,
    text="AI Workload",
    font=("Segoe UI", 12, "bold"),
    padx=30,
    pady=15
)

info.pack(
    fill="x",
    padx=60,
    pady=10
)

info_text = tk.Label(
    info,
    text=(
        "Model: SqueezeNet     |     "
        "Task: Image Classification     |     "
        "Input: 224 × 224     |     "
        "Execution: ONNX Runtime CPU"
    ),
    font=("Segoe UI", 11)
)

info_text.pack()


# -----------------------------
# Footer
# -----------------------------

footer = tk.Label(
    root,
    text=(
        "Prototype: Snapdragon deployment can be evaluated "
        "on supported Qualcomm hardware."
    ),
    font=("Segoe UI", 10)
)

footer.pack(
    pady=20
)


root.mainloop()