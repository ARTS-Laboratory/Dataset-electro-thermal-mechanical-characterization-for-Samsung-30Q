# Dataset Electrothermal Deformation Characterization for Samsung 30Q Cell
### LabView Code, Test setups, & impedance data need to be added
Dataset for the Samsung 30Q battery for electro-thermal and deformation characterization

The Samsung 30Q is a high-performance lithium-ion cell widely used in various applications, including e-bikes, power tools, and other high-drain devices. Cycling refers to the process of charging and discharging the battery repeatedly.

## Key Features of the Samsung 30Q:
- **Capacity**: 3000mAh
- **Nominal Voltage**: 3.6V
- **Max Continuous Discharge Current**: 15A
- **Cycle Life**:
  - The battery is rated for around 300-500 cycles with minimal capacity loss under optimal conditions.
  - Proper care can extend its lifespan.

## Test Types 
- Hybrid Pulse Power Characterization Tests (HPPC)
  - Current pulses are applied to the battery to test its response
- Multiple Cycles Tests
  - Batteries are cycled multiple times per test
- Single Cycle Tests
  - Batteries are only cycled once per test

<!-- ## Datasets
The dataset consists of three cells, each at:
 - Room temperature for for discharge rates C/10, 1C, 2C, 3C, and 4C
 - Room temperature, 30, 40, and 50 °C for 1C discharge and High Power Pulse Characterization (In Progress)
 - The monitored data includes current, voltage, temperature, and Hoop strain with respect to time -->

## Data Visualization
- The plotting folder contains codes in both MATLAB and python that can be used to plot data
- The following figures were created in MATLAB using the Rate_Compare.m file

<p align="center">
<img src="media/S001_Voltage.png"" alt="drawing" width="400"/>
</p>
<p align="center">
The voltage per C-rate with respect to depth of discharge for cell S001
</p>

<p align="center">
<img src="media/S003_Temperature.png" alt="drawing" width="400"/>
</p>
<p align="center">
The temperature per C-rate with respect to depth of discharge for cell S003
</p>

<p align="center">
<img src="media/S002_Strain.png" alt="drawing" width="400"/>
</p>
<p align="center">
 - The strain per C-rate with respect to depth of discharge for cell S002
</p>

## Licensing and Citation

This work is licensed under a Creative Commons Attribution-ShareAlike 4.0 International License [cc-by-sa 4.0].

[![License: CC BY-SA 4.0](https://img.shields.io/badge/License-CC_BY--SA_4.0-lightgrey.svg)](https://creativecommons.org/licenses/by-sa/4.0/)


Cite this as: 

@Misc{ARTSLabDatasetElectrothermalDeformation,    
  author = {ARTS-Lab},  
  howpublished = {GitHub},  
  title  = {Dataset Electrothermal Deformation Characterization for {S}amsung 30Q Cell},    
  groups = {ARTS-Lab},    
  url    = {https://github.com/ARTS-Laboratory/dataset-electrothermal-deformation-characterization-for-samsung-30Q-cell},   
  note  = {Accessed: Month dd, yyyy},   
}

<p align="center">
<img src="media/QR-code.png" alt="drawing" width="200"/>
</p>
<p align="center">
QR code for repo.
</p>
