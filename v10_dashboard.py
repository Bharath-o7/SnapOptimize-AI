import tkinter as tk
from tkinter import messagebox
import subprocess
import threading
import re
import psutil
import os
import sys


class SnapOptimizeDashboard:

    def __init__(self, root):
        self.root = root
        self.root.title("SnapOptimize AI - Performance Dashboard")
        self.root.geometry("1100x760")
        self.root.resizable(False, False)

        self.running = False

        # ==============================
        # Variables
        # ==============================

        self.baseline = tk.StringVar(value="--")
        self.optimized = tk.StringVar(value="--")
        self.latency = tk.StringVar(value="--")
        self.throughput = tk.StringVar(value="--")

        self.cpu = tk.StringVar(value="--")
        self.ram = tk.StringVar(value="--")
        self.battery = tk.StringVar(value="--")
        self.status = tk.StringVar(value="Ready")

        # ==============================
        # Background
        # ==============================

        self.root.configure(bg="#07111f")

        # ==============================
        # Header
        # ==============================

        header = tk.Frame(
            root,
            bg="#0b1d33",
            height=100
        )
        header.pack(fill="x")

        title = tk.Label(
            header,
            text="SNAPOPTIMIZE AI",
            font=("Segoe UI", 28, "bold"),
            fg="white",
            bg="#0b1d33"
        )
        title.pack(pady=(18, 0))

        subtitle = tk.Label(
            header,
            text="Adaptive AI Workload Performance Dashboard",
            font=("Segoe UI", 12),
            fg="#9fb3c8",
            bg="#0b1d33"
        )
        subtitle.pack()

        # ==============================
        # Model information
        # ==============================

        info_frame = tk.Frame(
            root,
            bg="#07111f"
        )
        info_frame.pack(pady=18)

        info = [
            ("MODEL", "SqueezeNet"),
            ("TASK", "Image Classification"),
            ("INPUT", "224 × 224"),
            ("RUNTIME", "ONNX Runtime"),
            ("DEVICE", "CPU")
        ]

        for name, value in info:

            box = tk.Frame(
                info_frame,
                bg="#10243b",
                width=190,
                height=70
            )
            box.pack(side="left", padx=6)
            box.pack_propagate(False)

            tk.Label(
                box,
                text=name,
                font=("Segoe UI", 9, "bold"),
                fg="#7f9db8",
                bg="#10243b"
            ).pack(pady=(10, 0))

            tk.Label(
                box,
                text=value,
                font=("Segoe UI", 12, "bold"),
                fg="white",
                bg="#10243b"
            ).pack()

        # ==============================
        # AI RESULTS TITLE
        # ==============================

        tk.Label(
            root,
            text="AI PERFORMANCE RESULTS",
            font=("Segoe UI", 15, "bold"),
            fg="white",
            bg="#07111f"
        ).pack(pady=(5, 10))

        # ==============================
        # Result cards
        # ==============================

        result_frame = tk.Frame(
            root,
            bg="#07111f"
        )
        result_frame.pack()

        self.create_result_card(
            result_frame,
            "BASELINE LATENCY",
            self.baseline,
            "ms"
        )

        self.create_result_card(
            result_frame,
            "OPTIMIZED LATENCY",
            self.optimized,
            "ms"
        )

        self.create_result_card(
            result_frame,
            "LATENCY IMPROVEMENT",
            self.latency,
            "%"
        )

        self.create_result_card(
            result_frame,
            "THROUGHPUT IMPROVEMENT",
            self.throughput,
            "%"
        )

        # ==============================
        # System monitoring
        # ==============================

        tk.Label(
            root,
            text="SYSTEM MONITOR",
            font=("Segoe UI", 15, "bold"),
            fg="white",
            bg="#07111f"
        ).pack(pady=(25, 10))

        monitor_frame = tk.Frame(
            root,
            bg="#07111f"
        )
        monitor_frame.pack()

        self.create_monitor_card(
            monitor_frame,
            "CPU USAGE",
            self.cpu
        )

        self.create_monitor_card(
            monitor_frame,
            "RAM USAGE",
            self.ram
        )

        self.create_monitor_card(
            monitor_frame,
            "BATTERY",
            self.battery
        )

        # ==============================
        # Run button
        # ==============================

        self.run_button = tk.Button(
            root,
            text="▶  RUN AI ANALYSIS",
            font=("Segoe UI", 13, "bold"),
            fg="white",
            bg="#1769aa",
            activebackground="#2185d0",
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            padx=30,
            pady=12,
            command=self.start_analysis
        )

        self.run_button.pack(pady=25)

        # ==============================
        # Status
        # ==============================

        status_frame = tk.Frame(
            root,
            bg="#0b1d33",
            height=50
        )
        status_frame.pack(
            side="bottom",
            fill="x"
        )

        tk.Label(
            status_frame,
            textvariable=self.status,
            font=("Segoe UI", 11),
            fg="#9fb3c8",
            bg="#0b1d33"
        ).pack(pady=14)

    # ==========================================================
    # RESULT CARD
    # ==========================================================

    def create_result_card(
        self,
        parent,
        title,
        variable,
        unit
    ):

        card = tk.Frame(
            parent,
            bg="#10243b",
            width=245,
            height=130
        )

        card.pack(
            side="left",
            padx=7
        )

        card.pack_propagate(False)

        tk.Label(
            card,
            text=title,
            font=("Segoe UI", 9, "bold"),
            fg="#7f9db8",
            bg="#10243b"
        ).pack(pady=(15, 5))

        value_frame = tk.Frame(
            card,
            bg="#10243b"
        )

        value_frame.pack()

        tk.Label(
            value_frame,
            textvariable=variable,
            font=("Segoe UI", 25, "bold"),
            fg="white",
            bg="#10243b"
        ).pack(side="left")

        tk.Label(
            value_frame,
            text=unit,
            font=("Segoe UI", 11),
            fg="#9fb3c8",
            bg="#10243b"
        ).pack(
            side="left",
            padx=5,
            pady=(12, 0)
        )

    # ==========================================================
    # MONITOR CARD
    # ==========================================================

    def create_monitor_card(
        self,
        parent,
        title,
        variable
    ):

        card = tk.Frame(
            parent,
            bg="#10243b",
            width=300,
            height=90
        )

        card.pack(
            side="left",
            padx=10
        )

        card.pack_propagate(False)

        tk.Label(
            card,
            text=title,
            font=("Segoe UI", 9, "bold"),
            fg="#7f9db8",
            bg="#10243b"
        ).pack(pady=(12, 2))

        tk.Label(
            card,
            textvariable=variable,
            font=("Segoe UI", 20, "bold"),
            fg="white",
            bg="#10243b"
        ).pack()

    # ==========================================================
    # START ANALYSIS
    # ==========================================================

    def start_analysis(self):

        if self.running:
            return

        self.running = True

        self.run_button.config(
            state="disabled",
            text="⏳  RUNNING AI ANALYSIS..."
        )

        self.status.set(
            "Running SqueezeNet AI inference..."
        )

        # Reset old values

        self.baseline.set("--")
        self.optimized.set("--")
        self.latency.set("--")
        self.throughput.set("--")

        thread = threading.Thread(
            target=self.run_analysis,
            daemon=True
        )

        thread.start()

    # ==========================================================
    # RUN AI ANALYSIS
    # ==========================================================

    def run_analysis(self):

        try:

            # ==========================================
            # Find project directory
            # ==========================================

            project_dir = os.path.dirname(
                os.path.abspath(__file__)
            )

            # ==========================================
            # Python executable
            # ==========================================

            python_exe = os.path.join(
                project_dir,
                "venv",
                "Scripts",
                "python.exe"
            )

            # ==========================================
            # AI inference script
            # ==========================================

            ai_script = os.path.join(
                project_dir,
                "main.cpp",
                "ai_inference.py"
            )

            # ==========================================
            # Check files
            # ==========================================

            if not os.path.exists(python_exe):

                raise FileNotFoundError(
                    "Python virtual environment not found:\n\n"
                    + python_exe
                )

            if not os.path.exists(ai_script):

                raise FileNotFoundError(
                    "AI inference script not found:\n\n"
                    + ai_script
                )

            # ==========================================
            # Battery
            # ==========================================

            battery = psutil.sensors_battery()

            if battery:

                battery_text = (
                    f"{battery.percent:.1f}%"
                )

                if battery.power_plugged:
                    battery_text += " (AC)"

            else:

                battery_text = "Not available"

            self.root.after(
                0,
                lambda v=battery_text:
                self.battery.set(v)
            )

            # ==========================================
            # CPU / RAM before AI
            # ==========================================

            cpu_before = psutil.cpu_percent(
                interval=0.2
            )

            ram_before = psutil.virtual_memory().percent

            # ==========================================
            # RUN AI INFERENCE
            # ==========================================

            process = subprocess.run(

                [
                    python_exe,
                    "-u",
                    ai_script
                ],

                stdout=subprocess.PIPE,

                stderr=subprocess.STDOUT,

                text=True,

                cwd=project_dir

            )

            # ==========================================
            # Capture complete AI output
            # ==========================================

            output = process.stdout

            print()
            print("====================================")
            print("        AI OUTPUT FROM V10")
            print("====================================")
            print(output)
            print("====================================")

            # ==========================================
            # CPU / RAM after AI
            # ==========================================

            cpu_after = psutil.cpu_percent(
                interval=0.2
            )

            ram_after = psutil.virtual_memory().percent

            average_cpu = (
                cpu_before + cpu_after
            ) / 2

            average_ram = (
                ram_before + ram_after
            ) / 2

            # ==========================================
            # Extract AI results
            # ==========================================

            baseline_match = re.search(
                r"Baseline latency:\s*([0-9.]+)\s*ms",
                output,
                re.IGNORECASE
            )

            optimized_match = re.search(
                r"Optimized latency:\s*([0-9.]+)\s*ms",
                output,
                re.IGNORECASE
            )

            latency_match = re.search(
                r"Latency improvement:\s*([0-9.]+)\s*%",
                output,
                re.IGNORECASE
            )

            throughput_match = re.search(
                r"Throughput improvement:\s*([0-9.]+)\s*%",
                output,
                re.IGNORECASE
            )

            # ==========================================
            # Extract values
            # ==========================================

            baseline_value = (
                baseline_match.group(1)
                if baseline_match
                else None
            )

            optimized_value = (
                optimized_match.group(1)
                if optimized_match
                else None
            )

            latency_value = (
                latency_match.group(1)
                if latency_match
                else None
            )

            throughput_value = (
                throughput_match.group(1)
                if throughput_match
                else None
            )

            # ==========================================
            # Debug
            # ==========================================

            print("Baseline:", baseline_value)
            print("Optimized:", optimized_value)
            print(
                "Latency improvement:",
                latency_value
            )
            print(
                "Throughput improvement:",
                throughput_value
            )

            # ==========================================
            # Update dashboard
            # ==========================================

            if baseline_value:

                self.root.after(
                    0,
                    lambda v=baseline_value:
                    self.baseline.set(
                        v + " ms"
                    )
                )

            if optimized_value:

                self.root.after(
                    0,
                    lambda v=optimized_value:
                    self.optimized.set(
                        v + " ms"
                    )
                )

            if latency_value:

                self.root.after(
                    0,
                    lambda v=latency_value:
                    self.latency.set(
                        v + "%"
                    )
                )

            if throughput_value:

                self.root.after(
                    0,
                    lambda v=throughput_value:
                    self.throughput.set(
                        v + "%"
                    )
                )

            # ==========================================
            # System monitor
            # ==========================================

            self.root.after(
                0,
                lambda v=average_cpu:
                self.cpu.set(
                    f"{v:.1f}%"
                )
            )

            self.root.after(
                0,
                lambda v=average_ram:
                self.ram.set(
                    f"{v:.1f}%"
                )
            )

            # ==========================================
            # Status
            # ==========================================

            if process.returncode == 0:

                self.root.after(
                    0,
                    lambda:
                    self.status.set(
                        "✓ Analysis complete — AI performance measured"
                    )
                )

            else:

                self.root.after(
                    0,
                    lambda:
                    self.status.set(
                        "⚠ AI script returned an error"
                    )
                )

        # ==============================================
        # ERROR HANDLING
        # ==============================================

        except Exception as error:

            print()
            print("====================================")
            print("ERROR")
            print("====================================")
            print(error)
            print("====================================")

            self.root.after(
                0,
                lambda e=error:
                messagebox.showerror(
                    "SnapOptimize AI",
                    "Analysis error:\n\n"
                    + str(e)
                )
            )

            self.root.after(
                0,
                lambda:
                self.status.set(
                    "Analysis failed"
                )
            )

        # ==============================================
        # FINISH
        # ==============================================

        finally:

            self.running = False

            self.root.after(
                0,
                lambda:
                self.run_button.config(
                    state="normal",
                    text="▶  RUN AI ANALYSIS"
                )
            )


# ==========================================================
# MAIN
# ==========================================================

if __name__ == "__main__":

    root = tk.Tk()

    app = SnapOptimizeDashboard(root)

    root.mainloop()