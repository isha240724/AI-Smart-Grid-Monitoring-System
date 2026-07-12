import csv
import random

file = open("smart_grid_dataset.csv", "w", newline="")
writer = csv.writer(file)

writer.writerow([
    "Voltage",
    "Current",
    "Frequency",
    "PowerFactor",
    "Power",
    "Fault"
])

for i in range(1000):

    voltage = random.randint(150,280)
    current = random.randint(5,70)
    frequency = round(random.uniform(48,52),2)
    pf = round(random.uniform(0.70,1.00),2)

    power = round(voltage*current*pf,2)

    if voltage<100 and current>50:
        fault="Short Circuit"

    elif voltage<180:
        fault="Voltage Sag"

    elif voltage>250:
        fault="Voltage Swell"

    elif current>30:
        fault="Overload"

    elif frequency<49 or frequency>51:
        fault="Frequency Fault"

    else:
        fault="Normal"

    writer.writerow([
        voltage,
        current,
        frequency,
        pf,
        power,
        fault
    ])

file.close()

print("1000 Records Generated Successfully.")
