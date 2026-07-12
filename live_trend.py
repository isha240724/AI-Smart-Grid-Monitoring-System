import pandas as pd
import matplotlib.pyplot as plt

# Dataset Load
data = pd.read_csv("smart_grid_dataset.csv")

# First 100 records
data = data.head(100)

plt.figure(figsize=(12,6))

plt.plot(data["Voltage"], label="Voltage (V)", linewidth=2)
plt.plot(data["Current"], label="Current (A)", linewidth=2)
plt.plot(data["Frequency"], label="Frequency (Hz)", linewidth=2)

plt.title("Smart Grid Electrical Parameters")
plt.xlabel("Sample Number")
plt.ylabel("Measured Value")
plt.grid(True)
plt.legend()

plt.tight_layout()
plt.show()
