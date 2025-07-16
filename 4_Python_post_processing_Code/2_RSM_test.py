"""
Test the RSM for initial Design conditions
--------------------------------------------------
Author: Pranav Deshpande
Date: July 2025

Changes:
- Address of the Super position file on line 20

Outputs:
"""
import pandas as pd
import numpy as np
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

# --- Step 1: Load Data ---
data = pd.read_csv(r'C:\Pranav_folders\Pranav6.1\Entire_thing\Superposition\Case1\le_r_10.csv', on_bad_lines='skip')            #Change the Address Accordingly

# --- Step 2: Define Input and Output Columns ---
input_cols = data.columns[1:12]   # Columns 1 to 12 (Python 0-indexed)
output_cols = data.columns[12:]   # Columns 13 onwards

# --- Step 4: Prepare Input and Output Data ---
X = data[input_cols]
Y = data[output_cols]

# --- Step 5: Train-Test Split (80% Train, 20% Test) ---
X_train, X_test, Y_train, Y_test = train_test_split(
    X, Y, test_size=0.2, random_state=42
)

# --- Step 6: Fit RSM for Each Output (Quadratic Polynomial Regression) ---
rsm_models = {}
r2_scores = {}

poly = PolynomialFeatures(degree=2, include_bias=False)
X_train_poly = poly.fit_transform(X_train)
X_test_poly = poly.transform(X_test)

for output in Y.columns:
    y_train = Y_train[output]
    y_test = Y_test[output]
    
    model = LinearRegression()
    model.fit(X_train_poly, y_train)
    
    r2 = model.score(X_test_poly, y_test)
    r2_scores[output] = r2
    
    rsm_models[output] = {
        'model': model,
        'r2_score': r2
    }

# --- Summary of R² Scores ---
print("\n📊 R² Scores for Each Output Variable:")
for output, r2 in r2_scores.items():
    print(f"{output:20s}: {r2:.4f}")

# --- Step 7: Predict for New Input Parameter ---
new_input = [[200, 10, 25, 60, 150, 25, 20, 0.3, 0.3, 0.4, 50]]  # Length must match 12 inputs
new_input_poly = poly.transform(new_input)

print("\n🔮 Predicted Stresses for New Input:")
for output in Y.columns:
    prediction = rsm_models[output]['model'].predict(new_input_poly)
    print(f"{output:20s}: {prediction[0]:.2f}")
