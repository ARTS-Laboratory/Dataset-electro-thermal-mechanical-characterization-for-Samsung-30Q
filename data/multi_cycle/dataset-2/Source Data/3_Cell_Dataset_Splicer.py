# -*- coding: utf-8 -*-
"""
Created on Fri Mar 13 11:43:44 2026

@author: malichi
"""

import os
import pandas as pd

cells = {
    "cell1": ["_1__ChargeCycle1.lvm","_1__DischargeCycle1.lvm"],
    "cell2": ["_2__ChargeCycle1.lvm","_2__DischargeCycle1.lvm"],
    "cell3": ["_3__ChargeCycle1.lvm","_3__DischargeCycle1.lvm"]
}

script_dir = os.path.dirname(os.path.abspath(__file__))

for i, (cell, phase) in enumerate(cells.items()):

    # Create output folders
    out_dir = os.path.join(script_dir, cell)
    charge_dir = os.path.join(out_dir, "charge")
    discharge_dir = os.path.join(out_dir, "discharge")

    os.makedirs(charge_dir, exist_ok=True)
    os.makedirs(discharge_dir, exist_ok=True)

    # Load charge
    Data = pd.read_csv(os.path.join(script_dir, phase[0]),
                       delimiter="\t", header=None).dropna(subset=[1,2])

    # Load discharge
    Data2 = pd.read_csv(os.path.join(script_dir, phase[1]),
                        delimiter="\t", header=None).dropna(subset=[1,2])

    # Find jump indices
    jump_idxs = Data[0].diff()[Data[0].diff() > 100].index.tolist()
    jump_idxs2 = Data2[0].diff()[Data2[0].diff() > 100].index.tolist()

    # Add final row so last segment closes properly
    jump_idxs.append(len(Data))
    jump_idxs2.append(len(Data2))

    # Add time offset to discharge dataset
    time_diff = Data.iloc[jump_idxs[0] - 1, 0]
    print(time_diff)
    Data2[0] = Data2[0] + time_diff
    Data[4] =  -Data[4]
    Data2[4] =  -Data2[4]
    # Start at 0
    prev = 0
    prev2 = 0

    for j, (idx, idx2) in enumerate(zip(jump_idxs, jump_idxs2)):

        # Slice between previous boundary and current boundary
        charge_slice = Data.iloc[prev:idx]
        discharge_slice = Data2.iloc[prev2:idx2]

        # Write files into separate folders
        charge_path = os.path.join(charge_dir, f"charge_{i+1}_{j+1}.lvm")
        discharge_path = os.path.join(discharge_dir, f"discharge_{i+1}_{j+1}.lvm")

        charge_slice.to_csv(charge_path, sep="\t", index=False, header=False)
        discharge_slice.to_csv(discharge_path, sep="\t", index=False, header=False)

        # Update boundaries
        prev = idx
        prev2 = idx2