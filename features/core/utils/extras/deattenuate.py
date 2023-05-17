import extinction
import numpy as np
from astropy.cosmology import WMAP5


def lsst(flux: np.ndarray, error: np.ndarray, band: np.ndarray, mwebv: float, zhost: float):
    """Modifies flux and error inplace"""
    zhost = zhost if zhost >= 0.003 else 0
    z_deatt = 10 ** (-(WMAP5.distmod(0.3).to("mag").value - WMAP5.distmod(zhost).to("mag")) / 2.5) if zhost else 1

    rv = 3.1
    av = rv * mwebv

    wavelengths = {  # ¿Central? Wavelength (in Angstroms) for each band
        "u": 3671.,
        "g": 4827.,
        "r": 6223.,
        "i": 7546.,
        "z": 8691.,
        "Y": 9712.,
    }

    for fid in np.unique(band):
        mask = band == fid
        dust_deatt, = 10 ** (extinction.odonnell94(np.full(1, wavelengths[band]), av, rv) / 2.5)

        flux[mask] *= z_deatt * dust_deatt
        error[mask] *= z_deatt * dust_deatt
