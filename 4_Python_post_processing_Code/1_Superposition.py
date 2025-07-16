
"""
Superposition of stresses based on given Load  data
--------------------------------------------------
Author: Pranav Deshpande
Date: July 2025

Do vector Addition of the stresses based on the Load data

Changes:
- Address of the 'Component_stresses' folder createdby '3_Combination.py' on line 51

Outputs: 

Superposition/
│
├── CaseX/              # Where Case vary from 1 to 6      
│   │
│   ├── le_1.csv             
│   ├── le_2.csv            
│   ├── ...
│   └── le_n.csv   
└── ...

"""

import pandas as pd
import os

# ==== STEP 1: Read multipliers from Forces1.csv ====
forces_df = pd.read_csv("Forces1.csv")

# Force-to-multiplier conversion
Mx_mult = forces_df.iloc[:, 3] / 100
My_mult = forces_df.iloc[:, 4] / 100
Mz_mult = forces_df.iloc[:, 5] / 100
Nx_mult = forces_df.iloc[:, 0] / 1000
Ny_mult = forces_df.iloc[:, 1] / 1000 
Nz_mult = forces_df.iloc[:, 2] / 1000

# === Paths ===
input_base = r"C:\Pranav_folders\Pranav6.1\Component_stresses"     #change the Address here
load1_path = os.path.join(input_base, "load1")
component_files = [f for f in os.listdir(load1_path) if f.endswith(".csv")]

# === Loop over DP0 to DP5 ===
for dp_index in range(6):
    print(f"\n🚀 Processing Design Point {dp_index} (Case{dp_index+1})")

    # Create output folder for this DP
    output_base = os.path.join("Superposition", f"Case{dp_index+1}")
    os.makedirs(output_base, exist_ok=True)

    # Define multipliers for this DP
    multiplier_map = {
        1: Mx_mult[dp_index],
        2: My_mult[dp_index],
        3: Mz_mult[dp_index],
        4: Nx_mult[dp_index],
        5: Ny_mult[dp_index],
        6: Nz_mult[dp_index]
    }

    for filename in component_files:
        print(f"▶ Processing: {filename}")
        total_sup_stress = None
        first_12_cols = None

        for load_num in range(1, 7):
            file_path = os.path.join(input_base, f"load{load_num}", filename)

            try:
                stresses = pd.read_csv(file_path, on_bad_lines='skip')
            except Exception as e:
                print(f"❌ Failed to read {file_path}: {e}")
                continue

            if stresses.shape[1] < 48:
                print(f"⚠️ Skipping {filename}, load{load_num}: not enough columns.")
                continue

            if first_12_cols is None:
                first_12_cols = stresses.iloc[:, :12].copy()

            stress1 = stresses.iloc[:, 12:]
            result = pd.DataFrame()
            cols = stress1.columns.tolist()

            i = 0
            while i < len(cols) - 1:
                col_max = cols[i]
                col_min = cols[i + 1]
                base_name = col_max.replace('_max', '')

                max_vals = stress1[col_max]
                min_vals = stress1[col_min]

                dominant = max_vals.where(abs(max_vals) >= abs(min_vals), min_vals)
                result[base_name] = dominant

                i += 2

            sup_stress = result * multiplier_map[load_num]

            if total_sup_stress is None:
                total_sup_stress = sup_stress
            else:
                total_sup_stress += sup_stress

        # === Combine and save ===
        if total_sup_stress is not None:
            final_result = pd.concat([first_12_cols, total_sup_stress], axis=1)
            output_path = os.path.join(output_base, filename)
            final_result.to_csv(output_path, index=False)
            print(f"✅ Saved: {output_path}")
        else:
            print(f"⚠️ Skipped: {filename} — no valid data")
