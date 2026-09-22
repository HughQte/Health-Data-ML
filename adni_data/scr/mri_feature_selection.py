# ADNI FreeSurfer MRI Feature Selection
# Goal is to select from 323 to 30 features -> MRI classification models
# Import working libraries
import os
import warnings
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer
from sklearn.feature_selection import f_classif
from statsmodels.stats.multitest import multipletests
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegressionCV
from sklearn.model_selection import StratifiedKFold
from sklearn.feature_selection import mutual_info_classif

# 1. Unsupervised feature selection:
# Selecting based on high correlation features 
def correlation_filter(df, features, threshold=0.70): # Set up threshold

    # Correlation matrix
    corr = df[features].corr().abs()

    # Keep only upper triangle
    upper = corr.where(np.triu(np.ones(corr.shape),k=1).astype(bool))

    # Features to drop
    to_drop = [col for col in upper.columns if (upper[col] > threshold).any()]

    # Features to keep
    keep = [col for col in features if col not in to_drop]

    return keep, to_drop

cv_keep, cv_drop = correlation_filter(df, cv_features)
sa_keep, sa_drop = correlation_filter(df, sa_features)
ta_keep, ta_drop = correlation_filter(df, ta_features)
ts_keep, ts_drop = correlation_filter(df, ts_features)
sv_keep, sv_drop = correlation_filter(df, sv_features)

# Put keep features and meta data in a temp df_clean table
keep_features = (cv_keep + sa_keep + ta_keep + ts_keep + sv_keep)

# New MRI table after correlation filtering
df_clean = df[meta_cols + keep_features].copy()

print(df_clean.shape)
print("MRI features:", len(keep_features))

# Merged df_clean with data set with labeled (AD/MCI/CN)
# Open entry_research_group table 
entry = pd.read_csv("../data/All_Subjects_Study_Entry_17Sep2026.csv") 

# Join entry and df1_clean
label = pd.merge(entry, df_clean, left_on = ['subject_id'], right_on= ['PTID'], how='inner')
print("PTID unique:",label['PTID'].nunique())
print("subject_id unique:",label['subject_id'].nunique())

# Combine EMCI and LMCI = MCI
label['entry_research_group'] = label["entry_research_group"].replace({
    'EMCI': 'MCI',
    'LMCI': 'MCI'
})

# Select only AD, CN, and MCI
label = label[label['entry_research_group'].isin(['CN', 'MCI', 'AD'])].copy()

# 2. Supervised Feature Selection
# Select feautures and target to be ready for the supervised feature selection
X = label[keep_features].copy()
y = label['entry_research_group']

# Train/split
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    stratify=y,
    random_state=42
)

# Handling missing values in X
imputer = SimpleImputer(strategy="median")

X_train_imp = pd.DataFrame(
    imputer.fit_transform(X_train),
    columns=X_train.columns,
    index=X_train.index
)

X_test_imp = pd.DataFrame(
    imputer.transform(X_test),
    columns=X_test.columns,
    index=X_test.index
)

# Performing ANOVA
f_scores, p_values = f_classif(
    X_train_imp,
    y_train
)

anova_results = pd.DataFrame({
    "feature": X_train_imp.columns,
    "F_score": f_scores,
    "p_value": p_values
})

anova_results = (
    anova_results
    .sort_values("F_score", ascending=False)
    .reset_index(drop=True)
)
# multiple-testing correction
anova_results["p_fdr"] = multipletests(
    anova_results["p_value"],
    method="fdr_bh"
)[1]

anova_results["significant_fdr"] = (
    anova_results["p_fdr"] < 0.05
)

print(anova_results.head(30),'\n')

print(anova_results["significant_fdr"].value_counts(),'\n')

print(
    "FDR-significant features:",
    anova_results["significant_fdr"].sum()

# For LASSO, first standardize:
scaler = StandardScaler()

X_train_scaled = pd.DataFrame(
    scaler.fit_transform(X_train_imp),
    columns=X_train_imp.columns,
    index=X_train_imp.index
)

X_test_scaled = pd.DataFrame(
    scaler.transform(X_test_imp),
    columns=X_test_imp.columns,
    index=X_test_imp.index
)

cv = StratifiedKFold(
    n_splits=5,
    shuffle=True,
    random_state=42
)

lasso = LogisticRegressionCV(
    Cs=np.logspace(-3, 2, 20),
    cv=cv,
    penalty="l1",
    solver="saga",
    class_weight="balanced",
    scoring="balanced_accuracy",
    max_iter=10000,
    n_jobs=-1,
    random_state=42
)

lasso.fit(X_train_scaled, y_train)

coef_df = pd.DataFrame(
    lasso.coef_,
    index=lasso.classes_,
    columns=X_train_scaled.columns
)

selected_mask = (coef_df.abs().max(axis=0) > 1e-8)

lasso_selected = coef_df.columns[selected_mask].tolist()

lasso_results = pd.DataFrame({
    "feature": coef_df.columns,
    "max_abs_coef": coef_df.abs().max(axis=0),
    "selected": selected_mask
})

lasso_results = (lasso_results
    .sort_values("max_abs_coef", ascending=False)
    .reset_index(drop=True)
)

# MI
mi_scores = mutual_info_classif(
    X_train_imp,
    y_train,
    random_state=42
)

mi_results = pd.DataFrame({
    "feature": X_train_imp.columns,
    "MI_score": mi_scores
})

mi_results = (
    mi_results
    .sort_values("MI_score", ascending=False)
    .reset_index(drop=True)
)

# Combine ANOVA + MI + LASSO into one consensus table:
# Add ranks within each method
# ANOVA: higher F-score = better
anova_results["ANOVA_rank"] = (
    anova_results["F_score"]
    .rank(ascending=False, method="min")
)

# Mutual Information: higher MI = better
mi_results["MI_rank"] = (
    mi_results["MI_score"]
    .rank(ascending=False, method="min")
)

# LASSO: larger absolute coefficient = stronger
lasso_results["LASSO_rank"] = (
    lasso_results["max_abs_coef"]
    .rank(ascending=False, method="min")
)

# Merge the three result tables
feature_compare = (
    anova_results[
        ["feature", "F_score", "p_value", "p_fdr", "ANOVA_rank"]
    ]
    .merge(
        mi_results[
            ["feature", "MI_score", "MI_rank"]
        ],
        on="feature",
        how="inner"
    )
    .merge(
        lasso_results[
            [
                "feature",
                "max_abs_coef",
                "selected",
                "LASSO_rank"
            ]
        ],
        on="feature",
        how="inner"
    )
)

# Add MRI Family
def get_family(feature):
    for fam in ["CV", "SA", "TA", "TS", "SV"]:
        if feature.endswith(fam):
            return fam
    return "Other"

feature_compare["family"] = (
    feature_compare["feature"]
    .apply(get_family)
)

# Convert ranks to percentile ranks
n_features = len(feature_compare)

feature_compare["ANOVA_pct"] = (
    feature_compare["ANOVA_rank"] / n_features
)

feature_compare["MI_pct"] = (
    feature_compare["MI_rank"] / n_features
)

feature_compare["LASSO_pct"] = (
    feature_compare["LASSO_rank"] / n_features
)

