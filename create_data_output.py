import os
import subprocess
import re

# Path to your input folder
INPUT_FOLDER = "./CSCI570_Project_Minimum_Jul_14-2/Datapoints"

# Path to your bash script
SCRIPT = "./efficient.sh"


def extract_number(filename):
    """
    Extract numeric ID from filenames like:
    in1.txt, in15.txt, input23.data, etc.

    Returns None if no number found.
    """
    match = re.search(r"(\d+)", filename)
    return match.group(1) if match else None


def main():
    # Create output directory if needed
    OUTPUT_FOLDER = "outputs_efficient"
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)

    # Loop through all files in input folder
    for fname in sorted(os.listdir(INPUT_FOLDER)):
        if not fname.lower().endswith(".txt"):
            continue

        num = extract_number(fname)
        if num is None:
            print(f"Skipping {fname}: no numeric ID found.")
            continue

        # Build full paths
        input_path = os.path.join(INPUT_FOLDER, fname)
        output_filename = f"out{num}efficient.txt"
        output_path = os.path.join(OUTPUT_FOLDER, output_filename)

        # Build command
        cmd = [SCRIPT, input_path, output_path]

        print(f"Running: {' '.join(cmd)}")

        # Run the bash script
        subprocess.run(cmd, check=True)

    print("All files processed!")


if __name__ == "__main__":
    main()
