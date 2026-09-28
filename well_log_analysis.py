
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
