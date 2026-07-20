# -*- coding: utf-8 -*-
"""
Created on Fri Mar 13 12:30:10 2026

@author: Malichi Flemming II
"""

import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ---------------------------------------------------------
# Helpers
# ---------------------------------------------------------

def list_cells():
    return [
        d for d in os.listdir(BASE_DIR)
        if d.startswith("cell") and os.path.isdir(os.path.join(BASE_DIR, d))
    ]

def list_cycles(cell):
    """Return sorted cycle numbers based on charge/discharge filenames."""
    charge_dir = os.path.join(BASE_DIR, cell, "charge")
    discharge_dir = os.path.join(BASE_DIR, cell, "discharge")

    charge_files = sorted(f for f in os.listdir(charge_dir) if f.endswith(".lvm"))
    discharge_files = sorted(f for f in os.listdir(discharge_dir) if f.endswith(".lvm"))

    # Extract segment number (the LAST number)
    def seg_num(fname):
        return int(fname.split("_")[-1].split(".")[0])

    charge_nums = {seg_num(f) for f in charge_files}
    discharge_nums = {seg_num(f) for f in discharge_files}

    # Only cycles that exist in BOTH folders
    return sorted(charge_nums & discharge_nums)


def load_cycle(cell, cycle_num):
    """Load matching charge and discharge files for a given cycle number."""
    charge_dir = os.path.join(BASE_DIR, cell, "charge")
    discharge_dir = os.path.join(BASE_DIR, cell, "discharge")

    # Find the correct filenames dynamically
    charge_file = next(
        f for f in os.listdir(charge_dir)
        if f.endswith(".lvm") and f.split("_")[-1].split(".")[0] == str(cycle_num)
    )
    discharge_file = next(
        f for f in os.listdir(discharge_dir)
        if f.endswith(".lvm") and f.split("_")[-1].split(".")[0] == str(cycle_num)
    )

    df_charge = pd.read_csv(os.path.join(charge_dir, charge_file),
                            delimiter="\t", header=None)
    df_discharge = pd.read_csv(os.path.join(discharge_dir, discharge_file),
                               delimiter="\t", header=None)

    return df_charge, df_discharge

# Mapping of column numbers to names
COLUMN_MAP = {
    1: "Current (A)",
    2: "Voltage (V)",
    3: "Temperature (°C)",
    4: "Strain (ε)"
}

# ---------------------------------------------------------
# MAIN INTERACTIVE LOGIC
# ---------------------------------------------------------

# 1. Choose cell
cells = list_cells()
print(f"\nNumber of cells: {len(cells)}")
for i, c in enumerate(cells):
    print(f"{i}: {c}")

cell_idx = int(input("\nSelect a cell number: "))
cell = cells[cell_idx]

# 2. Choose cycle
cycle_nums = list_cycles(cell)
print(f"\n{cell} contains {len(cycle_nums)} cycles")

for i, cyc in enumerate(cycle_nums):
    print(f"{i}: cycle {cyc}")

cycle_num = int(input("\nEnter cycle number to plot: "))

if cycle_num not in cycle_nums:
    print(f"Cycle {cycle_num} does not exist.")
    exit()

df_charge, df_discharge = load_cycle(cell, cycle_num)

# 3. Choose columns to plot
print("\nAvailable Y-axis options:")
for col, name in COLUMN_MAP.items():
    print(f"{col}: {name}")

cols = input("\nEnter column numbers to plot (comma-separated): ")
cols = [int(c.strip()) for c in cols.split(",")]

# ---------------------------------------------------------
# PLOTTING
# ---------------------------------------------------------

fig, ax = plt.subplots(figsize=(12, 6), constrained_layout=False)
fig.subplots_adjust(left=0.06, right=0.84, top=0.74)

# Assign a unique color to each selected column
colors = cm.tab10.colors
color_map = {col: colors[i % len(colors)] for i, col in enumerate(cols)}

axes = [ax]
lines = []

first = True
for col in cols:
    if first:
        ln, = ax.plot(df_charge[0], df_charge[col],
                      color=color_map[col],
                      label=f"Charge {COLUMN_MAP[col]}")
        ln2, = ax.plot(df_discharge[0], df_discharge[col],
                       color=color_map[col], linestyle="--",
                       label=f"Discharge {COLUMN_MAP[col]}")
        ax.set_ylabel(COLUMN_MAP[col])
        lines.extend([ln, ln2])
        first = False
    else:
        twin = ax.twinx()
        offset = 60 * (len(axes) - 1)
        twin.spines.right.set_position(("outward", offset))

        ln, = twin.plot(df_charge[0], df_charge[col],
                        color=color_map[col],
                        label=f"Charge {COLUMN_MAP[col]}")
        ln2, = twin.plot(df_discharge[0], df_discharge[col],
                         color=color_map[col], linestyle="--",
                         label=f"Discharge {COLUMN_MAP[col]}")
        twin.set_ylabel(COLUMN_MAP[col], color=color_map[col])
        axes.append(twin)
        lines.extend([ln, ln2])

ax.set_xlabel("Time (s)")
ax.grid(True)

labels = [l.get_label() for l in lines]

# Title ABOVE legend
fig.suptitle(f"{cell} — Cycle {cycle_num}", y=0.89, fontsize=14)

# Legend BELOW the title, ABOVE the plot
fig.legend(
    lines,
    labels,
    loc="upper center",
    bbox_to_anchor=(0.5, 0.86),   # move legend down a bit
    ncol=3,
    frameon=False
)

# plt.tight_layout(pad=1)
plt.show()

# ---------------------------------------------------------
# SAVE?
# ---------------------------------------------------------

save = input("\nSave figure? (y/n): ").lower()
if save == "y":
    chosen = "_".join([COLUMN_MAP[c].split()[0] for c in cols])
    fig_dir = os.path.join(BASE_DIR, cell, "figures")
    os.makedirs(fig_dir, exist_ok=True)
    out_path = os.path.join(fig_dir, f"cycle_{cycle_num}_{chosen}.png")
    fig.savefig(out_path, dpi=300)
    print(f"Saved to: {out_path}")
else:
    print("Figure not saved.")