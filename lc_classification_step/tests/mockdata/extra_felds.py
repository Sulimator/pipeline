import random
import pickle
import datetime

diaobject_keys = [
    "hostgal2_ellipticity",
    "hostgal2_mag_Y",
    "hostgal2_mag_g",
    "hostgal2_mag_i",
    "hostgal2_mag_r",
    "hostgal2_mag_u",
    "hostgal2_mag_z",
    "hostgal2_magerr_Y",
    "hostgal2_magerr_g",
    "hostgal2_magerr_i",
    "hostgal2_magerr_r",
    "hostgal2_magerr_u",
    "hostgal2_magerr_z",
    "hostgal2_snsep",
    "hostgal2_sqradius",
    "hostgal2_zphot",
    "hostgal2_zphot_err",
    "hostgal2_zphot_q000",
    "hostgal2_zphot_q010",
    "hostgal2_zphot_q020",
    "hostgal2_zphot_q030",
    "hostgal2_zphot_q040",
    "hostgal2_zphot_q050",
    "hostgal2_zphot_q060",
    "hostgal2_zphot_q070",
    "hostgal2_zphot_q080",
    "hostgal2_zphot_q090",
    "hostgal2_zphot_q100",
    "hostgal2_zspec",
    "hostgal2_zspec_err",
    "hostgal_ellipticity",
    "hostgal_mag_Y",
    "hostgal_mag_g",
    "hostgal_mag_i",
    "hostgal_mag_r",
    "hostgal_mag_u",
    "hostgal_mag_z",
    "hostgal_magerr_Y",
    "hostgal_magerr_g",
    "hostgal_magerr_i",
    "hostgal_magerr_r",
    "hostgal_magerr_u",
    "hostgal_magerr_z",
    "hostgal_snsep",
    "hostgal_sqradius",
    "hostgal_zphot",
    "hostgal_zphot_err",
    "hostgal_zphot_q000",
    "hostgal_zphot_q010",
    "hostgal_zphot_q020",
    "hostgal_zphot_q030",
    "hostgal_zphot_q040",
    "hostgal_zphot_q050",
    "hostgal_zphot_q060",
    "hostgal_zphot_q070",
    "hostgal_zphot_q080",
    "hostgal_zphot_q090",
    "hostgal_zphot_q100",
    "hostgal_zspec",
    "hostgal_zspec_err",
    "mwebv",
    "mwebv_err",
    "z_final",
    "z_final_err",
]


def generate_extra_fields():
    diaobject = {}
    for key in diaobject_keys:
        diaobject[key] = random.random()
    return {
        "diaObject": pickle.dumps([diaobject]),
        "timestamp": datetime.datetime.now().timestamp(),
        "brokerIngestTimestamp": datetime.datetime.now().timestamp(),
    }
