import onnxruntime as ort
import numpy as np
import time
import os
import statistics
import webbrowser


print("====================================")
print("       SNAPOPTIMIZE AI - V8")
print("       FINAL DASHBOARD")
print("====================================")


# -------------------------------------------------
# 1. Model
# -------------------------------------------------

model_path = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "..",
        "squeezenet.onnx"
    )
)

if not os.path.exists(model_path):
    print("ERROR: Model file not found!")
    exit()

print("\nModel: SqueezeNet")


# -------------------------------------------------
# 2. Same input for both tests
# -------------------------------------------------

np.random.seed(42)

input_data = np.random.rand(
    1, 3, 224, 224
).astype(np.float32)


# -------------------------------------------------
# 3. Benchmark function
# -------------------------------------------------

def benchmark(session, input_name, runs=20):

    session.run(
        None,
        {input_name: input_data}
    )

    times = []

    for _ in range(runs):

        start = time.perf_counter()

        session.run(
            None,
            {input_name: input_data}
        )

        end = time.perf_counter()

        times.append(
            (end - start) * 1000
        )

    average = statistics.mean(times)

    return {
        "average": average,
        "fastest": min(times),
        "slowest": max(times),
        "throughput": 1000 / average
    }


# -------------------------------------------------
# 4. Baseline
# -------------------------------------------------

baseline_options = ort.SessionOptions()

baseline_options.graph_optimization_level = (
    ort.GraphOptimizationLevel.ORT_DISABLE_ALL
)

baseline_session = ort.InferenceSession(
    model_path,
    sess_options=baseline_options,
    providers=["CPUExecutionProvider"]
)

baseline_input = baseline_session.get_inputs()[0].name

print("\nRunning baseline...")

baseline = benchmark(
    baseline_session,
    baseline_input
)


# -------------------------------------------------
# 5. Optimized
# -------------------------------------------------

optimized_options = ort.SessionOptions()

optimized_options.graph_optimization_level = (
    ort.GraphOptimizationLevel.ORT_ENABLE_ALL
)

optimized_session = ort.InferenceSession(
    model_path,
    sess_options=optimized_options,
    providers=["CPUExecutionProvider"]
)

optimized_input = optimized_session.get_inputs()[0].name

print("Running optimized configuration...")

optimized = benchmark(
    optimized_session,
    optimized_input
)


# -------------------------------------------------
# 6. Calculate improvement
# -------------------------------------------------

latency_improvement = (
    (baseline["average"] - optimized["average"])
    / baseline["average"]
) * 100

throughput_improvement = (
    (optimized["throughput"] - baseline["throughput"])
    / baseline["throughput"]
) * 100


# -------------------------------------------------
# 7. Console output
# -------------------------------------------------

print("\n====================================")
print("       FINAL RESULTS")
print("====================================")

print(
    f"Baseline latency:  {baseline['average']:.3f} ms"
)

print(
    f"Optimized latency: {optimized['average']:.3f} ms"
)

print(
    f"Latency improvement: {latency_improvement:.2f}%"
)

print(
    f"Baseline throughput:  {baseline['throughput']:.2f}/sec"
)

print(
    f"Optimized throughput: {optimized['throughput']:.2f}/sec"
)

print(
    f"Throughput improvement: {throughput_improvement:.2f}%"
)


# -------------------------------------------------
# 8. Create HTML dashboard
# -------------------------------------------------

dashboard_path = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "..",
        "snapoptimize_dashboard.html"
    )
)


html = f"""
<!DOCTYPE html>

<html>

<head>

<meta charset="UTF-8">

<title>SnapOptimize AI Dashboard</title>

<style>

body {{
    font-family: Arial, sans-serif;
    background: #f2f4f7;
    margin: 0;
    padding: 40px;
}}

.container {{
    max-width: 1000px;
    margin: auto;
}}

h1 {{
    text-align: center;
}}

.subtitle {{
    text-align: center;
    color: #555;
}}

.cards {{
    display: flex;
    gap: 20px;
    margin-top: 30px;
}}

.card {{
    background: white;
    padding: 25px;
    border-radius: 12px;
    flex: 1;
    text-align: center;
    box-shadow: 0 3px 10px rgba(0,0,0,0.1);
}}

.value {{
    font-size: 30px;
    font-weight: bold;
}}

.section {{
    background: white;
    margin-top: 25px;
    padding: 25px;
    border-radius: 12px;
}}

.bar {{
    height: 35px;
    margin: 12px 0;
    background: #ddd;
    border-radius: 8px;
    overflow: hidden;
}}

.baseline {{
    height: 100%;
    width: 100%;
    background: #777;
}}

.optimized {{
    height: 100%;
    width: {min(100, optimized["average"] / baseline["average"] * 100):.1f}%;
    background: #333;
}}

.result {{
    text-align: center;
    font-size: 28px;
    font-weight: bold;
    padding: 20px;
}}

.footer {{
    text-align: center;
    color: #777;
    margin-top: 30px;
}}

</style>

</head>


<body>

<div class="container">

<h1>⚡ SnapOptimize AI</h1>

<p class="subtitle">
AI Workload Performance Optimization Dashboard
</p>


<div class="cards">

<div class="card">

<h3>Baseline</h3>

<div class="value">
{baseline["average"]:.3f} ms
</div>

<p>
{baseline["throughput"]:.2f} inferences/sec
</p>

</div>


<div class="card">

<h3>Optimized</h3>

<div class="value">
{optimized["average"]:.3f} ms
</div>

<p>
{optimized["throughput"]:.2f} inferences/sec
</p>

</div>


<div class="card">

<h3>Latency Reduction</h3>

<div class="value">
{latency_improvement:.2f}%
</div>

</div>

</div>


<div class="section">

<h2>Latency Comparison</h2>

<p>
Baseline: {baseline["average"]:.3f} ms
</p>

<div class="bar">
<div class="baseline"></div>
</div>


<p>
Optimized: {optimized["average"]:.3f} ms
</p>

<div class="bar">
<div class="optimized"></div>
</div>

</div>


<div class="section">

<h2>Performance Improvement</h2>

<div class="result">

↓ {latency_improvement:.2f}% Latency

<br><br>

↑ {throughput_improvement:.2f}% Throughput

</div>

</div>


<div class="section">

<h2>AI Workload</h2>

<p><b>Model:</b> SqueezeNet</p>

<p><b>Task:</b> Image Classification</p>

<p><b>Input:</b> 224 × 224</p>

<p><b>Execution:</b> ONNX Runtime CPU</p>

</div>


<div class="section">

<h2>Optimization Recommendation</h2>

<p>
The measured optimized configuration reduced inference latency
on the development system.
</p>

<p>
For Snapdragon deployment, the same workload can be evaluated
using supported Qualcomm hardware and execution providers.
</p>

</div>


<div class="footer">

SnapOptimize AI — Development Prototype

</div>

</div>

</body>

</html>
"""


# -------------------------------------------------
# 9. Save dashboard
# -------------------------------------------------

with open(
    dashboard_path,
    "w",
    encoding="utf-8"
) as file:

    file.write(html)


print("\n====================================")
print("       DASHBOARD CREATED")
print("====================================")

print("File:")
print(dashboard_path)


# -------------------------------------------------
# 10. Open dashboard
# -------------------------------------------------

webbrowser.open(
    "file://" + dashboard_path
)

print("\nV8 DASHBOARD COMPLETE!")
