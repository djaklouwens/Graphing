#program to use mathplotlib to plot a comparison between XFLR5 numerical analysis data and data from the TU Delft low speed wind tunnel

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def load_xflr5_data(filename):
    data = np.genfromtxt(filename, skip_header=11)
    alpha = data[:, 0]  # Angle of attack
    cl = data[:, 1]     # Lift coefficient
    cd = data[:, 2]     # Drag coefficient
    cm = data[:, 4]     # Moment coefficient
    return alpha, cl, cd, cm

def load_experimental_data(csv_filename):
    """Load experimental wind tunnel data from a CSV file."""
    df = pd.read_csv(csv_filename)
    alpha = df['alpha'].values
    cl = df['CL'].values
    cd = df['CD'].values
    return alpha, cl, cd

def create_plots(xflr5_data, windtunnel_data):
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
    ax1.set_ylabel(r'$C_L$')
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
    ax2.set_ylabel(r'$C_D$')
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
xflr5_data = load_xflr5_data("NACA 63-412 AIRFOIL_T3_Re1.000_M0.82_N9.0.txt")
experimental_data = load_experimental_data("plots_data.csv")
#experimental_data = (alpha_exp, cl_exp, cd_exp)

# Generate the plots
create_plots(xflr5_data, experimental_data)