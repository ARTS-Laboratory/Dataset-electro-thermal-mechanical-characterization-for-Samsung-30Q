# -*- coding: utf-8 -*-
"""
Created on Tue Feb  3 10:29:58 2026

@author: malichi
"""
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks

cells = {"cell1": ["_1__ChargeCycle1.lvm","_1__DischargeCycle1.lvm"], 
         "cell2": ["_2__ChargeCycle1.lvm","_2__DischargeCycle1.lvm"], 
         "cell3": ["_3__ChargeCycle1.lvm","_3__DischargeCycle1.lvm"]}
script_dir = os.path.dirname(os.path.abspath(__file__))

for cell, phase in cells.items():
    
    file_path = os.path.join(script_dir, phase[0])
    file_path = os.path.abspath(file_path) 
    file_path2 = os.path.join(script_dir, phase[1])
    file_path2 = os.path.abspath(file_path2)
    # Load data
    Data = pd.read_csv(file_path, delimiter='\t', header=None)
    # Drop rows where column 1 or column 2 is NaN
    Data = Data.dropna(subset=[1, 2])
    GlobalX = Data.iloc[:, 0] / 3600  # Time column in hours
    CurrentY = Data.iloc[:, 1]
    VoltageY = Data.iloc[:, 2]
    CTempY = Data.iloc[:, 3]
    StrainY = Data.iloc[:, 4] * -1000000 
    
    # Ensure GlobalX and CurrentY are NumPy arrays
    GlobalX = GlobalX.to_numpy()
    CurrentY = CurrentY.to_numpy()
    
    # Calculate milliamp hours
    time_differences = np.diff(GlobalX)  # Time differences in hours
    current_average = (CurrentY[:-1] + CurrentY[1:]) / 2  # Average current for trapezoidal rule,
    milliamp_hours = 1000 * np.cumsum(current_average * time_differences)
    milliamp_hours_with_zero = np.insert(milliamp_hours, 0, 0)
    # GlobalX = milliamp_hours_with_zero
    
    # Load data2
    Data2 = pd.read_csv(file_path2, delimiter='\t', header=None)
    Data2 = Data2.dropna(subset=[1, 2])
   
    # Compute the difference between consecutive rows in column 0
    diffs = Data[0].diff()
    
    # Find the first index where the jump > 100
    idx = diffs[diffs > 100].index[0]
    
    # Print the row (or a specific column)
    time_diff = Data.iloc[idx - 1, 0]
    print(time_diff)

    Data2[0] = Data2[0] + time_diff
    GlobalX2 = Data2.iloc[:, 0] / 3600  # Time column in hours
    CurrentY2 = Data2.iloc[:, 1]
    VoltageY2 = Data2.iloc[:, 2]
    CTempY2 = Data2.iloc[:, 3]
    StrainY2 = Data2.iloc[:, 4] * -1000000 
    
    df_combined = pd.concat([Data, Data2], ignore_index=True)
    df_combined = df_combined.sort_values(by=df_combined.columns[0]).reset_index(drop=True)
    with open(f"{cell}.lvm", "w") as f:
        df_combined.to_csv(f, sep="\t", index=False, header=False)

    # data3
    if cell == "cell3":
        Data3 = df_combined
        Data3 = Data3[(Data3.iloc[:, 4] * -1000000) <= 10000].reset_index(drop=True)     
        Data3[0] = Data3[0] / 3600
        GlobalX3 = Data3.iloc[:, 0]  # Time column in hours
        CurrentY3 = Data3.iloc[:, 1]
        VoltageY3 = Data3.iloc[:, 2]
        CTempY3 = Data3.iloc[:, 3]        
        StrainY3 = Data3[4].astype(float).to_numpy() * -1000000
    else:
        Data3 = df_combined
        Data3[0] = Data3[0] / 3600
        GlobalX3 = Data3.iloc[:, 0]  # Time column in hours
        CurrentY3 = Data3.iloc[:, 1]
        VoltageY3 = Data3.iloc[:, 2]
        CTempY3 = Data3.iloc[:, 3]        
        StrainY3 = Data3.iloc[:, 4] * -1000000
        
    peaks, properties  = find_peaks(StrainY3, distance=5000,prominence=0.1)
    # print(peaks)
    npeaks = []
    for peak in peaks:
        if StrainY3[peak] > 0:
            npeaks.append(peak)
    cycles = len(npeaks)
    print("Number of cycles:", cycles)

    # Plotting
    fig, ax1 = plt.subplots(figsize=(6.9, 3))  # Increase the figure width
    
    # Strain plot
    color = 'tab:blue'
    ax1.set_title(f"{cell} cycle plot")
    ax1.plot(GlobalX3, StrainY3, label='microstrain', color=color, zorder=3)
    ax1.scatter(GlobalX3[npeaks], StrainY3[npeaks], color = 'tab:red')
    ax1.set_ylabel("hoop strain (\u03bc\u03b5)", color=color)
    ax1.set_xlabel("time (hr)")
    ax1.tick_params(axis='y', labelcolor=color)
    ax1.tick_params(axis='x', labelcolor='black')
    # fig.tight_layout(pad = 0)
    ax2 = ax1.twinx()
    color = 'tab:red'
    ax2.set_ylabel("max strain (\u03bc\u03b5)", color=color)
 
