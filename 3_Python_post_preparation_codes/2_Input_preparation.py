"""
Prepare the input paramters for RSM
--------------------------------------------------
Author: Pranav Deshpande
Date: July 2025

As the number of Plies are changing with each design point, the number of paramters are also changing
this can add complexity to the RSM generation, so the ply angles were replaced by percentage of each 
angle in the input paaramter, the number of each angle can be easily found by multiplying with, number of 
plies and there are very few combinations for the balanced symmetric Lay-up with given number of angles

Changes:
- Address of the sobol_composites_10_to_100_plies.csv on line 18

Outputs: 
- sobol_composites_cleaned.csv
"""

import pandas as pd

# Load original CSV
df = pd.read_csv("sobol_composites_10_to_100_plies.csv")                    # can be written as 'df = pd.read_csv(r"path/sobol_composites_10_to_100_plies.csv")'

# Identify ply columns
ply_angle_cols = [col for col in df.columns if col.startswith('ply_angle')]
ply_active_cols = [col for col in df.columns if col.startswith('ply_active')]

# Store new data
frac_0_list = []
frac_45_list = []
frac_90_list = []
num_active_plies = []

# Loop through each design point
for idx, row in df.iterrows():
    angles = row[ply_angle_cols].dropna().astype(int).values
    actives = row[ply_active_cols].dropna().astype(int).values

    # Filter only active plies
    active_angles = [angle for angle, active in zip(angles, actives) if active == 1]
    total_active = len(active_angles)

    # Avoid division by zero
    if total_active == 0:
        frac_0 = frac_45 = frac_90 = 0
    else:
        frac_0 = sum(1 for a in active_angles if a == 0) / total_active
        frac_90 = sum(1 for a in active_angles if a == 90) / total_active
        frac_45 = sum(1 for a in active_angles if abs(a) == 45) / total_active

    frac_0_list.append(frac_0)
    frac_45_list.append(frac_45)
    frac_90_list.append(frac_90)
    num_active_plies.append(total_active)

# Add new columns
df['frac_0_deg'] = frac_0_list
df['frac_45_deg'] = frac_45_list
df['frac_90_deg'] = frac_90_list
df['num_active_plies'] = num_active_plies

# Drop original ply angle & activity columns
df.drop(columns=ply_angle_cols + ply_active_cols, inplace=True)

# Save to new CSV
df.to_csv("sobol_composites_cleaned.csv", index=False)
print("✅ Saved: sobol_composites_cleaned.csv (fractions + active ply count, cleaned)")
