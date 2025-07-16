# -*- coding: utf-8 -*-
"""
Evolutionary Optimization of Composite Geometry Using RSM-Based Stress Predictions

Description:
-------------
This script implements a full Genetic Algorithm (GA) loop for optimizing a geometric parameter set 
based on stress predictions using Response Surface Models (RSM) trained from ANSYS data.
The fitness function is based on the Maximum Stress failure criterion.

Main Features:
- Reads RSM models trained from CSV files (one per component and case)
- Predicts stresses for random geometry inputs
- Computes Failure Index (FI) and fitness
- Evolves inputs across generations via mutation
- Saves top 10% results every 10 generations and finally

How to Use on Another System:
-----------------------------
✅ Update the following line to your own local path where your CSVs are stored:
    base_path = r"C:\your\own\path\to\Superposition"
    The folder must contain subfolders: Case1, Case2, ..., each containing component-wise CSVs

✅ Ensure each CSV has:
    - 11 input columns (cols 1 to 11) and >=1 stress output columns (cols 12+)
    - Proper formatting (tab/CSV)

✅ Output:
    - Folder named 'Evolution_Results' will be created with CSVs of top 10% per component-case.
    - Console output shows evolution progress and top results.

Inputs:
    - Geometry vector of 12 values: ext, a1, r1, r2, dist, fillet, a2, seg1, seg2, seg3, n

Outputs:
    - For each case/component: Stress vector, Failure Index (FI), and Fitness
    - Top 10% saved to CSV per iteration

Author: Pranav Deshpande
Date: July 2025
"""

import random
import os
import numpy as np
import pandas as pd
from collections import defaultdict
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

# ==================== CONFIG ==========================================
base_path = r"C:\Pranav_folders\Pranav6.1\Entire_thing\Superposition"           # Change the Address here
num_cases = 6

# =============================== STORAGE =================================
rsm_models_all = {}
poly_features_all = {}

# =========================== TRAINING ====================================
for case_num in range(1, num_cases + 1):
    case_key = f"Case{case_num}"
    rsm_models_all[case_key] = {}
    poly_features_all[case_key] = {}

    case_path = os.path.join(base_path, case_key)
    component_files = [f for f in os.listdir(case_path) if f.endswith(".csv")]

    for comp_file in component_files:
        file_path = os.path.join(case_path, comp_file)
        try:
            data = pd.read_csv(file_path, on_bad_lines='skip')
        except Exception as e:
            print(f"❌ {file_path}: {e}")
            continue

        if data.shape[1] < 13:
            print(f"⚠️ {comp_file}: Not enough columns.")
            continue

        input_cols = data.columns[1:12]
        output_cols = data.columns[12:]
        X = data[input_cols]
        Y = data[output_cols]

        if len(X) < 10:
            print(f"⚠️ {comp_file}: Too few rows.")
            continue

        try:
            X_train, _, Y_train, _ = train_test_split(X, Y, test_size=0.2, random_state=42)
        except:
            continue

        poly = PolynomialFeatures(degree=2, include_bias=False)
        X_train_poly = poly.fit_transform(X_train)

        stress_models = {}
        for output in Y.columns:
            model = LinearRegression()
            model.fit(X_train_poly, Y_train[output])
            stress_models[output] = model

        rsm_models_all[case_key][comp_file] = stress_models
        poly_features_all[case_key][comp_file] = poly

# =================== PREDICTION ======================================
def predict_all_cases(new_input_12vals):
    results = {}
    for case_key in rsm_models_all:
        results[case_key] = {}
        for comp_file in rsm_models_all[case_key]:
            models = rsm_models_all[case_key][comp_file]
            poly = poly_features_all[case_key][comp_file]
            input_df = pd.DataFrame([new_input_12vals], columns=poly.feature_names_in_)
            input_poly = poly.transform(input_df)
            predictions = {stress: model.predict(input_poly)[0] for stress, model in models.items()}
            results[case_key][comp_file] = predictions
    return results

# =================== Allowable stresses extracted from Ansys Engineering Data ===========================
Tensile_X = 513_000_000
Tensile_Y = 513_000_000
Tensile_Z = 50_000_000
Compressive_X = -437_000_000
Compressive_Y = -437_000_000
Compressive_Z = -150_000_000
Shear_XY = 120_000_000
Shear_YZ = 55_000_000
Shear_XZ = 55_000_000

#=========================Failure Criteria ========================================
def Max_stress_criteria(stress_dict):
    FI_dict = {}
    for key, stress_values in stress_dict.items():
        max_fi = 0.0
        for i in range(0, len(stress_values), 6):
            Sx, Sy, Sz, Sxy, Syz, Sxz = stress_values[i:i+6]
            fi_sx = abs(Sx) / (Tensile_X if Sx >= 0 else abs(Compressive_X))
            fi_sy = abs(Sy) / (Tensile_Y if Sy >= 0 else abs(Compressive_Y))
            fi_sz = abs(Sz) / (Tensile_Z if Sz >= 0 else abs(Compressive_Z))
            fi_sxy = abs(Sxy) / Shear_XY
            fi_syz = abs(Syz) / Shear_YZ
            fi_sxz = abs(Sxz) / Shear_XZ
            local_max_fi = max(fi_sx, fi_sy, fi_sz, fi_sxy, fi_syz, fi_sxz)
            max_fi = max(max_fi, local_max_fi)
        FI_dict[key] = max_fi
    return FI_dict

#==========================Fitness Function =====================================

def compute_fitness(fi, min_fitness=1e-6, sharpness=8, penalty_power=2.5):
    fi = max(fi, 1e-6)
    if fi <= 1:
        fitness = np.exp(-sharpness * fi)
    else:
        penalty_term = (fi - 1) ** penalty_power
        fitness = np.exp(-sharpness * (1 + penalty_term))
    return max(min_fitness, min(1.0, fitness))

# =================== INPUT GENERATION =============================
MIN_N = 10
MAX_N = 100
def generate_random_solution():
    n = random.randint(MIN_N, MAX_N)
    ext = 200
    a1 = 10
    r1 = random.uniform(0.7*20, 1.3*20)
    r2 = random.uniform(0.7*60, 1.3*60)
    fillet = random.uniform(0.7*25, 1.3*25)
    dist = random.uniform(0.85*150, 1.15*150)
    a2 = 20
    a, b = sorted([random.random(), random.random()])
    return ext, a1, r1, r2, dist, fillet, a2, a, b-a, 1-b, n

# =================== Initial INPUT =============================
def initial_population(no_solution):
    population_inputs, population_stress_dicts = [], []
    for _ in range(no_solution):
        input_vec = generate_random_solution()
        stresses_all_cases = predict_all_cases(input_vec)
        stress_dict = {}
        for case_key in sorted(stresses_all_cases.keys()):
            case_num = case_key.replace("Case", "")
            for comp_file in sorted(stresses_all_cases[case_key].keys()):
                comp_name = comp_file.replace(".csv", "")
                stress_key = f"stress_{comp_name}_case{case_num}"
                stress_vals = list(stresses_all_cases[case_key][comp_file].values())
                stress_dict[stress_key] = stress_vals
        population_inputs.append(input_vec)
        population_stress_dicts.append(stress_dict)
    return population_inputs, population_stress_dicts

#====================Ranking and Appending==========================

def FI_and_Fitness(inputs, stress_maps):
    for stress_dict in stress_maps:
        fi_result = Max_stress_criteria(stress_dict)
        for key, val in fi_result.items():
            if len(stress_dict[key]) % 6 == 0:
                stress_dict[key].append(val)
    for stress_dict in stress_maps:
        for key in stress_dict:
            if key.startswith("stress_") and isinstance(stress_dict[key], list):
                if len(stress_dict[key]) % 6 == 1:
                    fi = stress_dict[key][-1]
                    stress_dict[key].append(compute_fitness(fi))
    sorted_results = defaultdict(list)
    for input_vec, stress_dict in zip(inputs, stress_maps):
        for key in stress_dict:
            if key.startswith("stress_") and isinstance(stress_dict[key], list):
                stress_vec = stress_dict[key]
                fitness = stress_vec[-1]
                sorted_results[key].append((fitness, input_vec, stress_vec))
    for key in sorted_results:
        sorted_results[key].sort(key=lambda x: x[0], reverse=True)
    return sorted_results

#================Calling and Top10% generation=-===============
def GA():
    inputs, stress_maps = initial_population(100)
    sorted_results = FI_and_Fitness(inputs, stress_maps)
    top10_by_key = {}
    for key, all_results in sorted_results.items():
        top_n = max(1, len(all_results) // 10)
        top10_by_key[key] = all_results[:top_n]
    return sorted_results, top10_by_key


#===================Mutation ==================================
def mutation(top10_by_key, key, n_variants=9):
    indices_to_mutate = [2, 3, 4, 5, 7, 8, 9, 10]
    new_inputs, new_stress_maps = [], []
    for _, input_vec, _ in top10_by_key[key]:
        input_list = list(input_vec)
        for _ in range(n_variants):
            mutated = input_list.copy()
            for idx in indices_to_mutate:
                mutated[idx] *= random.uniform(0.9, 1.1)
            new_inputs.append(tuple(mutated))
    for mutated_input in new_inputs:
        stresses_all_cases = predict_all_cases(mutated_input)
        stress_dict = {}
        for case_key in sorted(stresses_all_cases.keys()):
            case_num = case_key.replace("Case", "")
            for comp_file in sorted(stresses_all_cases[case_key].keys()):
                comp_name = comp_file.replace(".csv", "")
                stress_key = f"stress_{comp_name}_case{case_num}"
                stress_vals = list(stresses_all_cases[case_key][comp_file].values())
                stress_dict[stress_key] = stress_vals
        new_stress_maps.append(stress_dict)
    sorted_mutated = FI_and_Fitness(new_inputs, new_stress_maps)
    full_result = defaultdict(list)
    for k in top10_by_key:
        full_result[k].extend(top10_by_key[k])
        full_result[k].extend(sorted_mutated.get(k, []))
        full_result[k].sort(key=lambda x: x[0], reverse=True)
    return full_result

# ============================ Iteration LOOP ======================================
def run_evolution(max_iters=100, convergence_threshold=1e-8):
    top_list_by_key, top10_by_key = GA()
    best_fitness_history = defaultdict(list)
    stagnant_counter = defaultdict(int)
    max_stagnant_generations = 10

    for iteration in range(max_iters):
        print(f"\n===== Generation {iteration + 1} =====")
        improved = False
        for key in top10_by_key:
            prev_best = top10_by_key[key][0][0] if top10_by_key[key] else 0.0
            sorted_mutated = mutation(top10_by_key, key)
            top_n = max(1, len(sorted_mutated[key]) // 10)
            new_top10 = sorted_mutated[key][:top_n]
            new_best = new_top10[0][0]
            top10_by_key[key] = new_top10
            best_fitness_history[key].append(new_best)
            if abs(new_best - prev_best) > convergence_threshold:
                stagnant_counter[key] = 0
                improved = True
            else:
                stagnant_counter[key] += 1
            print(f"▶️ {key}: Best fitness = {new_best:.6f}, Δ = {new_best - prev_best:.2e}")
        if (iteration + 1) % 1 == 0:
            save_top10_to_csv(top10_by_key, iteration + 1)
        if not improved and all(stagnant_counter[k] >= max_stagnant_generations for k in top10_by_key):
            print("\n✅ Convergence achieved across all keys.")
            break
    save_top10_to_csv(top10_by_key, 'final')
    for key in top10_by_key:
        print(f"\n📌 Final Top 5 for {key}:")
        for i, (fitness, input_vec, stress_vec) in enumerate(top10_by_key[key][:5]):
            print(f"  {i+1}. Fitness = {fitness:.6f} | Input = {input_vec}")
    return top10_by_key

#==========================Data Saving ===========================================
def save_top10_to_csv(top10_by_key, iteration):
    out_dir = "Evolution_Results"
    os.makedirs(out_dir, exist_ok=True)
    for key in top10_by_key:
        case_component = key.replace("stress_", "").replace("_case", "_Case")
        csv_name = f"top10_{case_component}_iter{iteration}.csv"
        full_path = os.path.join(out_dir, csv_name)
        with open(full_path, 'w') as f:
            f.write("Fitness,Input_Vector,Stress_Vector\n")
            for fitness, input_vec, stress_vec in top10_by_key[key]:
                input_str = ",".join(f"{v:.6f}" if isinstance(v, float) else str(v) for v in input_vec)
                stress_str = ",".join(f"{v:.6e}" for v in stress_vec)
                f.write(f"{fitness:.8f},[{input_str}],[{stress_str}]\n")
        print(f"💾 Saved top 10% of {key} to {csv_name}")

# ================================ MAIN ENTRY ======================================
if __name__ == "__main__":
    final_top = run_evolution(max_iters=100)
