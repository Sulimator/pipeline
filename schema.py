XMATCH = {
    "type": "map",
    "values": {"type": "map", "values": ["string", "float", "null"]},
}

DETECTIONS = {
    "type": "array",
    "items": {
        "name": "detections_record",
        "type": "record",
        "fields": [
            {"name": "oid", "type": "string"},
            {"name": "candid", "type": "long"},
            {"name": "mjd", "type": "float"},
            {"name": "fid", "type": "int"},
            {"name": "pid", "type": "float"},
            {"name": "diffmaglim", "type": "float"},
            {"name": "isdiffpos", "type": "int"},
            {"name": "nid", "type": "int"},
            {"name": "ra", "type": "float"},
            {"name": "dec", "type": "float"},
            {"name": "magpsf", "type": "float"},
            {"name": "sigmapsf", "type": "float"},
            {"name": "magap", "type": "float"},
            {"name": "sigmagap", "type": "float"},
            {"name": "distnr", "type": "float"},
            {"name": "rb", "type": "float"},
            {"name": "rbversion", "type": ["string", "null"]},
            {"name": "drb", "type": ["float", "null"]},
            {"name": "drbversion", "type": ["string", "null"]},
            {"name": "magapbig", "type": "float"},
            {"name": "sigmagapbig", "type": "float"},
            {"name": "rfid", "type": ["int", "null"]},
            {"name": "magpsf_corr", "type": ["float", "null"]},
            {"name": "sigmapsf_corr", "type": ["float", "null"]},
            {"name": "sigmapsf_corr_ext", "type": ["float", "null"]},
            {"name": "corrected", "type": "boolean"},
            {"name": "dubious", "type": "boolean"},
            {"name": "parent_candid", "type": ["long", "null"]},
            {"name": "has_stamp", "type": "boolean"},
            {"name": "step_id_corr", "type": "string"},
        ],
    },
}

NON_DETECTIONS = {
    "type": "array",
    "items": {
        "name": "non_detections_record",
        "type": "record",
        "fields": [
            {"name": "oid", "type": "string"},
            {"name": "mjd", "type": "float"},
            {"name": "diffmaglim", "type": "float"},
            {"name": "fid", "type": "int"},
        ],
    },
}

METADATA = {
    "name": "metadata",
    "type": "record",
    "fields": [
        {
            "name": "ps1",
            "type": {
                "name": "ps1",
                "type": "record",
                "fields": [
                    {"name": "simag1", "type": ["float", "null"]},
                    {"name": "objectidps3", "type": ["double", "null"]},
                    {"name": "objectidps1", "type": ["double", "null"]},
                    {"name": "unique1", "type": ["boolean", "null"]},
                    {"name": "unique2", "type": ["boolean", "null"]},
                    {"name": "szmag2", "type": ["double", "null"]},
                    {"name": "srmag3", "type": ["float", "null"]},
                    {"name": "sgscore1", "type": ["float", "null"]},
                    {"name": "szmag3", "type": ["float", "null"]},
                    {"name": "srmag1", "type": ["float", "null"]},
                    {"name": "sgmag1", "type": ["float", "null"]},
                    {"name": "szmag1", "type": ["float", "null"]},
                    {"name": "distpsnr1", "type": ["float", "null"]},
                    {"name": "sgscore2", "type": ["float", "null"]},
                    {"name": "candid", "type": ["long", "null"]},
                    {"name": "simag3", "type": ["float", "null"]},
                    {"name": "objectidps2", "type": ["double", "null"]},
                    {"name": "srmag2", "type": ["float", "null"]},
                    {"name": "unique3", "type": ["boolean", "null"]},
                    {"name": "sgmag3", "type": ["float", "null"]},
                    {"name": "sgmag2", "type": ["double", "null"]},
                    {"name": "simag2", "type": ["float", "null"]},
                    {"name": "distpsnr2", "type": ["float", "null"]},
                    {"name": "distpsnr3", "type": ["float", "null"]},
                    {"name": "nmtchps", "type": ["int", "null"]},
                    {"name": "sgscore3", "type": ["float", "null"]},
                ],
            },
        },
        {
            "name": "ss",
            "type": {
                "name": "ss",
                "type": "record",
                "fields": [
                    {"name": "ssdistnr", "type": ["double", "null"]},
                    {"name": "ssmagnr", "type": ["double", "null"]},
                    {"name": "ssnamenr", "type": ["string", "null"]},
                ],
            },
        },
        {
            "name": "reference",
            "type": {
                "name": "reference",
                "type": "record",
                "fields": [
                    {"name": "magnr", "type": "float"},
                    {"name": "ranr", "type": "float"},
                    {"name": "field", "type": "int"},
                    {"name": "chinr", "type": "float"},
                    {"name": "mjdstartref", "type": "float"},
                    {"name": "mjdendref", "type": "float"},
                    {"name": "decnr", "type": "float"},
                    {"name": "sharpnr", "type": "float"},
                    {"name": "candid", "type": "long"},
                    {"name": "nframesref", "type": "int"},
                    {"name": "rcid", "type": "int"},
                    {"name": "rfid", "type": "int"},
                    {"name": "fid", "type": "int"},
                    {"name": "sigmagnr", "type": "float"},
                ],
            },
        },
        {
            "name": "gaia",
            "type": {
                "name": "gaia",
                "type": "record",
                "fields": [
                    {"name": "maggaiabright", "type": ["float", "null"]},
                    {"name": "neargaiabright", "type": ["float", "null"]},
                    {"name": "unique1", "type": "boolean"},
                    {"name": "neargaia", "type": ["float", "null"]},
                    {"name": "maggaia", "type": ["float", "null"]},
                ],
            },
        },
    ],
}

SCHEMA = {
    "doc": "Light curve",
    "name": "light_curve",
    "type": "record",
    "fields": [
        {"name": "oid", "type": "string"},
        {"name": "candid", "type": "long"},
        {"name": "detections", "type": DETECTIONS},
        {
            "name": "non_detections",
            "type": NON_DETECTIONS,
        },
        {"name": "xmatches", "type": [XMATCH, "null"], "default": "null"}
        {"name": "fid", "type": "int"},
        {
            "name": "metadata",
            "type": METADATA_2,
        },
        {"name": "preprocess_step_id", "type": "string"},
        {"name": "preprocess_step_version", "type": "string"},
    ],
}
