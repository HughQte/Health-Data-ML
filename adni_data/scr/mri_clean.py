# Import libraries
import os
import warnings
import pansas as pd
import numpy as np

# Load dataset
df = pd.read_csv("ucsf_fsx7.csv")
print(df.head(10))
print()
print(df.tail(10))

# Check data's shape
print(f"Shape: {df.shape[0]} rows x {df.shape[1]} columns") # (12290, 347)

# Count data's type
print(df.dtypes.value_counts())

# Count how many MRI features in the dataset
id_cols = ["PTID",
           "VSCODE2"]
acquisition_cols = ["FIELD_STRENGTH"]

exclude_cols = id_cols + acquisition_cols

mri_features = [
    col for col in df.columns
    if col not in exclude_cols
    and pd.api.types.is_numeric_dtype(df[col])
]

print("MRI features:", len(mri_features))  # MRI features: 326

# Checking missing values of MRI features
missing = (df[mri_features].isna().mean().sort_values(ascending=False))

missing_df = pd.DataFrame({"missing_pct": missing * 100})

missing_df.head(30) # ST8SV has 99.06% and ST68SV	has 90.88% missing values

# Drop missing values due to threshold 
missing_threshold = 0.30

features_keep = missing[
    missing <= missing_threshold
].index.tolist()

print("Before:", len(mri_features))
print("After missingness filter:", len(features_keep)) 

# Check unique features
nunique = df[features_keep].nunique(dropna=True)

constant_features = nunique[
    nunique <= 1
].index.tolist()

constant_features # []

# Correlation and flag the high corr
corr = df[features_keep].corr().abs()

upper = corr.where(
    np.triu(
        np.ones(corr.shape),
        k=1
    ).astype(bool)
)

high_corr_features = [
    column
    for column in upper.columns
    if any(upper[column] > 0.90)
]

print("Highly correlated features:", len(high_corr_features)) # Highly correlated features: 10

# Create table of high correlation pairs
corr_pairs = []

for i in range(len(upper.columns)):
    for j in range(i):
        
        value = upper.iloc[j, i]
        
        if pd.notna(value) and value > 0.90:
            corr_pairs.append([
                upper.columns[j],
                upper.columns[i],
                value
            ])

corr_pairs_df = pd.DataFrame(
    corr_pairs,
    columns=[
        "Feature_1",
        "Feature_2",
        "Correlation"
    ]
)

corr_pairs_df = corr_pairs_df.sort_values(
    "Correlation",
    ascending=False
)

corr_pairs_df.head(30)

# Drop features with extreme missingness
df1 = df.drop(columns=["ST8SV", "ST68SV", "STATUS"]).copy()

# Keep identifiers/acquisition info + all ST features
keep_cols = [
    "PTID",
    "VISCODE2",
    "FIELD_STRENGTH"
] + [
    col for col in df1.columns
    if col.startswith("ST")
]

df1 = df1[keep_cols]

print(df1.shape)
df1.head()
