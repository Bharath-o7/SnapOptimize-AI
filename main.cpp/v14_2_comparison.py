import qai_hub as hub

# ==========================================
# SnapOptimize AI - V14.2
# Qualcomm AI Hub Before vs After Comparison
# ==========================================

BASELINE_JOB = "jpxl809jp"
COMPILED_JOB = "jgjr6617p"

print("=" * 60)
print("SNAPOPTIMIZE AI - V14.2")
print("Qualcomm AI Hub Before vs After Comparison")
print("=" * 60)

client = hub.Client()

# ------------------------------------------
# Download profiles
# ------------------------------------------

print("\nDownloading baseline profile...")
baseline = client.get_job(BASELINE_JOB).download_profile()

print("Downloading compiled profile...")
compiled = client.get_job(COMPILED_JOB).download_profile()

# ------------------------------------------
# Extract headline metrics
# ------------------------------------------

baseline_time = baseline["execution_summary"]["estimated_inference_time"]
compiled_time = compiled["execution_summary"]["estimated_inference_time"]

baseline_memory = baseline["execution_summary"][
    "estimated_inference_peak_memory"
]

compiled_memory = compiled["execution_summary"][
    "estimated_inference_peak_memory"
]

# ------------------------------------------
# Calculate latency improvement
# ------------------------------------------

latency_change = baseline_time - compiled_time
latency_percent = (latency_change / baseline_time) * 100

memory_change = compiled_memory - baseline_memory
memory_percent = (memory_change / baseline_memory) * 100

# ------------------------------------------
# Find QuantizeLinear CPU operation
# ------------------------------------------

def find_quantize_cpu(profile):

    operations = profile["execution_summary"]["execution_detail"]

    matches = []

    for operation in operations:

        op_type = str(operation.get("type", ""))
        name = str(operation.get("name", ""))
        device = str(operation.get("device", ""))

        if "QuantizeLinear" in op_type or "QuantizeLinear" in name:

            matches.append({
                "name": name,
                "type": op_type,
                "device": device,
                "time": operation.get("execution_time", 0)
            })

    return matches


baseline_quant = find_quantize_cpu(baseline)
compiled_quant = find_quantize_cpu(compiled)

# ------------------------------------------
# Display results
# ------------------------------------------

print("\n" + "=" * 60)
print("LATENCY COMPARISON")
print("=" * 60)

print(f"Baseline estimated inference : {baseline_time} us")
print(f"Compiled estimated inference : {compiled_time} us")

print(f"\nLatency change               : {latency_change} us")
print(f"Latency improvement         : {latency_percent:.2f}%")

# ------------------------------------------

print("\n" + "=" * 60)
print("MEMORY COMPARISON")
print("=" * 60)

print(f"Baseline peak memory : {baseline_memory / (1024 * 1024):.2f} MiB")
print(f"Compiled peak memory : {compiled_memory / (1024 * 1024):.2f} MiB")

print(f"\nMemory change        : {memory_change / (1024 * 1024):+.2f} MiB")
print(f"Memory change        : {memory_percent:+.2f}%")

# ------------------------------------------

print("\n" + "=" * 60)
print("QUANTIZELINEAR COMPARISON")
print("=" * 60)

if baseline_quant:
    for op in baseline_quant:
        print("\nBASELINE")
        print(f"Operation : {op['name']}")
        print(f"Type      : {op['type']}")
        print(f"Device    : {op['device']}")
        print(f"Time      : {op['time']} us")

if compiled_quant:
    for op in compiled_quant:
        print("\nCOMPILED")
        print(f"Operation : {op['name']}")
        print(f"Type      : {op['type']}")
        print(f"Device    : {op['device']}")
        print(f"Time      : {op['time']} us")

# ------------------------------------------
# Final interpretation
# ------------------------------------------

print("\n" + "=" * 60)
print("SNAPOPTIMIZE AI RESULT")
print("=" * 60)

if compiled_time < baseline_time:

    print("RESULT: LOWER ESTIMATED INFERENCE LATENCY")

    print(
        f"The compiled configuration reduced the "
        f"estimated inference latency by {latency_percent:.2f}%."
    )

else:

    print("RESULT: NO LATENCY IMPROVEMENT")

    print(
        "The compiled configuration did not reduce "
        "the estimated inference latency."
    )

print("\nIMPORTANT:")
print("The result demonstrates a measured AI Hub profile difference.")
print("It does NOT prove that QuantizeLinear alone caused the improvement.")

print("\nV14.2 COMPARISON COMPLETE!")
print("=" * 60)