##################################################
#       Late Classifier Settings File
##################################################
import os
from features_schema import FEATURES_SCHEMA

CONSUMER_CONFIG = {
    "CLASS": os.getenv("CONSUMER_CLASS", "apf.consumers.KafkaConsumer"),
    "TOPICS": os.environ["CONSUMER_TOPICS"].strip().split(","),
    "PARAMS": {
        "bootstrap.servers": os.environ["CONSUMER_SERVER"],
        "group.id": os.environ["CONSUMER_GROUP_ID"],
        "auto.offset.reset":"smallest"
    }
}

DB_CONFIG = {
    "SQL": {
        "ENGINE": os.getenv("DB_ENGINE", "postgresql"),
        "HOST": os.environ["DB_HOST"],
        "USER": os.environ["DB_USER"],
        "PASSWORD": os.environ["DB_PASSWORD"],
        "PORT": int(os.getenv("DB_PORT",5432)),
        "DB_NAME": os.environ["DB_NAME"]
    }
}

PRODUCER_CONFIG = {
    "TOPIC": os.environ["PRODUCER_TOPIC"],
    "PARAMS": {
        'bootstrap.servers': os.environ["PRODUCER_SERVER"],
    },
    "SCHEMA": {
        'doc': 'Late Classification',
        'name': 'probabilities_and_features',
        'type': 'record',
        'fields': [
            {'name': 'oid', 'type': 'string'},
            {"name": "candid", "type": "long"},
            FEATURES_SCHEMA,
            {
                'name': 'late_classification',
                'type': {
                    'type': 'record',
                    'name': 'late_record',
                    'fields': [
                        {
                            'name': 'probabilities',
                            'type': {
                                'type': 'map',
                                'values': ['float'],
                            }
                        },
                        {
                            'name': 'class',
                            'type': 'string'
                        },
                        {
                            'name': 'hierarchical',
                            'type':
                            {
                                'name': 'root',
                                'type': 'map',
                                'values': [
                                    {
                                        'type': 'map',
                                        'values': 'float'
                                    },
                                    {
                                        'type': 'map',
                                        'values': {
                                            'type': 'map',
                                            'values': 'float'
                                        }
                                    }
                                ]
                            }
                        }
                    ]
                }
            }
        ]
    }
}

METRICS_CONFIG = {
    "CLASS": "apf.metrics.KafkaMetricsProducer",
    "PARAMS": {
        "PARAMS": {
            "bootstrap.servers": os.environ["METRICS_HOST"],
            "auto.offset.reset":"smallest"},
        "TOPIC": os.environ["METRICS_TOPIC"],
        "SCHEMA": {
            "$schema": "http://json-schema.org/draft-07/schema",
            "$id": "http://example.com/example.json",
            "type": "object",
            "title": "The root schema",
            "description": "The root schema comprises the entire JSON document.",
            "default": {},
            "examples": [
                {"timestamp_sent": "2020-09-01", "timestamp_received": "2020-09-01"}
            ],
            "required": ["timestamp_sent", "timestamp_received"],
            "properties": {
                "timestamp_sent": {
                    "$id": "#/properties/timestamp_sent",
                    "type": "string",
                    "title": "The timestamp_sent schema",
                    "description": "Timestamp sent refers to the time at which a message is sent.",
                    "default": "",
                    "examples": ["2020-09-01"],
                },
                "timestamp_received": {
                    "$id": "#/properties/timestamp_received",
                    "type": "string",
                    "title": "The timestamp_received schema",
                    "description": "Timestamp received refers to the time at which a message is received.",
                    "default": "",
                    "examples": ["2020-09-01"],
                },
            },
            "additionalProperties": True,
        },
    },
}

STEP_METADATA = {
    "STEP_VERSION": os.getenv("STEP_VERSION", "dev"),
    "STEP_ID": os.getenv("STEP_ID", "late_classification"),
    "STEP_NAME": os.getenv("STEP_NAME", "late classification"),
    "STEP_COMMENTS": os.getenv("STEP_COMMENTS", ""),
}

STEP_CONFIG = {
    "DB_CONFIG": DB_CONFIG,
    "PRODUCER_CONFIG": PRODUCER_CONFIG,
    "STEP_METADATA": STEP_METADATA,
    "METRICS_CONFIG": METRICS_CONFIG,
}
