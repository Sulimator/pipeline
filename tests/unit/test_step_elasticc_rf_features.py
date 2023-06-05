from unittest import mock
from lc_classification.core.step import (
    LateClassifier,
)
from apf.producers import KafkaProducer
from apf.consumers import KafkaConsumer
from json import loads
from tests.mockdata.input_elasticc import INPUT_SCHEMA as INPUT_ELASTICC
from fastavro import utils
import pytest
import os

from tests.test_commons import (
    assert_elasticc_object_is_correct,
    assert_command_is_correct,
)

model_path = "https://assets.alerce.online/pipeline/elasticc/random_forest/2.0.1/"
step_mock_config = {
    "SCRIBE_PRODUCER_CONFIG": {"CLASS": "unittest.mock.MagicMock", "TOPIC": "test"},
    "PRODUCER_CONFIG": {"CLASS": "unittest.mock.MagicMock", "TOPIC": "test2"},
    "CONSUMER_CONFIG": {"CLASS": "unittest.mock.MagicMock", "TOPIC": "test3"},
    "MODEL_VERSION": "test",
    "PREDICTOR_CONFIG": {
        "PARAMS": {"model_path": model_path},
        "CLASS": "lc_classification.predictors.elasticc_random_forest.elasticc_random_forest_predictor.ElasticcRandomForestPredictor",
        "PARSER_CLASS": "lc_classification.predictors.elasticc_random_forest.elasticc_random_forest_parser.ElasticcRandomForestParser",
    },
    "SCRIBE_PARSER_CLASS": "lc_classification.core.parsers.scribe_parser.ScribeParser",
    "STEP_PARSER_CLASS": "lc_classification.core.parsers.elasticc_parser.ElasticcParser",
}

messages_elasticc = utils.generate_many(INPUT_ELASTICC, 10)


@pytest.mark.skipif(os.getenv("MODEL") != "elasticc", reason="elasticc only")
def test_step_elasticc():
    step = LateClassifier(config=step_mock_config)
    step.consumer = mock.MagicMock(KafkaConsumer)
    step.consumer.consume.return_value = messages_elasticc
    step.producer = mock.MagicMock(KafkaProducer)
    step.scribe_producer = mock.create_autospec(KafkaProducer)

    step.start()
    scribe_calls = step.scribe_producer.mock_calls

    # Tests scribe produces correct commands
    for call in scribe_calls:
        message = loads(call.args[0]["payload"])
        assert_command_is_correct(message)

    # Test producer produces correct data
    calls = step.producer.mock_calls
    for call in calls:
        obj = call.args[0]
        assert_elasticc_object_is_correct(obj)


@pytest.mark.skipif(os.getenv("MODEL") != "elasticc", reason="elasticc only")
def test_step_elasticc_without_features():
    step = LateClassifier(config=step_mock_config)
    step.consumer = mock.MagicMock(KafkaConsumer)
    empty_features = []
    for msg in messages_elasticc:
        msg["features"] = None
        empty_features.append(msg)
    step.consumer.consume.return_value = empty_features
    step.producer = mock.MagicMock(KafkaProducer)
    step.scribe_producer = mock.create_autospec(KafkaProducer)

    step.start()
    scribe_calls = step.scribe_producer.mock_calls

    # Tests scribe produces correct commands
    for call in scribe_calls:
        message = loads(call.args[0]["payload"])
        assert_command_is_correct(message)

    # Test producer produces correct data
    calls = step.producer.mock_calls
    for call in calls:
        obj = call.args[0]
        assert_elasticc_object_is_correct(obj)
