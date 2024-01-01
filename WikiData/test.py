import pandas as pd
import json


def minMaxPropertyValue(df: pd.DataFrame) -> (float, float):
    numeric_values = pd.to_numeric(
        df["Value"], errors="coerce"
    )  # Convert values to numeric, coercing errors to NaN
    numeric_values = numeric_values.dropna()  # Remove rows with non-numeric values
    return numeric_values.min(), numeric_values.max()


# Example usage
data = {"Value": ["5", "3.14", "7.2", "abc", "10.5"]}
df = pd.DataFrame(data)
min_value, max_value = minMaxPropertyValue(df)
print("Min Value:", min_value)
print("Max Value:", max_value)
