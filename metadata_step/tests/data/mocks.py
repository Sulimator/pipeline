object_mocks = [
    {
        "oid": "ZTF00llmn",
        "ndet": 1,
        "firstmjd": 55500,
        "g_r_max": 1.0,
        "g_r_mean_corr": 0.92,
        "meanra": 45.0,
        "meandec": 45.0,
    }
]

detection_mocks = [
    {
        "candid": 987654321,
        "oid": "ZTF00llmn",
        "mjd": 55500,
        "fid": 1,
        "pid": 245342400,
        "diffmaglim": 0.8,
        "isdiffpos": -1,
        "ra": 45.0,
        "dec": 45.0,
        "magpsf": 23.1,
        "sigmapsf": 0.9,
        "corrected": False,
        "dubious": False,
        "has_stamp": False,
        "step_id_corr": "step",
    },
    {
        "candid": 1234567890,
        "oid": "ZTF00llmn",
        "mjd": 55500,
        "fid": 1,
        "pid": 245342400,
        "diffmaglim": 0.8,
        "isdiffpos": -1,
        "ra": 45.0,
        "dec": 45.0,
        "magpsf": 23.1,
        "sigmapsf": 0.9,
        "corrected": False,
        "dubious": False,
        "has_stamp": False,
        "step_id_corr": "step",
    },
]

gaia_mocks = [
    {"oid": "ZTF00llmn", "candid": 987654321, "neargaia": 55.55, "unique1": True},
]

ps1_mocks = [
    {
        "oid": "ZTF00llmn",
        "candid": 987654321,
        "objectidps1": 55.55,
        "objectidps2": 44.44,
        "objectidps3": 33.33,
        "nmtchps": 1,
        "unique1": True,
        "unique2": True,
        "unique3": True,
    },
    {
        "oid": "ZTF00llmn",
        "candid": 1234567890,
        "objectidps1": 11.11,
        "objectidps2": 22.22,
        "objectidps3": 33.33,
        "nmtchps": 1,
        "unique1": True,
        "unique2": True,
        "unique3": True,
    },
]
