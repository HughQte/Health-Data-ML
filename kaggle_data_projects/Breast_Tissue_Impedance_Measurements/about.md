# **About Dataset**

## Breast Tissue Dataset
This dataset contains electrical impedance measurements of freshly excised tissue samples from the breast. The data is sourced from the UCI Machine Learning Repository.

### Dataset Characteristics
- Type: Multivariate
- Subject Area: Health and Medicine
- Associated Tasks: Classification
- Feature Type: Real
- Instances: 106
- Features: Various impedance measurements
### Dataset Information
Impedance measurements were taken at the following frequencies: 15.625, 31.25, 62.5, 125, 250, 500, and 1000 KHz. 
These measurements, when plotted in the (real, -imaginary) plane, constitute the impedance spectrum from which the breast tissue features are computed. 
The dataset can be used for predicting the classification of either the original 6 classes or of 4 classes by merging the fibro-adenoma, mastopathy, and glandular classes, which are hard to discriminate.

### Features
- I0: Impedivity (ohm) at zero frequency
- PA500: Phase angle at 500 KHz
- HFS: High-frequency slope of phase angle
- DA: Impedance distance between spectral ends
- AREA: Area under spectrum
- A/DA: Area normalized by DA
- MAX IP: Maximum of the spectrum
- DR: Distance between I0 and real part of the maximum frequency point
- P: Length of the spectral curve
- Class: Tissue type (carcinoma, fibro-adenoma, mastopathy, glandular, connective, adipose)
### Classes
- car: Carcinoma
- fad: Fibro-adenoma
- mas: Mastopathy
- gla: Glandular
- con: Connective
- adi: Adipose
### Usage
This dataset is suitable for classification tasks. The impedance measurements can be used to predict the type of breast tissue.

If you use this dataset, please cite it as follows:

S, JP and Jossinet, J. (2010). Breast Tissue. UCI Machine Learning Repository. https://doi.org/10.24432/C5P31H.

@misc{misc_breast_tissue_192,
author = "S, JP and Jossinet, J",
title = "Breast Tissue",
year = 2010,
howpublished = "UCI Machine Learning Repository",
note = "DOI: https://doi.org/10.24432/C5P31H"
}
