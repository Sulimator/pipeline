from ..utils.no_class_post_processor import (
    NoClassifiedPostProcessor,
)
from .kafka_parser import KafkaOutput, KafkaParser
from lc_classification.predictors.predictor.predictor_parser import PredictorOutput
import numpy as np
import pandas as pd
import datetime


class ElasticcParser(KafkaParser):
    _class_mapper = {
        "Periodic/Other": 210,
        "Cepheid": 211,
        "RR Lyrae": 212,
        "Delta Scuti": 213,
        "EB": 214,
        "LPV/Mira": 215,
        "Non-Periodic/Other": 220,
        "AGN": 221,
        "SN-like/Other": 110,
        "Ia": 111,
        "Ib/c": 112,
        "II": 113,
        "Iax": 114,
        "91bg": 115,
        "Fast/Other": 120,
        "KN": 121,
        "M-dwarf Flare": 122,
        "Dwarf Novae": 123,
        "uLens": 124,
        "Long/Other": 130,
        "SLSN": 131,
        "TDE": 132,
        "ILOT": 133,
        "CART": 134,
        "PISN": 135,
        "no_class": 0,
    }

    def parse(self, model_output: PredictorOutput, **kwargs) -> KafkaOutput[list]:
        predictions = model_output.classifications["probabilities"]
        messages = kwargs.get("messages", pd.DataFrame())
        messages = pd.DataFrame().from_records(messages)
        predictions = NoClassifiedPostProcessor(
            messages, predictions
        ).get_modified_classifications()
        classifier_name = kwargs["classifier_name"]
        classifier_version = kwargs["classifier_version"]
        for class_name in self._class_mapper.keys():
            if class_name not in predictions.columns:
                predictions[class_name] = 0.0
        classifications = predictions.to_dict(orient="records")
        output = []
        for classification in classifications:
            output_classification = [
                {
                    "classId": self._class_mapper[predicted_class],
                    "probability": prob,
                }
                for predicted_class, prob in classification.items()
            ]
            response = {
                "classifications": output_classification,
                "brokerVersion": classifier_version,
                "classifierName": classifier_name,
                "classifierParams": classifier_version,
            }

            response["brokerPublishTimestamp"] = int(
                datetime.datetime.now().timestamp() * 1000
            )
            response["brokerName"] = "ALeRCE"
            output.append(response)
        return KafkaOutput(output)
