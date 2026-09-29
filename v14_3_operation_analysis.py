import qai_hub as hub

BASELINE_JOB = "jpxl809jp"
COMPILED_JOB = "jgjr6617p"

print("=" * 65)
print("SNAPOPTIMIZE AI - V14.3")
print("AI Hub Operation-Level Analysis")
print("=" * 65)

client = hub.Client()

print("\nDownloading baseline profile...")
baseline = client.get_job(BASELINE_JOB).download_profile()

print("Downloading compiled profile...")
compiled = client.get_job(COMPILED_JOB).download_profile()


def get_operations(profile):
    return profile.get("execution_detail", [])


def analyze_operations(profile):
    operations = get_operations(profile)

    cpu_ops = []
    npu_ops = []

    for op in operations:

        device = str(op.get("device", "")).upper()

        if "CPU" in device:
            cpu_ops.append(op)

        elif "NPU" in device:
            npu_ops.append(op)

    return cpu_ops, npu_ops


def print_operations(title, profile):

    cpu_ops, npu_ops = analyze_operations(profile)

    print("\n" + "=" * 65)
    print(title)
    print("=" * 65)

    print(f"\nCPU operations : {len(cpu_ops)}")
    print(f"NPU operations : {len(npu_ops)}")

    print("\nCPU OPERATIONS")

    if cpu_ops:
        for op in cpu_ops:
            print(
                f"  {op.get('name', 'Unknown')} | "
                f"{op.get('type', 'Unknown')} | "
                f"{op.get('execution_time', 'N/A')} us"
            )
    else:
        print("  None detected")

    print("\nNPU OPERATIONS")

    if npu_ops:
        for op in npu_ops:
            print(
                f"  {op.get('name', 'Unknown')} | "
                f"{op.get('type', 'Unknown')} | "
                f"{op.get('execution_time', 'N/A')} us"
            )
    else:
        print("  None detected")


print_operations("BASELINE PROFILE", baseline)

print_operations("COMPILED PROFILE", compiled)


print("\n" + "=" * 65)
print("QUANTIZELINEAR SEARCH")
print("=" * 65)


def find_quantize(profile):

    operations = get_operations(profile)

    found = []

    for op in operations:

        name = str(op.get("name", ""))
        op_type = str(op.get("type", ""))

        if (
            "QuantizeLinear" in name
            or "QuantizeLinear" in op_type
        ):
            found.append(op)

    return found


baseline_quant = find_quantize(baseline)
compiled_quant = find_quantize(compiled)


print("\nBASELINE QuantizeLinear:")

for op in baseline_quant:
    print(
        f"  Device: {op.get('device', 'Unknown')}"
    )
    print(
        f"  Time  : {op.get('execution_time', 'N/A')} us"
    )


print("\nCOMPILED QuantizeLinear:")

for op in compiled_quant:
    print(
        f"  Device: {op.get('device', 'Unknown')}"
    )
    print(
        f"  Time  : {op.get('execution_time', 'N/A')} us"
    )


print("\n" + "=" * 65)
print("V14.3 COMPLETE")
print("=" * 65)