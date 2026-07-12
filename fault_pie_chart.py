import pandas as pd
import matplotlib.pyplot as plt

# Load Dataset
data = pd.read_csv("smart_grid_dataset.csv")

# Count faults
fault_count = data["Fault"].value_counts()

plt.figure(figsize=(8,8))

plt.pie(
    fault_count,
    labels=fault_count.index,
    autopct="%1.1f%%",
    startangle=90
)

plt.title("Smart Grid Fault Percentage")

plt.axis("equal")

plt.show()
