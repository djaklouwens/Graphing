import pandas as pd
import matplotlib.pyplot as plt
import math

# Define the file path
file_path = '3D\\xflr5_data\\3d Wing analyses_T1-22_6 m_s-VLM1.txt'

# Read the file and extract relevant lines
with open(file_path, 'r') as file:
    lines = file.readlines()

# Find the header line and data lines
data_start_index = next(i for i, line in enumerate(lines) if "alpha" in line)
header_line = lines[data_start_index].split()
data_lines = lines[data_start_index + 1:]

# Extract the alpha column data
data = []
for line in data_lines:
    if line.strip():  # Ignore empty lines
        try:
            values = line.split()
            # Extract alpha, CL, CDi (columns 0, 2, and 3 respectively)
            alpha = float(values[0])
            cl = float(values[2])
            cdi = float(values[3])
            data.append([alpha, cl, cdi])
        except (IndexError, ValueError):
            pass  # Skip lines that don't have numeric data

# Create a DataFrame for the extracted values
df = pd.DataFrame(data, columns=["alpha", "CL", "CDi"])

# Display the table
print(df)

#CDi calculated
AR = 800**2 / (800*160)
e = 1
CDi_calc = df["CL"]**2 / (math.pi * AR * e)

# Plot alpha vs CL
plt.figure(figsize=(8, 6))
plt.plot(df["alpha"], CDi_calc, marker='o', linestyle='-', color='b', label='CD_calc vs alpha')
plt.plot(df["alpha"], df["CDi"], marker='^', linestyle='-', color='r', label='CDi vs alpha')
plt.title("Alpha vs CDi", fontsize=14)
plt.xlabel("Alpha (degrees)", fontsize=12)
plt.ylabel("CL (Lift Coefficient)", fontsize=12)
plt.grid(True, linestyle='--', alpha=0.7)
plt.legend(fontsize=10)
plt.show()

'''
# Save the table to a CSV (optional)
output_path = 'alpha_cl_cdi_values.csv'
df.to_csv(output_path, index=False)
print(f"Data saved to {output_path}")
'''

