# ADNI Analysis-Ready Dataset Description

## 1. Source of data
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

Official ADNI references:
- ADNI data overview: https://adni.loni.usc.edu/data-samples/adni-data/
- ADNI MRI overview: https://adni.loni.usc.edu/data-samples/adni-data/neuroimaging/mri/
- ADNI data dictionary search: https://adni.loni.usc.edu/data-samples/data-dictionary-search/

## 2. Purpose of the data
The purpose of this merged dataset is to support exploratory data analysis
and machine-learning classification of three research groups:

- CN: cognitively normal;
- MCI: mild cognitive impairment;
- AD: Alzheimer's disease.

The table combines demographic, cognitive/functional, structural MRI
morphometry, and resting-state fMRI metadata so that these feature groups can
be compared or integrated in predictive models.

## 3. Cohort construction and important note
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

## 4. Current file summary
- Rows: **24,254**
- Columns: **343**
- Unique subjects: **4,562**

### Research-group counts by unique subject
- AD: **581** subjects
- CN: **1,431** subjects
- MCI: **1,674** subjects
- Unlabeled (`entry_research_group` missing): **876** subjects
- Rows with matched resting-state fMRI metadata: **735**
- FreeSurfer-derived ST features: **325**

## 5. Data dictionary

| Column | Feature group | Type | Description | Unit | Missing % |
|---|---|---|---|---|---:|
| `subject_id` | Identifier | object | ADNI participant identifier (e.g., 002_S_0295). | None | 0.00% |
| `visit` | Visit | object | Harmonized ADNI clinical visit code. Examples: bl = baseline, m06 = month 6, m12 = month 12. | None | 0.00% |
| `PTGENDER` | Demographic | float64 | Participant sex/gender code used by ADNI: 1 = Male, 2 = Female. | Categorical | 0.21% |
| `entry_age` | Demographic | float64 | Participant age at study entry/baseline. | Years | 0.21% |
| `entry_research_group` | Target / diagnosis | object | Derived three-class entry research-group label used in this project: CN, MCI, or AD. MCI combines original MCI, EMCI, and LMCI groups. | Categorical | 3.62% |
| `CDRSB` | Clinical / cognitive | float64 | Clinical Dementia Rating Sum of Boxes (CDR-SB); global functional/cognitive impairment score. Higher values indicate greater impairment. | Score | 41.29% |
| `TRAASCOR` | Clinical / cognitive | float64 | Trail Making Test Part A score, generally recorded as time to complete the task; larger values indicate slower performance. | Seconds / score | 48.23% |
| `TRABSCOR` | Clinical / cognitive | float64 | Trail Making Test Part B score, generally recorded as time to complete the task; larger values indicate slower performance. | Seconds / score | 49.71% |
| `LDELTOTAL` | Clinical / cognitive | float64 | Logical Memory delayed recall total score (LDELTOTAL); higher values generally indicate better delayed verbal memory. | Score | 49.82% |
| `MMSCORE` | Clinical / cognitive | float64 | Mini-Mental State Examination (MMSE) total score; typically 0-30, with lower values indicating greater cognitive impairment. | Score | 41.69% |
| `GDTOTAL` | Clinical / cognitive | float64 | Geriatric Depression Scale total score. | Score | 45.44% |
| `CATANIMSC` | Clinical / cognitive | float64 | Category Fluency - Animals total correct; number of animal names generated during the task. | Count / score | 47.81% |
| `FAQTOTAL` | Clinical / functional | float64 | Functional Activities Questionnaire (FAQ) total score; higher values indicate greater impairment in instrumental activities of daily living. | Score | 46.29% |
| `TOTAL13` | Clinical / cognitive | float64 | ADAS-Cog 13-item total score; higher values indicate greater cognitive impairment. | Score | 48.31% |
| `PHASE` | Study metadata | object | ADNI study phase associated with the matched imaging record (e.g., ADNI1, ADNIGO, ADNI2, ADNI3, ADNI4). | Categorical | 68.63% |
| `fmri_visit` | fMRI metadata | object | Visit code associated with the matched resting-state fMRI scan. | None | 96.97% |
| `fmri_description` | fMRI metadata | object | MRI series description for the resting-state functional MRI record. | Text | 96.97% |
| `fmri_tr` | fMRI metadata | float64 | Repetition time (TR) of the resting-state fMRI acquisition. | Milliseconds | 96.97% |
| `ST101SV` | Structural MRI / FreeSurfer | float64 | Subcortical / aseg volume of RightPallidum. | mm^3 | 68.70% |
| `ST102CV` | Structural MRI / FreeSurfer | float64 | Cortical volume of RightParacentral. | mm^3 | 69.43% |
| `ST102SA` | Structural MRI / FreeSurfer | float64 | Surface area of RightParacentral. | mm^2 | 69.43% |
| `ST102TA` | Structural MRI / FreeSurfer | float64 | Mean cortical thickness of RightParacentral. | mm | 69.43% |
| `ST102TS` | Structural MRI / FreeSurfer | float64 | Cortical thickness standard deviation of RightParacentral. | mm | 69.43% |
| `ST103CV` | Structural MRI / FreeSurfer | float64 | Cortical volume of RightParahippocampal. | mm^3 | 69.31% |
| `ST103SA` | Structural MRI / FreeSurfer | float64 | Surface area of RightParahippocampal. | mm^2 | 69.31% |
| `ST103TA` | Structural MRI / FreeSurfer | float64 | Mean cortical thickness of RightParahippocampal. | mm | 69.31% |
| `ST103TS` | Structural MRI / FreeSurfer | float64 | Cortical thickness standard deviation of RightParahippocampal. | mm | 69.31% |
| `ST104CV` | Structural MRI / FreeSurfer | float64 | Cortical volume of RightParsOpercularis. | mm^3 | 68.70% |
| `ST104SA` | Structural MRI / FreeSurfer | float64 | Surface area of RightParsOpercularis. | mm^2 | 68.70% |
| `ST104TA` | Structural MRI / FreeSurfer | float64 | Mean cortical thickness of RightParsOpercularis. | mm | 68.70% |
| `ST104TS` | Structural MRI / FreeSurfer | float64 | Cortical thickness standard deviation of RightParsOpercularis. | mm | 68.70% |
| `ST105CV` | Structural MRI / FreeSurfer | float64 | Cortical volume of RightParsOrbitalis. | mm^3 | 68.70% |
| `ST105SA` | Structural MRI / FreeSurfer | float64 | Surface area of RightParsOrbitalis. | mm^2 | 68.70% |
| `ST105TA` | Structural MRI / FreeSurfer | float64 | Mean cortical thickness of RightParsOrbitalis. | mm | 68.70% |
| `ST105TS` | Structural MRI / FreeSurfer | float64 | Cortical thickness standard deviation of RightParsOrbitalis. | mm | 68.70% |
| `ST106CV` | Structural MRI / FreeSurfer | float64 | Cortical volume of RightParsTriangularis. | mm^3 | 68.70% |
| `ST106SA` | Structural MRI / FreeSurfer | float64 | Surface area of RightParsTriangularis. | mm^2 | 68.70% |
| `ST106TA` | Structural MRI / FreeSurfer | float64 | Mean cortical thickness of RightParsTriangularis. | mm | 68.70% |
| `ST106TS` | Structural MRI / FreeSurfer | float64 | Cortical thickness standard deviation of RightParsTriangularis. | mm | 68.70% |
| `ST107CV` | Structural MRI / FreeSurfer | float64 | Cortical volume of RightPericalcarine. | mm^3 | 70.12% |
| `ST107SA` | Structural MRI / FreeSurfer | float64 | Surface area of RightPericalcarine. | mm^2 | 70.12% |
| `ST107TA` | Structural MRI / FreeSurfer | float64 | Mean cortical thickness of RightPericalcarine. | mm | 70.12% |
| `ST107TS` | Structural MRI / FreeSurfer | float64 | Cortical thickness standard deviation of RightPericalcarine. | mm | 70.12% |
| `ST108CV` | Structural MRI / FreeSurfer | float64 | Cortical volume of RightPostcentral. | mm^3 | 69.43% |
| `ST108SA` | Structural MRI / FreeSurfer | float64 | Surface area of RightPostcentral. | mm^2 | 69.43% |
| `ST108TA` | Structural MRI / FreeSurfer | float64 | Mean cortical thickness of RightPostcentral. | mm | 69.43% |
| `ST108TS` | Structural MRI / FreeSurfer | float64 | Cortical thickness standard deviation of RightPostcentral. | mm | 69.43% |
| `ST109CV` | Structural MRI / FreeSurfer | float64 | Cortical volume of RightPosteriorCingulate. | mm^3 | 68.70% |
| `ST109SA` | Structural MRI / FreeSurfer | float64 | Surface area of RightPosteriorCingulate. | mm^2 | 68.70% |
| `ST109TA` | Structural MRI / FreeSurfer | float64 | Mean cortical thickness of RightPosteriorCingulate. | mm | 68.70% |
| `ST109TS` | Structural MRI / FreeSurfer | float64 | Cortical thickness standard deviation of RightPosteriorCingulate. | mm | 68.70% |
| `ST10CV` | Structural MRI / FreeSurfer | float64 | Estimated intracranial volume (ICV) from the UCSF FreeSurfer output. | mm^3 | 68.66% |
| `ST110CV` | Structural MRI / FreeSurfer | float64 | Cortical volume of RightPrecentral. | mm^3 | 69.19% |
| `ST110SA` | Structural MRI / FreeSurfer | float64 | Surface area of RightPrecentral. | mm^2 | 69.19% |
| `ST110TA` | Structural MRI / FreeSurfer | float64 | Mean cortical thickness of RightPrecentral. | mm | 69.19% |
| `ST110TS` | Structural MRI / FreeSurfer | float64 | Cortical thickness standard deviation of RightPrecentral. | mm | 69.19% |
| `ST111CV` | Structural MRI / FreeSurfer | float64 | Cortical volume of RightPrecuneus. | mm^3 | 68.70% |
| `ST111SA` | Structural MRI / FreeSurfer | float64 | Surface area of RightPrecuneus. | mm^2 | 68.70% |
| `ST111TA` | Structural MRI / FreeSurfer | float64 | Mean cortical thickness of RightPrecuneus. | mm | 68.70% |
| `ST111TS` | Structural MRI / FreeSurfer | float64 | Cortical thickness standard deviation of RightPrecuneus. | mm | 68.70% |
| `ST112SV` | Structural MRI / FreeSurfer | float64 | Subcortical / aseg volume of RightPutamen. | mm^3 | 68.70% |
| `ST113CV` | Structural MRI / FreeSurfer | float64 | Cortical volume of RightRostralAnteriorCingulate. | mm^3 | 68.70% |
| `ST113SA` | Structural MRI / FreeSurfer | float64 | Surface area of RightRostralAnteriorCingulate. | mm^2 | 68.70% |
| `ST113TA` | Structural MRI / FreeSurfer | float64 | Mean cortical thickness of RightRostralAnteriorCingulate. | mm | 68.70% |
| `ST113TS` | Structural MRI / FreeSurfer | float64 | Cortical thickness standard deviation of RightRostralAnteriorCingulate. | mm | 68.70% |
| `ST114CV` | Structural MRI / FreeSurfer | float64 | Cortical volume of RightRostralMiddleFrontal. | mm^3 | 69.19% |
| `ST114SA` | Structural MRI / FreeSurfer | float64 | Surface area of RightRostralMiddleFrontal. | mm^2 | 69.19% |
| `ST114TA` | Structural MRI / FreeSurfer | float64 | Mean cortical thickness of RightRostralMiddleFrontal. | mm | 69.19% |
| `ST114TS` | Structural MRI / FreeSurfer | float64 | Cortical thickness standard deviation of RightRostralMiddleFrontal. | mm | 69.19% |
| `ST115CV` | Structural MRI / FreeSurfer | float64 | Cortical volume of RightSuperiorFrontal. | mm^3 | 69.19% |
| `ST115SA` | Structural MRI / FreeSurfer | float64 | Surface area of RightSuperiorFrontal. | mm^2 | 69.19% |
| `ST115TA` | Structural MRI / FreeSurfer | float64 | Mean cortical thickness of RightSuperiorFrontal. | mm | 69.19% |
| `ST115TS` | Structural MRI / FreeSurfer | float64 | Cortical thickness standard deviation of RightSuperiorFrontal. | mm | 69.19% |
| `ST116CV` | Structural MRI / FreeSurfer | float64 | Cortical volume of RightSuperiorParietal. | mm^3 | 69.43% |
| `ST116SA` | Structural MRI / FreeSurfer | float64 | Surface area of RightSuperiorParietal. | mm^2 | 69.43% |
| `ST116TA` | Structural MRI / FreeSurfer | float64 | Mean cortical thickness of RightSuperiorParietal. | mm | 69.43% |
| `ST116TS` | Structural MRI / FreeSurfer | float64 | Cortical thickness standard deviation of RightSuperiorParietal. | mm | 69.43% |
| `ST117CV` | Structural MRI / FreeSurfer | float64 | Cortical volume of RightSuperiorTemporal. | mm^3 | 69.59% |
| `ST117SA` | Structural MRI / FreeSurfer | float64 | Surface area of RightSuperiorTemporal. | mm^2 | 69.59% |
| `ST117TA` | Structural MRI / FreeSurfer | float64 | Mean cortical thickness of RightSuperiorTemporal. | mm | 69.59% |
| `ST117TS` | Structural MRI / FreeSurfer | float64 | Cortical thickness standard deviation of RightSuperiorTemporal. | mm | 69.59% |
| `ST118CV` | Structural MRI / FreeSurfer | float64 | Cortical volume of RightSupramarginal. | mm^3 | 69.43% |
| `ST118SA` | Structural MRI / FreeSurfer | float64 | Surface area of RightSupramarginal. | mm^2 | 69.43% |
| `ST118TA` | Structural MRI / FreeSurfer | float64 | Mean cortical thickness of RightSupramarginal. | mm | 69.43% |
| `ST118TS` | Structural MRI / FreeSurfer | float64 | Cortical thickness standard deviation of RightSupramarginal. | mm | 69.43% |
| `ST119CV` | Structural MRI / FreeSurfer | float64 | Cortical volume of RightTemporalPole. | mm^3 | 69.59% |
| `ST119SA` | Structural MRI / FreeSurfer | float64 | Surface area of RightTemporalPole. | mm^2 | 69.59% |
| `ST119TA` | Structural MRI / FreeSurfer | float64 | Mean cortical thickness of RightTemporalPole. | mm | 69.59% |
| `ST119TS` | Structural MRI / FreeSurfer | float64 | Cortical thickness standard deviation of RightTemporalPole. | mm | 69.59% |
| `ST11SV` | Structural MRI / FreeSurfer | float64 | Subcortical / aseg volume of LeftAccumbensArea. | mm^3 | 68.70% |
| `ST120SV` | Structural MRI / FreeSurfer | float64 | Subcortical / aseg volume of RightThalamus. | mm^3 | 68.70% |
| `ST121CV` | Structural MRI / FreeSurfer | float64 | Cortical volume of RightTransverseTemporal. | mm^3 | 68.70% |
| `ST121SA` | Structural MRI / FreeSurfer | float64 | Surface area of RightTransverseTemporal. | mm^2 | 68.70% |
| `ST121TA` | Structural MRI / FreeSurfer | float64 | Mean cortical thickness of RightTransverseTemporal. | mm | 68.70% |
| `ST121TS` | Structural MRI / FreeSurfer | float64 | Cortical thickness standard deviation of RightTransverseTemporal. | mm | 68.70% |
| `ST124SV` | Structural MRI / FreeSurfer | float64 | Subcortical / aseg volume of RightVentralDC. | mm^3 | 68.70% |
| `ST125SV` | Structural MRI / FreeSurfer | float64 | Subcortical / aseg volume of RightVessel. | mm^3 | 69.86% |
| `ST127SV` | Structural MRI / FreeSurfer | float64 | Subcortical / aseg volume of ThirdVentricle. | mm^3 | 68.76% |
| `ST128SV` | Structural MRI / FreeSurfer | float64 | Subcortical / aseg volume of WhiteMatterHypointensities. | mm^3 | 68.70% |
| `ST129CV` | Structural MRI / FreeSurfer | float64 | Cortical volume of LeftInsula. | mm^3 | 68.74% |
| `ST129SA` | Structural MRI / FreeSurfer | float64 | Surface area of LeftInsula. | mm^2 | 68.74% |
| `ST129TA` | Structural MRI / FreeSurfer | float64 | Mean cortical thickness of LeftInsula. | mm | 68.74% |
| `ST129TS` | Structural MRI / FreeSurfer | float64 | Cortical thickness standard deviation of LeftInsula. | mm | 68.74% |
| `ST12SV` | Structural MRI / FreeSurfer | float64 | Subcortical / aseg volume of LeftAmygdala. | mm^3 | 69.31% |
| `ST130CV` | Structural MRI / FreeSurfer | float64 | Cortical volume of RightInsula. | mm^3 | 68.74% |
| `ST130SA` | Structural MRI / FreeSurfer | float64 | Surface area of RightInsula. | mm^2 | 68.74% |
| `ST130TA` | Structural MRI / FreeSurfer | float64 | Mean cortical thickness of RightInsula. | mm | 68.74% |
| `ST130TS` | Structural MRI / FreeSurfer | float64 | Cortical thickness standard deviation of RightInsula. | mm | 68.74% |
| `ST13CV` | Structural MRI / FreeSurfer | float64 | Cortical volume of LeftBanksSTS. | mm^3 | 68.70% |
| `ST13SA` | Structural MRI / FreeSurfer | float64 | Surface area of LeftBanksSTS. | mm^2 | 68.70% |
| `ST13TA` | Structural MRI / FreeSurfer | float64 | Mean cortical thickness of LeftBanksSTS. | mm | 68.70% |
| `ST13TS` | Structural MRI / FreeSurfer | float64 | Cortical thickness standard deviation of LeftBanksSTS. | mm | 68.70% |
| `ST14CV` | Structural MRI / FreeSurfer | float64 | Cortical volume of LeftCaudalAnteriorCingulate. | mm^3 | 68.70% |
| `ST14SA` | Structural MRI / FreeSurfer | float64 | Surface area of LeftCaudalAnteriorCingulate. | mm^2 | 68.70% |
| `ST14TA` | Structural MRI / FreeSurfer | float64 | Mean cortical thickness of LeftCaudalAnteriorCingulate. | mm | 68.70% |
| `ST14TS` | Structural MRI / FreeSurfer | float64 | Cortical thickness standard deviation of LeftCaudalAnteriorCingulate. | mm | 68.70% |
| `ST15CV` | Structural MRI / FreeSurfer | float64 | Cortical volume of LeftCaudalMiddleFrontal. | mm^3 | 69.19% |
| `ST15SA` | Structural MRI / FreeSurfer | float64 | Surface area of LeftCaudalMiddleFrontal. | mm^2 | 69.19% |
| `ST15TA` | Structural MRI / FreeSurfer | float64 | Mean cortical thickness of LeftCaudalMiddleFrontal. | mm | 69.19% |
| `ST15TS` | Structural MRI / FreeSurfer | float64 | Cortical thickness standard deviation of LeftCaudalMiddleFrontal. | mm | 69.19% |
| `ST16SV` | Structural MRI / FreeSurfer | float64 | Subcortical / aseg volume of LeftCaudate. | mm^3 | 68.70% |
| `ST17SV` | Structural MRI / FreeSurfer | float64 | Subcortical / aseg volume of LeftCerebellumCortex. | mm^3 | 68.70% |
| `ST18SV` | Structural MRI / FreeSurfer | float64 | Subcortical / aseg volume of LeftCerebellumWhiteMatter. | mm^3 | 68.70% |
| `ST1SV` | Structural MRI / FreeSurfer | float64 | Subcortical / aseg volume of Brainstem. | mm^3 | 68.70% |
| `ST21SV` | Structural MRI / FreeSurfer | float64 | Subcortical / aseg volume of LeftChoroidPlexus. | mm^3 | 68.76% |
| `ST23CV` | Structural MRI / FreeSurfer | float64 | Cortical volume of LeftCuneus. | mm^3 | 70.12% |
| `ST23SA` | Structural MRI / FreeSurfer | float64 | Surface area of LeftCuneus. | mm^2 | 70.12% |
| `ST23TA` | Structural MRI / FreeSurfer | float64 | Mean cortical thickness of LeftCuneus. | mm | 70.12% |
| `ST23TS` | Structural MRI / FreeSurfer | float64 | Cortical thickness standard deviation of LeftCuneus. | mm | 70.12% |
| `ST24CV` | Structural MRI / FreeSurfer | float64 | Cortical volume of LeftEntorhinal. | mm^3 | 69.32% |
| `ST24SA` | Structural MRI / FreeSurfer | float64 | Surface area of LeftEntorhinal. | mm^2 | 69.32% |
| `ST24TA` | Structural MRI / FreeSurfer | float64 | Mean cortical thickness of LeftEntorhinal. | mm | 69.32% |
| `ST24TS` | Structural MRI / FreeSurfer | float64 | Cortical thickness standard deviation of LeftEntorhinal. | mm | 69.32% |
| `ST25CV` | Structural MRI / FreeSurfer | float64 | Cortical volume of LeftFrontalPole. | mm^3 | 69.19% |
| `ST25SA` | Structural MRI / FreeSurfer | float64 | Surface area of LeftFrontalPole. | mm^2 | 69.19% |
| `ST25TA` | Structural MRI / FreeSurfer | float64 | Mean cortical thickness of LeftFrontalPole. | mm | 69.19% |
| `ST25TS` | Structural MRI / FreeSurfer | float64 | Cortical thickness standard deviation of LeftFrontalPole. | mm | 69.19% |
| `ST26CV` | Structural MRI / FreeSurfer | float64 | Cortical volume of LeftFusiform. | mm^3 | 70.01% |
| `ST26SA` | Structural MRI / FreeSurfer | float64 | Surface area of LeftFusiform. | mm^2 | 70.01% |
| `ST26TA` | Structural MRI / FreeSurfer | float64 | Mean cortical thickness of LeftFusiform. | mm | 70.01% |
| `ST26TS` | Structural MRI / FreeSurfer | float64 | Cortical thickness standard deviation of LeftFusiform. | mm | 70.01% |
| `ST28SA` | Structural MRI / FreeSurfer | float64 | Surface area of LeftHemisphereWhiteMatter. | mm^2 | 68.81% |
| `ST29SV` | Structural MRI / FreeSurfer | float64 | Subcortical / aseg volume of LeftHippocampus. | mm^3 | 69.27% |
| `ST2SV` | Structural MRI / FreeSurfer | float64 | Subcortical / aseg volume of CorpusCallosumAnterior. | mm^3 | 68.70% |
| `ST30SV` | Structural MRI / FreeSurfer | float64 | Subcortical / aseg volume of LeftInferiorLateralVentricle. | mm^3 | 68.76% |
| `ST31CV` | Structural MRI / FreeSurfer | float64 | Cortical volume of LeftInferiorParietal. | mm^3 | 69.43% |
| `ST31SA` | Structural MRI / FreeSurfer | float64 | Surface area of LeftInferiorParietal. | mm^2 | 69.43% |
| `ST31TA` | Structural MRI / FreeSurfer | float64 | Mean cortical thickness of LeftInferiorParietal. | mm | 69.43% |
| `ST31TS` | Structural MRI / FreeSurfer | float64 | Cortical thickness standard deviation of LeftInferiorParietal. | mm | 69.43% |
| `ST32CV` | Structural MRI / FreeSurfer | float64 | Cortical volume of LeftInferiorTemporal. | mm^3 | 69.59% |
| `ST32SA` | Structural MRI / FreeSurfer | float64 | Surface area of LeftInferiorTemporal. | mm^2 | 69.59% |
| `ST32TA` | Structural MRI / FreeSurfer | float64 | Mean cortical thickness of LeftInferiorTemporal. | mm | 69.59% |
| `ST32TS` | Structural MRI / FreeSurfer | float64 | Cortical thickness standard deviation of LeftInferiorTemporal. | mm | 69.59% |
| `ST34CV` | Structural MRI / FreeSurfer | float64 | Cortical volume of LeftIsthmusCingulate. | mm^3 | 68.70% |
| `ST34SA` | Structural MRI / FreeSurfer | float64 | Surface area of LeftIsthmusCingulate. | mm^2 | 68.70% |
| `ST34TA` | Structural MRI / FreeSurfer | float64 | Mean cortical thickness of LeftIsthmusCingulate. | mm | 68.70% |
| `ST34TS` | Structural MRI / FreeSurfer | float64 | Cortical thickness standard deviation of LeftIsthmusCingulate. | mm | 68.70% |
| `ST35CV` | Structural MRI / FreeSurfer | float64 | Cortical volume of LeftLateralOccipital. | mm^3 | 70.12% |
| `ST35SA` | Structural MRI / FreeSurfer | float64 | Surface area of LeftLateralOccipital. | mm^2 | 70.12% |
| `ST35TA` | Structural MRI / FreeSurfer | float64 | Mean cortical thickness of LeftLateralOccipital. | mm | 70.12% |
| `ST35TS` | Structural MRI / FreeSurfer | float64 | Cortical thickness standard deviation of LeftLateralOccipital. | mm | 70.12% |
| `ST36CV` | Structural MRI / FreeSurfer | float64 | Cortical volume of LeftLateralOrbitofrontal. | mm^3 | 68.70% |
| `ST36SA` | Structural MRI / FreeSurfer | float64 | Surface area of LeftLateralOrbitofrontal. | mm^2 | 68.70% |
| `ST36TA` | Structural MRI / FreeSurfer | float64 | Mean cortical thickness of LeftLateralOrbitofrontal. | mm | 68.70% |
| `ST36TS` | Structural MRI / FreeSurfer | float64 | Cortical thickness standard deviation of LeftLateralOrbitofrontal. | mm | 68.70% |
| `ST37SV` | Structural MRI / FreeSurfer | float64 | Subcortical / aseg volume of LeftLateralVentricle. | mm^3 | 68.76% |
| `ST38CV` | Structural MRI / FreeSurfer | float64 | Cortical volume of LeftLingual. | mm^3 | 70.12% |
| `ST38SA` | Structural MRI / FreeSurfer | float64 | Surface area of LeftLingual. | mm^2 | 70.12% |
| `ST38TA` | Structural MRI / FreeSurfer | float64 | Mean cortical thickness of LeftLingual. | mm | 70.12% |
| `ST38TS` | Structural MRI / FreeSurfer | float64 | Cortical thickness standard deviation of LeftLingual. | mm | 70.12% |
| `ST39CV` | Structural MRI / FreeSurfer | float64 | Cortical volume of LeftMedialOrbitofrontal. | mm^3 | 69.19% |
| `ST39SA` | Structural MRI / FreeSurfer | float64 | Surface area of LeftMedialOrbitofrontal. | mm^2 | 69.19% |
| `ST39TA` | Structural MRI / FreeSurfer | float64 | Mean cortical thickness of LeftMedialOrbitofrontal. | mm | 69.19% |
| `ST39TS` | Structural MRI / FreeSurfer | float64 | Cortical thickness standard deviation of LeftMedialOrbitofrontal. | mm | 69.19% |
| `ST3SV` | Structural MRI / FreeSurfer | float64 | Subcortical / aseg volume of CorpusCallosumCentral. | mm^3 | 68.70% |
| `ST40CV` | Structural MRI / FreeSurfer | float64 | Cortical volume of LeftMiddleTemporal. | mm^3 | 69.59% |
| `ST40SA` | Structural MRI / FreeSurfer | float64 | Surface area of LeftMiddleTemporal. | mm^2 | 69.59% |
| `ST40TA` | Structural MRI / FreeSurfer | float64 | Mean cortical thickness of LeftMiddleTemporal. | mm | 69.59% |
| `ST40TS` | Structural MRI / FreeSurfer | float64 | Cortical thickness standard deviation of LeftMiddleTemporal. | mm | 69.59% |
| `ST42SV` | Structural MRI / FreeSurfer | float64 | Subcortical / aseg volume of LeftPallidum. | mm^3 | 68.70% |
| `ST43CV` | Structural MRI / FreeSurfer | float64 | Cortical volume of LeftParacentral. | mm^3 | 69.43% |
| `ST43SA` | Structural MRI / FreeSurfer | float64 | Surface area of LeftParacentral. | mm^2 | 69.43% |
| `ST43TA` | Structural MRI / FreeSurfer | float64 | Mean cortical thickness of LeftParacentral. | mm | 69.43% |
| `ST43TS` | Structural MRI / FreeSurfer | float64 | Cortical thickness standard deviation of LeftParacentral. | mm | 69.43% |
| `ST44CV` | Structural MRI / FreeSurfer | float64 | Cortical volume of LeftParahippocampal. | mm^3 | 69.31% |
| `ST44SA` | Structural MRI / FreeSurfer | float64 | Surface area of LeftParahippocampal. | mm^2 | 69.31% |
| `ST44TA` | Structural MRI / FreeSurfer | float64 | Mean cortical thickness of LeftParahippocampal. | mm | 69.31% |
| `ST44TS` | Structural MRI / FreeSurfer | float64 | Cortical thickness standard deviation of LeftParahippocampal. | mm | 69.31% |
| `ST45CV` | Structural MRI / FreeSurfer | float64 | Cortical volume of LeftParsOpercularis. | mm^3 | 68.70% |
| `ST45SA` | Structural MRI / FreeSurfer | float64 | Surface area of LeftParsOpercularis. | mm^2 | 68.70% |
| `ST45TA` | Structural MRI / FreeSurfer | float64 | Mean cortical thickness of LeftParsOpercularis. | mm | 68.70% |
| `ST45TS` | Structural MRI / FreeSurfer | float64 | Cortical thickness standard deviation of LeftParsOpercularis. | mm | 68.70% |
| `ST46CV` | Structural MRI / FreeSurfer | float64 | Cortical volume of LeftParsOrbitalis. | mm^3 | 68.70% |
| `ST46SA` | Structural MRI / FreeSurfer | float64 | Surface area of LeftParsOrbitalis. | mm^2 | 68.70% |
| `ST46TA` | Structural MRI / FreeSurfer | float64 | Mean cortical thickness of LeftParsOrbitalis. | mm | 68.70% |
| `ST46TS` | Structural MRI / FreeSurfer | float64 | Cortical thickness standard deviation of LeftParsOrbitalis. | mm | 68.70% |
| `ST47CV` | Structural MRI / FreeSurfer | float64 | Cortical volume of LeftParsTriangularis. | mm^3 | 68.70% |
| `ST47SA` | Structural MRI / FreeSurfer | float64 | Surface area of LeftParsTriangularis. | mm^2 | 68.70% |
| `ST47TA` | Structural MRI / FreeSurfer | float64 | Mean cortical thickness of LeftParsTriangularis. | mm | 68.70% |
| `ST47TS` | Structural MRI / FreeSurfer | float64 | Cortical thickness standard deviation of LeftParsTriangularis. | mm | 68.70% |
| `ST48CV` | Structural MRI / FreeSurfer | float64 | Cortical volume of LeftPericalcarine. | mm^3 | 70.12% |
| `ST48SA` | Structural MRI / FreeSurfer | float64 | Surface area of LeftPericalcarine. | mm^2 | 70.12% |
| `ST48TA` | Structural MRI / FreeSurfer | float64 | Mean cortical thickness of LeftPericalcarine. | mm | 70.12% |
| `ST48TS` | Structural MRI / FreeSurfer | float64 | Cortical thickness standard deviation of LeftPericalcarine. | mm | 70.12% |
| `ST49CV` | Structural MRI / FreeSurfer | float64 | Cortical volume of LeftPostcentral. | mm^3 | 69.43% |
| `ST49SA` | Structural MRI / FreeSurfer | float64 | Surface area of LeftPostcentral. | mm^2 | 69.43% |
| `ST49TA` | Structural MRI / FreeSurfer | float64 | Mean cortical thickness of LeftPostcentral. | mm | 69.43% |
| `ST49TS` | Structural MRI / FreeSurfer | float64 | Cortical thickness standard deviation of LeftPostcentral. | mm | 69.43% |
| `ST4SV` | Structural MRI / FreeSurfer | float64 | Subcortical / aseg volume of CorpusCallosumMidAnterior. | mm^3 | 68.70% |
| `ST50CV` | Structural MRI / FreeSurfer | float64 | Cortical volume of LeftPosteriorCingulate. | mm^3 | 68.70% |
| `ST50SA` | Structural MRI / FreeSurfer | float64 | Surface area of LeftPosteriorCingulate. | mm^2 | 68.70% |
| `ST50TA` | Structural MRI / FreeSurfer | float64 | Mean cortical thickness of LeftPosteriorCingulate. | mm | 68.70% |
| `ST50TS` | Structural MRI / FreeSurfer | float64 | Cortical thickness standard deviation of LeftPosteriorCingulate. | mm | 68.70% |
| `ST51CV` | Structural MRI / FreeSurfer | float64 | Cortical volume of LeftPrecentral. | mm^3 | 69.19% |
| `ST51SA` | Structural MRI / FreeSurfer | float64 | Surface area of LeftPrecentral. | mm^2 | 69.19% |
| `ST51TA` | Structural MRI / FreeSurfer | float64 | Mean cortical thickness of LeftPrecentral. | mm | 69.19% |
| `ST51TS` | Structural MRI / FreeSurfer | float64 | Cortical thickness standard deviation of LeftPrecentral. | mm | 69.19% |
| `ST52CV` | Structural MRI / FreeSurfer | float64 | Cortical volume of LeftPrecuneus. | mm^3 | 68.70% |
| `ST52SA` | Structural MRI / FreeSurfer | float64 | Surface area of LeftPrecuneus. | mm^2 | 68.70% |
| `ST52TA` | Structural MRI / FreeSurfer | float64 | Mean cortical thickness of LeftPrecuneus. | mm | 68.70% |
| `ST52TS` | Structural MRI / FreeSurfer | float64 | Cortical thickness standard deviation of LeftPrecuneus. | mm | 68.70% |
| `ST53SV` | Structural MRI / FreeSurfer | float64 | Subcortical / aseg volume of LeftPutamen. | mm^3 | 68.70% |
| `ST54CV` | Structural MRI / FreeSurfer | float64 | Cortical volume of LeftRostralAnteriorCingulate. | mm^3 | 68.70% |
| `ST54SA` | Structural MRI / FreeSurfer | float64 | Surface area of LeftRostralAnteriorCingulate. | mm^2 | 68.70% |
| `ST54TA` | Structural MRI / FreeSurfer | float64 | Mean cortical thickness of LeftRostralAnteriorCingulate. | mm | 68.70% |
| `ST54TS` | Structural MRI / FreeSurfer | float64 | Cortical thickness standard deviation of LeftRostralAnteriorCingulate. | mm | 68.70% |
| `ST55CV` | Structural MRI / FreeSurfer | float64 | Cortical volume of LeftRostralMiddleFrontal. | mm^3 | 69.19% |
| `ST55SA` | Structural MRI / FreeSurfer | float64 | Surface area of LeftRostralMiddleFrontal. | mm^2 | 69.19% |
| `ST55TA` | Structural MRI / FreeSurfer | float64 | Mean cortical thickness of LeftRostralMiddleFrontal. | mm | 69.19% |
| `ST55TS` | Structural MRI / FreeSurfer | float64 | Cortical thickness standard deviation of LeftRostralMiddleFrontal. | mm | 69.19% |
| `ST56CV` | Structural MRI / FreeSurfer | float64 | Cortical volume of LeftSuperiorFrontal. | mm^3 | 69.19% |
| `ST56SA` | Structural MRI / FreeSurfer | float64 | Surface area of LeftSuperiorFrontal. | mm^2 | 69.19% |
| `ST56TA` | Structural MRI / FreeSurfer | float64 | Mean cortical thickness of LeftSuperiorFrontal. | mm | 69.19% |
| `ST56TS` | Structural MRI / FreeSurfer | float64 | Cortical thickness standard deviation of LeftSuperiorFrontal. | mm | 69.19% |
| `ST57CV` | Structural MRI / FreeSurfer | float64 | Cortical volume of LeftSuperiorParietal. | mm^3 | 69.43% |
| `ST57SA` | Structural MRI / FreeSurfer | float64 | Surface area of LeftSuperiorParietal. | mm^2 | 69.43% |
| `ST57TA` | Structural MRI / FreeSurfer | float64 | Mean cortical thickness of LeftSuperiorParietal. | mm | 69.43% |
| `ST57TS` | Structural MRI / FreeSurfer | float64 | Cortical thickness standard deviation of LeftSuperiorParietal. | mm | 69.43% |
| `ST58CV` | Structural MRI / FreeSurfer | float64 | Cortical volume of LeftSuperiorTemporal. | mm^3 | 69.59% |
| `ST58SA` | Structural MRI / FreeSurfer | float64 | Surface area of LeftSuperiorTemporal. | mm^2 | 69.59% |
| `ST58TA` | Structural MRI / FreeSurfer | float64 | Mean cortical thickness of LeftSuperiorTemporal. | mm | 69.59% |
| `ST58TS` | Structural MRI / FreeSurfer | float64 | Cortical thickness standard deviation of LeftSuperiorTemporal. | mm | 69.59% |
| `ST59CV` | Structural MRI / FreeSurfer | float64 | Cortical volume of LeftSupramarginal. | mm^3 | 69.43% |
| `ST59SA` | Structural MRI / FreeSurfer | float64 | Surface area of LeftSupramarginal. | mm^2 | 69.43% |
| `ST59TA` | Structural MRI / FreeSurfer | float64 | Mean cortical thickness of LeftSupramarginal. | mm | 69.43% |
| `ST59TS` | Structural MRI / FreeSurfer | float64 | Cortical thickness standard deviation of LeftSupramarginal. | mm | 69.43% |
| `ST5SV` | Structural MRI / FreeSurfer | float64 | Subcortical / aseg volume of CorpusCallosumMidPosterior. | mm^3 | 68.70% |
| `ST60CV` | Structural MRI / FreeSurfer | float64 | Cortical volume of LeftTemporalPole. | mm^3 | 69.59% |
| `ST60SA` | Structural MRI / FreeSurfer | float64 | Surface area of LeftTemporalPole. | mm^2 | 69.59% |
| `ST60TA` | Structural MRI / FreeSurfer | float64 | Mean cortical thickness of LeftTemporalPole. | mm | 69.59% |
| `ST60TS` | Structural MRI / FreeSurfer | float64 | Cortical thickness standard deviation of LeftTemporalPole. | mm | 69.59% |
| `ST61SV` | Structural MRI / FreeSurfer | float64 | Subcortical / aseg volume of LeftThalamus. | mm^3 | 68.70% |
| `ST62CV` | Structural MRI / FreeSurfer | float64 | Cortical volume of LeftTransverseTemporal. | mm^3 | 68.70% |
| `ST62SA` | Structural MRI / FreeSurfer | float64 | Surface area of LeftTransverseTemporal. | mm^2 | 68.70% |
| `ST62TA` | Structural MRI / FreeSurfer | float64 | Mean cortical thickness of LeftTransverseTemporal. | mm | 68.70% |
| `ST62TS` | Structural MRI / FreeSurfer | float64 | Cortical thickness standard deviation of LeftTransverseTemporal. | mm | 68.70% |
| `ST65SV` | Structural MRI / FreeSurfer | float64 | Subcortical / aseg volume of LeftVentralDC. | mm^3 | 68.70% |
| `ST66SV` | Structural MRI / FreeSurfer | float64 | Subcortical / aseg volume of LeftVessel. | mm^3 | 69.52% |
| `ST68SV` | Structural MRI / FreeSurfer | float64 | Subcortical / aseg volume of NonWhiteMatterHypointensities. | mm^3 | 97.71% |
| `ST69SV` | Structural MRI / FreeSurfer | float64 | Subcortical / aseg volume of OpticChiasm. | mm^3 | 68.70% |
| `ST6SV` | Structural MRI / FreeSurfer | float64 | Subcortical / aseg volume of CorpusCallosumPosterior. | mm^3 | 68.70% |
| `ST70SV` | Structural MRI / FreeSurfer | float64 | Subcortical / aseg volume of RightAccumbensArea. | mm^3 | 68.70% |
| `ST71SV` | Structural MRI / FreeSurfer | float64 | Subcortical / aseg volume of RightAmygdala. | mm^3 | 69.31% |
| `ST72CV` | Structural MRI / FreeSurfer | float64 | Cortical volume of RightBanksSTS. | mm^3 | 68.70% |
| `ST72SA` | Structural MRI / FreeSurfer | float64 | Surface area of RightBanksSTS. | mm^2 | 68.70% |
| `ST72TA` | Structural MRI / FreeSurfer | float64 | Mean cortical thickness of RightBanksSTS. | mm | 68.70% |
| `ST72TS` | Structural MRI / FreeSurfer | float64 | Cortical thickness standard deviation of RightBanksSTS. | mm | 68.70% |
| `ST73CV` | Structural MRI / FreeSurfer | float64 | Cortical volume of RightCaudalAnteriorCingulate. | mm^3 | 68.70% |
| `ST73SA` | Structural MRI / FreeSurfer | float64 | Surface area of RightCaudalAnteriorCingulate. | mm^2 | 68.70% |
| `ST73TA` | Structural MRI / FreeSurfer | float64 | Mean cortical thickness of RightCaudalAnteriorCingulate. | mm | 68.70% |
| `ST73TS` | Structural MRI / FreeSurfer | float64 | Cortical thickness standard deviation of RightCaudalAnteriorCingulate. | mm | 68.70% |
| `ST74CV` | Structural MRI / FreeSurfer | float64 | Cortical volume of RightCaudalMiddleFrontal. | mm^3 | 69.19% |
| `ST74SA` | Structural MRI / FreeSurfer | float64 | Surface area of RightCaudalMiddleFrontal. | mm^2 | 69.19% |
| `ST74TA` | Structural MRI / FreeSurfer | float64 | Mean cortical thickness of RightCaudalMiddleFrontal. | mm | 69.19% |
| `ST74TS` | Structural MRI / FreeSurfer | float64 | Cortical thickness standard deviation of RightCaudalMiddleFrontal. | mm | 69.19% |
| `ST75SV` | Structural MRI / FreeSurfer | float64 | Subcortical / aseg volume of RightCaudate. | mm^3 | 68.70% |
| `ST76SV` | Structural MRI / FreeSurfer | float64 | Subcortical / aseg volume of RightCerebellumCortex. | mm^3 | 68.70% |
| `ST77SV` | Structural MRI / FreeSurfer | float64 | Subcortical / aseg volume of RightCerebellumWhiteMatter. | mm^3 | 68.70% |
| `ST7SV` | Structural MRI / FreeSurfer | float64 | Subcortical / aseg volume of CSF. | mm^3 | 68.70% |
| `ST80SV` | Structural MRI / FreeSurfer | float64 | Subcortical / aseg volume of RightChoroidPlexus. | mm^3 | 68.76% |
| `ST82CV` | Structural MRI / FreeSurfer | float64 | Cortical volume of RightCuneus. | mm^3 | 70.12% |
| `ST82SA` | Structural MRI / FreeSurfer | float64 | Surface area of RightCuneus. | mm^2 | 70.12% |
| `ST82TA` | Structural MRI / FreeSurfer | float64 | Mean cortical thickness of RightCuneus. | mm | 70.12% |
| `ST82TS` | Structural MRI / FreeSurfer | float64 | Cortical thickness standard deviation of RightCuneus. | mm | 70.12% |
| `ST83CV` | Structural MRI / FreeSurfer | float64 | Cortical volume of RightEntorhinal. | mm^3 | 69.31% |
| `ST83SA` | Structural MRI / FreeSurfer | float64 | Surface area of RightEntorhinal. | mm^2 | 69.31% |
| `ST83TA` | Structural MRI / FreeSurfer | float64 | Mean cortical thickness of RightEntorhinal. | mm | 69.31% |
| `ST83TS` | Structural MRI / FreeSurfer | float64 | Cortical thickness standard deviation of RightEntorhinal. | mm | 69.31% |
| `ST84CV` | Structural MRI / FreeSurfer | float64 | Cortical volume of RightFrontalPole. | mm^3 | 69.19% |
| `ST84SA` | Structural MRI / FreeSurfer | float64 | Surface area of RightFrontalPole. | mm^2 | 69.19% |
| `ST84TA` | Structural MRI / FreeSurfer | float64 | Mean cortical thickness of RightFrontalPole. | mm | 69.19% |
| `ST84TS` | Structural MRI / FreeSurfer | float64 | Cortical thickness standard deviation of RightFrontalPole. | mm | 69.19% |
| `ST85CV` | Structural MRI / FreeSurfer | float64 | Cortical volume of RightFusiform. | mm^3 | 70.01% |
| `ST85SA` | Structural MRI / FreeSurfer | float64 | Surface area of RightFusiform. | mm^2 | 70.01% |
| `ST85TA` | Structural MRI / FreeSurfer | float64 | Mean cortical thickness of RightFusiform. | mm | 70.01% |
| `ST85TS` | Structural MRI / FreeSurfer | float64 | Cortical thickness standard deviation of RightFusiform. | mm | 70.01% |
| `ST87sa` | Structural MRI / FreeSurfer | float64 | Surface area of RightHemisphereWhiteMatter. | mm^2 | 68.81% |
| `ST88SV` | Structural MRI / FreeSurfer | float64 | Subcortical / aseg volume of RightHippocampus. | mm^3 | 69.27% |
| `ST89SV` | Structural MRI / FreeSurfer | float64 | Subcortical / aseg volume of RightInferiorLateralVentricle. | mm^3 | 68.76% |
| `ST8SV` | Structural MRI / FreeSurfer | float64 | Subcortical / aseg volume of FifthVentricle. | mm^3 | 99.67% |
| `ST90CV` | Structural MRI / FreeSurfer | float64 | Cortical volume of RightInferiorParietal. | mm^3 | 69.43% |
| `ST90SA` | Structural MRI / FreeSurfer | float64 | Surface area of RightInferiorParietal. | mm^2 | 69.43% |
| `ST90TA` | Structural MRI / FreeSurfer | float64 | Mean cortical thickness of RightInferiorParietal. | mm | 69.43% |
| `ST90TS` | Structural MRI / FreeSurfer | float64 | Cortical thickness standard deviation of RightInferiorParietal. | mm | 69.43% |
| `ST91CV` | Structural MRI / FreeSurfer | float64 | Cortical volume of RightInferiorTemporal. | mm^3 | 69.59% |
| `ST91SA` | Structural MRI / FreeSurfer | float64 | Surface area of RightInferiorTemporal. | mm^2 | 69.59% |
| `ST91TA` | Structural MRI / FreeSurfer | float64 | Mean cortical thickness of RightInferiorTemporal. | mm | 69.59% |
| `ST91TS` | Structural MRI / FreeSurfer | float64 | Cortical thickness standard deviation of RightInferiorTemporal. | mm | 69.59% |
| `ST93CV` | Structural MRI / FreeSurfer | float64 | Cortical volume of RightIsthmusCingulate. | mm^3 | 68.70% |
| `ST93SA` | Structural MRI / FreeSurfer | float64 | Surface area of RightIsthmusCingulate. | mm^2 | 68.70% |
| `ST93TA` | Structural MRI / FreeSurfer | float64 | Mean cortical thickness of RightIsthmusCingulate. | mm | 68.70% |
| `ST93TS` | Structural MRI / FreeSurfer | float64 | Cortical thickness standard deviation of RightIsthmusCingulate. | mm | 68.70% |
| `ST94CV` | Structural MRI / FreeSurfer | float64 | Cortical volume of RightLateralOccipital. | mm^3 | 70.12% |
| `ST94SA` | Structural MRI / FreeSurfer | float64 | Surface area of RightLateralOccipital. | mm^2 | 70.12% |
| `ST94TA` | Structural MRI / FreeSurfer | float64 | Mean cortical thickness of RightLateralOccipital. | mm | 70.12% |
| `ST94TS` | Structural MRI / FreeSurfer | float64 | Cortical thickness standard deviation of RightLateralOccipital. | mm | 70.12% |
| `ST95CV` | Structural MRI / FreeSurfer | float64 | Cortical volume of RightLateralOrbitofrontal. | mm^3 | 68.70% |
| `ST95SA` | Structural MRI / FreeSurfer | float64 | Surface area of RightLateralOrbitofrontal. | mm^2 | 68.70% |
| `ST95TA` | Structural MRI / FreeSurfer | float64 | Mean cortical thickness of RightLateralOrbitofrontal. | mm | 68.70% |
| `ST95TS` | Structural MRI / FreeSurfer | float64 | Cortical thickness standard deviation of RightLateralOrbitofrontal. | mm | 68.70% |
| `ST96SV` | Structural MRI / FreeSurfer | float64 | Subcortical / aseg volume of RightLateralVentricle. | mm^3 | 68.76% |
| `ST97CV` | Structural MRI / FreeSurfer | float64 | Cortical volume of RightLingual. | mm^3 | 70.12% |
| `ST97SA` | Structural MRI / FreeSurfer | float64 | Surface area of RightLingual. | mm^2 | 70.12% |
| `ST97TA` | Structural MRI / FreeSurfer | float64 | Mean cortical thickness of RightLingual. | mm | 70.12% |
| `ST97TS` | Structural MRI / FreeSurfer | float64 | Cortical thickness standard deviation of RightLingual. | mm | 70.12% |
| `ST98CV` | Structural MRI / FreeSurfer | float64 | Cortical volume of RightMedialOrbitofrontal. | mm^3 | 69.19% |
| `ST98SA` | Structural MRI / FreeSurfer | float64 | Surface area of RightMedialOrbitofrontal. | mm^2 | 69.19% |
| `ST98TA` | Structural MRI / FreeSurfer | float64 | Mean cortical thickness of RightMedialOrbitofrontal. | mm | 69.19% |
| `ST98TS` | Structural MRI / FreeSurfer | float64 | Cortical thickness standard deviation of RightMedialOrbitofrontal. | mm | 69.19% |
| `ST99CV` | Structural MRI / FreeSurfer | float64 | Cortical volume of RightMiddleTemporal. | mm^3 | 69.59% |
| `ST99SA` | Structural MRI / FreeSurfer | float64 | Surface area of RightMiddleTemporal. | mm^2 | 69.59% |
| `ST99TA` | Structural MRI / FreeSurfer | float64 | Mean cortical thickness of RightMiddleTemporal. | mm | 69.59% |
| `ST99TS` | Structural MRI / FreeSurfer | float64 | Cortical thickness standard deviation of RightMiddleTemporal. | mm | 69.59% |
| `ST9SV` | Structural MRI / FreeSurfer | float64 | Subcortical / aseg volume of FourthVentricle. | mm^3 | 68.76% |
| `ST147SV` | Structural MRI / FreeSurfer | float64 | FreeSurfer aseg-derived volume of LeftCorticalGrayMatter. | mm^3 | 68.70% |
| `ST148SV` | Structural MRI / FreeSurfer | float64 | FreeSurfer aseg-derived volume of RightCorticalGrayMatter. | mm^3 | 68.70% |
| `ST149SV` | Structural MRI / FreeSurfer | float64 | FreeSurfer aseg-derived volume of TotalCorticalGrayMatter. | mm^3 | 68.70% |
| `ST150SV` | Structural MRI / FreeSurfer | float64 | FreeSurfer aseg-derived volume of LeftCorticalWhiteMatter. | mm^3 | 68.81% |
| `ST151SV` | Structural MRI / FreeSurfer | float64 | FreeSurfer aseg-derived volume of RightCorticalWhiteMatter. | mm^3 | 68.81% |
| `ST152SV` | Structural MRI / FreeSurfer | float64 | FreeSurfer aseg-derived volume of TotalCorticalWhiteMatter. | mm^3 | 68.81% |
| `ST153SV` | Structural MRI / FreeSurfer | float64 | FreeSurfer aseg-derived volume of SubcorticalGrayMatter. | mm^3 | 68.70% |
| `ST154SV` | Structural MRI / FreeSurfer | float64 | FreeSurfer aseg-derived volume of TotalGrayMatter. | mm^3 | 68.70% |
| `ST155SV` | Structural MRI / FreeSurfer | float64 | FreeSurfer aseg-derived volume of SupratentorialVolume. | mm^3 | 68.70% |

## 6. FreeSurfer naming convention

Most structural MRI variables follow the UCSF/ADNI `ST<number><suffix>` convention:

- `CV` = cortical volume (mm³)
- `SA` = surface area (mm²)
- `TA` = average cortical thickness (mm)
- `TS` = cortical thickness standard deviation (mm)
- `SV` = subcortical/aseg volume (mm³)

Examples:
- `ST29SV` = left hippocampal volume
- `ST88SV` = right hippocampal volume
- `ST24TA` = mean left entorhinal cortical thickness
- `ST83TA` = mean right entorhinal cortical thickness
- `ST10CV` = estimated intracranial volume (ICV)

The ST codes should be interpreted according to the UCSF FreeSurfer data dictionary corresponding to the ADNI FreeSurfer release used in the project.