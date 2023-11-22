from fastavro.utils import generate_one
import random


def _get_random_key(dictionary: dict):
    return random.choice(list(dictionary.keys()))


def features_elasticc(
    force_empty_features=False, force_missing_features=False
):
    FEATURES_SCHEMA = {
        "name": "features_record",
        "type": "record",
        "fields": [
            {"name": "Amplitude_Y", "type": ["float", "null"]},
            {"name": "Amplitude_g", "type": ["float", "null"]},
            {"name": "Amplitude_i", "type": ["float", "null"]},
            {"name": "Amplitude_r", "type": ["float", "null"]},
            {"name": "Amplitude_u", "type": ["float", "null"]},
            {"name": "Amplitude_z", "type": ["float", "null"]},
            {"name": "AndersonDarling_Y", "type": ["float", "null"]},
            {"name": "AndersonDarling_g", "type": ["float", "null"]},
            {"name": "AndersonDarling_i", "type": ["float", "null"]},
            {"name": "AndersonDarling_r", "type": ["float", "null"]},
            {"name": "AndersonDarling_u", "type": ["float", "null"]},
            {"name": "AndersonDarling_z", "type": ["float", "null"]},
            {"name": "Autocor_length_Y", "type": ["float", "null"]},
            {"name": "Autocor_length_g", "type": ["float", "null"]},
            {"name": "Autocor_length_i", "type": ["float", "null"]},
            {"name": "Autocor_length_r", "type": ["float", "null"]},
            {"name": "Autocor_length_u", "type": ["float", "null"]},
            {"name": "Autocor_length_z", "type": ["float", "null"]},
            {"name": "Beyond1Std_Y", "type": ["float", "null"]},
            {"name": "Beyond1Std_g", "type": ["float", "null"]},
            {"name": "Beyond1Std_i", "type": ["float", "null"]},
            {"name": "Beyond1Std_r", "type": ["float", "null"]},
            {"name": "Beyond1Std_u", "type": ["float", "null"]},
            {"name": "Beyond1Std_z", "type": ["float", "null"]},
            {"name": "Con_Y", "type": ["float", "null"]},
            {"name": "Con_g", "type": ["float", "null"]},
            {"name": "Con_i", "type": ["float", "null"]},
            {"name": "Con_r", "type": ["float", "null"]},
            {"name": "Con_u", "type": ["float", "null"]},
            {"name": "Con_z", "type": ["float", "null"]},
            {"name": "Eta_e_Y", "type": ["float", "null"]},
            {"name": "Eta_e_g", "type": ["float", "null"]},
            {"name": "Eta_e_i", "type": ["float", "null"]},
            {"name": "Eta_e_r", "type": ["float", "null"]},
            {"name": "Eta_e_u", "type": ["float", "null"]},
            {"name": "Eta_e_z", "type": ["float", "null"]},
            {"name": "ExcessVar_Y", "type": ["float", "null"]},
            {"name": "ExcessVar_g", "type": ["float", "null"]},
            {"name": "ExcessVar_i", "type": ["float", "null"]},
            {"name": "ExcessVar_r", "type": ["float", "null"]},
            {"name": "ExcessVar_u", "type": ["float", "null"]},
            {"name": "ExcessVar_z", "type": ["float", "null"]},
            {"name": "GP_DRW_sigma_Y", "type": ["float", "null"]},
            {"name": "GP_DRW_sigma_g", "type": ["float", "null"]},
            {"name": "GP_DRW_sigma_i", "type": ["float", "null"]},
            {"name": "GP_DRW_sigma_r", "type": ["float", "null"]},
            {"name": "GP_DRW_sigma_u", "type": ["float", "null"]},
            {"name": "GP_DRW_sigma_z", "type": ["float", "null"]},
            {"name": "GP_DRW_tau_Y", "type": ["float", "null"]},
            {"name": "GP_DRW_tau_g", "type": ["float", "null"]},
            {"name": "GP_DRW_tau_i", "type": ["float", "null"]},
            {"name": "GP_DRW_tau_r", "type": ["float", "null"]},
            {"name": "GP_DRW_tau_u", "type": ["float", "null"]},
            {"name": "GP_DRW_tau_z", "type": ["float", "null"]},
            {"name": "Gskew_Y", "type": ["float", "null"]},
            {"name": "Gskew_g", "type": ["float", "null"]},
            {"name": "Gskew_i", "type": ["float", "null"]},
            {"name": "Gskew_r", "type": ["float", "null"]},
            {"name": "Gskew_u", "type": ["float", "null"]},
            {"name": "Gskew_z", "type": ["float", "null"]},
            {"name": "HOSTGAL2_ELLIPTICITY", "type": ["float", "null"]},
            {"name": "HOSTGAL2_MAGERR_Y", "type": ["float", "null"]},
            {"name": "HOSTGAL2_MAGERR_g", "type": ["float", "null"]},
            {"name": "HOSTGAL2_MAGERR_i", "type": ["float", "null"]},
            {"name": "HOSTGAL2_MAGERR_r", "type": ["float", "null"]},
            {"name": "HOSTGAL2_MAGERR_u", "type": ["float", "null"]},
            {"name": "HOSTGAL2_MAGERR_z", "type": ["float", "null"]},
            {"name": "HOSTGAL2_MAG_Y", "type": ["float", "null"]},
            {"name": "HOSTGAL2_MAG_g", "type": ["float", "null"]},
            {"name": "HOSTGAL2_MAG_i", "type": ["float", "null"]},
            {"name": "HOSTGAL2_MAG_r", "type": ["float", "null"]},
            {"name": "HOSTGAL2_MAG_u", "type": ["float", "null"]},
            {"name": "HOSTGAL2_MAG_z", "type": ["float", "null"]},
            {"name": "HOSTGAL2_PHOTOZ", "type": ["float", "null"]},
            {"name": "HOSTGAL2_PHOTOZ_ERR", "type": ["float", "null"]},
            {"name": "HOSTGAL2_SNSEP", "type": ["float", "null"]},
            {"name": "HOSTGAL2_SPECZ", "type": ["float", "null"]},
            {"name": "HOSTGAL2_SPECZ_ERR", "type": ["float", "null"]},
            {"name": "HOSTGAL2_SQRADIUS", "type": ["float", "null"]},
            {"name": "HOSTGAL2_ZPHOT_Q000", "type": ["float", "null"]},
            {"name": "HOSTGAL2_ZPHOT_Q010", "type": ["float", "null"]},
            {"name": "HOSTGAL2_ZPHOT_Q020", "type": ["float", "null"]},
            {"name": "HOSTGAL2_ZPHOT_Q030", "type": ["float", "null"]},
            {"name": "HOSTGAL2_ZPHOT_Q040", "type": ["float", "null"]},
            {"name": "HOSTGAL2_ZPHOT_Q050", "type": ["float", "null"]},
            {"name": "HOSTGAL2_ZPHOT_Q060", "type": ["float", "null"]},
            {"name": "HOSTGAL2_ZPHOT_Q070", "type": ["float", "null"]},
            {"name": "HOSTGAL2_ZPHOT_Q080", "type": ["float", "null"]},
            {"name": "HOSTGAL2_ZPHOT_Q090", "type": ["float", "null"]},
            {"name": "HOSTGAL2_ZPHOT_Q100", "type": ["float", "null"]},
            {"name": "HOSTGAL_ELLIPTICITY", "type": ["float", "null"]},
            {"name": "HOSTGAL_MAGERR_Y", "type": ["float", "null"]},
            {"name": "HOSTGAL_MAGERR_g", "type": ["float", "null"]},
            {"name": "HOSTGAL_MAGERR_i", "type": ["float", "null"]},
            {"name": "HOSTGAL_MAGERR_r", "type": ["float", "null"]},
            {"name": "HOSTGAL_MAGERR_u", "type": ["float", "null"]},
            {"name": "HOSTGAL_MAGERR_z", "type": ["float", "null"]},
            {"name": "HOSTGAL_MAG_Y", "type": ["float", "null"]},
            {"name": "HOSTGAL_MAG_g", "type": ["float", "null"]},
            {"name": "HOSTGAL_MAG_i", "type": ["float", "null"]},
            {"name": "HOSTGAL_MAG_r", "type": ["float", "null"]},
            {"name": "HOSTGAL_MAG_u", "type": ["float", "null"]},
            {"name": "HOSTGAL_MAG_z", "type": ["float", "null"]},
            {"name": "HOSTGAL_PHOTOZ", "type": ["float", "null"]},
            {"name": "HOSTGAL_PHOTOZ_ERR", "type": ["float", "null"]},
            {"name": "HOSTGAL_SNSEP", "type": ["float", "null"]},
            {"name": "HOSTGAL_SPECZ", "type": ["float", "null"]},
            {"name": "HOSTGAL_SPECZ_ERR", "type": ["float", "null"]},
            {"name": "HOSTGAL_SQRADIUS", "type": ["float", "null"]},
            {"name": "HOSTGAL_ZPHOT_Q000", "type": ["float", "null"]},
            {"name": "HOSTGAL_ZPHOT_Q010", "type": ["float", "null"]},
            {"name": "HOSTGAL_ZPHOT_Q020", "type": ["float", "null"]},
            {"name": "HOSTGAL_ZPHOT_Q030", "type": ["float", "null"]},
            {"name": "HOSTGAL_ZPHOT_Q040", "type": ["float", "null"]},
            {"name": "HOSTGAL_ZPHOT_Q050", "type": ["float", "null"]},
            {"name": "HOSTGAL_ZPHOT_Q060", "type": ["float", "null"]},
            {"name": "HOSTGAL_ZPHOT_Q070", "type": ["float", "null"]},
            {"name": "HOSTGAL_ZPHOT_Q080", "type": ["float", "null"]},
            {"name": "HOSTGAL_ZPHOT_Q090", "type": ["float", "null"]},
            {"name": "HOSTGAL_ZPHOT_Q100", "type": ["float", "null"]},
            {"name": "Harmonics_chi_Y", "type": ["float", "null"]},
            {"name": "Harmonics_chi_g", "type": ["float", "null"]},
            {"name": "Harmonics_chi_i", "type": ["float", "null"]},
            {"name": "Harmonics_chi_r", "type": ["float", "null"]},
            {"name": "Harmonics_chi_u", "type": ["float", "null"]},
            {"name": "Harmonics_chi_z", "type": ["float", "null"]},
            {"name": "Harmonics_mag_1_Y", "type": ["float", "null"]},
            {"name": "Harmonics_mag_1_g", "type": ["float", "null"]},
            {"name": "Harmonics_mag_1_i", "type": ["float", "null"]},
            {"name": "Harmonics_mag_1_r", "type": ["float", "null"]},
            {"name": "Harmonics_mag_1_u", "type": ["float", "null"]},
            {"name": "Harmonics_mag_1_z", "type": ["float", "null"]},
            {"name": "Harmonics_mag_2_Y", "type": ["float", "null"]},
            {"name": "Harmonics_mag_2_g", "type": ["float", "null"]},
            {"name": "Harmonics_mag_2_i", "type": ["float", "null"]},
            {"name": "Harmonics_mag_2_r", "type": ["float", "null"]},
            {"name": "Harmonics_mag_2_u", "type": ["float", "null"]},
            {"name": "Harmonics_mag_2_z", "type": ["float", "null"]},
            {"name": "Harmonics_mag_3_Y", "type": ["float", "null"]},
            {"name": "Harmonics_mag_3_g", "type": ["float", "null"]},
            {"name": "Harmonics_mag_3_i", "type": ["float", "null"]},
            {"name": "Harmonics_mag_3_r", "type": ["float", "null"]},
            {"name": "Harmonics_mag_3_u", "type": ["float", "null"]},
            {"name": "Harmonics_mag_3_z", "type": ["float", "null"]},
            {"name": "Harmonics_mag_4_Y", "type": ["float", "null"]},
            {"name": "Harmonics_mag_4_g", "type": ["float", "null"]},
            {"name": "Harmonics_mag_4_i", "type": ["float", "null"]},
            {"name": "Harmonics_mag_4_r", "type": ["float", "null"]},
            {"name": "Harmonics_mag_4_u", "type": ["float", "null"]},
            {"name": "Harmonics_mag_4_z", "type": ["float", "null"]},
            {"name": "Harmonics_mag_5_Y", "type": ["float", "null"]},
            {"name": "Harmonics_mag_5_g", "type": ["float", "null"]},
            {"name": "Harmonics_mag_5_i", "type": ["float", "null"]},
            {"name": "Harmonics_mag_5_r", "type": ["float", "null"]},
            {"name": "Harmonics_mag_5_u", "type": ["float", "null"]},
            {"name": "Harmonics_mag_5_z", "type": ["float", "null"]},
            {"name": "Harmonics_mag_6_Y", "type": ["float", "null"]},
            {"name": "Harmonics_mag_6_g", "type": ["float", "null"]},
            {"name": "Harmonics_mag_6_i", "type": ["float", "null"]},
            {"name": "Harmonics_mag_6_r", "type": ["float", "null"]},
            {"name": "Harmonics_mag_6_u", "type": ["float", "null"]},
            {"name": "Harmonics_mag_6_z", "type": ["float", "null"]},
            {"name": "Harmonics_mag_7_Y", "type": ["float", "null"]},
            {"name": "Harmonics_mag_7_g", "type": ["float", "null"]},
            {"name": "Harmonics_mag_7_i", "type": ["float", "null"]},
            {"name": "Harmonics_mag_7_r", "type": ["float", "null"]},
            {"name": "Harmonics_mag_7_u", "type": ["float", "null"]},
            {"name": "Harmonics_mag_7_z", "type": ["float", "null"]},
            {"name": "Harmonics_mse_Y", "type": ["float", "null"]},
            {"name": "Harmonics_mse_g", "type": ["float", "null"]},
            {"name": "Harmonics_mse_i", "type": ["float", "null"]},
            {"name": "Harmonics_mse_r", "type": ["float", "null"]},
            {"name": "Harmonics_mse_u", "type": ["float", "null"]},
            {"name": "Harmonics_mse_z", "type": ["float", "null"]},
            {"name": "Harmonics_phase_2_Y", "type": ["float", "null"]},
            {"name": "Harmonics_phase_2_g", "type": ["float", "null"]},
            {"name": "Harmonics_phase_2_i", "type": ["float", "null"]},
            {"name": "Harmonics_phase_2_r", "type": ["float", "null"]},
            {"name": "Harmonics_phase_2_u", "type": ["float", "null"]},
            {"name": "Harmonics_phase_2_z", "type": ["float", "null"]},
            {"name": "Harmonics_phase_3_Y", "type": ["float", "null"]},
            {"name": "Harmonics_phase_3_g", "type": ["float", "null"]},
            {"name": "Harmonics_phase_3_i", "type": ["float", "null"]},
            {"name": "Harmonics_phase_3_r", "type": ["float", "null"]},
            {"name": "Harmonics_phase_3_u", "type": ["float", "null"]},
            {"name": "Harmonics_phase_3_z", "type": ["float", "null"]},
            {"name": "Harmonics_phase_4_Y", "type": ["float", "null"]},
            {"name": "Harmonics_phase_4_g", "type": ["float", "null"]},
            {"name": "Harmonics_phase_4_i", "type": ["float", "null"]},
            {"name": "Harmonics_phase_4_r", "type": ["float", "null"]},
            {"name": "Harmonics_phase_4_u", "type": ["float", "null"]},
            {"name": "Harmonics_phase_4_z", "type": ["float", "null"]},
            {"name": "Harmonics_phase_5_Y", "type": ["float", "null"]},
            {"name": "Harmonics_phase_5_g", "type": ["float", "null"]},
            {"name": "Harmonics_phase_5_i", "type": ["float", "null"]},
            {"name": "Harmonics_phase_5_r", "type": ["float", "null"]},
            {"name": "Harmonics_phase_5_u", "type": ["float", "null"]},
            {"name": "Harmonics_phase_5_z", "type": ["float", "null"]},
            {"name": "Harmonics_phase_6_Y", "type": ["float", "null"]},
            {"name": "Harmonics_phase_6_g", "type": ["float", "null"]},
            {"name": "Harmonics_phase_6_i", "type": ["float", "null"]},
            {"name": "Harmonics_phase_6_r", "type": ["float", "null"]},
            {"name": "Harmonics_phase_6_u", "type": ["float", "null"]},
            {"name": "Harmonics_phase_6_z", "type": ["float", "null"]},
            {"name": "Harmonics_phase_7_Y", "type": ["float", "null"]},
            {"name": "Harmonics_phase_7_g", "type": ["float", "null"]},
            {"name": "Harmonics_phase_7_i", "type": ["float", "null"]},
            {"name": "Harmonics_phase_7_r", "type": ["float", "null"]},
            {"name": "Harmonics_phase_7_u", "type": ["float", "null"]},
            {"name": "Harmonics_phase_7_z", "type": ["float", "null"]},
            {"name": "IAR_phi_Y", "type": ["float", "null"]},
            {"name": "IAR_phi_g", "type": ["float", "null"]},
            {"name": "IAR_phi_i", "type": ["float", "null"]},
            {"name": "IAR_phi_r", "type": ["float", "null"]},
            {"name": "IAR_phi_u", "type": ["float", "null"]},
            {"name": "IAR_phi_z", "type": ["float", "null"]},
            {"name": "LinearTrend_Y", "type": ["float", "null"]},
            {"name": "LinearTrend_g", "type": ["float", "null"]},
            {"name": "LinearTrend_i", "type": ["float", "null"]},
            {"name": "LinearTrend_r", "type": ["float", "null"]},
            {"name": "LinearTrend_u", "type": ["float", "null"]},
            {"name": "LinearTrend_z", "type": ["float", "null"]},
            {"name": "MHPS_PN_flag_Y", "type": ["float", "null"]},
            {"name": "MHPS_PN_flag_g", "type": ["float", "null"]},
            {"name": "MHPS_PN_flag_i", "type": ["float", "null"]},
            {"name": "MHPS_PN_flag_r", "type": ["float", "null"]},
            {"name": "MHPS_PN_flag_u", "type": ["float", "null"]},
            {"name": "MHPS_PN_flag_z", "type": ["float", "null"]},
            {"name": "MHPS_high_Y", "type": ["float", "null"]},
            {"name": "MHPS_high_g", "type": ["float", "null"]},
            {"name": "MHPS_high_i", "type": ["float", "null"]},
            {"name": "MHPS_high_r", "type": ["float", "null"]},
            {"name": "MHPS_high_u", "type": ["float", "null"]},
            {"name": "MHPS_high_z", "type": ["float", "null"]},
            {"name": "MHPS_low_Y", "type": ["float", "null"]},
            {"name": "MHPS_low_g", "type": ["float", "null"]},
            {"name": "MHPS_low_i", "type": ["float", "null"]},
            {"name": "MHPS_low_r", "type": ["float", "null"]},
            {"name": "MHPS_low_u", "type": ["float", "null"]},
            {"name": "MHPS_low_z", "type": ["float", "null"]},
            {"name": "MHPS_non_zero_Y", "type": ["float", "null"]},
            {"name": "MHPS_non_zero_g", "type": ["float", "null"]},
            {"name": "MHPS_non_zero_i", "type": ["float", "null"]},
            {"name": "MHPS_non_zero_r", "type": ["float", "null"]},
            {"name": "MHPS_non_zero_u", "type": ["float", "null"]},
            {"name": "MHPS_non_zero_z", "type": ["float", "null"]},
            {"name": "MHPS_ratio_Y", "type": ["float", "null"]},
            {"name": "MHPS_ratio_g", "type": ["float", "null"]},
            {"name": "MHPS_ratio_i", "type": ["float", "null"]},
            {"name": "MHPS_ratio_r", "type": ["float", "null"]},
            {"name": "MHPS_ratio_u", "type": ["float", "null"]},
            {"name": "MHPS_ratio_z", "type": ["float", "null"]},
            {"name": "MWEBV", "type": ["float", "null"]},
            {"name": "MWEBV_ERR", "type": ["float", "null"]},
            {"name": "MaxSlope_Y", "type": ["float", "null"]},
            {"name": "MaxSlope_g", "type": ["float", "null"]},
            {"name": "MaxSlope_i", "type": ["float", "null"]},
            {"name": "MaxSlope_r", "type": ["float", "null"]},
            {"name": "MaxSlope_u", "type": ["float", "null"]},
            {"name": "MaxSlope_z", "type": ["float", "null"]},
            {"name": "Mean_Y", "type": ["float", "null"]},
            {"name": "Mean_g", "type": ["float", "null"]},
            {"name": "Mean_i", "type": ["float", "null"]},
            {"name": "Mean_r", "type": ["float", "null"]},
            {"name": "Mean_u", "type": ["float", "null"]},
            {"name": "Mean_z", "type": ["float", "null"]},
            {"name": "Meanvariance_Y", "type": ["float", "null"]},
            {"name": "Meanvariance_g", "type": ["float", "null"]},
            {"name": "Meanvariance_i", "type": ["float", "null"]},
            {"name": "Meanvariance_r", "type": ["float", "null"]},
            {"name": "Meanvariance_u", "type": ["float", "null"]},
            {"name": "Meanvariance_z", "type": ["float", "null"]},
            {"name": "MedianAbsDev_Y", "type": ["float", "null"]},
            {"name": "MedianAbsDev_g", "type": ["float", "null"]},
            {"name": "MedianAbsDev_i", "type": ["float", "null"]},
            {"name": "MedianAbsDev_r", "type": ["float", "null"]},
            {"name": "MedianAbsDev_u", "type": ["float", "null"]},
            {"name": "MedianAbsDev_z", "type": ["float", "null"]},
            {"name": "MedianBRP_Y", "type": ["float", "null"]},
            {"name": "MedianBRP_g", "type": ["float", "null"]},
            {"name": "MedianBRP_i", "type": ["float", "null"]},
            {"name": "MedianBRP_r", "type": ["float", "null"]},
            {"name": "MedianBRP_u", "type": ["float", "null"]},
            {"name": "MedianBRP_z", "type": ["float", "null"]},
            {"name": "Multiband_period", "type": ["float", "null"]},
            {"name": "PPE", "type": ["float", "null"]},
            {"name": "PairSlopeTrend_Y", "type": ["float", "null"]},
            {"name": "PairSlopeTrend_g", "type": ["float", "null"]},
            {"name": "PairSlopeTrend_i", "type": ["float", "null"]},
            {"name": "PairSlopeTrend_r", "type": ["float", "null"]},
            {"name": "PairSlopeTrend_u", "type": ["float", "null"]},
            {"name": "PairSlopeTrend_z", "type": ["float", "null"]},
            {"name": "PercentAmplitude_Y", "type": ["float", "null"]},
            {"name": "PercentAmplitude_g", "type": ["float", "null"]},
            {"name": "PercentAmplitude_i", "type": ["float", "null"]},
            {"name": "PercentAmplitude_r", "type": ["float", "null"]},
            {"name": "PercentAmplitude_u", "type": ["float", "null"]},
            {"name": "PercentAmplitude_z", "type": ["float", "null"]},
            {"name": "Period_band_Y", "type": ["float", "null"]},
            {"name": "Period_band_g", "type": ["float", "null"]},
            {"name": "Period_band_i", "type": ["float", "null"]},
            {"name": "Period_band_r", "type": ["float", "null"]},
            {"name": "Period_band_u", "type": ["float", "null"]},
            {"name": "Period_band_z", "type": ["float", "null"]},
            {"name": "Power_rate_1/2", "type": ["float", "null"]},
            {"name": "Power_rate_1/3", "type": ["float", "null"]},
            {"name": "Power_rate_1/4", "type": ["float", "null"]},
            {"name": "Power_rate_2", "type": ["float", "null"]},
            {"name": "Power_rate_3", "type": ["float", "null"]},
            {"name": "Power_rate_4", "type": ["float", "null"]},
            {"name": "Psi_CS_Y", "type": ["float", "null"]},
            {"name": "Psi_CS_g", "type": ["float", "null"]},
            {"name": "Psi_CS_i", "type": ["float", "null"]},
            {"name": "Psi_CS_r", "type": ["float", "null"]},
            {"name": "Psi_CS_u", "type": ["float", "null"]},
            {"name": "Psi_CS_z", "type": ["float", "null"]},
            {"name": "Psi_eta_Y", "type": ["float", "null"]},
            {"name": "Psi_eta_g", "type": ["float", "null"]},
            {"name": "Psi_eta_i", "type": ["float", "null"]},
            {"name": "Psi_eta_r", "type": ["float", "null"]},
            {"name": "Psi_eta_u", "type": ["float", "null"]},
            {"name": "Psi_eta_z", "type": ["float", "null"]},
            {"name": "Pvar_Y", "type": ["float", "null"]},
            {"name": "Pvar_g", "type": ["float", "null"]},
            {"name": "Pvar_i", "type": ["float", "null"]},
            {"name": "Pvar_r", "type": ["float", "null"]},
            {"name": "Pvar_u", "type": ["float", "null"]},
            {"name": "Pvar_z", "type": ["float", "null"]},
            {"name": "Q31_Y", "type": ["float", "null"]},
            {"name": "Q31_g", "type": ["float", "null"]},
            {"name": "Q31_i", "type": ["float", "null"]},
            {"name": "Q31_r", "type": ["float", "null"]},
            {"name": "Q31_u", "type": ["float", "null"]},
            {"name": "Q31_z", "type": ["float", "null"]},
            {"name": "REDSHIFT_HELIO", "type": ["float", "null"]},
            {"name": "REDSHIFT_HELIO_ERR", "type": ["float", "null"]},
            {"name": "Rcs_Y", "type": ["float", "null"]},
            {"name": "Rcs_g", "type": ["float", "null"]},
            {"name": "Rcs_i", "type": ["float", "null"]},
            {"name": "Rcs_r", "type": ["float", "null"]},
            {"name": "Rcs_u", "type": ["float", "null"]},
            {"name": "Rcs_z", "type": ["float", "null"]},
            {"name": "SF_ML_amplitude_Y", "type": ["float", "null"]},
            {"name": "SF_ML_amplitude_g", "type": ["float", "null"]},
            {"name": "SF_ML_amplitude_i", "type": ["float", "null"]},
            {"name": "SF_ML_amplitude_r", "type": ["float", "null"]},
            {"name": "SF_ML_amplitude_u", "type": ["float", "null"]},
            {"name": "SF_ML_amplitude_z", "type": ["float", "null"]},
            {"name": "SF_ML_gamma_Y", "type": ["float", "null"]},
            {"name": "SF_ML_gamma_g", "type": ["float", "null"]},
            {"name": "SF_ML_gamma_i", "type": ["float", "null"]},
            {"name": "SF_ML_gamma_r", "type": ["float", "null"]},
            {"name": "SF_ML_gamma_u", "type": ["float", "null"]},
            {"name": "SF_ML_gamma_z", "type": ["float", "null"]},
            {"name": "SPM_A_Y", "type": ["float", "null"]},
            {"name": "SPM_A_g", "type": ["float", "null"]},
            {"name": "SPM_A_i", "type": ["float", "null"]},
            {"name": "SPM_A_r", "type": ["float", "null"]},
            {"name": "SPM_A_u", "type": ["float", "null"]},
            {"name": "SPM_A_z", "type": ["float", "null"]},
            {"name": "SPM_beta_Y", "type": ["float", "null"]},
            {"name": "SPM_beta_g", "type": ["float", "null"]},
            {"name": "SPM_beta_i", "type": ["float", "null"]},
            {"name": "SPM_beta_r", "type": ["float", "null"]},
            {"name": "SPM_beta_u", "type": ["float", "null"]},
            {"name": "SPM_beta_z", "type": ["float", "null"]},
            {"name": "SPM_chi_Y", "type": ["float", "null"]},
            {"name": "SPM_chi_g", "type": ["float", "null"]},
            {"name": "SPM_chi_i", "type": ["float", "null"]},
            {"name": "SPM_chi_r", "type": ["float", "null"]},
            {"name": "SPM_chi_u", "type": ["float", "null"]},
            {"name": "SPM_chi_z", "type": ["float", "null"]},
            {"name": "SPM_gamma_Y", "type": ["float", "null"]},
            {"name": "SPM_gamma_g", "type": ["float", "null"]},
            {"name": "SPM_gamma_i", "type": ["float", "null"]},
            {"name": "SPM_gamma_r", "type": ["float", "null"]},
            {"name": "SPM_gamma_u", "type": ["float", "null"]},
            {"name": "SPM_gamma_z", "type": ["float", "null"]},
            {"name": "SPM_t0_Y", "type": ["float", "null"]},
            {"name": "SPM_t0_g", "type": ["float", "null"]},
            {"name": "SPM_t0_i", "type": ["float", "null"]},
            {"name": "SPM_t0_r", "type": ["float", "null"]},
            {"name": "SPM_t0_u", "type": ["float", "null"]},
            {"name": "SPM_t0_z", "type": ["float", "null"]},
            {"name": "SPM_tau_fall_Y", "type": ["float", "null"]},
            {"name": "SPM_tau_fall_g", "type": ["float", "null"]},
            {"name": "SPM_tau_fall_i", "type": ["float", "null"]},
            {"name": "SPM_tau_fall_r", "type": ["float", "null"]},
            {"name": "SPM_tau_fall_u", "type": ["float", "null"]},
            {"name": "SPM_tau_fall_z", "type": ["float", "null"]},
            {"name": "SPM_tau_rise_Y", "type": ["float", "null"]},
            {"name": "SPM_tau_rise_g", "type": ["float", "null"]},
            {"name": "SPM_tau_rise_i", "type": ["float", "null"]},
            {"name": "SPM_tau_rise_r", "type": ["float", "null"]},
            {"name": "SPM_tau_rise_u", "type": ["float", "null"]},
            {"name": "SPM_tau_rise_z", "type": ["float", "null"]},
            {"name": "Skew_Y", "type": ["float", "null"]},
            {"name": "Skew_g", "type": ["float", "null"]},
            {"name": "Skew_i", "type": ["float", "null"]},
            {"name": "Skew_r", "type": ["float", "null"]},
            {"name": "Skew_u", "type": ["float", "null"]},
            {"name": "Skew_z", "type": ["float", "null"]},
            {"name": "SmallKurtosis_Y", "type": ["float", "null"]},
            {"name": "SmallKurtosis_g", "type": ["float", "null"]},
            {"name": "SmallKurtosis_i", "type": ["float", "null"]},
            {"name": "SmallKurtosis_r", "type": ["float", "null"]},
            {"name": "SmallKurtosis_u", "type": ["float", "null"]},
            {"name": "SmallKurtosis_z", "type": ["float", "null"]},
            {"name": "Std_Y", "type": ["float", "null"]},
            {"name": "Std_g", "type": ["float", "null"]},
            {"name": "Std_i", "type": ["float", "null"]},
            {"name": "Std_r", "type": ["float", "null"]},
            {"name": "Std_u", "type": ["float", "null"]},
            {"name": "Std_z", "type": ["float", "null"]},
            {"name": "StetsonK_Y", "type": ["float", "null"]},
            {"name": "StetsonK_g", "type": ["float", "null"]},
            {"name": "StetsonK_i", "type": ["float", "null"]},
            {"name": "StetsonK_r", "type": ["float", "null"]},
            {"name": "StetsonK_u", "type": ["float", "null"]},
            {"name": "StetsonK_z", "type": ["float", "null"]},
            {"name": "Timespan", "type": ["float", "null"]},
            {"name": "delta_period_Y", "type": ["float", "null"]},
            {"name": "delta_period_g", "type": ["float", "null"]},
            {"name": "delta_period_i", "type": ["float", "null"]},
            {"name": "delta_period_r", "type": ["float", "null"]},
            {"name": "delta_period_u", "type": ["float", "null"]},
            {"name": "delta_period_z", "type": ["float", "null"]},
            {"name": "dflux_first_det_band_Y", "type": ["float", "null"]},
            {"name": "dflux_first_det_band_g", "type": ["float", "null"]},
            {"name": "dflux_first_det_band_i", "type": ["float", "null"]},
            {"name": "dflux_first_det_band_r", "type": ["float", "null"]},
            {"name": "dflux_first_det_band_u", "type": ["float", "null"]},
            {"name": "dflux_first_det_band_z", "type": ["float", "null"]},
            {"name": "dflux_non_det_band_Y", "type": ["float", "null"]},
            {"name": "dflux_non_det_band_g", "type": ["float", "null"]},
            {"name": "dflux_non_det_band_i", "type": ["float", "null"]},
            {"name": "dflux_non_det_band_r", "type": ["float", "null"]},
            {"name": "dflux_non_det_band_u", "type": ["float", "null"]},
            {"name": "dflux_non_det_band_z", "type": ["float", "null"]},
            {"name": "g-r", "type": ["float", "null"]},
            {"name": "i-z", "type": ["float", "null"]},
            {"name": "iqr_Y", "type": ["float", "null"]},
            {"name": "iqr_g", "type": ["float", "null"]},
            {"name": "iqr_i", "type": ["float", "null"]},
            {"name": "iqr_r", "type": ["float", "null"]},
            {"name": "iqr_u", "type": ["float", "null"]},
            {"name": "iqr_z", "type": ["float", "null"]},
            {"name": "last_flux_before_band_Y", "type": ["float", "null"]},
            {"name": "last_flux_before_band_g", "type": ["float", "null"]},
            {"name": "last_flux_before_band_i", "type": ["float", "null"]},
            {"name": "last_flux_before_band_r", "type": ["float", "null"]},
            {"name": "last_flux_before_band_u", "type": ["float", "null"]},
            {"name": "last_flux_before_band_z", "type": ["float", "null"]},
            {"name": "max_flux_after_band_Y", "type": ["float", "null"]},
            {"name": "max_flux_after_band_g", "type": ["float", "null"]},
            {"name": "max_flux_after_band_i", "type": ["float", "null"]},
            {"name": "max_flux_after_band_r", "type": ["float", "null"]},
            {"name": "max_flux_after_band_u", "type": ["float", "null"]},
            {"name": "max_flux_after_band_z", "type": ["float", "null"]},
            {"name": "max_flux_before_band_Y", "type": ["float", "null"]},
            {"name": "max_flux_before_band_g", "type": ["float", "null"]},
            {"name": "max_flux_before_band_i", "type": ["float", "null"]},
            {"name": "max_flux_before_band_r", "type": ["float", "null"]},
            {"name": "max_flux_before_band_u", "type": ["float", "null"]},
            {"name": "max_flux_before_band_z", "type": ["float", "null"]},
            {"name": "median_flux_after_band_Y", "type": ["float", "null"]},
            {"name": "median_flux_after_band_g", "type": ["float", "null"]},
            {"name": "median_flux_after_band_i", "type": ["float", "null"]},
            {"name": "median_flux_after_band_r", "type": ["float", "null"]},
            {"name": "median_flux_after_band_u", "type": ["float", "null"]},
            {"name": "median_flux_after_band_z", "type": ["float", "null"]},
            {"name": "median_flux_before_band_Y", "type": ["float", "null"]},
            {"name": "median_flux_before_band_g", "type": ["float", "null"]},
            {"name": "median_flux_before_band_i", "type": ["float", "null"]},
            {"name": "median_flux_before_band_r", "type": ["float", "null"]},
            {"name": "median_flux_before_band_u", "type": ["float", "null"]},
            {"name": "median_flux_before_band_z", "type": ["float", "null"]},
            {"name": "n_non_det_after_band_Y", "type": ["float", "null"]},
            {"name": "n_non_det_after_band_g", "type": ["float", "null"]},
            {"name": "n_non_det_after_band_i", "type": ["float", "null"]},
            {"name": "n_non_det_after_band_r", "type": ["float", "null"]},
            {"name": "n_non_det_after_band_u", "type": ["float", "null"]},
            {"name": "n_non_det_after_band_z", "type": ["float", "null"]},
            {"name": "n_non_det_before_band_Y", "type": ["float", "null"]},
            {"name": "n_non_det_before_band_g", "type": ["float", "null"]},
            {"name": "n_non_det_before_band_i", "type": ["float", "null"]},
            {"name": "n_non_det_before_band_r", "type": ["float", "null"]},
            {"name": "n_non_det_before_band_u", "type": ["float", "null"]},
            {"name": "n_non_det_before_band_z", "type": ["float", "null"]},
            {"name": "positive_fraction_Y", "type": ["float", "null"]},
            {"name": "positive_fraction_g", "type": ["float", "null"]},
            {"name": "positive_fraction_i", "type": ["float", "null"]},
            {"name": "positive_fraction_r", "type": ["float", "null"]},
            {"name": "positive_fraction_u", "type": ["float", "null"]},
            {"name": "positive_fraction_z", "type": ["float", "null"]},
            {"name": "r-i", "type": ["float", "null"]},
            {"name": "u-g", "type": ["float", "null"]},
            {"name": "z-Y", "type": ["float", "null"]},
        ],
    }
    if force_empty_features:
        return {}
    features = generate_one(FEATURES_SCHEMA)
    if force_missing_features:
        for _ in range(random.randint(1, len(features))):
            try:
                key = _get_random_key(features)
                features[key] = None
            except KeyError:
                pass
    return features
