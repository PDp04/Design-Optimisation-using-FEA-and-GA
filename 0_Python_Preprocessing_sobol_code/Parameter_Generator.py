"""
Parameters Generator using Sobol Sequencing
--------------------------------------------------
Author: Pranav Deshpande
Date: July 2025


Inputs:
- The maximum and Minimum values of the parameters to be varied

Outputs:
- sobol_composites_10_to_100_plies.csv

Warning:
- The CSV generaed wont have all the values, will have to input the dp no. and the Extrusion, Angle1, Angle2 using excel.
- While copying to Ansys, make sure you replace TRUE with 'True and FALSE with 'False, or it will show error
"""

import numpy as np
import pandas as pd
from scipy.stats import qmc
import random
from collections import Counter

# --- Ply layup generation helpers ---
def is_balanced(sequence):
    counts = Counter()
    for angle in sequence:
        if abs(angle) not in [0, 90]:
            counts[abs(angle)] += angle // abs(angle)
    return all(count == 0 for count in counts.values())

def generate_symmetric_balanced_laminate(n):
    base_angles = [0, 45, 90]
    if n % 2 == 0:
        half_n = n // 2
        while True:
            half_sequence = []
            for _ in range(half_n):
                base_angle = random.choice(base_angles)
                if base_angle in [0, 90]:
                    half_sequence.append(base_angle)
                else:
                    sign = random.choice([1, -1])
                    half_sequence.append(sign * base_angle)
            full_sequence = half_sequence + list(reversed(half_sequence))
            if is_balanced(full_sequence):
                return full_sequence
    else:
        half_n = (n - 1) // 2
        middle_ply = random.choice([0, 90])
        while True:
            half_sequence = []
            for _ in range(half_n):
                base_angle = random.choice(base_angles)
                if base_angle in [0, 90]:
                    half_sequence.append(base_angle)
                else:
                    sign = random.choice([1, -1])
                    half_sequence.append(sign * base_angle)
            full_sequence = half_sequence + [middle_ply] + list(reversed(half_sequence))
            if is_balanced(full_sequence):
                return full_sequence

# --- Geometric parameter bounds ---
param_bounds = {
    "radius_small": ((0.7*20), (1.3*20)),
    "radius_large": ((0.7*60), (1.3*60)),
    "distance_between_circles": ((0.85*150), (1.15*150)),
    "frame_fillet_radius": ((0.7*25), (1.3*25)),
}

n_samples = 4000
min_plies = 10
max_plies = 100

# Sobol sampling for geometric parameters
l_bounds = np.array([v[0] for v in param_bounds.values()])
u_bounds = np.array([v[1] for v in param_bounds.values()])
sampler = qmc.Sobol(d=len(param_bounds), scramble=True)
sample = sampler.random_base2(m=12)
scaled_sample = qmc.scale(sample, l_bounds, u_bounds)[:n_samples]

# --- Build dataset ---
rows = []

for i in range(n_samples):
    row = list(scaled_sample[i])
    
    # Random number of plies between 20 and 50
    n_plies = random.randint(min_plies, max_plies)
    layup = generate_symmetric_balanced_laminate(n_plies)

    # Pad angles and active flags
    padded_angles = layup + [0] * (max_plies - len(layup))
    active_flags = [1]*len(layup) + [0]*(max_plies - len(layup))


    row.extend(padded_angles)
    row.extend(active_flags)
    rows.append(row)

# Column names
columns = list(param_bounds.keys())
columns += [f"ply_angle_{i+1}" for i in range(max_plies)]
columns += [f"ply_active_{i+1}" for i in range(max_plies)]

# Create DataFrame and export
df = pd.DataFrame(rows, columns=columns)
df.to_csv("sobol_composites_10_to_100_plies.csv", index=False)

print("✅ 4000 samples with 10–100 ply stacks saved.")
