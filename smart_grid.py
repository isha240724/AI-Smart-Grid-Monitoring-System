import csv
import os

print("========== AI-Based Smart Grid Fault Detection System ==========")

voltage = float(input("Enter Voltage (V): "))
current = float(input("Enter Current (A): "))
frequency = float(input("Enter Frequency (Hz): "))
power_factor = float(input("Enter Power Factor (0 to 1): "))

power = voltage * current * power_factor

# Fault Detection
if voltage < 100 and current > 50:
    fault = "Short Circuit"

elif voltage < 180:
    fault = "Voltage Sag"

elif voltage > 250:
    fault = "Voltage Swell"

elif current > 30:
    fault = "Overload"

elif frequency < 49 or frequency > 51:
    fault = "Frequency Fault"

else:
    fault = "Normal"

print("\n------ System Readings ------")
print("Voltage      :", voltage, "V")
print("Current      :", current, "A")
print("Frequency    :", frequency, "Hz")
print("Power Factor :", power_factor)
print("Power        :", round(power,2), "W")
print("Fault Status :", fault)

# Save to CSV
filename = "fault_history.csv"

file_exists = os.path.isfile(filename)

with open(filename, "a", newline="") as file:
    writer = csv.writer(file)

    if not file_exists:
        writer.writerow([
            "Voltage",
            "Current",
            "Frequency",
            "Power Factor",
            "Power",
            "Fault"
        ])

    writer.writerow([
        voltage,
        current,
        frequency,
        power_factor,
        round(power,2),
        fault
    ])

print("\nData Saved Successfully!")
