# -*- coding: utf-8 -*-
"""
Created on Sun Mar 15 18:56:43 2026

@author: malichi
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# -----------------------------------------
# Settings
# -----------------------------------------
cells = {
    "cell1": ["_1__ChargeCycle1.lvm","_1__DischargeCycle1.lvm"],
    "cell2": ["_2__ChargeCycle1.lvm","_2__DischargeCycle1.lvm"],
    "cell3": ["_3__ChargeCycle1.lvm","_3__DischargeCycle1.lvm"]
}

# Per-cell QSTART (Ah) – applies to cycle 1 charge only
QSTARTS = {
    "cell1": .15,
    "cell2": 2.4,
    "cell3": .40
}

Q = .1
script_dir = os.path.dirname(os.path.abspath(__file__))
GAP_THRESHOLD = 1000.0  # seconds

# -----------------------------------------
# Cycle detection
# -----------------------------------------
def detect_cycles(df, time_col=0, gap_threshold=GAP_THRESHOLD):
    t = df[time_col].values
    dt = np.diff(t, prepend=t[0])
    new_cycle = (dt < 0) | (dt > gap_threshold)
    cycle_idx = np.cumsum(new_cycle)
    return cycle_idx + 1

def split_by_cycle(df, time_col=0):
    df = df.copy()
    df["cycle_id"] = detect_cycles(df, time_col=time_col)
    return {int(cid): g.drop(columns=["cycle_id"]) for cid, g in df.groupby("cycle_id")}

# -----------------------------------------
# Per-cycle capacities
# -----------------------------------------
def compute_charge_capacity(df, is_first_cycle, QSTART, time_col=0, current_col=1):
    dt = df[time_col].diff().fillna(0)
    dQ = df[current_col] * dt / 3600.0
    Qc = dQ.cumsum().iloc[-1]
    return float(QSTART + Qc) if is_first_cycle else float(Q + Qc)

def compute_discharge_capacity(df, Qc, time_col=0, current_col=1):
    """
    Discharge continues from charge within the same cycle:
    capacity(t) = Qc - ∫|I_discharge| dt
    We return the final remaining capacity at end of discharge.
    """
    dt = df[time_col].diff().fillna(0)
    dQ = abs(df[current_col]) * dt / 3600.0
    cap = Qc - dQ.cumsum()
    return float(cap.iloc[-1])

# -----------------------------------------
# Main export loop
# -----------------------------------------
out_root = os.path.join(script_dir, "Capacity")
os.makedirs(out_root, exist_ok=True)

for cell, phase in cells.items():
    charge_path = os.path.join(script_dir, phase[0])
    discharge_path = os.path.join(script_dir, phase[1])

    charge_df = pd.read_csv(charge_path, delimiter="\t", header=None).dropna(subset=[0,1])
    discharge_df = pd.read_csv(discharge_path, delimiter="\t", header=None).dropna(subset=[0,1])

    charge_cycles = split_by_cycle(charge_df, time_col=0)
    discharge_cycles = split_by_cycle(discharge_df, time_col=0)

    all_cycle_ids = sorted(set(charge_cycles.keys()) | set(discharge_cycles.keys()))

    QSTART = QSTARTS[cell]
    first_charge_cycle_done = False
    results = []

    for cid in all_cycle_ids:
        is_first = not first_charge_cycle_done
        Qc = np.nan
        Qd = np.nan

        # Charge capacity for this cycle
        if cid in charge_cycles:
            Qc = compute_charge_capacity(
                charge_cycles[cid],
                is_first_cycle=is_first,
                QSTART=QSTART
            )
            first_charge_cycle_done = True

        # Discharge capacity continuing from charge for this cycle
        if cid in discharge_cycles and not np.isnan(Qc):
            Qd = compute_discharge_capacity(
                discharge_cycles[cid],
                Qc=Qc
            )

        results.append([cid, Qc, Qd])

    summary_df = pd.DataFrame(
        results,
        columns=["Cycle", "ChargeCapacity_Ah", "RemainingCapacity_after_Discharge_Ah"]
    )

    out_path = os.path.join(out_root, f"{cell}_capacity_summary.lvm")
    summary_df.to_csv(out_path, sep="\t", index=False, header=True)
    
    # -----------------------------------------
    # Plot capacity vs cycle for this cell
    # -----------------------------------------
    plt.figure(figsize=(8,5))

    plt.plot(
        summary_df["Cycle"],
        summary_df["ChargeCapacity_Ah"],
        marker="o",
        label="Charge Capacity (Ah)"
    )

    plt.plot(
        summary_df["Cycle"],
        summary_df["RemainingCapacity_after_Discharge_Ah"],
        marker="s",
        label="Remaining Capacity After Discharge (Ah)"
    )

    plt.title(f"{cell}: Capacity vs Cycle")
    plt.xlabel("Cycle Number")
    plt.ylabel("Capacity (Ah)")
    plt.grid(True, alpha=0.3)
    plt.legend()

    plot_path = os.path.join(out_root, f"{cell}_capacity_plot.png")
    plt.savefig(plot_path, dpi=300, bbox_inches="tight")
    plt.close()

print("Per-cell capacity summary files created with per-cell QSTART and discharge continuing from charge.")

