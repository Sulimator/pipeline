import pytest
import unittest
from fastavro.schema import load_schema

from xmatch_step import XmatchStep
from xmatch_step.core.xmatch_client import XmatchClient
from schema import SCHEMA
from unittest import mock
from tests.data.messages import (
    generate_input_batch,
    get_fake_xmatch,
    get_fake_empty_xmatch,
)
import os

PRODUCER_SCHEMA_PATH = os.path.join(os.path.dirname(__file__), "test_producer_schema.avsc")
SCRIBE_SCHEMA_PATH =  os.path.join(os.path.dirname(__file__), "../../scribe_schema.avsc")

CONSUMER_CONFIG = {
    "CLASS": "apf.consumers.KafkaConsumer",
    "PARAMS": {
        "bootstrap.servers": "localhost:9092",
        "group.id": "group_id",
        "auto.offset.reset": "beginning",
        "enable.partition.eof": False,
    },
    "TOPICS": ["correction"],
    "consume.messages": "1",
    "consume.timeout": "10",
}

PRODUCER_CONFIG = {
    "CLASS": "apf.producers.KafkaProducer",
    "TOPIC": "xmatch",
    "PARAMS": {
        "bootstrap.servers": "localhost:9092",
    },
    "SCHEMA_PATH": PRODUCER_SCHEMA_PATH,
}

SCRIBE_PRODUCER_CONFIG = {
    "CLASS": "apf.producers.KafkaProducer",
    "TOPIC": "w_object",
    "PARAMS": {"bootstrap.servers": "localhost:9092"},
    "SCHEMA_PATH": SCRIBE_SCHEMA_PATH,
}

XMATCH_CONFIG = {
    "CATALOG": {
        "name": "allwise",
        "columns": [
            "AllWISE",
            "RAJ2000",
            "DEJ2000",
            "W1mag",
            "W2mag",
            "W3mag",
            "W4mag",
            "e_W1mag",
            "e_W2mag",
            "e_W3mag",
            "e_W4mag",
            "Jmag",
            "e_Jmag",
            "Hmag",
            "e_Hmag",
            "Kmag",
            "e_Kmag",
        ],
    }
}


@pytest.mark.usefixtures("kafka_service")
class StepXmatchTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.step_config = {
            "CONSUMER_CONFIG": CONSUMER_CONFIG,
            "PRODUCER_CONFIG": PRODUCER_CONFIG,
            "SCRIBE_PRODUCER_CONFIG": SCRIBE_PRODUCER_CONFIG,
            "XMATCH_CONFIG": XMATCH_CONFIG,
            "RETRIES": 3,
            "RETRY_INTERVAL": 1,
        }
        cls.step = XmatchStep(config=cls.step_config)
        cls.batch = generate_input_batch(20)

    @mock.patch.object(XmatchClient, "execute")
    def test_execute(self, mock_xmatch: mock.Mock):
        mock_xmatch.return_value = get_fake_xmatch(self.batch)
        output_messages, xmatches, oids = self.step.execute(self.batch)
        for oid in oids.values():
            assert isinstance(oid, list)
        assert len(output_messages) == 20
        assert xmatches.shape == (20, 22)

    @mock.patch.object(XmatchClient, "execute")
    def test_execute_empty_xmatch(self, mock_xmatch: mock.Mock):
        mock_xmatch.return_value = get_fake_empty_xmatch(self.batch)
        output_messages, xmatches, oids = self.step.execute(self.batch)
        for oid in oids.values():
            assert isinstance(oid, list)
        assert len(output_messages) == 20
        assert xmatches.shape == (0, 5)
