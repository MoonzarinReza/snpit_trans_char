# trans_char_codes

Light-curve fitting and photometric classification of simulated Roman supernovae (SN Ia vs. non-SN Ia).

## Overview

1. **`lc_fitting.ipynb`** fits each multi-band light curve with a Functional PCA (FPCA) template using `mpfit`. Each band is described by peak time, peak magnitude, and two FPCA coefficients (β₁, β₂). The fitted peak magnitudes are then converted to absolute magnitudes using the cosmology set in `config.py`.
2. **`classification_binary.ipynb`** trains a CatBoost classifier on the fitted features (per-band absolute magnitude, β₁, β₂, and photo-z). It reports results over repeated random splits and 5-fold stratified cross-validation, and produces feature-importance, confusion-matrix, ROC, and misclassification-vs-redshift plots.

## Files

| File | Description |
|---|---|
| `config.py` | Shared settings: bands, survey fields, input/output paths, fit options, cosmology, classifier settings |
| `lc_fitting.ipynb` | FPCA light-curve fitting and conversion to absolute magnitudes |
| `classification_binary.ipynb` | Binary SN Ia / non-SN Ia classification with CatBoost |
| `eigen_val.txt` | FPCA template: rest-frame phase (−10 to +40 d), mean curve, and eigenvectors FPC1–FPC4 (the fit uses the mean, FPC1, and FPC2) |
| `mpfit.py` | Levenberg–Marquardt least-squares solver |

## Requirements

Python 3.10, `numpy`, `scipy`, `pandas`, `matplotlib`, `astropy`, `sncosmo`, `scikit-learn`, `catboost`.

## Usage

1. Put the SNANA-format simulation files (`*HEAD.FITS*` / `*PHOT.FITS*` pairs) in the folder set by `sim_dir` in `config.py`. The simulations are not included in this repository.
2. Adjust `config.py` as needed.
3. Run `lc_fitting.ipynb`. It writes:
   - `Files/Output_Long.csv`: one row per SN–band fit
   - `Files/Output_Wide.csv`: one row per SN
   - `Files/Output_Final.csv`: one row per SN, with absolute magnitudes
4. Run `classification_binary.ipynb`. It reads `Output_Final.csv` and saves figures to `Figures/`.


