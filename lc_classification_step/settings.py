##################################################
#       Late Classifier Settings File
##################################################
import os
from schemas import SCHEMA, SCRIBE_SCHEMA
from models_settings import configurator
from fastavro.schema import load_schema
from fastavro.repository.base import SchemaRepositoryError

# SCHEMA PATH RELATIVE TO THE SETTINGS FILE
PRODUCER_SCHEMA_PATH = os.path.join(os.path.dirname(__file__), os.getenv("PRODUCER_SCHEMA_PATH"))
METRICS_SCHEMA_PATH = os.path.join(os.path.dirname(__file__), os.getenv("METRIS_SCHEMA_PATH"))
SCRIBE_SCHEMA_PATH =  os.path.join(os.path.dirname(__file__), os.getenv("SCRIBE_SCHEMA_PATH"))

CONSUMER_CONFIG = {
    "CLASS": os.getenv("CONSUMER_CLASS", "apf.consumers.KafkaConsumer"),
    "TOPICS": os.environ["CONSUMER_TOPICS"].strip().split(","),
    "PARAMS": {
        "bootstrap.servers": os.environ["CONSUMER_SERVER"],
        "group.id": os.environ["CONSUMER_GROUP_ID"],
        "auto.offset.reset": "beginning",
        "enable.partition.eof": bool(os.getenv("ENABLE_PARTITION_EOF", None)),
    },
    "consume.timeout": int(os.getenv("CONSUME_TIMEOUT", 0)),
    "consume.messages": int(os.getenv("CONSUME_MESSAGES", 1000)),
}

PRODUCER_CONFIG = {
    "TOPIC_STRATEGY": {
        "PARAMS": {
            "topic_format": os.environ["PRODUCER_TOPIC_FORMAT"],
            "date_format": os.environ["PRODUCER_DATE_FORMAT"],
            "change_hour": int(os.environ["PRODUCER_CHANGE_HOUR"]),
            "retention_days": int(os.environ["PRODUCER_RETENTION_DAYS"]),
        },
        "CLASS": os.getenv(
            "PRODUCER_TOPIC_STRATEGY_CLASS",
            "apf.core.topic_management.DailyTopicStrategy",
        ),
    },
    "PARAMS": {
        "bootstrap.servers": os.environ["PRODUCER_SERVER"],
    },
    "CLASS": os.getenv("PRODUCER_CLASS", "apf.producers.kafka.KafkaProducer"),
    "SCHEMA_PATH": PRODUCER_SCHEMA_PATH,
}

SCRIBE_PRODUCER_CONFIG = {
    "CLASS": "apf.producers.KafkaProducer",
    "PARAMS": {
        "bootstrap.servers": os.environ["SCRIBE_SERVER"],
    },
    "TOPIC": os.environ["SCRIBE_TOPIC"],
    "SCHEMA_PATH": SCRIBE_SCHEMA_PATH,
}

METRICS_CONFIG = {
    "CLASS": "apf.metrics.KafkaMetricsProducer",
    "EXTRA_METRICS": [
        {"key": "aid", "alias": "aid"},
    ],
    "PARAMS": {
        "PARAMS": {
            "bootstrap.servers": os.environ["METRICS_HOST"],
        },
        "TOPIC": os.environ["METRICS_TOPIC"],
        "SCHEMA_PATH": METRICS_SCHEMA_PATH,
    },
}

if os.getenv("CONSUMER_KAFKA_USERNAME") and os.getenv(
    "CONSUMER_KAFKA_PASSWORD"
):
    CONSUMER_CONFIG["PARAMS"]["security.protocol"] = "SASL_SSL"
    CONSUMER_CONFIG["PARAMS"]["sasl.mechanism"] = "SCRAM-SHA-512"
    CONSUMER_CONFIG["PARAMS"]["sasl.username"] = os.getenv(
        "CONSUMER_KAFKA_USERNAME"
    )
    CONSUMER_CONFIG["PARAMS"]["sasl.password"] = os.getenv(
        "CONSUMER_KAFKA_PASSWORD"
    )
if os.getenv("PRODUCER_KAFKA_USERNAME") and os.getenv(
    "PRODUCER_KAFKA_PASSWORD"
):
    PRODUCER_CONFIG["PARAMS"]["security.protocol"] = os.getenv(
        "PRODUCER_SECURITY_PROTOCOL", "SASL_PLAINTEXT"
    )
    PRODUCER_CONFIG["PARAMS"]["sasl.mechanism"] = os.getenv(
        "PRODUCER_SASL_MECHANISM", "SCRAM-SHA-256"
    )
    PRODUCER_CONFIG["PARAMS"]["sasl.username"] = os.getenv(
        "PRODUCER_KAFKA_USERNAME"
    )
    PRODUCER_CONFIG["PARAMS"]["sasl.password"] = os.getenv(
        "PRODUCER_KAFKA_PASSWORD"
    )
if os.getenv("SCRIBE_KAFKA_USERNAME") and os.getenv("SCRIBE_KAFKA_PASSWORD"):
    SCRIBE_PRODUCER_CONFIG["PARAMS"]["security.protocol"] = "SASL_SSL"
    SCRIBE_PRODUCER_CONFIG["PARAMS"]["sasl.mechanism"] = "SCRAM-SHA-512"
    SCRIBE_PRODUCER_CONFIG["PARAMS"]["sasl.username"] = os.getenv(
        "SCRIBE_KAFKA_USERNAME"
    )
    SCRIBE_PRODUCER_CONFIG["PARAMS"]["sasl.password"] = os.getenv(
        "SCRIBE_KAFKA_PASSWORD"
    )
if os.getenv("METRICS_KAFKA_USERNAME") and os.getenv("METRICS_KAFKA_PASSWORD"):
    METRICS_CONFIG["PARAMS"]["PARAMS"]["security.protocol"] = "SASL_SSL"
    METRICS_CONFIG["PARAMS"]["PARAMS"]["sasl.mechanism"] = "SCRAM-SHA-512"
    METRICS_CONFIG["PARAMS"]["PARAMS"]["sasl.username"] = os.getenv(
        "METRICS_KAFKA_USERNAME"
    )
    METRICS_CONFIG["PARAMS"]["PARAMS"]["sasl.password"] = os.getenv(
        "METRICS_KAFKA_PASSWORD"
    )


def model_config_factory():
    modelclass = os.getenv("MODEL_CLASS")
    config = configurator(modelclass)
    return config


STEP_CONFIG = {
    "PROMETHEUS": bool(os.getenv("USE_PROMETHEUS", True)),
    "SCRIBE_PRODUCER_CONFIG": SCRIBE_PRODUCER_CONFIG,
    "CONSUMER_CONFIG": CONSUMER_CONFIG,
    "PRODUCER_CONFIG": PRODUCER_CONFIG,
    "METRICS_CONFIG": METRICS_CONFIG,
    "MODEL_VERSION": os.getenv("MODEL_VERSION", "dev"),
    "MODEL_CONFIG": model_config_factory(),
    "SCRIBE_PARSER_CLASS": os.getenv("SCRIBE_PARSER_CLASS"),
    "STEP_PARSER_CLASS": os.getenv("STEP_PARSER_CLASS"),
}
