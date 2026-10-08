"""
config.py

Shared configuration for the Roman SN analysis notebooks.

  Global         : bands, survey fields, absolute-magnitude output path.
  Fitting        : FPCA template fit (mpfit) per SN per band (lc_fitting.ipynb).
                   Input   : HEAD/PHOT FITS pairs in `sim_dir`,
                             FPCA eigenvectors in `eigen_val_path`.
                   Outputs : long table (one row per SN-band), wide table
                             (one row per SN), per-band LC tables and plots.
  Cosmology      : astropy cosmology used to convert peak mags to absolute mags.
  Classification : CatBoost train/test split and cross-validation folds.


"""

from __future__ import annotations
from dataclasses import dataclass, field


@dataclass
class GlobalConfig:
    """Settings shared across all notebooks: bands, fields, and output files."""
    
    abs_mag_csv: str = "Files/Output_Final.csv"   # absolute peak magnitudes
    # --- bands / survey field ---
    bands: tuple[str, ...] = ('R', 'Z', 'Y', 'J', 'H', 'F')
    # Survey fields to keep (PHOT 'FIELD' column). Empty tuple = keep all.
    fields: tuple[str, ...] = () ## N_WIDE, S_WIDE, N_DEEP, S_DEEP
    fields: tuple[str, ...] = ()



@dataclass
class FittingConfig:
    """FPCA template fitting (mpfit) of Roman simulated light curves."""

    seed: int = 0

    # --- inputs ---
    sim_dir: str = "Sundial_Sims"                 # folder with *HEAD.FITS* / *PHOT.FITS* pairs
    head_pattern: str = "*HEAD.FITS*"
    eigen_val_path: str = "eigen_val.txt"         # FPCA eigenvectors: phase, vec0, vec1, vec2

    

    # --- data cuts ---
    min_point: int = 5                            # min points per band (and within fit phase window)
                        

    # --- fit behavior ---
    num_attempts: int = 1                        # random restarts per band
    jitter_time_first: float = 0.0               # t0 jitter (rest-frame days) for first band
    jitter_time_other: float = 0.0               # t0 jitter for remaining bands
    jitter_mag: float = 0.0                      # mag jitter  
    jitter_beta1: float = 0.0                    # First_FPCA_jitter
    jitter_beta2: float = 0.0                    # Second_FPCA_jitter             
    #max_mag_err: float=  0.5                     #   
                 
   
    # --- outputs ---
    tables_dir: str = "Tables"                    # per-SN per-band LC csvs
    plots_dir: str = "Plots"                      # per-SN fit plots
    long_csv: str = "Files/Output_Long.csv"       # one row per (SN, band)
    wide_csv: str = "Files/Output_Wide.csv"       # one row per SN
    



@dataclass
class CosmologyConfig:
    """Cosmology for absolute-magnitude conversion."""
    models: tuple[str, ...] = ("FlatLambdaCDM", "LambdaCDM", "FlatwCDM", "Flatw0waCDM")
    model: str = "FlatLambdaCDM"      # pick one of `models`
    H0: float = 70.0
    Om0: float = 0.3
    Ode0: float = 0.7        # used by LambdaCDM
    w0: float = -1.0         # used by FlatwCDM, Flatw0waCDM
    wa: float = 0.0          # used by Flatw0waCDM


    def build(self):
        """Return an astropy cosmology object from these settings."""
        
        from astropy import cosmology as c
        if self.model == "FlatLambdaCDM":
            return c.FlatLambdaCDM(H0=self.H0, Om0=self.Om0)
        if self.model == "LambdaCDM":
            return c.LambdaCDM(H0=self.H0, Om0=self.Om0, Ode0=self.Ode0)
        if self.model == "FlatwCDM":
            return c.FlatwCDM(H0=self.H0, Om0=self.Om0, w0=self.w0)
        if self.model == "Flatw0waCDM":
            return c.Flatw0waCDM(H0=self.H0, Om0=self.Om0,  w0=self.w0, wa=self.wa)
        raise ValueError(f"Unknown cosmology model: {self.model}")


@dataclass
class ClassificationConfig:
    """CatBoost classification"""
    seed: int = 42
    test_size: float = 0.2
    n_folds: int = 5
    figures_dir: str = "Figures"   
    


@dataclass
class AnalysisConfig:
    globals: GlobalConfig = field(default_factory=GlobalConfig)
    fitting: FittingConfig = field(default_factory=FittingConfig)
    cosmology: CosmologyConfig = field(default_factory=CosmologyConfig)
    classification: ClassificationConfig = field(default_factory=ClassificationConfig)


config = AnalysisConfig()
