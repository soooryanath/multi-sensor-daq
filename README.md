# Multi-Sensor Data Acquisition System

Simultaneous multi-channel sensor data acquisition from networked devices over WiFi with real-time tolerance checking.

## Overview

Connects to 2+ networked sensor devices (PhyPhox phones), simultaneously reads measurements from multiple sensors (accelerometer, light, temperature, etc.), checks each against tolerance limits, and logs synchronized CSV data.

This demonstrates core ATE (Automated Test Equipment) architecture: **parallel instrument communication → real-time validation → synchronized logging**.

## Features

✓ Simultaneous multi-channel sensor reading (2+ devices)  
✓ WiFi/network-based data acquisition  
✓ Real-time tolerance checking (parallel channels)  
✓ HTTP/REST API integration with PhyPhox  
✓ JSON parsing and nested data extraction  
✓ Synchronized CSV logging with precise timestamps  
✓ Error handling and retry logic (network resilience)  
✓ Timeout management (prevents hanging)  
✓ Statistical analysis: mean, std dev, min, max, pass rate  

## Installation

```bash
# Clone repository
git clone https://github.com/soooryanath/multi-sensor-daq.git
cd multi-sensor-daq

# Install requirements
pip install requests numpy

# Run script
python project2_multi_sensor_daq.py
```

## Requirements

- 2+ smartphones with PhyPhox app installed
- All devices on same WiFi network
- Remote access enabled in PhyPhox settings
- Python 3 with: requests, numpy, csv, datetime

## Usage

### Step 1: Get Device IP Addresses

On each phone running PhyPhox:
1. Start PhyPhox app
2. Settings (gear icon)
3. Network settings
4. Enable "Remote access"
5. Note the IP address displayed

Example: `10.179.132.251`

### Step 2: Update Script

Edit `project2_multi_sensor_daq.py`:

```python
DEVICES = [
    {
        "ip": "10.179.132.251",  # Your phone 1 IP
        "sensor": "accX",         # Accelerometer X
        "name": "Accelerometer X",
        "min_limit": -2,
        "max_limit": 2
    },
    {
        "ip": "10.179.132.186",  # Your phone 2 IP
        "sensor": "illum",       # Light sensor
        "name": "Light Sensor",
        "min_limit": 50,
        "max_limit": 500
    }
]
```

### Step 3: Run

```bash
python project2_multi_sensor_daq.py
```

### Step 4: Check Output

Creates: `multi_sensor_test_results.csv` with all measurements and results

## Example Output

**Console:**
```
======================================================================
MULTI-SENSOR DATA ACQUISITION SYSTEM
======================================================================

Configuration:
  Accelerometer X: 10.179.132.251 (-2-2 m/s²)
  Light Sensor: 10.179.132.186 (50-500 lux)
  Measurements: 10
  Output: multi_sensor_test_results.csv

Step 1: Verifying device connectivity...
  ✓ Accelerometer X: Connected
  ✓ Light Sensor: Connected

Step 2: Collecting measurements...
  # | Time                 | Accel (m/s²) | Accel | Light (lux) | Light
--------- | 2026-07-01 10:15:23 |       1.0200 |   PASS |      250.00 |  PASS
  1 | 2026-07-01 10:15:24 |       0.9800 |   PASS |      255.00 |  PASS
  2 | 2026-07-01 10:15:24 |       1.0500 |   PASS |      248.00 |  PASS
  ...

Step 3: Calculating statistics...

  Channel 1 - Accelerometer X:
    Measurements: 10
    Mean: 1.0050 m/s²
    Std Dev: 0.0865
    Min: 0.9200
    Max: 1.1500
    Passed: 10/10 (100.0%)

  Channel 2 - Light Sensor:
    Measurements: 10
    Mean: 252.5000 lux
    Std Dev: 3.5000
    Min: 248.0000
    Max: 258.0000
    Passed: 10/10 (100.0%)

Step 4: Saving results to CSV...
  ✓ Saved to multi_sensor_test_results.csv

======================================================================
✓ TEST COMPLETE
======================================================================
```

**CSV Output (multi_sensor_test_results.csv):**
```
Test #,Timestamp,Accel X (m/s²),Accel Status,Light (lux),Light Status
1,2026-07-01 10:15:23,1.0200,PASS,250.00,PASS
2,2026-07-01 10:15:24,0.9800,PASS,255.00,PASS
3,2026-07-01 10:15:24,1.0500,PASS,248.00,PASS
4,2026-07-01 10:15:25,1.0100,PASS,252.00,PASS
5,2026-07-01 10:15:25,0.9900,PASS,250.00,PASS
...
```

## Available PhyPhox Sensors

```
Accelerometer:  accX, accY, accZ (m/s²)
Gyroscope:      gyroX, gyroY, gyroZ (rad/s)
Magnetometer:   magX, magY, magZ (μT)
Light:          illum (lux)
Pressure:       pressure (Pa)
Temperature:    temperature (°C)
Humidity:       humidity (%)
Altitude:       altitude (m)
```

## Tolerance Configuration

Edit in script:

```python
DEVICES = [
    {
        "ip": "...",
        "sensor": "...",
        "min_limit": -2,  # Lower tolerance
        "max_limit": 2    # Upper tolerance
    }
]
```

## Key Concepts Demonstrated

- **Multi-channel acquisition:** Simultaneous reading from 2+ devices
- **Network communication:** HTTP/REST API over WiFi
- **JSON parsing:** Extract data from nested JSON responses
- **Parallel testing:** Check multiple channels simultaneously
- **Synchronized logging:** Timestamp alignment across channels
- **Error handling:** Try-except, retry logic, timeout management
- **Statistical analysis:** Mean, std dev, min, max, pass rate
- **Real-time validation:** Pass/fail decisions during acquisition

## Technologies

- Python 3
- requests (HTTP/REST API)
- JSON (data parsing)
- CSV I/O
- numpy (statistics)

## Architecture

```
┌─────────────────┐
│  Phone 1 (IP)   │ ←── Read accX ──→
│   PhyPhox       │                   ├── Check tolerance
│   Server        │                   ├── Log to CSV
└─────────────────┘                   └── Calculate stats

┌─────────────────┐
│  Phone 2 (IP)   │ ←── Read illum ──→
│   PhyPhox       │                   
│   Server        │                   
└─────────────────┘                   

Controller PC (this script)
```

## Troubleshooting

**Issue: "Connection refused"**
- Check both phones are on same WiFi
- Verify PhyPhox remote access is enabled
- Check IP addresses are correct

**Issue: "Timeout error"**
- Phone too far from WiFi router
- Network congestion
- Reduce `NUM_MEASUREMENTS` or increase `TIMEOUT`

**Issue: "JSON decode error"**
- Wrong sensor name (check available sensors list)
- PhyPhox app not responding
- Try restarting PhyPhox app

## Author

Soorya Nath Manikantan  
MSc Smart Electronic Systems, RTU Riga (2026)  
GitHub: https://github.com/soooryanath

## Portfolio Context

**Part 2 of 3-project hardware test automation portfolio:**
1. Voltage Test Logger (tolerance checking)
2. Multi-Sensor DAQ (networked instruments) ← You are here
3. Measurement Analysis Tool (statistical reporting + Cpk)
