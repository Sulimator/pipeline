import json
import os
from typing import Callable

import pytest
from apf.consumers import KafkaConsumer

from lc_classification.core.step import LateClassifier
from tests.test_commons import (
    assert_command_is_correct,
    assert_elasticc_object_is_correct,
)


@pytest.mark.elasticc
def test_step_elasticc_result(
    kafka_service,
    env_variables_elasticc,
    kafka_consumer: Callable[[str], KafkaConsumer],
    scribe_consumer: Callable[[], KafkaConsumer],
):
    env_variables_elasticc(
        "barney",
        "alerce_classifiers.rf_features_header_classifier.model.RandomForestFeaturesHeaderClassifier",
        {
            "MODEL_PATH": os.getenv("TEST_BARNEY_MODEL_PATH"),
            "MAPPER_CLASS": "alerce_classifiers.rf_features_header_classifier.mapper.BarneyMapper",
        },
    )

    from settings import STEP_CONFIG

    kconsumer = kafka_consumer("barney")
    sconsumer = scribe_consumer()

    step = LateClassifier(config=STEP_CONFIG)
    step.start()

    for message in kconsumer.consume():
        assert_elasticc_object_is_correct(message)
        kconsumer.commit()

    for message in sconsumer.consume():
        command = json.loads(message["payload"])
        assert_command_is_correct(command)
        sconsumer.commit()
