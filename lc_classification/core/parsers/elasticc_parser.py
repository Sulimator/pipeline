from ..utils.no_class_post_processor import (
    NoClassifiedPostProcessor,
)
from .kafka_parser import KafkaOutput, KafkaParser
from lc_classification.predictors.predictor.predictor_parser import PredictorOutput
import pandas as pd
import datetime
from lc_classification.core.parsers.classes.elasticc_mapper import ClassMapper

class ElasticcParser(KafkaParser):
    def parse(self, model_output: PredictorOutput, **kwargs) -> KafkaOutput[list]:
        # create a hashmap that contains the new info (candid, oid and timestamps)
        detection_extra_info = {}

        messages = kwargs["messages"]
        for message in messages:
            new_detection = [
                det for det in message["detections"] if det["new"] and det["has_stamp"]
            ]

            if len(new_detection) == 0:
                continue

            new_detection = new_detection[0]

            detection_extra_info[new_detection["aid"]] = {
                "candid": new_detection["candid"],
                "oid": new_detection["oid"],
            }
        predictions = model_output.classifications["probabilities"]
        messages = kwargs.get("messages", pd.DataFrame())
        messages = pd.DataFrame().from_records(messages)
        predictions = NoClassifiedPostProcessor(
            messages, predictions
        ).get_modified_classifications()
        predictions["aid"] = predictions.index
        classifier_name = kwargs["classifier_name"]
        classifier_version = kwargs["classifier_version"]
        for class_name in ClassMapper.get_class_names():
            if class_name not in predictions.columns:
                predictions[class_name] = 0.0
        classifications = predictions.to_dict(orient="records")
        output = []
        for classification in classifications:
            aid = classification.pop("aid")
            if "classifier_name" in classification:
                classification.pop("classifier_name")

            output_classification = [
                {
                    "classId": ClassMapper.get_class_value(predicted_class),
                    "probability": prob,
                }
                for predicted_class, prob in classification.items()
            ]
            response = {
                "alertId": int(detection_extra_info[aid]["candid"]),
                "diaSourceId": int(detection_extra_info[aid]["oid"]),
                "elasticcPublishTimestamp": 0,  # TODO: get this from extraFields
                "brokerIngestTimestamp": None,  # TODO: get this from extraFields
                "classifications": output_classification,
                "brokerVersion": classifier_version,
                "classifierName": classifier_name,
                "classifierParams": classifier_version,
                "brokerName": "ALeRCE",
                "brokerPublishTimestamp": int(
                    datetime.datetime.now().timestamp() * 1000
                ),
            }
            output.append(response)
        return KafkaOutput(output)
