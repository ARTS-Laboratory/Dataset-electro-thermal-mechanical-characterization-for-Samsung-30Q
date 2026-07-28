# Data

## Test Types
- **HPPC**:
    - Hybrid Pulse Power Characterization Test
      - Current pulses are applied to the battery to test its response
        - Current is constant 
        - C-Rate is recorded in the file name 
- **multi_cycle**:
  - Constant Current Test
    - Battery is charged and then discharged over a certain number of cycles
      - Current is constant 
      - C-rate is recorded in the file name
- **single_cycle**:
  - Constant Current Test
    - Datasets will have:
      - Discharge cycle:
        - Starts at 100% SoC and then discharges to 0% SoC
      - Charge cycle:
        - Starts at 0% SoC and then charges to 100% SoC
      - Wait cycle
        - Holds the battery in a steady state  

## Datasets
### HPPC 
- **Dataset 1**
    - HPPC tests that collected following data:
        - Time
        - Current
        - Voltage
        - Power
        - Battery Temp
        - Chamber Temp

- **Dataset 2** <!-- this is Connors paper HPPC data that was used to work with his Neural Network stage 2 code -->
    - Data for the HPPC section of the PCML paper
    - Data was used to train the second section of the Neural Network code
    - Data has been:
        - Processed
            - State of charge at each point has been added using coulomb counting equation 
        - Scrubbed
            - Any nan values have been removed

- **Dataset 3** 
  - Tests need to be run
  - Cells Tested: 30Q_1 -> 30Q_3
  - Impedance data has been added
  

### multi_cycle
- **Dataset 1**
    - Charge & discharge data from 3 independent cells.

- **Dataset 2**
    - Dataset for battery cycling experiments, including synchronized measurements of current, voltage, temperature, and mechanical strain
    - Impedance data can be found in the post-test-spectroscopy folder

- **Dataset 3**
  - Tests are being run
  - Cells Tested: 30Q_4 -> 30Q_6
  - Impedance data has been added
    <p align="center">
    <img src="media/multi_cycle_ds3_testsetup1.jpg" title="Dataset 3 Test Setup" alt="dataset-3 Test Setup" width="300"/>
    </p>
    <p align="center">
    multi_cycle dataset 3 test setup.
    </p>
    <p align="center">
    <img src="media/multi_cycle_ds3_testsetup2.jpg" title="Dataset 2 Test Setup" alt="dataset-3 Test Setup" width="300"/>
    </p>
    <p align="center">
    multi_cycle dataset 3 test board.
    </p>

- **Dataset 4**
  - Tests need to be run
  - Cells Tested: 30Q_7 -> 30Q_9
  - Impedance data has been added

- **Dataset 5**
  - Tests need to be run
  - Cells Tested: 30Q_1_2C -> 30Q_3_2C
  - Impedance data has been added

### single_cycle
- **Dataset 1**
    - Electro-thermal-deformation data
    - Data was used for the first stage of training for PCML. 
