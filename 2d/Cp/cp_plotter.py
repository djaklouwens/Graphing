import pandas as pd
import matplotlib.pyplot as plt
import os


    

def read_xflr5_file(filepath):
    # Open the file and read lines
    with open(filepath, 'r') as file:
        lines = file.readlines()
    
    # Skip the first few lines to find the header (starting with "x" and column names)
    for i, line in enumerate(lines):
        if line.strip().startswith("x"):
            header_index = i
    
    # Extract column names from the header line
    columns = lines[header_index].split()
    
    # Read the data starting from the line after the header
    data = []
    for line in lines[header_index + 1:]:
        # Split each line by spaces and convert to float
        values = list(map(float, line.split()))
        data.append(values)
    
    # Create a DataFrame from the parsed data
    df = pd.DataFrame(data, columns=columns)
   
    index = 0
    for i in range(header_index+1, len(df)):
        if df["x"].iloc[i] > df["x"].iloc[i - 1]:
            index = i
            break
    
    
        
    return df

def read_experiment_file(filepath):
    # Read the file using pandas read_csv with comma as delimiter
    df = pd.read_csv(filepath)
    df_upper = df[df['Surface'] == 'Upper']
    df_lower = df[df['Surface'] == 'Lower']
    return df_upper, df_lower

def plot_cp_distribution(experiment_data_upper, experiment_data_lower, xflr5_data, output_folder, filename):
   # Create a figure and axis
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Plot the experimental data
    ax.plot(experiment_data_upper['x/c'], experiment_data_upper['Cp'], 'o-', color='black', label='Experimental Data Upper')
    ax.plot(experiment_data_lower['x/c'], experiment_data_lower['Cp'], 'o-', color='red', label='Experimental Data Lower')
    
    # Plot the XFLR5 data
    ax.plot(xflr5_data['x'], +xflr5_data['Cpv'], '^-', color='blue', label='XFLR5 Data')
    
    # Invert the y-axis
    ax.invert_yaxis()
    
    # Set axis labels
    ax.set_xlabel('x/c [-]')
    ax.set_ylabel('$C_p$ [-]')
    
    # Add grid
    ax.grid(True)
    
    # Add legend
    ax.legend()
    
    # Save the plot to the output folder
    plt.savefig(os.path.join(output_folder, f"{filename}.png"), dpi=300)
    
    # Show the plot
    plt.show()
    
    return fig

xflr5_filepath = "2d/Cp/xflr5_results/"
experiment_filepath = "2d/Cp/real_results/"
output_folder = "2d/Cp/combined_plots"

alpha = -5.0
while alpha < 18:
    xflr5_file = xflr5_filepath + str(alpha) + ".txt"
    experiment_file = experiment_filepath + str(alpha) + ".csv"
    
    try:
        xflr5_data = read_xflr5_file(xflr5_file)
        experiment_data_upper, experiment_data_lower = read_experiment_file(experiment_file)
        
        plot_cp_distribution(experiment_data_upper, experiment_data_lower, xflr5_data, output_folder,f"combined_cp_aoa={alpha}")
    
    except Exception as e:
        print(f"AoA={alpha} not found")
    
    finally:
        alpha = alpha + 0.25


