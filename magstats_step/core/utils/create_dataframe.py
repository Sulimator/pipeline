from typing import List
import pandas as pd


def generate_detections_dataframe(detections: List[dict]) -> pd.DataFrame:
    extra_columns = ["candid", "distpsnr1", "sgscore1", "chinr", "sharpnr"]
    extras = [{"candid": det["candid"], **det["extra_fields"]} for det in detections]
    detections = pd.DataFrame.from_records(
        detections, exclude=["extra_fields"], index="candid"
    )
    extras = pd.DataFrame.from_records(extras, columns=extra_columns, index="candid")
    return detections.join(extras)


def generate_non_detections_dataframe(nd: List[dict]) -> pd.DataFrame:
    return pd.DataFrame.from_records(nd).sort_values("mjd")
