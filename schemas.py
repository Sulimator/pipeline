FEATURES_SCHEMA = {
    "name": "features",
    "type": {
        "name": "features_record",
        "type": "record",
        "fields": [
            {"name": "Amplitude_1", "type": ["float", "null"]},
            {"name": "Amplitude_2", "type": ["float", "null"]},
            {"name": "AndersonDarling_1", "type": ["float", "null"]},
            {"name": "AndersonDarling_2", "type": ["float", "null"]},
            {"name": "Autocor_length_1", "type": ["double", "null"]},
            {"name": "Autocor_length_2", "type": ["double", "null"]},
            {"name": "Beyond1Std_1", "type": ["float", "null"]},
            {"name": "Beyond1Std_2", "type": ["float", "null"]},
            {"name": "Con_1", "type": ["double", "null"]},
            {"name": "Con_2", "type": ["double", "null"]},
            {"name": "Eta_e_1", "type": ["float", "null"]},
            {"name": "Eta_e_2", "type": ["float", "null"]},
            {"name": "ExcessVar_1", "type": ["double", "null"]},
            {"name": "ExcessVar_2", "type": ["double", "null"]},
            {"name": "GP_DRW_sigma_1", "type": ["double", "null"]},
            {"name": "GP_DRW_sigma_2", "type": ["double", "null"]},
            {"name": "GP_DRW_tau_1", "type": ["float", "null"]},
            {"name": "GP_DRW_tau_2", "type": ["float", "null"]},
            {"name": "Gskew_1", "type": ["float", "null"]},
            {"name": "Gskew_2", "type": ["float", "null"]},
            {"name": "Harmonics_mag_1_1", "type": ["float", "null"]},
            {"name": "Harmonics_mag_1_2", "type": ["float", "null"]},
            {"name": "Harmonics_mag_2_1", "type": ["float", "null"]},
            {"name": "Harmonics_mag_2_2", "type": ["float", "null"]},
            {"name": "Harmonics_mag_3_1", "type": ["float", "null"]},
            {"name": "Harmonics_mag_3_2", "type": ["float", "null"]},
            {"name": "Harmonics_mag_4_1", "type": ["float", "null"]},
            {"name": "Harmonics_mag_4_2", "type": ["float", "null"]},
            {"name": "Harmonics_mag_5_1", "type": ["float", "null"]},
            {"name": "Harmonics_mag_5_2", "type": ["float", "null"]},
            {"name": "Harmonics_mag_6_1", "type": ["float", "null"]},
            {"name": "Harmonics_mag_6_2", "type": ["float", "null"]},
            {"name": "Harmonics_mag_7_1", "type": ["float", "null"]},
            {"name": "Harmonics_mag_7_2", "type": ["float", "null"]},
            {"name": "Harmonics_mse_1", "type": ["double", "null"]},
            {"name": "Harmonics_mse_2", "type": ["double", "null"]},
            {"name": "Harmonics_phase_2_1", "type": ["float", "null"]},
            {"name": "Harmonics_phase_2_2", "type": ["float", "null"]},
            {"name": "Harmonics_phase_3_1", "type": ["float", "null"]},
            {"name": "Harmonics_phase_3_2", "type": ["float", "null"]},
            {"name": "Harmonics_phase_4_1", "type": ["float", "null"]},
            {"name": "Harmonics_phase_4_2", "type": ["float", "null"]},
            {"name": "Harmonics_phase_5_1", "type": ["float", "null"]},
            {"name": "Harmonics_phase_5_2", "type": ["float", "null"]},
            {"name": "Harmonics_phase_6_1", "type": ["float", "null"]},
            {"name": "Harmonics_phase_6_2", "type": ["float", "null"]},
            {"name": "Harmonics_phase_7_1", "type": ["float", "null"]},
            {"name": "Harmonics_phase_7_2", "type": ["float", "null"]},
            {"name": "IAR_phi_1", "type": ["double", "null"]},
            {"name": "IAR_phi_2", "type": ["float", "null"]},
            {"name": "LinearTrend_1", "type": ["float", "null"]},
            {"name": "LinearTrend_2", "type": ["double", "null"]},
            {"name": "MHPS_PN_flag_1", "type": ["double", "null"]},
            {"name": "MHPS_PN_flag_2", "type": ["double", "null"]},
            {"name": "MHPS_high_1", "type": ["float", "null"]},
            {"name": "MHPS_high_2", "type": ["double", "null"]},
            {"name": "MHPS_low_1", "type": ["float", "null"]},
            {"name": "MHPS_low_2", "type": ["float", "null"]},
            {"name": "MHPS_non_zero_1", "type": ["double", "null"]},
            {"name": "MHPS_non_zero_2", "type": ["double", "null"]},
            {"name": "MHPS_ratio_1", "type": ["float", "null"]},
            {"name": "MHPS_ratio_2", "type": ["float", "null"]},
            {"name": "MaxSlope_1", "type": ["float", "null"]},
            {"name": "MaxSlope_2", "type": ["float", "null"]},
            {"name": "Mean_1", "type": ["float", "null"]},
            {"name": "Mean_2", "type": ["float", "null"]},
            {"name": "Meanvariance_1", "type": ["float", "null"]},
            {"name": "Meanvariance_2", "type": ["float", "null"]},
            {"name": "MedianAbsDev_1", "type": ["float", "null"]},
            {"name": "MedianAbsDev_2", "type": ["float", "null"]},
            {"name": "MedianBRP_1", "type": ["float", "null"]},
            {"name": "MedianBRP_2", "type": ["float", "null"]},
            {"name": "Multiband_period", "type": ["float", "null"]},
            {"name": "PairSlopeTrend_1", "type": ["float", "null"]},
            {"name": "PairSlopeTrend_2", "type": ["float", "null"]},
            {"name": "PercentAmplitude_1", "type": ["float", "null"]},
            {"name": "PercentAmplitude_2", "type": ["float", "null"]},
            {"name": "Period_band_1", "type": ["float", "null"]},
            {"name": "Period_band_2", "type": ["float", "null"]},
            {"name": "delta_period_1", "type": ["float", "null"]},
            {"name": "delta_period_2", "type": ["float", "null"]},
            {"name": "Period_fit", "type": ["float", "null"]},
            {"name": "Power_rate_1/2", "type": ["float", "null"]},
            {"name": "Power_rate_1/3", "type": ["float", "null"]},
            {"name": "Power_rate_1/4", "type": ["float", "null"]},
            {"name": "Power_rate_2", "type": ["float", "null"]},
            {"name": "Power_rate_3", "type": ["float", "null"]},
            {"name": "Power_rate_4", "type": ["float", "null"]},
            {"name": "Psi_CS_1", "type": ["float", "null"]},
            {"name": "Psi_CS_2", "type": ["float", "null"]},
            {"name": "Psi_eta_1", "type": ["float", "null"]},
            {"name": "Psi_eta_2", "type": ["float", "null"]},
            {"name": "Pvar_1", "type": ["float", "null"]},
            {"name": "Pvar_2", "type": ["float", "null"]},
            {"name": "Q31_1", "type": ["float", "null"]},
            {"name": "Q31_2", "type": ["float", "null"]},
            {"name": "Rcs_1", "type": ["float", "null"]},
            {"name": "Rcs_2", "type": ["float", "null"]},
            {"name": "SF_ML_amplitude_1", "type": ["float", "null"]},
            {"name": "SF_ML_amplitude_2", "type": ["float", "null"]},
            {"name": "SF_ML_gamma_1", "type": ["float", "null"]},
            {"name": "SF_ML_gamma_2", "type": ["float", "null"]},
            {"name": "SPM_A_1", "type": ["float", "null"]},
            {"name": "SPM_A_2", "type": ["float", "null"]},
            {"name": "SPM_beta_1", "type": ["float", "null"]},
            {"name": "SPM_beta_2", "type": ["float", "null"]},
            {"name": "SPM_chi_1", "type": ["float", "null"]},
            {"name": "SPM_chi_2", "type": ["float", "null"]},
            {"name": "SPM_gamma_1", "type": ["float", "null"]},
            {"name": "SPM_gamma_2", "type": ["float", "null"]},
            {"name": "SPM_t0_1", "type": ["float", "null"]},
            {"name": "SPM_t0_2", "type": ["float", "null"]},
            {"name": "SPM_tau_fall_1", "type": ["float", "null"]},
            {"name": "SPM_tau_fall_2", "type": ["float", "null"]},
            {"name": "SPM_tau_rise_1", "type": ["float", "null"]},
            {"name": "SPM_tau_rise_2", "type": ["float", "null"]},
            {"name": "Skew_1", "type": ["float", "null"]},
            {"name": "Skew_2", "type": ["float", "null"]},
            {"name": "SmallKurtosis_1", "type": ["float", "null"]},
            {"name": "SmallKurtosis_2", "type": ["float", "null"]},
            {"name": "Std_1", "type": ["float", "null"]},
            {"name": "Std_2", "type": ["float", "null"]},
            {"name": "StetsonK_1", "type": ["float", "null"]},
            {"name": "StetsonK_2", "type": ["float", "null"]},
            {"name": "W1-W2", "type": ["double", "null"]},
            {"name": "W2-W3", "type": ["double", "null"]},
            {"name": "delta_mag_fid_1", "type": ["float", "null"]},
            {"name": "delta_mag_fid_2", "type": ["float", "null"]},
            {"name": "delta_mjd_fid_1", "type": ["float", "null"]},
            {"name": "delta_mjd_fid_2", "type": ["float", "null"]},
            {"name": "dmag_first_det_fid_1", "type": ["double", "null"]},
            {"name": "dmag_first_det_fid_2", "type": ["double", "null"]},
            {"name": "dmag_non_det_fid_1", "type": ["double", "null"]},
            {"name": "dmag_non_det_fid_2", "type": ["double", "null"]},
            {"name": "first_mag_1", "type": ["float", "null"]},
            {"name": "first_mag_2", "type": ["float", "null"]},
            {"name": "g-W2", "type": ["double", "null"]},
            {"name": "g-W3", "type": ["double", "null"]},
            {"name": "g-r_max", "type": ["float", "null"]},
            {"name": "g-r_max_corr", "type": ["float", "null"]},
            {"name": "g-r_mean", "type": ["float", "null"]},
            {"name": "g-r_mean_corr", "type": ["float", "null"]},
            {"name": "gal_b", "type": ["float", "null"]},
            {"name": "gal_l", "type": ["float", "null"]},
            {"name": "iqr_1", "type": ["float", "null"]},
            {"name": "iqr_2", "type": ["float", "null"]},
            {
                "name": "last_diffmaglim_before_fid_1",
                "type": ["double", "null"],
            },
            {
                "name": "last_diffmaglim_before_fid_2",
                "type": ["double", "null"],
            },
            {"name": "last_mjd_before_fid_1", "type": ["double", "null"]},
            {"name": "last_mjd_before_fid_2", "type": ["double", "null"]},
            {
                "name": "max_diffmaglim_after_fid_1",
                "type": ["double", "null"],
            },
            {
                "name": "max_diffmaglim_after_fid_2",
                "type": ["double", "null"],
            },
            {
                "name": "max_diffmaglim_before_fid_1",
                "type": ["double", "null"],
            },
            {
                "name": "max_diffmaglim_before_fid_2",
                "type": ["double", "null"],
            },
            {"name": "mean_mag_1", "type": ["float", "null"]},
            {"name": "mean_mag_2", "type": ["float", "null"]},
            {
                "name": "median_diffmaglim_after_fid_1",
                "type": ["double", "null"],
            },
            {
                "name": "median_diffmaglim_after_fid_2",
                "type": ["double", "null"],
            },
            {
                "name": "median_diffmaglim_before_fid_1",
                "type": ["double", "null"],
            },
            {
                "name": "median_diffmaglim_before_fid_2",
                "type": ["double", "null"],
            },
            {"name": "min_mag_1", "type": ["float", "null"]},
            {"name": "min_mag_2", "type": ["float", "null"]},
            {"name": "n_det_1", "type": ["double", "null"]},
            {"name": "n_det_2", "type": ["double", "null"]},
            {"name": "n_neg_1", "type": ["double", "null"]},
            {"name": "n_neg_2", "type": ["double", "null"]},
            {"name": "n_non_det_after_fid_1", "type": ["double", "null"]},
            {"name": "n_non_det_after_fid_2", "type": ["double", "null"]},
            {"name": "n_non_det_before_fid_1", "type": ["double", "null"]},
            {"name": "n_non_det_before_fid_2", "type": ["double", "null"]},
            {"name": "n_pos_1", "type": ["double", "null"]},
            {"name": "n_pos_2", "type": ["double", "null"]},
            {"name": "positive_fraction_1", "type": ["double", "null"]},
            {"name": "positive_fraction_2", "type": ["double", "null"]},
            {"name": "r-W2", "type": ["double", "null"]},
            {"name": "r-W3", "type": ["double", "null"]},
            {"name": "rb", "type": ["float", "null"]},
            {"name": "sgscore1", "type": ["float", "null"]},
        ],
    },
}


SCHEMA = {
    "doc": "Late Classification",
    "name": "probabilities_and_features",
    "type": "record",
    "fields": [
        {"name": "aid", "type": "string"},
        FEATURES_SCHEMA,
        {
            "name": "lc_classification",
            "type": {
                "type": "record",
                "name": "late_record",
                "fields": [
                    {
                        "name": "probabilities",
                        "type": {
                            "type": "map",
                            "values": ["float"],
                        },
                    },
                    {"name": "class", "type": "string"},
                    {
                        "name": "hierarchical",
                        "type": {
                            "name": "root",
                            "type": "map",
                            "values": [
                                {"type": "map", "values": "float"},
                                {
                                    "type": "map",
                                    "values": {"type": "map", "values": "float"},
                                },
                            ],
                        },
                    },
                ],
            },
        },
    ],
}
ELASTICC_SCHEMA = {
    "namespace": "elasticc.v0_9",
    "type": "record",
    "name": "brokerClassification",
    "doc": "sample avro alert schema v4.1",
    "fields": [
        {
            "name": "brokerName",
            "type": "string",
            "doc": "Name of broker (never changes)",
        },
        {
            "name": "brokerVersion",
            "type": "string",
            "doc": "Version/Release of broker's software",
        },
        {
            "name": "classifications",
            "type": {
                "type": "array",
                "items": {
                    "type": "record",
                    "name": "classificationDict",
                    "fields": [
                        {
                            "name": "classId",
                            "type": "int",
                            "doc": "See https://github.com/LSSTDESC/elasticc/tree/main/taxonomy/taxonomy.ipynb for specification",
                        },
                        {"name": "probability", "type": "float", "doc": "0-1"},
                    ],
                },
            },
        },
    ],
}


SCRIBE_SCHEMA = {
    "type": "record",
    "name": "scribe_message",
    "fields": [{"name": "payload", "type": "string"}],
}
