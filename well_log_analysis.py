
# Python Well Log Analysis

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load well log data
data = pd.read_csv("well_log_data.csv")

# Display the first rows
print(data.head())

# Display basic information
print(data.info())
# Basic statistical analysis
print("\nStatistical Summary:")
print(data.describe())
# Plot Gamma Ray log
plt.figure(figsize=(6, 8))
plt.plot(data["GR"], data["DEPTH"])
plt.gca().invert_yaxis()

plt.xlabel("Gamma Ray (API)")
plt.ylabel("Depth")
plt.title("Gamma Ray Log")

plt.show()
