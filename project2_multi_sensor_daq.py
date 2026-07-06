#!/usr/bin/env python3
"""
Multi-Sensor Data Acquisition System - Project 2

Simultaneous multi-channel sensor data acquisition from networked devices
over WiFi with real-time tolerance checking and error handling.

This demonstrates core ATE (Automated Test Equipment) architecture:
- Parallel instrument communication (2+ devices simultaneously)
- Real-time tolerance checking on multiple channels
- Synchronized CSV logging with timestamps
- Network error handling and retry logic

Author: Soorya Nath Manikantan
MSc Smart Electronic Systems, RTU Riga (2026)
"""

import requests
import csv
import datetime
import time
import numpy as np

# ============================================================================
# CONFIGURATION
# ============================================================================

# Sensor devices (IPs and sensor names)
DEVICES = [
    {
        "ip": "10.179.132.251",
        "sensor": "accX",
        "name": "Accelerometer X",
        "unit": "m/s²",
        "min_limit": -2,
        "max_limit": 2
    },
    {
        "ip": "10.179.132.186",
        "sensor": "illum",
        "name": "Light Sensor",
        "unit": "lux",
        "min_limit": 50,
        "max_limit": 500
    }
]

# Test parameters
NUM_MEASUREMENTS = 10
TIMEOUT = 2  # seconds
RETRY_COUNT = 3
OUTPUT_CSV = "multi_sensor_test_results.csv"

# ============================================================================
# FUNCTIONS
# ============================================================================

def read_sensor(ip_address, sensor_name, timeout=2, retries=3):
    """
    Read measurement from sensor device via HTTP.
    
    Args:
        ip_address: IP address of device
        sensor_name: PhyPhox sensor name (e.g., "accX", "illum")
        timeout: Request timeout in seconds
        retries: Number of retry attempts on failure
    
    Returns:
        Sensor value (float) or None if failed
    """
    for attempt in range(retries):
        try:
            url = f"http://{ip_address}:8080/get?{sensor_name}"
            response = requests.get(url, timeout=timeout)
            value = response.json()["buffer"][sensor_name]["buffer"][-1]
            return value
        except Exception as e:
            if attempt < retries - 1:
                time.sleep(0.5)  # Wait before retry
            else:
                print(f"  ✗ Failed to read {sensor_name} from {ip_address}: {e}")
                return None


def check_tolerance(value, min_limit, max_limit):
    """
    Check if value is within specification limits.
    
    Args:
        value: Measured value
        min_limit: Lower tolerance limit
        max_limit: Upper tolerance limit
    
    Returns:
        "PASS" or "FAIL"
    """
    if value is None:
        return "ERROR"
    if min_limit <= value <= max_limit:
        return "PASS"
    else:
        return "FAIL"


# ============================================================================
# MAIN
# ============================================================================

def main():
    """Main test workflow"""
    
    print("\n" + "="*70)
    print("MULTI-SENSOR DATA ACQUISITION SYSTEM")
    print("="*70 + "\n")
    
    print("Configuration:")
    for device in DEVICES:
        print(f"  {device['name']}: {device['ip']} ({device['min_limit']}-{device['max_limit']} {device['unit']})")
    print(f"  Measurements: {NUM_MEASUREMENTS}")
    print(f"  Output: {OUTPUT_CSV}\n")
    
    # Step 1: Verify device connectivity
    print("Step 1: Verifying device connectivity...")
    for device in DEVICES:
        value = read_sensor(device['ip'], device['sensor'], timeout=TIMEOUT, retries=1)
        if value is not None:
            print(f"  ✓ {device['name']}: Connected")
        else:
            print(f"  ✗ {device['name']}: Not reachable")
    
    print()
    
    # Step 2: Collect measurements
    print("Step 2: Collecting measurements...")
    print(f"{'#':>3} | {'Time':^19} | {'Accel (m/s²)':>12} | {'Accel':>6} | {'Light (lux)':>12} | {'Light':>6}")
    print("-" * 80)
    
    csv_rows = []
    all_accel_values = []
    all_light_values = []
    all_accel_status = []
    all_light_status = []
    
    for step in range(1, NUM_MEASUREMENTS + 1):
        # Read both sensors
        accel_value = read_sensor(
            DEVICES[0]['ip'],
            DEVICES[0]['sensor'],
            timeout=TIMEOUT,
            retries=RETRY_COUNT
        )
        light_value = read_sensor(
            DEVICES[1]['ip'],
            DEVICES[1]['sensor'],
            timeout=TIMEOUT,
            retries=RETRY_COUNT
        )
        
        # Check tolerance
        accel_status = check_tolerance(accel_value, DEVICES[0]['min_limit'], DEVICES[0]['max_limit'])
        light_status = check_tolerance(light_value, DEVICES[1]['min_limit'], DEVICES[1]['max_limit'])
        
        # Get timestamp
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Store values
        if accel_value is not None:
            all_accel_values.append(accel_value)
            all_accel_status.append(accel_status)
        if light_value is not None:
            all_light_values.append(light_value)
            all_light_status.append(light_status)
        
        # Create CSV row
        accel_str = f"{accel_value:.4f}" if accel_value else "ERROR"
        light_str = f"{light_value:.4f}" if light_value else "ERROR"
        row = [step, timestamp, accel_str, accel_status, light_str, light_status]
        csv_rows.append(row)
        
        # Print result
        print(f"{step:>3} | {timestamp} | {accel_str:>12} | {accel_status:>6} | {light_str:>12} | {light_status:>6}")
        
        time.sleep(0.2)  # Small delay between measurements
    
    print()
    
    # Step 3: Calculate statistics
    print("Step 3: Calculating statistics...")
    
    # Accelerometer stats
    if all_accel_values:
        accel_mean = np.mean(all_accel_values)
        accel_std = np.std(all_accel_values)
        accel_min = min(all_accel_values)
        accel_max = max(all_accel_values)
        accel_pass = all_accel_status.count("PASS")
    else:
        accel_mean = accel_std = accel_min = accel_max = accel_pass = 0
    
    # Light sensor stats
    if all_light_values:
        light_mean = np.mean(all_light_values)
        light_std = np.std(all_light_values)
        light_min = min(all_light_values)
        light_max = max(all_light_values)
        light_pass = all_light_status.count("PASS")
    else:
        light_mean = light_std = light_min = light_max = light_pass = 0
    
    print(f"\n  Channel 1 - Accelerometer X:")
    print(f"    Measurements: {len(all_accel_values)}")
    print(f"    Mean: {accel_mean:.4f} m/s²")
    print(f"    Std Dev: {accel_std:.4f}")
    print(f"    Min: {accel_min:.4f}")
    print(f"    Max: {accel_max:.4f}")
    print(f"    Passed: {accel_pass}/{len(all_accel_values)} ({(accel_pass/len(all_accel_values)*100):.1f}%)")
    
    print(f"\n  Channel 2 - Light Sensor:")
    print(f"    Measurements: {len(all_light_values)}")
    print(f"    Mean: {light_mean:.4f} lux")
    print(f"    Std Dev: {light_std:.4f}")
    print(f"    Min: {light_min:.4f}")
    print(f"    Max: {light_max:.4f}")
    print(f"    Passed: {light_pass}/{len(all_light_values)} ({(light_pass/len(all_light_values)*100):.1f}%)")
    
    print()
    
    # Step 4: Save to CSV
    print("Step 4: Saving results to CSV...")
    try:
        with open(OUTPUT_CSV, 'w', newline='') as f:
            writer = csv.writer(f)
            # Write header
            writer.writerow(["Test #", "Timestamp", "Accel X (m/s²)", "Accel Status", "Light (lux)", "Light Status"])
            # Write data rows
            writer.writerows(csv_rows)
        print(f"  ✓ Saved to {OUTPUT_CSV}\n")
    except Exception as e:
        print(f"  ✗ Error saving file: {e}\n")
        return False
    
    # Summary
    print("="*70)
    print("✓ TEST COMPLETE")
    print("="*70 + "\n")
    
    return True


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
