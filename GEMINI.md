# Project Overview

**Project Name:** sartoquarium-hmi

This project is a Python-based Human-Machine Interface (HMI) built using **Streamlit**. It is designed to visualize real-time data received from an external device (likely an Arduino) via a serial connection (COM port).

The application reads a continuous stream of temperature and power metrics, parses the data, and displays it using interactive charts and metrics on a web interface.

## Key Features
- **Serial Communication:** Connects to a configurable COM port and Baud rate.
- **Real-time Visualization:** Dynamic line charts with dual Y-axes for temperature and power.
- **Demo Mode:** Allows testing the UI with simulated data without hardware.
- **Historical View:** Configurable time window for data display.
- **Data Parsing:** Robustly extracts values using Regular Expressions.
- **Metrics Monitored:**
    - `Soll` (Target Temperature)
    - `Ist` (Current Temperature)
    - `T_sicher` (Safety Temperature)
    - `Leistung` (Power Output %)

# Building and Running

## Prerequisites
Ensure you have Python installed. You will need to install the following dependencies:

```bash
pip install streamlit pyserial pandas altair
```

## Running the Application
To start the web interface, run the following command in the terminal:

```bash
streamlit run data-vis.py
```

This will launch a local web server (usually at `http://localhost:8501`) where you can view the dashboard.

## Configuration
On the sidebar of the running application, you can configure:
- **Demo-Modus:** Toggle between live serial data and simulated manual inputs.
- **COM-Port:** The serial port where the device is connected.
- **Baudrate:** The communication speed (default: `9600`).
- **Zeitraum (Minuten):** Adjust the time window displayed in the chart.

# Development Conventions

## Code Structure
- **`data-vis.py`:** The main entry point and logic for the application. It handles both the UI rendering and the serial data processing loop.

## Data Protocol
The application expects line-delimited serial data in a specific format:
`Soll: <float> C, Ist: <float> C, T_sicher: <float> C, Leistung: <float> %`

Example:
`Soll: 37.5 C, Ist: 37.2 C, T_sicher: 40.0 C, Leistung: 85.5 %`

Regex is used for validation: `r"Soll: (\d+\.\d+) C, Ist: (\d+\.\d+) C, T_sicher: (\d+\.\d+) C, Leistung: (\d+\.\d+) %"`
