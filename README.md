# Actuator Fatigue Tester

A testing framework for UDP-based actuators that allows for automated cycling tests and real-time data visualization.

## Overview

This repository contains tools to conduct fatigue testing on actuators by cycling them through repeated movement patterns while collecting performance data. The system communicates with actuators via UDP and provides several visualization options for analyzing the results.

## Components

- **mainTester.py**: Main testing script that:
  - Establishes UDP connection with the actuator
  - Controls actuator movement (in/out cycling)
  - Collects data (angle, voltage, status, errors)
  - Saves data to CSV files for analysis

- **Data Visualization Tools**:
  - **MatplotlibGrapher.py**: Real-time data plotting using Matplotlib
  - **PlotlyGrapher.py**: Interactive dashboard using Plotly and Dash
  - **DataPlotter.R**: R-based analysis and visualization with anomaly detection

## Usage

1. Configure the test parameters in `mainTester.py`:
   ```python
   fileName = "YourTestName"
   cycle_num = 50  # Number of test cycles
   ```

2. Set up network configuration:
   ```python
   Actuator_ip = '192.168.0.36'
   Actuator_port = 5001
   Local_ip = '192.168.0.150'
   Local_port = 5000
   ```

3. Run the test:
   ```bash
   python mainTester.py
   ```

4. Visualize the data:
   - For real-time Matplotlib visualization:
     ```bash
     python MatplotlibGrapher.py
     ```
   - For interactive Dash dashboard:
     ```bash
     python PlotlyGrapher.py
     ```
   - For detailed analysis with anomaly detection (R):
     ```bash
     Rscript DataPlotter.R
     ```

## Requirements

- Python 3.x
- Required Python packages (see requirements.txt):
  - matplotlib==3.8.2
  - pandas==2.1.4
  - plotly (for interactive dashboard)
  - dash (for interactive dashboard)

- R (for advanced analysis)
  - Required R packages:
    - pacman
    - dplyr
    - ggplot2
    - plotly
    - readr
    - lubridate
    - anomalize

## Features

- Automated cycling of actuators for fatigue testing
- Real-time data collection and visualization
- Multiple visualization options (Matplotlib, Plotly/Dash, R/ggplot2)
- Anomaly detection for identifying irregular actuator behavior
- Comprehensive logging for test monitoring and debugging
