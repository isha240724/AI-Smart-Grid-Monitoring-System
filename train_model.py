import joblib
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

# Dataset Load
data = pd.read_csv("smart_grid_dataset.csv")

# Input Features
X = data[[
    "Voltage",
    "Current",
    "Frequency",
    "PowerFactor",
    "Power"
]]

# Output
y = data["Fault"]

# Split Dataset
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# AI Model
model = RandomForestClassifier()

model.fit(X_train, y_train)

accuracy = model.score(X_test, y_test)

print("Model Trained Successfully")
print("Accuracy =", round(accuracy*100,2), "%")
joblib.dump(model, "smart_grid_model.pkl")

print("Model Saved Successfully")
