import pandas as pd
import matplotlib.pyplot as plt

# File paths (update these paths according to your file locations)
raw_txt_path = r'2d\Cp\raw_2D.txt'  # Updated to .txt
coordinates_excel_path = r'2d\Cp\SLT_practical_coordinates.xlsx'

# Load the raw TXT data
# Since it's space-separated and has two header rows, use delim_whitespace=True and skiprows=2
try:
    raw_data = pd.read_csv(raw_txt_path, delim_whitespace=True, skiprows=2, header=None)
except Exception as e:
    print(f"Error reading raw_2D.txt: {e}")
    exit(1)

# Inspect the first few rows to ensure correct parsing
print("First few rows of raw_data:")
print(raw_data.head())

# Load the coordinates from Excel
try:
    coordinates = pd.read_excel(coordinates_excel_path, sheet_name=0)
except Exception as e:
    print(f"Error reading SLT_practical_coordinates.xlsx: {e}")
    exit(1)

# Create a dictionary to map PXXX to x/c locations
# Assuming the first column has PXXX labels and the second column has x/c percentages
point_dict = dict(zip(coordinates.iloc[:, 0].astype(str), coordinates.iloc[:, 1]))
# Ensure that PXXX keys are strings with leading zeros (e.g., P001)
point_dict = {str(k).zfill(4): v for k, v in point_dict.items()}

# Function to plot Cp for a specific row and export CSV
def plot_cp(row_number, show = True ):
    try:
        # Adjust for zero-based indexing
        # Since we skipped first two rows and header is None, data starts at index 0
        # If row_number starts at 3, then raw_data index is row_number - 3
        row_index = row_number - 3
        if row_index < 0 or row_index >= len(raw_data):
            print(f"Row number out of range. Please enter a row number between 3 and {len(raw_data) + 2}.")
            return
        row = raw_data.iloc[row_index]
    except IndexError:
        print("Row number out of range.")
        return

    # Assuming alpha is in the 3rd column (0-based index 2)
    try:
        alpha = row.iloc[2]
    except IndexError:
        print(f"Alpha value not found in row {row_number}. Please check the data structure.")
        return

    # Assuming Delta_Pb is in the 4th column (0-based index 3)
    try:
        delta_Pb = row.iloc[3]
    except IndexError:
        print(f"Delta_Pb value not found in row {row_number}. Please check the data structure.")
        return

    # Calculate dynamic pressure
    dynamic_pressure = 0.211 + 1.9284 * delta_Pb + 1.8793e-4 * (delta_Pb)**2

    print(f"Plotting Cp for Row {row_number} with alpha = {alpha} degrees "
          f"and dynamic pressure = {dynamic_pressure:.3f} Pa.")

    # Extract P001 to P049
    # The user mentioned that points begin at the 9th column
    # Since Python uses 0-based indexing, 9th column is index 8
    try:
        p_values = row.iloc[8:8+49].values  # P001 to P049
    except IndexError:
        print(f"Pressure values not found in row {row_number}. Please check the data structure.")
        return

    # Check if we have exactly 49 points
    if len(p_values) < 49:
        print(f"Expected 49 pressure values, but found {len(p_values)} in row {row_number}.")
        # Optionally, handle missing values
        p_values = p_values.tolist() + [0]*(49 - len(p_values))  # Fill missing with 0
    elif len(p_values) > 49:
        p_values = p_values[:49]  # Truncate extra values

    # Compute Cp
    cp = p_values / dynamic_pressure  # Cp = PXXX / dynamic pressure

    # Get corresponding x/c locations
    p_labels = [f'P{str(i).zfill(3)}' for i in range(1, 50)]  # P001 to P049
    x_c = [point_dict.get(p, None) for p in p_labels]

    # Check for any missing x/c values
    if None in x_c:
        missing = [p for p, xval in zip(p_labels, x_c) if xval is None]
        print(f"Warning: Missing x/c locations for points: {missing}")
        # Remove points with missing x/c
        new_cp, new_x_c, new_labels = [], [], []
        for cval, xval, lab in zip(cp, x_c, p_labels):
            if xval is not None:
                new_cp.append(cval)
                new_x_c.append(xval)
                new_labels.append(lab)
        cp = new_cp
        x_c = new_x_c
        p_labels = new_labels

    # Normalize x/c from 0-100 to 0-1
    x_c_normalized = [xc / 100 for xc in x_c]

    # Define split index for P025 and P026
    # P025 is index 24 (0-based), P026 is index 25
    split_index = 25  # Start of P026

    # Split the data (first 25 = upper, last 24 = lower)
    x_c_first  = x_c_normalized[:split_index]  # P001 to P025
    cp_first   = cp[:split_index]
    label_first= p_labels[:split_index]

    x_c_second  = x_c_normalized[split_index:]  # P026 to P049
    cp_second   = cp[split_index:]
    label_second= p_labels[split_index:]

    # Plotting
    plt.figure(figsize=(8, 5))  # Adjusted figure size

    # Plot first segment (Upper Surface: P001-P025)
    plt.plot(x_c_first, cp_first, color='blue', label=f'Upper Surface (α={alpha}°)')
    plt.scatter(x_c_first, cp_first, color='blue')

    # Plot second segment (Lower Surface: P026-P049)
    plt.plot(x_c_second, cp_second, color='red', label=f'Lower Surface (α={alpha}°)')
    plt.scatter(x_c_second, cp_second, color='red')

    # Invert y-axis for Cp
    plt.gca().invert_yaxis()

    # Set axis labels with units
    plt.xlabel('x/c [-]')
    plt.ylabel('$C_p$ [-]')

    # Set x-axis limits
    plt.xlim(-0.05, 1.05)

    # Add grid
    plt.grid(True)

    # Add legend
    # Show the plot
    if show:
        plt.show()
    
    

    # === CSV Export Added ===
    # Build DataFrame for upper and lower surfaces
    df_upper = pd.DataFrame({
        'Point': label_first,
        'x/c': x_c_first,
        'Cp': cp_first,
        'Surface': ['Upper'] * len(x_c_first)
    })
    df_lower = pd.DataFrame({
        'Point': label_second,
        'x/c': x_c_second,
        'Cp': cp_second,
        'Surface': ['Lower'] * len(x_c_second)
    })

    # Combine and export
    df_out = pd.concat([df_upper, df_lower], ignore_index=True)
   # csv_filename = f"CP_distribution_row_{row_number}.csv"
    csv_filename = f"2d\\Cp\\real_results\\{alpha}.csv"
    df_out.to_csv(csv_filename, index=False)
    print(f"Exported CSV of (x/c, Cp) to: {csv_filename}")

# Main Execution
def main():
    print(f"Total number of data rows: {len(raw_data)} (corresponding to rows 3 to {len(raw_data) + 2})")
    while True:
        user_input = input(f"Enter the row number you want to plot (starting from row 3 to {len(raw_data) + 2}), 'all' to save everything, or 'exit' to quit: ")
        if user_input.lower() == 'exit':
            print("Exiting the program.")
            break
        if user_input.lower() == 'all':
            for row_num in range(3, len(raw_data) + 2):
                plot_cp(row_num, False)
            print(f"Plots saved for rows 3 to {len(raw_data) + 2}.")
        try:
            row_num = int(user_input)
            if row_num < 3 or row_num > len(raw_data) + 2:
                print(f"Please enter a row number between 3 and {len(raw_data) + 2}.")
                continue
            plot_cp(row_num)
        except ValueError:
            print("Invalid input. Please enter a valid row number or 'exit'.")

if __name__ == "__main__":

    main()