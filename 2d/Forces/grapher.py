#program to use mathplotlib to plot a comparison between XFLR5 numerical analysis data and data from the TU Delft low speed wind tunnel

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def load_xflr5_data(filename):
    data = np.genfromtxt(filename, skip_header=11)
    
    # Extract columns
    alpha = data[:, 0]  # Angle of attack
    cl = data[:, 1]     # Lift coefficient
    cd = data[:, 2]     # Drag coefficient
    cm = data[:, 4]     # Moment coefficient
    
    # Filter for step size of 1 up to alpha = 9
    mask1 = (alpha <= 9) & (alpha % 1 == 0)
    
    # Filter for step size of 0.5 beyond alpha = 9
    mask2 = (alpha > 9) & (alpha % 0.5 == 0)
    
    # Combine the two masks
    mask = mask1 | mask2
    
    # Apply the combined mask to filter the data
    alpha_filtered = alpha[mask]
    cl_filtered = cl[mask]
    cd_filtered = cd[mask]
    cm_filtered = cm[mask]
    
    return alpha_filtered, cl_filtered, cd_filtered, cm_filtered

def load_experimental_data(csv_filename):
    """Load experimental wind tunnel data from a CSV file."""
    df = pd.read_csv(csv_filename)
    alpha = df['alpha'].values
    cl = df['CL'].values
    cd = df['CD'].values
    return alpha, cl, cd

def create_plots(xflr5_data, windtunnel_data):
    plt.rcParams.update({'font.size': 13})
    alpha_xflr5, cl_xflr5, cd_xflr5, _ = xflr5_data
    alpha_wt, cl_wt, cd_wt = windtunnel_data
     
    # Create Lift coefficient plot
    fig1, ax1 = plt.subplots(figsize=(8, 6))
    
    # Plot data with markers and lines
    ax1.plot(alpha_wt, cl_wt, 'o-', color='black', label='Wind Tunnel', 
             markerfacecolor='orange', markeredgecolor='black', markersize=8)
    ax1.plot(alpha_xflr5, cl_xflr5, '^-', color='black', label='Numerical Analysis',
             markerfacecolor='pink', markeredgecolor='black', markersize=8)
    
    # Customize the plot
    ax1.set_xlabel(r'$\alpha$ (deg)')
    ax1.set_ylabel(r'$C_l$')
    ax1.grid(True, linestyle='-')
 #   ax1.set_xlim(0, 20)
 #   ax1.set_ylim(0, 1.0)
    
    # Add legend
    ax1.legend()
    
    # Save the first plot
    plt.savefig('lift_coefficient.png', dpi=1000, bbox_inches='tight')
    
    # Create figure 2: Drag coefficient
    fig2, ax2 = plt.subplots(figsize=(8, 6))
    
    # Plot data with markers and lines
    ax2.plot(alpha_wt, cd_wt, 'o-', color='black', label='Wind Tunnel', 
             markerfacecolor='orange', markeredgecolor='black', markersize=8)
    ax2.plot(alpha_xflr5, cd_xflr5, '^-', color='black', label='Numerical Analysis',
             markerfacecolor='pink', markeredgecolor='black', markersize=8)
    
    # Customize the plot
    ax2.set_xlabel(r'$\alpha$ (deg)')
    ax2.set_ylabel(r'$C_d$')
    ax2.grid(True, linestyle='-')
    #ax2.set_xlim(0, 20)
    
    # Add legend
    ax2.legend()
    
    # Save the second plot
    plt.savefig('drag_coefficient.png', dpi=1000, bbox_inches='tight')
 
    plt.show()



# Experimental data
alpha_exp = np.linspace(0, 20, 20)
cl_exp = 0.095 * alpha_exp * (1 - alpha_exp/25)
cd_exp = 0.015 + 0.002 * alpha_exp

# Create the data tuples
xflr5_data = load_xflr5_data("SD6060-104-88_T1_Re0.231_M0.00_N9.0.txt")
experimental_data = load_experimental_data("plots_data.csv")
#experimental_data = (alpha_exp, cl_exp, cd_exp)

# Generate the plots
create_plots(xflr5_data, experimental_data)