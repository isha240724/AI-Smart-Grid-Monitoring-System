import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix


# Dataset load
data = pd.read_csv("smart_grid_dataset.csv")

# Input features
X = data[[
    "Voltage",
    "Current",
    "Frequency",
    "PowerFactor",
    "Power"
]]

# Output labels
y = data["Fault"]

# Same test split
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# Saved model load
model = joblib.load("smart_grid_model.pkl")

# Prediction
y_prediction = model.predict(X_test)

# Accuracy
accuracy = accuracy_score(y_test, y_prediction)

print("========== AI Model Evaluation ==========")

print("\nModel Accuracy:", round(accuracy * 100, 2), "%")

print("\n========== Classification Report ==========")
print(classification_report(y_test, y_prediction))

print("\n========== Confusion Matrix ==========")
print(confusion_matrix(y_test, y_prediction))
