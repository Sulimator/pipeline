from unittest import mock
from lc_classification.core.step import (
    LateClassifier,
)
from apf.producers import KafkaProducer
from apf.consumers import KafkaConsumer
from json import loads
from tests.mockdata.input_ztf import INPUT_SCHEMA as INPUT_ZTF
from fastavro import utils
import pytest
import os


step_mock_config = {
    "SCRIBE_PRODUCER_CONFIG": {"CLASS": "unittest.mock.MagicMock", "TOPIC": "test"},
    "PRODUCER_CONFIG": {"CLASS": "unittest.mock.MagicMock", "TOPIC": "test2"},
    "CONSUMER_CONFIG": {"CLASS": "unittest.mock.MagicMock", "TOPIC": "test3"},
    "MODEL_VERSION": "test",
    "PREDICTOR_CONFIG": {
        "PARAMS": {},
        "CLASS": "lc_classification.predictors.ztf_random_forest.ztf_random_forest_predictor.ZtfRandomForestPredictor",
        "PARSER_CLASS": "lc_classification.predictors.ztf_random_forest.ztf_random_forest_parser.ZtfRandomForestParser",
    },
    "SCRIBE_PARSER_CLASS": "lc_classification.core.parsers.scribe_parser.ScribeParser",
    "STEP_PARSER_CLASS": "lc_classification.core.parsers.alerce_parser.AlerceParser",
}

messages_ztf = utils.generate_many(INPUT_ZTF, 10)


def assert_object_is_correct(obj):
    assert "aid" in obj
    assert "features" in obj
    assert "lc_classification" in obj
    assert len(obj["lc_classification"]["probabilities"]) > 0


def assert_command_is_correct(command):
    assert command["collection"] == "object"
    assert command["type"] == "update_probabilities"
    assert command["criteria"]["_id"] is not None
    assert "aid" not in command["data"]
    assert not command["options"]["set_on_insert"]


@pytest.mark.skipif(os.getenv("STREAM") != "ztf", reason="ztf only")
def test_step():
    step = LateClassifier(config=step_mock_config)
    step.consumer = mock.MagicMock(KafkaConsumer)
    step.consumer.consume.return_value = messages_ztf
    step.producer = mock.MagicMock(KafkaProducer)
    step.scribe_producer = mock.create_autospec(KafkaProducer)

    step.start()
    scribe_calls = step.scribe_producer.mock_calls

    # Tests scribe produces correct commands
    assert len(scribe_calls) > 0
    for call in scribe_calls:
        message = loads(call.args[0]["payload"])
        assert_command_is_correct(message)

    # Test producer produces correct data
    calls = step.producer.mock_calls
    assert len(calls) > 0
    for call in calls:
        obj = call.args[0]
        assert_object_is_correct(obj)


@pytest.mark.skipif(os.getenv("STREAM") != "ztf", reason="ztf only")
def test_step_empty_features():
    step = LateClassifier(config=step_mock_config)
    step.consumer = mock.MagicMock(KafkaConsumer)
    empty_features = []
    for msg in messages_ztf:
        msg["features"] = None
        empty_features.append(msg)
    step.consumer.consume.return_value = empty_features
    step.producer = mock.MagicMock(KafkaProducer)
    step.scribe_producer = mock.create_autospec(KafkaProducer)

    step.start()
    scribe_calls = step.scribe_producer.mock_calls
    assert scribe_calls == []
    calls = step.producer.mock_calls
    assert calls == []
