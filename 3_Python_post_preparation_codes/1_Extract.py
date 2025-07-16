"""
Extract and Organise Data from the Ansys Output
--------------------------------------------------
Author: Pranav Deshpande
Date: July 2025

Changes:
- Address of the Design Point Data File extracted Out of the Ansys on line 91
- Change the DP to be Extracted on line 126, can even run multiple python codes with different intervals to extract faster

Outputs:
combined_stress_output/
│
├── dpX/                            # Design point folder (e.g., dp0, dp1, ...)
│   │       
│   ├── loadY/                      # Load case folder (e.g., load1, load2, ...)
│   │   ├── le_1.csv                # Stress result CSV file
│   │   ├── le_r_2.csv
│   │   ├── ...
│   │   ├── stress_summary.csv      # Has the maximum and minimum  stresses at each component
│   │   ├── ...
│   │   └── le_n.csv
│   │
│   └── ...
│
└── ...

"""

import os
import pandas as pd

# Stress label names
STRESS_LABELS = [
    "Ply1_SX", "Ply1_SY", "Ply1_SZ",
    "Ply1_SXY", "Ply1_SYZ", "Ply1_SXZ",
    "Ply2_SX", "Ply2_SY", "Ply2_SZ",
    "Ply2_SXY", "Ply2_SYZ", "Ply2_SXZ",
    "Ply3_SX", "Ply3_SY", "Ply3_SZ",
    "Ply3_SXY", "Ply3_SYZ", "Ply3_SXZ"
]


def extract_node_ids(node_file_path):
    node_ids = []
    with open(node_file_path, 'r') as f:
        lines = f.readlines()
    for line in lines:
        try:
            first_token = line.strip().split()[0]
            node_id = int(first_token.split('-')[0])
            node_ids.append(node_id)
        except (IndexError, ValueError):
            raise ValueError(f"❌ Could not parse line: {line.strip()}")
    return node_ids


def process_stress_files(stress_dir):
    stress_data = {}
    stress_files = sorted([f for f in os.listdir(stress_dir) if f.endswith(".txt")])
    if len(stress_files) < 18:
        raise ValueError(f"❌ Only {len(stress_files)} stress files found in {stress_dir}. Expected 18.")
    for i, file in enumerate(stress_files[:18]):
        df = pd.read_csv(os.path.join(stress_dir, file), sep=r'\s+', engine="python")
        if df.shape[1] >= 2:
            df = df.iloc[:, :2]
            df.columns = ['Node', STRESS_LABELS[i]]
            stress_data[file] = df.set_index("Node")
        else:
            raise ValueError(f"❌ Not enough columns in stress file: {file}")
    return pd.concat(stress_data.values(), axis=1)


def generate_summary(output_dir):
    summary_rows = []
    csv_files = sorted([f for f in os.listdir(output_dir) if f.endswith(".csv")])
    for file in csv_files:
        df = pd.read_csv(os.path.join(output_dir, file))
        row = {"Component": file}
        for col in df.columns:
            if col == "Node":
                continue
            row[f"{col}_max"] = df[col].max()
            row[f"{col}_min"] = df[col].min()
        summary_rows.append(row)
    summary_df = pd.DataFrame(summary_rows)
    summary_csv = os.path.join(output_dir, "stress_summary.csv")
    summary_df.to_csv(summary_csv, index=False)
    print(f"📄 Summary created: {summary_csv}")


def process_load_case(dp_index, load_index):
    base_dp_path = fr"C:\\Pranav_folders\\Pranav6.0\\dp{dp_index}"                  #will have to change the Address to your Ansys output file
    node_dir = os.path.join(base_dp_path, "Nodes")
    stress_dir = os.path.join(base_dp_path, f"stresses_load_{load_index}")
    if not os.path.exists(node_dir) or not os.path.exists(stress_dir):
        print(f"⚠️ Skipped dp{dp_index} load{load_index}: required directory not found.")
        return

    try:
        stress_df = process_stress_files(stress_dir)
    except Exception as e:
        print(f"❌ Error processing stress files in dp{dp_index} load{load_index}: {e}")
        return

    output_dir = os.path.join(os.getcwd(), "combined_stress_output", f"dp{dp_index}", f"load{load_index}")
    os.makedirs(output_dir, exist_ok=True)

    for node_file in os.listdir(node_dir):
        if not node_file.endswith(".node"):
            continue
        node_file_path = os.path.join(node_dir, node_file)
        try:
            node_ids = extract_node_ids(node_file_path)
            filtered_df = stress_df.loc[stress_df.index.isin(node_ids)].reset_index()
            if filtered_df.empty:
                raise ValueError("No matching stress values found.")
            output_file = os.path.join(output_dir, node_file.replace(".node", ".csv"))
            filtered_df.to_csv(output_file, index=False)
        except Exception as e:
            print(f"⚠️ Error with {node_file} in dp{dp_index} load{load_index}: {e}")

    generate_summary(output_dir)


# === MAIN LOOP ===
for dp in range(592, 907):                              #The design Points you wanna extract
    for load in range(1, 7):                            #can even run multiple Python code with extracting it in interval
        print(f"\n🔄 Processing dp{dp} load{load}")
        process_load_case(dp, load)

print("\n✅ Done processing all design points and loads.")
