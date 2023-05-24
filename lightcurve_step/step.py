from typing import List

import numpy as np
import pandas as pd
from apf.core.step import GenericStep
from db_plugins.db.mongo import MongoConnection
from db_plugins.db.mongo.models import Detection, NonDetection, ForcedPhotometry


class LightcurveStep(GenericStep):
    def __init__(self, config: dict, db_client: MongoConnection):
        super().__init__(config=config)
        self.db_client = db_client
        self.db_client.connect(config["DB_CONFIG"])

    @classmethod
    def pre_execute(cls, messages: List[dict]) -> dict:
        aids, detections, non_detections = set(), [], []
        for msg in messages:
            aids.add(msg["aid"])
            detections.extend([det | {"new": True} for det in msg["detections"]])
            non_detections.extend(msg["non_detections"])
        return {
            "aids": aids,
            "detections": detections,
            "non_detections": non_detections,
        }

    def execute(self, messages: dict) -> dict:
        """Queries the database for all detections and non-detections for each AID and removes duplicates"""
        query_detections = self.db_client.query(Detection)
        query_non_detections = self.db_client.query(NonDetection)
        query_forced_photometries = self.db_client.query(ForcedPhotometry)

        db_detections = query_detections.collection.aggregate(
            [
                {"$match": {"aid": {"$in": list(messages["aids"])}}},
                {
                    "$addFields": {
                        "candid": "$_id",
                        "forced": False,
                        "new": False,
                    }
                },
                {"$project": {"_id": False}},
            ]
        )
        db_non_detections = query_non_detections.collection.find(
            {"aid": {"$in": list(messages["aids"])}}, {"_id": False}
        )

        db_forced_photometries = query_forced_photometries.collection.aggregate(
            [
                {"$match": {"aid": {"$in": list(messages["aids"])}}},
                {"$addFields": {"candid": "$_id", "forced": True, "new": False}},
                {"$project": {"_id": False}},
            ]
        )

        detections = pd.DataFrame(
            messages["detections"] + list(db_detections) + list(db_forced_photometries)
        )
        non_detections = pd.DataFrame(
            messages["non_detections"] + list(db_non_detections)
        )

        # Try to keep those with stamp coming from the DB if there are clashes
        detections = detections.sort_values(
            ["has_stamp", "new"], ascending=[False, True]
        ).drop_duplicates("candid", keep="first")
        non_detections = non_detections.drop_duplicates(["oid", "fid", "mjd"])

        return {
            "detections": detections.replace(np.nan, None).to_dict("records"),
            "non_detections": non_detections.replace(np.nan, None).to_dict("records"),
        }

    @classmethod
    def pre_produce(cls, result: dict) -> List[dict]:
        detections = pd.DataFrame(result["detections"]).groupby("aid")
        try:  # At least one non-detection
            non_detections = pd.DataFrame(result["non_detections"]).groupby("aid")
        except (
            KeyError
        ):  # to reproduce expected error for missing non-detections in loop
            non_detections = pd.DataFrame(columns=["aid"]).groupby("aid")
        output = []
        for aid, dets in detections:
            try:
                nd = non_detections.get_group(aid).to_dict("records")
            except KeyError:
                nd = []
            output.append(
                {
                    "aid": aid,
                    "detections": dets.to_dict("records"),
                    "non_detections": nd,
                }
            )
        return output
