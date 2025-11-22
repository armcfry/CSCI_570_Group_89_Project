import os
import matplotlib.pyplot as plt

def extract_data_from_file(filepath):
    """Extracts CPU time, memory, and problem size from a result file."""
    with open(filepath, "r") as f:
        lines = [line.strip() for line in f.readlines()]

    # Lines:
    # 0: cost
    # 1: aligned string 1
    # 2: aligned string 2
    # 3: CPU time (ms)
    # 4: memory (KB)
    aligned_1 = lines[1]
    aligned_2 = lines[2]

    time_ms = float(lines[3])
    memory_kb = float(lines[4])

    # Compute original string lengths (non-gap characters)
    m = len(aligned_1.replace("_", ""))
    n = len(aligned_2.replace("_", ""))

    problem_size = m + n

    return problem_size, time_ms, memory_kb


def load_folder(folder):
    """Load all files in a folder and return sorted lists by problem size."""
    results = []

    for filename in os.listdir(folder):
        if filename.startswith("."):
            continue
        filepath = os.path.join(folder, filename)
        try:
            data = extract_data_from_file(filepath)
            results.append(data)
        except Exception as e:
            print(f"Error reading {filepath}: {e}")

    # Sort by problem size
    results.sort(key=lambda x: x[0])
    return results


def plot_results(basic, efficient):
    # Unpack
    basic_sizes = [r[0] for r in basic]
    basic_time = [r[1] for r in basic]
    basic_mem = [r[2] for r in basic]

    efficient_sizes = [r[0] for r in efficient]
    efficient_time = [r[1] for r in efficient]
    efficient_mem = [r[2] for r in efficient]

    # ---- Plot CPU Time ----
    plt.figure(figsize=(10, 6))
    plt.plot(basic_sizes, basic_time, marker="o", label="Basic")
    plt.plot(efficient_sizes, efficient_time, marker="o", label="Efficient")
    plt.xlabel("Problem Size (m + n)")
    plt.ylabel("CPU Time (ms)")
    plt.title("CPU Time vs Problem Size")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("cpu_time_plot.png")
    print("Saved cpu_time_plot.png")

    # ---- Plot Memory ----
    plt.figure(figsize=(10, 6))
    plt.plot(basic_sizes, basic_mem, marker="o", label="Basic")
    plt.plot(efficient_sizes, efficient_mem, marker="o", label="Efficient")
    plt.xlabel("Problem Size (m + n)")
    plt.ylabel("Memory (KB)")
    plt.title("Memory Usage vs Problem Size")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("memory_plot.png")
    print("Saved memory_plot.png")


if __name__ == "__main__":
    basic_results = load_folder("/Users/armcfry/repos/CSCI_570_Group_89_Project/CSCI570_Project_Minimum_Jul_14-2/Datapoints/basic_alg_output")
    efficient_results = load_folder("/Users/armcfry/repos/CSCI_570_Group_89_Project/CSCI570_Project_Minimum_Jul_14-2/Datapoints/efficient_alg_output")

    plot_results(basic_results, efficient_results)
