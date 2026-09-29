import qai_hub as hub

BASELINE_JOB = "jpxl809jp"
COMPILED_JOB = "jgjr6617p"

print("=" * 60)
print("SNAPOPTIMIZE AI - V14.2")
print("Qualcomm AI Hub Before vs After Comparison")
print("=" * 60)

client = hub.Client()

print("\nDownloading baseline profile...")
baseline = client.get_job(BASELINE_JOB).download_profile()

print("Downloading compiled profile...")
compiled = client.get_job(COMPILED_JOB).download_profile()


# ------------------------------------------
# Helper function
# ------------------------------------------

def get_summary(profile):
    if "execution_summary" in profile:
        return profile["execution_summary"]

    return profile


baseline_summary = get_summary(baseline)
compiled_summary = get_summary(compiled)


# ------------------------------------------
# Get headline inference time
# ------------------------------------------

baseline_time = baseline_summary["estimated_inference_time"]
compiled_time = compiled_summary["estimated_inference_time"]

latency_change = baseline_time - compiled_time
latency_percent = (latency_change / baseline_time) * 100


# ------------------------------------------
# Get memory
# ------------------------------------------

baseline_memory = baseline_summary.get(
    "estimated_inference_peak_memory", 0
)

compiled_memory = compiled_summary.get(
    "estimated_inference_peak_memory", 0
)


print("\n" + "=" * 60)
print("LATENCY COMPARISON")
print("=" * 60)

print(f"Baseline estimated inference : {baseline_time} us")
print(f"Compiled estimated inference : {compiled_time} us")
print(f"Latency change               : {latency_change} us")
print(f"Latency improvement          : {latency_percent:.2f}%")


print("\n" + "=" * 60)
print("MEMORY COMPARISON")
print("=" * 60)

if baseline_memory:
    print(
        f"Baseline peak memory : "
        f"{baseline_memory / (1024 * 1024):.2f} MiB"
    )

if compiled_memory:
    print(
        f"Compiled peak memory : "
        f"{compiled_memory / (1024 * 1024):.2f} MiB"
    )

if baseline_memory and compiled_memory:

    memory_change = compiled_memory - baseline_memory
    memory_percent = (memory_change / baseline_memory) * 100

    print(
        f"Memory change        : "
        f"{memory_change / (1024 * 1024):+.2f} MiB"
    )

    print(
        f"Memory change        : "
        f"{memory_percent:+.2f}%"
    )


# ------------------------------------------
# Inspect profile structure safely
# ------------------------------------------

print("\n" + "=" * 60)
print("PROFILE INFORMATION")
print("=" * 60)

print("Baseline profile sections:")

for key in baseline.keys():
    print(" -", key)

print("\nCompiled profile sections:")

for key in compiled.keys():
    print(" -", key)


# ------------------------------------------
# Final result
# ------------------------------------------

print("\n" + "=" * 60)
print("SNAPOPTIMIZE AI RESULT")
print("=" * 60)

if compiled_time < baseline_time:

    print("RESULT: LOWER ESTIMATED INFERENCE LATENCY")

    print(
        f"The compiled configuration reduced "
        f"estimated inference latency by "
        f"{latency_percent:.2f}%."
    )

elif compiled_time > baseline_time:

    print("RESULT: HIGHER ESTIMATED INFERENCE LATENCY")

else:

    print("RESULT: NO CHANGE IN ESTIMATED LATENCY")


print("\nNo CPU/NPU operation-level conclusion is made")
print("until the returned AI Hub profile structure is inspected.")

print("\nV14.2 COMPARISON COMPLETE!")
print("=" * 60)