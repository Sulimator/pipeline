from typing import Tuple
from apf.core.step import GenericStep
from prv_candidates_step.core.candidates.process_prv_candidates import (
    process_prv_candidates,
)
from prv_candidates_step.core.strategy.ztf_strategy import ZTFPrvCandidatesStrategy
from prv_candidates_step.core.processor.processor import Processor
from prv_candidates_step.core import ZTFPreviousDetectionsParser, ZTFNonDetectionsParser


import logging


class PrvCandidatesStep(GenericStep):
    """PrvDetectionStep Description

    Parameters
    ----------
    consumer : GenericConsumer
        Description of parameter `consumer`.
    **step_args : type
        Other args passed to step (DB connections, API requests, etc.)

    """

    def __init__(
        self,
        config,
        level=logging.INFO,
        **step_args,
    ):
        super().__init__(config=config, level=level, **step_args)
        self.prv_candidates_processor = Processor(
            ZTFPrvCandidatesStrategy()
        )  # initial strategy (can change)
        self.producers = {"scribe": None, "alerts": None}

    def pre_produce(self, result: Tuple):
        self.set_producer_key_field("aid")
        output = []
        for index, alert in enumerate(result[0]):
            ztf_prv_detections_parser = ZTFPreviousDetectionsParser()
            ztf_non_detections_parser = ZTFNonDetectionsParser()
            parsed_prv_detections = ztf_prv_detections_parser.parse(
                result[1][index], alert["oid"], alert["aid"], alert["candid"]
            )
            parsed_non_detections = ztf_non_detections_parser.parse(
                result[2][index], alert["aid"], alert["tid"], alert["oid"]
            )
            output.append(
                {
                    "aid": alert["aid"],
                    "new_alert": alert,
                    "prv_detections": parsed_prv_detections,
                    "non_detections": parsed_non_detections,
                }
            )
        return output

    def execute(self, messages):
        self.logger.info("Processing %s alerts", str(len(messages)))
        prv_detections, non_detections = process_prv_candidates(
            self.prv_candidates_processor, messages
        )

        return messages, prv_detections, non_detections
