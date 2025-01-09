
from gettext import find
import pandas as pd
import matplotlib.pyplot as plt
import os
import glob

# Folder paths (change these paths as per your directory structure)
xflr5_folder = "2d\\Cp\\xflr5_results"
experiment_folder = "2d\\Cp\\real_results\\"
output_folder = "2d\\Cp\\combined_plots"

# Create output folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)


def parse_xflr5_file(file_path):
    """
    Parses an XFLR5 file with the specified format and extracts AoA and data.
    
    Parameters:
        file_path (str): Path to the XFLR5 data file.
    
    Returns:
        tuple: (alpha, dataframe), where alpha is the AoA and dataframe contains parsed data.
    """
    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    # Extract AoA from the header line (assuming it starts with 'Alpha =')
    for line in lines:
        if line.strip().startswith("Alpha ="):
            alpha = float(line.split('=')[1].split(',')[0].strip())

            break
    
    # Find the starting line of the data (after the blank line following the header)
    data_start_idx = 0
    for i, line in enumerate(lines):
        if line.strip() == "":
            data_start_idx = i + 1
            break
    
    # Read the data into a DataFrame
    column_names = ["x/c", "Cpi", "Cpv", "Qi", "Qv"]
    data = pd.read_csv(file_path, skiprows=data_start_idx, delim_whitespace=True, names=column_names)
    return alpha, data

# Function to parse experimental data
def parse_experiment_file(file_path):
    df = pd.read_csv(file_path)
    aoa = float(file_path.split('\\')[-1].replace(".csv", ""))  # Extract AoA from filename

    return aoa, df

# Load XFLR5 files
xflr5_files = glob.glob(os.path.join(xflr5_folder, "*.txt"))
xflr5_data = {parse_xflr5_file(file)[0]: parse_xflr5_file(file)[1] for file in xflr5_files}

# Load experimental files
experiment_files = glob.glob(os.path.join(experiment_folder, "*.csv"))
experiment_data = {parse_experiment_file(file)[0]: parse_experiment_file(file)[1] for file in experiment_files}

# Find common angles of attack
common_aoas = set(xflr5_data.keys()).intersection(set(experiment_data.keys()))
print(f"Common AoAs: {sorted(common_aoas)}")

# Plot data for each common AoA
for aoa in sorted(common_aoas):
    xflr5_df = xflr5_data[aoa]
    exp_df = experiment_data[aoa]
    
    # Separate upper and lower surfaces in experimental data
    exp_upper = exp_df[exp_df['Surface'] == 'Upper']
    exp_lower = exp_df[exp_df['Surface'] == 'Lower']
    
    print("x/c: ", xflr5_df["x/c"])
    print("cp: ", xflr5_df["Cpi"])
    print("x/c: ", exp_upper["x/c"])
    print("cp: ", exp_upper["Cp"])
    # Plotting
    plt.figure(figsize=(10, 6))
    plt.plot(xflr5_df["x/c"], xflr5_df["Cpi"], label="XFLR5 Cp", linestyle="--")
    plt.scatter(exp_upper["x/c"], exp_upper["Cp"], color='b', label="Experiment Cp Upper")
    plt.scatter(exp_lower["x/c"], exp_lower["Cp"], color='r', label="Experiment Cp Lower")
    
    plt.title(f"Pressure Coefficient Distribution at AoA = {aoa}")
    plt.xlabel("x/c")
    plt.ylabel("Cp")
    plt.gca().invert_yaxis()  # Invert y-axis for Cp
    plt.legend()
    plt.grid(True)
    
    # Save plot
    plt.savefig(os.path.join(output_folder, f"Cp_Distribution_AoA_{aoa}.png"))
    plt.show()
 

print(f"Plots saved in {output_folder}")
