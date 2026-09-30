
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
# Plot selected well logs
fig, axes = plt.subplots(1, 4, figsize=(14, 8), sharey=True)

# Gamma Ray
axes[0].plot(data["GR"], data["DEPTH"])
axes[0].set_xlabel("GR (API)")
axes[0].set_ylabel("Depth")
axes[0].set_title("Gamma Ray")

# Bulk Density
axes[1].plot(data["RHOB"], data["DEPTH"])
axes[1].set_xlabel("RHOB (g/cc)")
axes[1].set_title("Bulk Density")

# Neutron Porosity
axes[2].plot(data["NPHI"], data["DEPTH"])
axes[2].set_xlabel("NPHI")
axes[2].set_title("Neutron Porosity")

# Resistivity
axes[3].plot(data["RT"], data["DEPTH"])
axes[3].set_xlabel("RT (ohm.m)")
axes[3].set_title("Resistivity")

for ax in axes:
    ax.invert_yaxis()
    ax.grid(True)

plt.tight_layout()
plt.savefig("well_log_overview.png", dpi=300, bbox_inches="tight")
# Simple shale indicator based on Gamma Ray
data["SHALE_FLAG"] = data["GR"] > 60

print("\nPotential shale intervals:")
print(data[data["SHALE_FLAG"]][["DEPTH", "GR"]])
# Linear Gamma Ray Index
GR_clean = 38
GR_shale = 82

data["VSH_GR"] = (
    (data["GR"] - GR_clean) /
    (GR_shale - GR_clean)
).clip(0, 1)

print("\nGamma Ray Shale Volume:")
print(data[["DEPTH", "GR", "VSH_GR"]])
# Density Porosity
RHOMATRIX = 2.65
RHOFLUID = 1.0

data["PHI_D"] = (
    (RHOMATRIX - data["RHOB"]) /
    (RHOMATRIX - RHOFLUID)
)

print("\nDensity Porosity:")
print(data[["DEPTH", "RHOB", "PHI_D"]])
# Compare Density and Neutron Porosity
data["PHI_DIFF"] = data["PHI_D"] - data["NPHI"]

print("\nDensity-Neutron Porosity Comparison:")
print(data[["DEPTH", "PHI_D", "NPHI", "PHI_DIFF"]])
# Density-Neutron Crossplot
plt.figure(figsize=(7, 6))

plt.scatter(
    data["PHI_D"],
    data["NPHI"],
    c=data["DEPTH"],
    cmap="viridis"
)

plt.xlabel("Density Porosity (fraction)")
plt.ylabel("Neutron Porosity (fraction)")
plt.title("Density-Neutron Porosity Crossplot")
plt.colorbar(label="Depth")
plt.grid(True)

plt.tight_layout()
plt.savefig("density_neutron_crossplot.png", dpi=300, bbox_inches="tight")

data["PHI_AVG"] = (data["PHI_D"] + data["NPHI"]) / 2
print("\nAverage Porosity:")
print(data[["DEPTH", "PHI_D", "NPHI", "PHI_AVG"]])
# Average Porosity vs Depth
plt.figure(figsize=(6, 8))

plt.plot(data["PHI_AVG"], data["DEPTH"], marker="o")

plt.xlabel("Average Porosity (fraction)")
plt.ylabel("Depth")
plt.title("Average Porosity vs Depth")

plt.gca().invert_yaxis()
plt.grid(True)

plt.tight_layout()
plt.savefig("average_porosity_vs_depth.png", dpi=300, bbox_inches="tight")


# Shale-adjusted porosity
data["NET_POROSITY"] = data["PHI_AVG"] * (1 - data["VSH_GR"])

print("\nShale-adjusted Porosity:")
print(data[["DEPTH", "VSH_GR", "PHI_AVG", "NET_POROSITY"]])
# Shale-adjusted Porosity vs Depth
plt.figure(figsize=(6, 8))

plt.plot(
    data["NET_POROSITY"],
    data["DEPTH"],
    marker="o"
)

plt.xlabel("Shale-adjusted Porosity (fraction)")
plt.ylabel("Depth")
plt.title("Shale-adjusted Porosity vs Depth")

plt.gca().invert_yaxis()
plt.grid(True)

plt.tight_layout()
plt.savefig("shale_adjusted_porosity_vs_depth.png", dpi=300, bbox_inches="tight")

# Final Petrophysical Summary
summary = data[
    [
        "DEPTH",
        "GR",
        "VSH_GR",
        "PHI_D",
        "NPHI",
        "PHI_AVG",
        "NET_POROSITY"
    ]
]

print("\nPetrophysical Summary:")
print(summary)
# Potential Reservoir Interval

data["RESERVOIR_FLAG"] = (
    (data["VSH_GR"] < 0.35) &
    (data["NET_POROSITY"] > 0.15) &
    (data["RT"] > 10)
)

print("\nPotential Reservoir Intervals:")
print(
    data[
        data["RESERVOIR_FLAG"]
    ][
        ["DEPTH", "VSH_GR", "NET_POROSITY", "RT", "RESERVOIR_FLAG"]
    ]
)
# Reservoir Quality Classification

data["RESERVOIR_QUALITY"] = "Poor"

data.loc[
    (data["NET_POROSITY"] > 0.15) &
    (data["VSH_GR"] < 0.35) &
    (data["RT"] > 10),
    "RESERVOIR_QUALITY"
] = "Moderate"

data.loc[
    (data["NET_POROSITY"] > 0.18) &
    (data["VSH_GR"] < 0.20) &
    (data["RT"] > 18),
    "RESERVOIR_QUALITY"
] = "Good"

print("\nReservoir Quality Classification:")
print(
    data[
        ["DEPTH", "VSH_GR", "NET_POROSITY", "RT", "RESERVOIR_QUALITY"]
    ]
)
# Reservoir Quality vs Depth

quality_map = {
    "Poor": 0,
    "Moderate": 1,
    "Good": 2
}

data["QUALITY_CODE"] = data["RESERVOIR_QUALITY"].map(quality_map)

plt.figure(figsize=(6, 8))

colors = {
    "Poor": "red",
    "Moderate": "orange",
    "Good": "green"
}

for quality in ["Poor", "Moderate", "Good"]:
    subset = data[data["RESERVOIR_QUALITY"] == quality]

    plt.scatter(
        subset["QUALITY_CODE"],
        subset["DEPTH"],
        s=100,
        color=colors[quality],
        label=quality
    )

plt.xticks(
    [0, 1, 2],
    ["Poor", "Moderate", "Good"]
)

plt.xlabel("Reservoir Quality")
plt.ylabel("Depth")
plt.title("Reservoir Quality vs Depth")

plt.gca().invert_yaxis()
plt.grid(True)
plt.legend()

plt.tight_layout()
plt.savefig("reservoir_quality_vs_depth.png", dpi=300, bbox_inches="tight")

# Reservoir Interval Thickness

reservoir_data = data[data["RESERVOIR_FLAG"]]

top_depth = reservoir_data["DEPTH"].min()
base_depth = reservoir_data["DEPTH"].max()

reservoir_thickness = base_depth - top_depth

print("\nReservoir Interval:")
print("Top Depth:", top_depth)
print("Base Depth:", base_depth)
print("Thickness:", reservoir_thickness)
# Average Reservoir Properties

avg_vsh = reservoir_data["VSH_GR"].mean()
avg_net_porosity = reservoir_data["NET_POROSITY"].mean()
avg_rt = reservoir_data["RT"].mean()

print("\nAverage Reservoir Properties:")
print("Average VSH:", avg_vsh)
print("Average Net Porosity:", avg_net_porosity)
print("Average Resistivity:", avg_rt)
# Reservoir Interval Summary

interval_summary = pd.DataFrame({
    "Top_Depth": [top_depth],
    "Base_Depth": [base_depth],
    "Thickness": [reservoir_thickness],
    "Average_VSH": [avg_vsh],
    "Average_Net_Porosity": [avg_net_porosity],
    "Average_Resistivity": [avg_rt]
})

print("\nReservoir Interval Summary:")
print(interval_summary)
# Save Reservoir Interval Summary

interval_summary.to_csv(
    "reservoir_interval_summary.csv",
    index=False
)

print("\nReservoir Interval Summary saved to CSV.")