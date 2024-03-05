import random
import pathlib

from fastavro import schema
from fastavro import utils

SCHEMA_PATH = str(
    pathlib.Path(
        pathlib.Path(__file__).parent.parent.parent.parent.parent,
        "schemas/correction_step",
        "output.avsc",
    )
)

SCHEMA = schema.load_schema(SCHEMA_PATH)

aids_pool = [f"AID22X{i}" for i in range(3)]
ztf_oids_pool = [f"ZTF{i}llmn" for i in range(5)]
atlas_oids_pool = [f"{i}" for i in range(5)]

data = list(utils.generate_many(SCHEMA, 10))
for d in data:
    if random.random() < 0.5:
        sid = "ZTF"
        oid = random.choice(ztf_oids_pool)
        fid = random.choice(["r", "g"])
    else:
        sid = "ATLAS"
        oid = random.choice(atlas_oids_pool)
        fid = random.choice(["o", "c"])
    aid = random.choice(aids_pool)
    d["oid"] = oid
    for detection in d["detections"]:
        detection["aid"] = aid
        detection["oid"] = oid
        detection["sid"] = sid
        detection["fid"] = fid
        detection["forced"] = False

    for non_detection in d["non_detections"]:
        non_detection["aid"] = aid
        non_detection["oid"] = oid
        non_detection["sid"] = sid
        non_detection["fid"] = fid
