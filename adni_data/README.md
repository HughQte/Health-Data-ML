***ADNI Data Used in This Project***
---
***Information About Data Use***

Dataset: _Alzheimer's Disease Neuroimaging Initiative (ADNI)_

ADNI is a longitudinal, multi-center observational study designed to support research on Alzheimer's disease (AD) and related cognitive impairment. The dataset includes clinical assessments, demographic information, structural MRI, functional MRI, PET imaging, biomarkers, and genetic data.

Website: https://adni.loni.usc.edu

ADNI data are available to approved researchers through the LONI Image and Data Archive (IDA). Participant-level ADNI data should not be redistributed through this repository.

**Project Objective**

The goal of this project is to explore whether clinical information and neuroimaging-derived features can be used to distinguish Alzheimer's disease from cognitively normal participants.

The project focuses on combining:

Clinical and demographic information
Structural MRI-derived brain measurements
Functional MRI information
Machine-learning methods for classification and exploratory analysis

The analysis is intended as a healthcare data science / machine-learning project and not as a clinical diagnostic tool.

***Data Files Used***
1. ucsf_fsx7.csv

Source: UCSF Cross-Sectional FreeSurfer 7.x analysis provided through ADNI.

This dataset contains structural MRI measurements generated using the FreeSurfer 7.x image-processing pipeline.

Examples of measurements include:

Cortical thickness
Cortical surface area
Regional brain volume
Subcortical structure volume
Intracranial volume
MRI quality-control information

This dataset provides quantitative structural brain features that can be used as predictors in statistical and machine-learning models.

In this project, FreeSurfer-derived features are used to investigate structural brain differences associated with Alzheimer's disease.

2. adni_all.csv

This is the combined tabular dataset used for the main data-analysis workflow.

It contains subject-level and visit-level information obtained from ADNI and prepared for analysis.

Depending on the analysis, variables may include:

Participant ID
Visit information
Diagnostic group
Age
Sex
Education
Clinical assessments
Cognitive test results
Other available participant characteristics

The dataset is used to create the analysis-ready cohort and provide the outcome labels and clinical variables needed for machine-learning analysis.

3. adni_fmri/

This directory contains selected functional MRI information used for the project.

ADNI functional MRI data provide measurements of spontaneous brain activity using BOLD imaging, including resting-state fMRI acquisitions.

The fMRI component can be used to investigate functional differences between cognitively normal participants and participants with Alzheimer's disease or cognitive impairment.

Potential derived features include:

Regional BOLD signal measurements
Functional connectivity
Network-level measurements
Region-to-region correlations
Other resting-state fMRI features

Raw imaging files are not redistributed through this GitHub repository.
