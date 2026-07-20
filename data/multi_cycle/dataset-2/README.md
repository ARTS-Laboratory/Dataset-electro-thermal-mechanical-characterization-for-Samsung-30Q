# Dataset‑2
![Status](https://img.shields.io/badge/status-in%20progress-yellow)
![Data](https://img.shields.io/badge/data-LVM%20files-blue)
![Python](https://img.shields.io/badge/python-3.10+-brightgreen)

A structured dataset of battery cycling experiments, including synchronized measurements of current, voltage, temperature, and mechanical strain. Data acquisition is ongoing, and new cycles are added as testing continues.

## 📊 Data Columns
- Time
Timestamp of each measurement, recorded in seconds.
- Current
Cell current measured in amperes (A).
- Voltage
Cell voltage measured in volts (V).
- Cell Temperature
Surface temperature of the cell in degrees Celsius (°C).
- Hoop Strain
Mechanical hoop strain on the battery casing, measured in strain (ε).

## 📁 Folder Structure
The dataset is organized by cell, and each cell directory contains two subfolders:

```text
cellX/
    charge/
        charge_<fileIndex>_<cycleNum>.lvm
    discharge/
        discharge_<fileIndex>_<cycleNum>.lvm
```      

Each .lvm file is named using a file index and a cycle number.
The cycle number is always the final number in the filename, allowing the script to automatically match charge and discharge files for the same cycle.

## 📈 Cycle_Plotter Script
What the script does
The Cycle_Plotter script loads battery test data for a selected cell and cycle, then generates a multi‑axis plot showing how current, temperature, and strain evolve during that cycle. It automatically locates the matching charge and discharge files, reads them, and plots both phases together using solid lines for charge and dashed lines for discharge. The script adds a clear title and legend above the plot and saves the final figure into a dedicated figures/ folder to keep visual outputs separate from raw data.

### ▶️ How to Use the Script
1. Run the script
You’ll be prompted to choose which battery cell to analyze.
2. Select a cycle number
The script lists all available cycles for that cell.
Enter the cycle number you want to plot.
3. Choose variables to plot
Select any combination of:
- Voltage
- Current
- Temperature
- Strain
4. View the generated plot
The script loads the matching charge and discharge data and displays a combined multi‑axis graph.
5. Save the figure (optional)
If you choose to save, the figure is written to the figures/ folder with a descriptive filename such as:
cell2_cycle_342_Current_Temperature_Strain.png



### 🧭 Usage Diagram
```text
          ┌──────────────────────┐
          │   Run the script     │
          └──────────┬───────────┘
                     │
                     ▼
        ┌────────────────────────────┐
        │ Select cell (e.g., cell2)  │
        └──────────┬─────────────────┘
                   │
                   ▼
     ┌────────────────────────────────┐
     │ Choose cycle number (e.g., 342)│
     └──────────┬─────────────────────┘  
                │
                ▼
   ┌───────────────────────────────────┐
   │ Select variables (I, T, strain)   │
   └──────────┬────────────────────────┘
              │
              ▼
     ┌──────────────────────────────┐
     │   Plot is generated & shown  │
     └──────────┬───────────────────┘
                │
                ▼
     ┌──────────────────────────────┐
     │ Save figure (optional)       │
     └──────────────────────────────┘
```

### Example Figure
![Cycle 342 Plot](./images/cycle_342_Current_Temperature_Strain.png)

