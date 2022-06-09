import unittest

import pytest
from confluent_kafka import Producer
from cmirrormaker.step import CustomMirrormaker
from cmirrormaker.utils import RawKafkaConsumer
from tests.unittest.data.datagen import create_data


STEP_METADATA = {
    'STEP_VERSION': 'test',
    'STEP_ID': 'cmirrormaker',
    'STEP_NAME': 'cmirrormaker',
    'STEP_COMMENTS': 'test version',
}

PRODUCER_CONFIG = {
    'TOPIC': 'test',
    'PARAMS': {
        'bootstrap.servers': 'localhost:9093'
    }
}

CONSUMER_CONFIG = {
    'CLASS': 'cmirrormaker.utils.RawKafkaConsumer',
    'TOPICS': ['test_topic'],
    'PARAMS': {
        'bootstrap.servers': 'localhost:9092',
        'group.id': 'cmirrormaker_test',
        'auto.offset.reset': 'beginning',
        'enable.partition.eof': True
    },
    'consume.timeout': 1,
    'consume.messages': 1,
}


@pytest.mark.usefixtures("kafka_service")
class MyTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.step_config = {
            'PRODUCER_CONFIG': PRODUCER_CONFIG,
            'STEP_METADATA': STEP_METADATA
        }

    def test_step_exection_copies_full_topic(self):
        n_messages = 10
        external = Producer({'bootstrap.servers': 'localhost:9092'})
        rkconsumer = RawKafkaConsumer(CONSUMER_CONFIG)
        step = CustomMirrormaker(consumer=rkconsumer, config=self.step_config)

        messages = create_data(n_messages)
        for msg in messages:
            external.produce(topic='test_topic', value=repr(msg))
        external.flush()

        step.start()
