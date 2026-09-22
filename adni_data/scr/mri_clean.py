# This textfile is used for preprocessing UCSF FreeSurfer MRI derived from ADNI
# Import working libraries
import os
import warnings
import pandas as pd
import numpy as np

# Data source:
# Alzheimer's Disease Neuroimaging Initiative (ADNI)
# Load dataset
df = pd.read_csv('../data/ucsf_fsx7.csv') # The dataset will be provided

# Print original shape
print(f"Original shape: {df.shape[0]} rows x {df.shape[1]} columns") # (12290, 347)

# Filtering based on study reference
# Select Field Strength = 3T only
df = (df[df["FIELD_STRENGTH"] == "3T"].copy().reset_index(drop=True))

# Conver EXAMDATE to a real date
df["EXAMDATE"] = pd.to_datetime(df["EXAMDATE"], errors="coerce")

# Use EXAMDATE to select the earliest visit for MRI for each subjects
df = (df.sort_values(["PTID", "EXAMDATE"])  # Sort subject id based on the ealiest exam date
      .drop_duplicates(subset="PTID", keep="first") # Drop duplicate rows for subject, but keep 1 unique row
      .reset_index(drop=True))

# Drop unnecessary columns
keep_cols = ["PTID", "VISCODE2", "FIELD_STRENGTH", "EXAMDATE"] + [col for col in df.columns if col.startswith("ST")]
df = df[keep_cols]

print(f"Total of duplicated rows: {df["PTID"].duplicated().sum()} rows") # 0 rows
print(f"Shape after preprocessing: {df.shape[0]} rows x {df.shape[1]} columns") # (2565, 330)

# Preprocessing +300 FreeSurfer MRI features set
mri_features = [col for col in df.columns if col.startswith("ST") # Select only column contains 'ST'
                
                      and pd.api.types.is_numeric_dtype(df[col])]       # Those 'ST' columns must contain numeric varibles

# Report number of mri features of the curent table
print("Original MRI features:", len(mri_features))   # 325

# Divide features into 5 sets according to type of 
cv_features = [c for c in df.columns if c.endswith('CV')] # Cortical Volume
sa_features = [c for c in df.columns if c.endswith('SA')] # Surface Area
ta_features = [c for c in df.columns if c.endswith('TA')] # Mean Cortical Thickness
ts_features = [c for c in df.columns if c.endswith('TS')] # Cortical Thickness Standard Deviation
sv_features = [c for c in df.columns if c.endswith('SV')] # Subcortical / Aseg Volume

print("Cortical Volume:", len(cv_features))                                # 69
print("Surface Area:", len(sa_features))                                   # 69
print("Mean Cortical Thickness:", len(ta_features))                        # 68
print("Cortical Thickness Standard Deviation:", len(ts_features))          # 68
print("Subcortical/Aseg Volume:", len(sv_features))                        # 50

# Checking missing values within groups
def check_missing(df, *features):

    names = ["CV", "SA", "TA", "TS", "SV"]

    for name, feature_group in zip(names, features):

        missing = df[feature_group].isna().sum()
        missing_pct = round((missing/len(df)*100),3)      # Giving missing percentage of each columns

        print(f"\n{name}")
        print(missing_pct[missing_pct > 0].sort_values(ascending=False))

check_missing(
    df,
    cv_features,
    sa_features,
    ta_features,
    ts_features,
    sv_features
)
# Drop 2 features: ST8SV and ST68SV have 98.8% and 93.7% missing values
df = df.drop(columns=['ST8SV','ST68SV'])

# Update mri_features
mri_features = [col for col in mri_features if col not in ["ST8SV", "ST68SV"]]

print("Total of the features after dropping mising:", len(mri_features), "features") 
# Update
cv_features = [c for c in df.columns if c.endswith('CV')] # Cortical volume
sa_features = [c for c in df.columns if c.endswith('SA')] # Surface area
ta_features = [c for c in df.columns if c.endswith('TA')] # Mean cortical thickness
ts_features = [c for c in df.columns if c.endswith('TS')] # Cortical thickness standard deviation
sv_features = [c for c in df.columns if c.endswith('SV')] # Subcortical / aseg volume

print("CV:", len(cv_features))
print("SA:", len(sa_features))
print("TA:", len(ta_features))
print("TS:", len(ts_features))
print("SV:", len(sv_features))
