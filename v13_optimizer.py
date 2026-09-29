import qai_hub as hub

JOB_ID = "jpxl809jp"

print("=" * 65)
print("        SNAPOPTIMIZE AI - V13")
print("        AUTOMATIC OPTIMIZATION ENGINE")
print("=" * 65)

client = hub.Client()

print("\nLoading Snapdragon profile...")
job = client.get_job(JOB_ID)
profile = job.download_profile()

summary = profile["execution_summary"]
details = profile["execution_detail"]

# ---------------------------------------------------------
# Basic measurements
# ---------------------------------------------------------

inference_us = summary["estimated_inference_time"]
peak_memory = summary["estimated_inference_peak_memory"]

cpu_ops = [
    op for op in details
    if op["compute_unit"] == "CPU"
]

npu_ops = [
    op for op in details
    if op["compute_unit"] == "NPU"
]

cpu_time = sum(op["execution_time"] for op in cpu_ops)
npu_time = sum(op["execution_time"] for op in npu_ops)

# ---------------------------------------------------------
# Find largest CPU operation
# ---------------------------------------------------------

largest_cpu_op = None

if cpu_ops:
    largest_cpu_op = max(
        cpu_ops,
        key=lambda op: op["execution_time"]
    )

# ---------------------------------------------------------
# Automatic recommendation
# ---------------------------------------------------------

recommendations = []

if largest_cpu_op:
    op_name = largest_cpu_op["name"]
    op_type = largest_cpu_op["type"]
    op_time = largest_cpu_op["execution_time"]

    recommendations.append(
        f"Investigate {op_type} '{op_name}' because it executes on CPU."
    )

    recommendations.append(
        "Reduce CPU preprocessing and CPU-to-NPU data movement where possible."
    )

    recommendations.append(
        "Investigate whether the operation can be represented using "
        "an accelerator-compatible configuration."
    )

if len(npu_ops) > len(cpu_ops):
    recommendations.append(
        "The majority of graph operations are already mapped to the NPU."
    )

if inference_us < 1000:
    performance_level = "LOW-LATENCY AI WORKLOAD"
elif inference_us < 5000:
    performance_level = "MODERATE-LATENCY AI WORKLOAD"
else:
    performance_level = "HIGH-LATENCY AI WORKLOAD"

# ---------------------------------------------------------
# Display report
# ---------------------------------------------------------

print("\n" + "=" * 65)
print("                    ANALYSIS")
print("=" * 65)

print(f"Model:                 SqueezeNet ONNX")
print(f"Target:                Snapdragon X Elite CRD")

print("\nPERFORMANCE")
print("-" * 65)
print(f"Inference time:        {inference_us} us")
print(f"Inference time:        {inference_us / 1000:.3f} ms")
print(f"Performance class:     {performance_level}")

print("\nEXECUTION")
print("-" * 65)
print(f"CPU operations:        {len(cpu_ops)}")
print(f"NPU operations:        {len(npu_ops)}")
print(f"CPU operation time:    {cpu_time} us")
print(f"NPU operation time:    {npu_time} us")

print("\nMEMORY")
print("-" * 65)
print(f"Peak inference memory: {peak_memory / (1024 * 1024):.2f} MiB")

# ---------------------------------------------------------
# Bottleneck
# ---------------------------------------------------------

print("\nDETECTED OPTIMIZATION TARGET")
print("-" * 65)

if largest_cpu_op:

    print(f"Operation:             {largest_cpu_op['name']}")
    print(f"Type:                  {largest_cpu_op['type']}")
    print(f"Compute unit:          {largest_cpu_op['compute_unit']}")
    print(f"Execution time:        {largest_cpu_op['execution_time']} us")

else:

    print("No CPU operation detected.")

# ---------------------------------------------------------
# Recommendations
# ---------------------------------------------------------

print("\nAUTOMATIC RECOMMENDATIONS")
print("-" * 65)

for number, recommendation in enumerate(recommendations, 1):
    print(f"{number}. {recommendation}")

# ---------------------------------------------------------
# Final decision
# ---------------------------------------------------------

print("\n" + "=" * 65)
print("                 SNAPOPTIMIZE DECISION")
print("=" * 65)

if largest_cpu_op:
    print("STATUS: OPTIMIZATION OPPORTUNITY DETECTED")
    print()
    print(
        "Primary target:",
        largest_cpu_op["type"],
        "running on",
        largest_cpu_op["compute_unit"]
    )
else:
    print("STATUS: NO CPU BOTTLENECK DETECTED")

print("=" * 65)
print("             V13 ANALYSIS COMPLETE")
print("=" * 65)