"""
ADNI merged dataset documentation generator.

Outputs
-------
1. ADNI_DATASET_DESCRIPTION.md
   - Source of data
   - Purpose
   - Cohort construction / selection notes
   - Dataset summary
   - Data dictionary

2. adni_data_dictionary.csv
   - One row per column with type, description, unit, missingness, and example

Usage
-----
python adni_data_dictionary.py merged_fmri.csv
"""

import sys
import re
import pandas as pd


# ============================================================
# 1. DATASET-LEVEL DOCUMENTATION
# ============================================================

DATA_SOURCE = """
This analysis-ready dataset was derived from the Alzheimer's Disease
Neuroimaging Initiative (ADNI), a longitudinal, multi-center observational
study designed to support research on Alzheimer's disease progression and
biomarker development.

The merged file combines selected information from:
- ADNI clinical/demographic and cognitive assessment data;
- UCSF cross-sectional FreeSurfer 7.x MRI-derived morphometric summaries;
- resting-state fMRI scan metadata.

ADNI data are distributed to approved researchers through the LONI
Image and Data Archive (IDA).
"""

DATA_PURPOSE = """
The purpose of this merged dataset is to support exploratory data analysis
and machine-learning classification of three research groups:

- CN: cognitively normal;
- MCI: mild cognitive impairment;
- AD: Alzheimer's disease.

The table combines demographic, cognitive/functional, structural MRI
morphometry, and resting-state fMRI metadata so that these feature groups can
be compared or integrated in predictive models.
"""

COHORT_NOTE = """
IMPORTANT: This is not an original/raw ADNI table. It is a researcher-created,
analysis-ready subset produced after filtering, recoding, and merging ADNI
files.

Cohort construction:
1. The intended labeled analytic cohort contains three research groups:
   CN, MCI, and AD.
2. The derived MCI class combines participants originally categorized as
   MCI, EMCI (early MCI), or LMCI (late MCI).
3. Some rows/subjects without an `entry_research_group` label may still be
   present because unmatched records were retained during merging. These
   unlabeled rows should not be used as target observations in supervised
   classification unless a valid label is recovered from the source data.
4. MRI/fMRI records were restricted upstream to magnetic field strength = 3T.
   Because magnetic field strength was used as a filtering criterion before
   the final merge, a `magnetic_field` column may not be present in this file.
5. `entry_research_group` represents the entry/baseline research-group label
   used for this analysis. It should not automatically be interpreted as the
   participant's diagnosis at every later longitudinal visit.
6. Unmatched longitudinal visits may remain in the merged table. Therefore,
   missing imaging values can indicate that no matching imaging record was
   available for that subject/visit rather than a measurement failure.
"""


# ============================================================
# 2. MANUAL DATA DICTIONARY FOR NON-FREESURFER VARIABLES
# ============================================================

MANUAL_DICTIONARY = {
    "subject_id": {
        "group": "Identifier",
        "description": "ADNI participant identifier (e.g., 002_S_0295).",
        "unit": "None",
    },
    "visit": {
        "group": "Visit",
        "description": (
            "Harmonized ADNI clinical visit code. Examples: bl = baseline, "
            "m06 = month 6, m12 = month 12."
        ),
        "unit": "None",
    },
    "PTGENDER": {
        "group": "Demographic",
        "description": "Participant sex/gender code used by ADNI: 1 = Male, 2 = Female.",
        "unit": "Categorical",
    },
    "entry_age": {
        "group": "Demographic",
        "description": "Participant age at study entry/baseline.",
        "unit": "Years",
    },
    "entry_research_group": {
        "group": "Target / diagnosis",
        "description": (
            "Derived three-class entry research-group label used in this project: "
            "CN, MCI, or AD. MCI combines original MCI, EMCI, and LMCI groups."
        ),
        "unit": "Categorical",
    },
    "CDRSB": {
        "group": "Clinical / cognitive",
        "description": (
            "Clinical Dementia Rating Sum of Boxes (CDR-SB); global functional/"
            "cognitive impairment score. Higher values indicate greater impairment."
        ),
        "unit": "Score",
    },
    "TRAASCOR": {
        "group": "Clinical / cognitive",
        "description": (
            "Trail Making Test Part A score, generally recorded as time to complete "
            "the task; larger values indicate slower performance."
        ),
        "unit": "Seconds / score",
    },
    "TRABSCOR": {
        "group": "Clinical / cognitive",
        "description": (
            "Trail Making Test Part B score, generally recorded as time to complete "
            "the task; larger values indicate slower performance."
        ),
        "unit": "Seconds / score",
    },
    "LDELTOTAL": {
        "group": "Clinical / cognitive",
        "description": (
            "Logical Memory delayed recall total score (LDELTOTAL); higher values "
            "generally indicate better delayed verbal memory."
        ),
        "unit": "Score",
    },
    "MMSCORE": {
        "group": "Clinical / cognitive",
        "description": (
            "Mini-Mental State Examination (MMSE) total score; typically 0-30, "
            "with lower values indicating greater cognitive impairment."
        ),
        "unit": "Score",
    },
    "GDTOTAL": {
        "group": "Clinical / cognitive",
        "description": "Geriatric Depression Scale total score.",
        "unit": "Score",
    },
    "CATANIMSC": {
        "group": "Clinical / cognitive",
        "description": (
            "Category Fluency - Animals total correct; number of animal names "
            "generated during the task."
        ),
        "unit": "Count / score",
    },
    "FAQTOTAL": {
        "group": "Clinical / functional",
        "description": (
            "Functional Activities Questionnaire (FAQ) total score; higher values "
            "indicate greater impairment in instrumental activities of daily living."
        ),
        "unit": "Score",
    },
    "TOTAL13": {
        "group": "Clinical / cognitive",
        "description": (
            "ADAS-Cog 13-item total score; higher values indicate greater "
            "cognitive impairment."
        ),
        "unit": "Score",
    },
    "PHASE": {
        "group": "Study metadata",
        "description": (
            "ADNI study phase associated with the matched imaging record "
            "(e.g., ADNI1, ADNIGO, ADNI2, ADNI3, ADNI4)."
        ),
        "unit": "Categorical",
    },
    "fmri_visit": {
        "group": "fMRI metadata",
        "description": "Visit code associated with the matched resting-state fMRI scan.",
        "unit": "None",
    },
    "fmri_description": {
        "group": "fMRI metadata",
        "description": "MRI series description for the resting-state functional MRI record.",
        "unit": "Text",
    },
    "fmri_tr": {
        "group": "fMRI metadata",
        "description": (
            "Repetition time (TR) of the resting-state fMRI acquisition."
        ),
        "unit": "Milliseconds",
    },
}


# ============================================================
# 3. FREESURFER REGION MAP
#    STxxx codes are ADNI/UCSF FreeSurfer summary variable names.
# ============================================================

ST_REGION_MAP = {
    1: "Brainstem",
    2: "CorpusCallosumAnterior",
    3: "CorpusCallosumCentral",
    4: "CorpusCallosumMidAnterior",
    5: "CorpusCallosumMidPosterior",
    6: "CorpusCallosumPosterior",
    7: "CSF",
    8: "FifthVentricle",
    9: "FourthVentricle",
    10: "IntracranialVolume",
    11: "LeftAccumbensArea",
    12: "LeftAmygdala",
    13: "LeftBanksSTS",
    14: "LeftCaudalAnteriorCingulate",
    15: "LeftCaudalMiddleFrontal",
    16: "LeftCaudate",
    17: "LeftCerebellumCortex",
    18: "LeftCerebellumWhiteMatter",
    21: "LeftChoroidPlexus",
    23: "LeftCuneus",
    24: "LeftEntorhinal",
    25: "LeftFrontalPole",
    26: "LeftFusiform",
    28: "LeftHemisphereWhiteMatter",
    29: "LeftHippocampus",
    30: "LeftInferiorLateralVentricle",
    31: "LeftInferiorParietal",
    32: "LeftInferiorTemporal",
    34: "LeftIsthmusCingulate",
    35: "LeftLateralOccipital",
    36: "LeftLateralOrbitofrontal",
    37: "LeftLateralVentricle",
    38: "LeftLingual",
    39: "LeftMedialOrbitofrontal",
    40: "LeftMiddleTemporal",
    42: "LeftPallidum",
    43: "LeftParacentral",
    44: "LeftParahippocampal",
    45: "LeftParsOpercularis",
    46: "LeftParsOrbitalis",
    47: "LeftParsTriangularis",
    48: "LeftPericalcarine",
    49: "LeftPostcentral",
    50: "LeftPosteriorCingulate",
    51: "LeftPrecentral",
    52: "LeftPrecuneus",
    53: "LeftPutamen",
    54: "LeftRostralAnteriorCingulate",
    55: "LeftRostralMiddleFrontal",
    56: "LeftSuperiorFrontal",
    57: "LeftSuperiorParietal",
    58: "LeftSuperiorTemporal",
    59: "LeftSupramarginal",
    60: "LeftTemporalPole",
    61: "LeftThalamus",
    62: "LeftTransverseTemporal",
    65: "LeftVentralDC",
    66: "LeftVessel",
    68: "NonWhiteMatterHypointensities",
    69: "OpticChiasm",
    70: "RightAccumbensArea",
    71: "RightAmygdala",
    72: "RightBanksSTS",
    73: "RightCaudalAnteriorCingulate",
    74: "RightCaudalMiddleFrontal",
    75: "RightCaudate",
    76: "RightCerebellumCortex",
    77: "RightCerebellumWhiteMatter",
    80: "RightChoroidPlexus",
    82: "RightCuneus",
    83: "RightEntorhinal",
    84: "RightFrontalPole",
    85: "RightFusiform",
    87: "RightHemisphereWhiteMatter",
    88: "RightHippocampus",
    89: "RightInferiorLateralVentricle",
    90: "RightInferiorParietal",
    91: "RightInferiorTemporal",
    93: "RightIsthmusCingulate",
    94: "RightLateralOccipital",
    95: "RightLateralOrbitofrontal",
    96: "RightLateralVentricle",
    97: "RightLingual",
    98: "RightMedialOrbitofrontal",
    99: "RightMiddleTemporal",
    101: "RightPallidum",
    102: "RightParacentral",
    103: "RightParahippocampal",
    104: "RightParsOpercularis",
    105: "RightParsOrbitalis",
    106: "RightParsTriangularis",
    107: "RightPericalcarine",
    108: "RightPostcentral",
    109: "RightPosteriorCingulate",
    110: "RightPrecentral",
    111: "RightPrecuneus",
    112: "RightPutamen",
    113: "RightRostralAnteriorCingulate",
    114: "RightRostralMiddleFrontal",
    115: "RightSuperiorFrontal",
    116: "RightSuperiorParietal",
    117: "RightSuperiorTemporal",
    118: "RightSupramarginal",
    119: "RightTemporalPole",
    120: "RightThalamus",
    121: "RightTransverseTemporal",
    124: "RightVentralDC",
    125: "RightVessel",
    127: "ThirdVentricle",
    128: "WhiteMatterHypointensities",
    129: "LeftInsula",
    130: "RightInsula",
    147: "LeftCorticalGrayMatter",
    148: "RightCorticalGrayMatter",
    149: "TotalCorticalGrayMatter",
    150: "LeftCorticalWhiteMatter",
    151: "RightCorticalWhiteMatter",
    152: "TotalCorticalWhiteMatter",
    153: "SubcorticalGrayMatter",
    154: "TotalGrayMatter",
    155: "SupratentorialVolume",
}

MEASURE_MAP = {
    "CV": ("Cortical volume", "mm^3"),
    "SA": ("Surface area", "mm^2"),
    "TA": ("Mean cortical thickness", "mm"),
    "TS": ("Cortical thickness standard deviation", "mm"),
    "SV": ("Subcortical / aseg volume", "mm^3"),
}


def describe_st_column(column_name):
    """
    Decode an ADNI/UCSF FreeSurfer ST variable.

    Examples
    --------
    ST29SV  -> Left hippocampal subcortical volume
    ST83TA  -> Mean cortical thickness of right entorhinal cortex
    ST10CV  -> Estimated intracranial volume
    """
    # Normalize occasional lower-case suffixes, e.g. ST87sa
    normalized = column_name.upper()

    match = re.fullmatch(r"ST(\d+)(CV|SA|TA|TS|SV)", normalized)
    if not match:
        return None

    region_number = int(match.group(1))
    suffix = match.group(2)

    region = ST_REGION_MAP.get(region_number)
    if region is None:
        return {
            "group": "Structural MRI / FreeSurfer",
            "description": "UCSF FreeSurfer-derived morphometric feature; see the official ADNI/UCSF FreeSurfer data dictionary.",
            "unit": MEASURE_MAP.get(suffix, ("Unknown", "Unknown"))[1],
        }

    # Special cases
    if region_number == 10:
        return {
            "group": "Structural MRI / FreeSurfer",
            "description": "Estimated intracranial volume (ICV) from the UCSF FreeSurfer output.",
            "unit": "mm^3",
        }

    if region_number in range(147, 156):
        return {
            "group": "Structural MRI / FreeSurfer",
            "description": f"FreeSurfer aseg-derived volume of {region}.",
            "unit": "mm^3",
        }

    measure_name, unit = MEASURE_MAP[suffix]

    return {
        "group": "Structural MRI / FreeSurfer",
        "description": f"{measure_name} of {region}.",
        "unit": unit,
    }


def safe_example(series):
    vals = series.dropna()
    if vals.empty:
        return ""
    value = vals.iloc[0]
    if isinstance(value, float):
        return round(value, 4)
    return str(value)


def build_data_dictionary(df):
    rows = []

    for column in df.columns:
        info = MANUAL_DICTIONARY.get(column)

        if info is None and column.upper().startswith("ST"):
            info = describe_st_column(column)

        if info is None:
            info = {
                "group": "Other / derived",
                "description": "Derived or merged variable; verify against the source table used to construct this dataset.",
                "unit": "Unknown",
            }

        rows.append({
            "column": column,
            "feature_group": info["group"],
            "dtype": str(df[column].dtype),
            "description": info["description"],
            "unit": info["unit"],
            "non_missing_n": int(df[column].notna().sum()),
            "missing_n": int(df[column].isna().sum()),
            "missing_percent": round(df[column].isna().mean() * 100, 2),
            "unique_values": int(df[column].nunique(dropna=True)),
            "example_value": safe_example(df[column]),
        })

    return pd.DataFrame(rows)


def make_markdown(df, dictionary):
    n_rows, n_cols = df.shape
    n_subjects = df["subject_id"].nunique() if "subject_id" in df else None

    lines = [
        "# ADNI Analysis-Ready Dataset Description",
        "",
        "## 1. Source of data",
        DATA_SOURCE.strip(),
        "",
        "Official ADNI references:",
        "- ADNI data overview: https://adni.loni.usc.edu/data-samples/adni-data/",
        "- ADNI MRI overview: https://adni.loni.usc.edu/data-samples/adni-data/neuroimaging/mri/",
        "- ADNI data dictionary search: https://adni.loni.usc.edu/data-samples/data-dictionary-search/",
        "",
        "## 2. Purpose of the data",
        DATA_PURPOSE.strip(),
        "",
        "## 3. Cohort construction and important note",
        COHORT_NOTE.strip(),
        "",
        "## 4. Current file summary",
        f"- Rows: **{n_rows:,}**",
        f"- Columns: **{n_cols:,}**",
    ]

    if n_subjects is not None:
        lines.append(f"- Unique subjects: **{n_subjects:,}**")

    if "entry_research_group" in df:
        lines.extend(["", "### Research-group counts by unique subject"])
        counts = (
            df.dropna(subset=["entry_research_group"])
              .groupby("entry_research_group")["subject_id"]
              .nunique()
              .sort_index()
        )
        for group, count in counts.items():
            lines.append(f"- {group}: **{count:,}** subjects")

        unlabeled_subjects = df.loc[
            df["entry_research_group"].isna(), "subject_id"
        ].nunique()
        if unlabeled_subjects:
            lines.append(
                f"- Unlabeled (`entry_research_group` missing): "
                f"**{unlabeled_subjects:,}** subjects"
            )

    if "fmri_description" in df:
        matched_fmri = int(df["fmri_description"].notna().sum())
        lines.append(f"- Rows with matched resting-state fMRI metadata: **{matched_fmri:,}**")

    st_columns = [c for c in df.columns if c.upper().startswith("ST")]
    lines.append(f"- FreeSurfer-derived ST features: **{len(st_columns):,}**")

    lines.extend([
        "",
        "## 5. Data dictionary",
        "",
        "| Column | Feature group | Type | Description | Unit | Missing % |",
        "|---|---|---|---|---|---:|",
    ])

    for _, row in dictionary.iterrows():
        description = str(row["description"]).replace("|", "/")
        lines.append(
            f"| `{row['column']}` | {row['feature_group']} | {row['dtype']} | "
            f"{description} | {row['unit']} | {row['missing_percent']:.2f}% |"
        )

    lines.extend([
        "",
        "## 6. FreeSurfer naming convention",
        "",
        "Most structural MRI variables follow the UCSF/ADNI `ST<number><suffix>` convention:",
        "",
        "- `CV` = cortical volume (mm³)",
        "- `SA` = surface area (mm²)",
        "- `TA` = average cortical thickness (mm)",
        "- `TS` = cortical thickness standard deviation (mm)",
        "- `SV` = subcortical/aseg volume (mm³)",
        "",
        "Examples:",
        "- `ST29SV` = left hippocampal volume",
        "- `ST88SV` = right hippocampal volume",
        "- `ST24TA` = mean left entorhinal cortical thickness",
        "- `ST83TA` = mean right entorhinal cortical thickness",
        "- `ST10CV` = estimated intracranial volume (ICV)",
        "",
        "The ST codes should be interpreted according to the UCSF FreeSurfer data dictionary "
        "corresponding to the ADNI FreeSurfer release used in the project.",
    ])

    return "\n".join(lines)


def main(input_csv):
    df = pd.read_csv(input_csv, low_memory=False)

    dictionary = build_data_dictionary(df)

    dictionary.to_csv("adni_data_dictionary.csv", index=False)

    markdown = make_markdown(df, dictionary)
    with open("ADNI_DATASET_DESCRIPTION.md", "w", encoding="utf-8") as f:
        f.write(markdown)

    print("Created:")
    print("  - adni_data_dictionary.csv")
    print("  - ADNI_DATASET_DESCRIPTION.md")
    print()
    print(f"Dataset shape: {df.shape[0]:,} rows x {df.shape[1]:,} columns")
    if "subject_id" in df:
        print(f"Unique subjects: {df['subject_id'].nunique():,}")


if __name__ == "__main__":
    input_csv = sys.argv[1] if len(sys.argv) > 1 else "merged_fmri.csv"
    main(input_csv)