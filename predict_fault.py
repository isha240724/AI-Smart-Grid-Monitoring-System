import pandas as pd
import joblib

# Saved AI model load
model = joblib.load("smart_grid_model.pkl")

print("===== Smart Grid Fault Prediction =====")

voltage = float(input("Enter Voltage: "))
current = float(input("Enter Current: "))
frequency = float(input("Enter Frequency: "))
power_factor = float(input("Enter Power Factor: "))

power = voltage * current * power_factor

new_data = pd.DataFrame({
    "Voltage": [voltage],
    "Current": [current],
    "Frequency": [frequency],
    "PowerFactor": [power_factor],
    "Power": [power]
})

prediction = model.predict(new_data)

print("\n------ Calculated Readings ------")
print("Active Power:", round(power, 2), "W")
print("Predicted Fault:", prediction[0])
