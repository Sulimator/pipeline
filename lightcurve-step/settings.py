import os
from fastavro import schema
from fastavro.repository.base import SchemaRepositoryError
from credentials import get_credentials

##################################################
#       lightcurve_step   Settings File
##################################################

# SCHEMA PATH RELATIVE TO THE SETTINGS FILE
PRODUCER_SCHEMA_PATH = os.path.join(os.path.dirname(__file__), os.getenv("PRODUCER_SCHEMA_PATH"))
METRICS_SCHEMA_PATH = os.path.join(os.path.dirname(__file__), os.getenv("METRIS_SCHEMA_PATH"))
SCRIBE_SCHEMA_PATH =  os.path.join(os.path.dirname(__file__), os.getenv("SCRIBE_SCHEMA_PATH"))

def settings_creator():
    # Set the global logging level to debug
    logging_debug = bool(os.getenv("LOGGING_DEBUG"))

    db_config_mongo = get_credentials(
        os.environ["MONGODB_SECRET_NAME"], db_name="mongo"
    )
    if os.getenv("SQL_SECRET_NAME"):
        db_config_sql = get_credentials(
            os.environ.get("SQL_SECRET_NAME"), db_name="sql"
        )
    else:
        db_config_sql = None

    # Consumer configuration
    # Each consumer has different parameters and can be found in the documentation
    consumer_config = {
        "CLASS": "apf.consumers.KafkaConsumer",
        "PARAMS": {
            "bootstrap.servers": os.environ["CONSUMER_SERVER"],
            "group.id": os.environ["CONSUMER_GROUP_ID"],
            "auto.offset.reset": "beginning",
            "enable.partition.eof": True
            if os.getenv("ENABLE_PARTITION_EOF")
            else False,
        },
        "TOPICS": os.environ["CONSUMER_TOPICS"].split(","),
        "consume.messages": int(os.getenv("CONSUME_MESSAGES", 50)),
        "consume.timeout": int(os.getenv("CONSUME_TIMEOUT", 15)),
    }

    producer_config = {
        "CLASS": "apf.producers.KafkaProducer",
        "PARAMS": {
            "bootstrap.servers": os.environ["PRODUCER_SERVER"],
            "message.max.bytes": int(os.getenv("PRODUCER_MESSAGE_MAX_BYTES", 6291456)),
        },
        "TOPIC": os.environ["PRODUCER_TOPIC"],
        "SCHEMA_PATH": PRODUCER_SCHEMA_PATH,
    }

    metrics_config = {
        "CLASS": "apf.metrics.KafkaMetricsProducer",
        "EXTRA_METRICS": [
            {"key": "aid", "format": lambda x: str(x)},
            {"key": "candid"},
        ],
        "PARAMS": {
            "PARAMS": {
                "bootstrap.servers": os.environ["METRICS_SERVER"],
            },
            "TOPIC": os.getenv("METRICS_TOPIC", "metrics"),
            "SCHEMA_PATH": METRICS_SCHEMA_PATH,
        },
    }

    if os.getenv("CONSUMER_KAFKA_USERNAME") and os.getenv("CONSUMER_KAFKA_PASSWORD"):
        consumer_config["PARAMS"]["security.protocol"] = "SASL_SSL"
        consumer_config["PARAMS"]["sasl.mechanism"] = "SCRAM-SHA-512"
        consumer_config["PARAMS"]["sasl.username"] = os.getenv(
            "CONSUMER_KAFKA_USERNAME"
        )
        consumer_config["PARAMS"]["sasl.password"] = os.getenv(
            "CONSUMER_KAFKA_PASSWORD"
        )
    if os.getenv("PRODUCER_KAFKA_USERNAME") and os.getenv("PRODUCER_KAFKA_PASSWORD"):
        producer_config["PARAMS"]["security.protocol"] = "SASL_SSL"
        producer_config["PARAMS"]["sasl.mechanism"] = "SCRAM-SHA-512"
        producer_config["PARAMS"]["sasl.username"] = os.getenv(
            "PRODUCER_KAFKA_USERNAME"
        )
        producer_config["PARAMS"]["sasl.password"] = os.getenv(
            "PRODUCER_KAFKA_PASSWORD"
        )
    if os.getenv("METRICS_KAFKA_USERNAME") and os.getenv("METRICS_KAFKA_PASSWORD"):
        metrics_config["PARAMS"]["PARAMS"]["security.protocol"] = "SASL_SSL"
        metrics_config["PARAMS"]["PARAMS"]["sasl.mechanism"] = "SCRAM-SHA-512"
        metrics_config["PARAMS"]["PARAMS"]["sasl.username"] = os.getenv(
            "METRICS_KAFKA_USERNAME"
        )
        metrics_config["PARAMS"]["PARAMS"]["sasl.password"] = os.getenv(
            "METRICS_KAFKA_PASSWORD"
        )

    prometheus = os.getenv("USE_PROMETHEUS", False)
    use_profiling = bool(os.getenv("USE_PROFILING", True))
    pyroscope_server = os.getenv("PYROSCOPE_SERVER", "http://pyroscope.pyroscope:4040")

    # Step Configuration
    step_config = {
        "CONSUMER_CONFIG": consumer_config,
        "PRODUCER_CONFIG": producer_config,
        "METRICS_CONFIG": metrics_config,
        "PROMETHEUS": prometheus,
        "DB_CONFIG": db_config_mongo,
        "DB_CONFIG_SQL": db_config_sql,
        "LOGGING_DEBUG": logging_debug,
        "USE_PROFILING": use_profiling,
        "PYROSCOPE_SERVER": pyroscope_server,
    }
    return step_config
