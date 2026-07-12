import pandas as pd
import matplotlib.pyplot as plt

# Dataset load
data = pd.read_csv("smart_grid_dataset.csv")

# Fault count
fault_count = data["Fault"].value_counts()

print("Fault Distribution:")
print(fault_count)

# Bar graph
fault_count.plot(kind="bar")

plt.title("Smart Grid Fault Distribution")
plt.xlabel("Fault Type")
plt.ylabel("Number of Records")
plt.xticks(rotation=30)
plt.tight_layout()

plt.show()
