from typing import List
import pandas as pd
from apf.core import get_class
from apf.core.step import GenericStep
from lc_classification.core.parsers.kafka_parser import KafkaParser
import logging
import json
import numexpr
from lc_classification.predictors.predictor.predictor import Predictor
from lc_classification.predictors.predictor.predictor_parser import PredictorParser
from alerce_classifiers.base.dto import InputDTO, OutputDTO
from lc_classification.core.parsers.input_dto import create_input_dto
from lc_classifier.classifier.models import HierarchicalRandomForest


class LateClassifier(GenericStep):
    """Light Curve Classification Step, for a description of the algorithm used
    to process check the `execute()` method.

    Parameters
    ----------
    consumer : GenericConsumer
        Description of parameter `consumer`.
    **step_args : type
        Other args passed to step (DB connections, API requests, etc.)

    """

    base_name = "lc_classifier"

    def __init__(self, config={}, level=logging.INFO, model=None, **step_args):
        super().__init__(config=config, level=level, **step_args)
        numexpr.utils.set_num_threads(1)

        self.isztf = (
            config["MODEL_CONFIG"]["CLASS"]
            == "lc_classifier.classifier.models.HierarchicalRandomForest"
        )

        self.logger.info("Loading Models")

        if model:
            self.model = model

        else:
            if self.isztf:
                self.model = get_class(config["MODEL_CONFIG"]["CLASS"])()
                self.model.download_model()
                self.model.load_model(self.model.MODEL_PICKLE_PATH)
            else:
                # inicializar mapper
                mapper_class = config["MODEL_CONFIG"].get("MAPPER_CLASS")
                if mapper_class:
                    mapper = get_class(mapper_class)()
                    self.model = get_class(config["MODEL_CONFIG"]["CLASS"])(
                        **config["MODEL_CONFIG"]["PARAMS"], mapper=mapper
                    )
                else:
                    self.model = get_class(config["MODEL_CONFIG"]["CLASS"])(
                        **config["MODEL_CONFIG"]["PARAMS"]
                    )

        self.scribe_producer = get_class(config["SCRIBE_PRODUCER_CONFIG"]["CLASS"])(
            config["SCRIBE_PRODUCER_CONFIG"]
        )
        self.scribe_parser: KafkaParser = get_class(config["SCRIBE_PARSER_CLASS"])()
        self.step_parser: KafkaParser = get_class(config["STEP_PARSER_CLASS"])()

        self.classifier_name = self.config["MODEL_CONFIG"]["NAME"]
        self.classifier_version = (self.config["MODEL_VERSION"],)

    def pre_produce(self, result: tuple):
        return self.step_parser.parse(
            result[0],
            messages=result[1],
            features=result[2],
            classifier_name=self.classifier_name,
            classifier_version=self.classifier_version,
        ).value

    def produce_scribe(self, commands: List[dict]):
        for command in commands:
            self.scribe_producer.produce({"payload": json.dumps(command)})

    def execute(self, messages):
        """Run the classification.

        Parameters
        ----------
        messages : dict-like
            Current object data, it must have the features and object id.

        """
        self.logger.info("Processing %i messages.", len(messages))
        self.logger.info("Getting batch alert data")
        model_input = create_input_dto(messages)

        if self.isztf:
            model_input = model_input.features

        self.logger.info("Doing inference")
        if self.isztf:
            probabilities = self.model.predict_in_pipeline(model_input)
        else:
            probabilities = self.model.predict(model_input)

        if self.isztf:
            # some test need this
            if isinstance(probabilities, OutputDTO):
                probabilities = {
                    "probabilities": probabilities.probabilities,
                    "hierarchical": {"top": pd.DataFrame(), "children": pd.DataFrame()},
                }

        self.logger.info("Processing results")
        return {
            "public_info": (probabilities, messages, model_input),
            "db_results": self.scribe_parser.parse(
                probabilities, classifier_version=self.config["MODEL_VERSION"]
            ),
        }

    def post_execute(self, result: dict):
        db_results = result.pop("db_results")
        self.produce_scribe(db_results.value)
        return result["public_info"]
