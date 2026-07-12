import pandas as pd
import matplotlib.pyplot as plt

# Load dataset
data = pd.read_csv("smart_grid_dataset.csv")

# Sirf pehle 100 records dikhayenge
data = data.head(100)

plt.figure(figsize=(10,5))

plt.plot(data["Voltage"], label="Voltage (V)", linewidth=2)

plt.plot(data["Current"], label="Current (A)", linewidth=2)

plt.title("Voltage and Current Trend")
plt.xlabel("Record Number")
plt.ylabel("Value")
plt.grid(True)
plt.legend()

plt.show()
