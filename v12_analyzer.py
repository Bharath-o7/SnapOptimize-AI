import qai_hub as hub

JOB_ID = "jpxl809jp"

print("=" * 60)
print("       SNAPOPTIMIZE AI - V12")
print("       SNAPDRAGON EXECUTION ANALYZER")
print("=" * 60)

client = hub.Client()

print("\nLoading Qualcomm AI Hub profile...")
job = client.get_job(JOB_ID)

profile = job.download_profile()

summary = profile["execution_summary"]
details = profile["execution_detail"]

# ---------------------------------------------------------
# Basic information
# ---------------------------------------------------------

inference_us = summary["estimated_inference_time"]
inference_ms = inference_us / 1000

peak_memory = summary["estimated_inference_peak_memory"]
peak_memory_mib = peak_memory / (1024 * 1024)

first_load_us = summary["first_load_time"]
warm_load_us = summary["warm_load_time"]

# ---------------------------------------------------------
# CPU / NPU analysis
# ---------------------------------------------------------

cpu_ops = []
npu_ops = []

for op in details:
    if op["compute_unit"] == "CPU":
        cpu_ops.append(op)

    elif op["compute_unit"] == "NPU":
        npu_ops.append(op)

cpu_time = sum(op["execution_time"] for op in cpu_ops)
npu_time = sum(op["execution_time"] for op in npu_ops)

total_profile_time = cpu_time + npu_time

if total_profile_time > 0:
    cpu_percent = cpu_time / total_profile_time * 100
    npu_percent = npu_time / total_profile_time * 100
else:
    cpu_percent = 0
    npu_percent = 0

# ---------------------------------------------------------
# Display results
# ---------------------------------------------------------

print("\n" + "=" * 60)
print("                 PROFILE RESULTS")
print("=" * 60)

print(f"Model:                 SqueezeNet ONNX")
print(f"Device:                Snapdragon X Elite CRD")
print(f"Job ID:                {JOB_ID}")

print("\nPERFORMANCE")
print("-" * 60)
print(f"Estimated inference:   {inference_us} us")
print(f"Estimated inference:   {inference_ms:.3f} ms")
print(f"Estimated throughput:   {1 / (inference_us / 1_000_000):.2f} inferences/sec")

print("\nMEMORY")
print("-" * 60)
print(f"Inference peak memory: {peak_memory_mib:.2f} MiB")
print(f"First load time:       {first_load_us / 1000:.3f} ms")
print(f"Warm load time:        {warm_load_us / 1000:.3f} ms")

print("\nEXECUTION ANALYSIS")
print("-" * 60)
print(f"CPU operations:        {len(cpu_ops)}")
print(f"NPU operations:        {len(npu_ops)}")
print(f"CPU execution time:    {cpu_time} us")
print(f"NPU execution time:    {npu_time} us")
print(f"CPU share:             {cpu_percent:.2f}%")
print(f"NPU share:             {npu_percent:.2f}%")

# ---------------------------------------------------------
# CPU operation details
# ---------------------------------------------------------

print("\nCPU OPERATIONS")
print("-" * 60)

if cpu_ops:
    for op in cpu_ops:
        print(
            f"{op['name']:<45} "
            f"{op['type']:<18} "
            f"{op['execution_time']} us"
        )
else:
    print("No CPU operations detected.")

# ---------------------------------------------------------
# Optimization suggestions
# ---------------------------------------------------------

print("\nOPTIMIZATION ANALYSIS")
print("-" * 60)

if cpu_ops:
    print("CPU operations detected inside the AI pipeline.")
    print("Potential optimization target:")
    print("  -> Reduce CPU preprocessing/postprocessing")
    print("  -> Investigate CPU/NPU data movement")
    print("  -> Increase accelerator-compatible operations")
else:
    print("No CPU operations detected in the profiled graph.")

if npu_percent > 90:
    print("NPU utilization pattern: HIGH")
elif npu_percent > 50:
    print("NPU utilization pattern: MODERATE")
else:
    print("NPU utilization pattern: LOW")

print("\n" + "=" * 60)
print("       V12 ANALYSIS COMPLETE")
print("=" * 60)