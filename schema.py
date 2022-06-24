SCHEMA = {
  "namespace": "elasticc.v0_9",
  "type": "record",
  "name": "brokerClassification",
  "doc": "sample avro alert schema v4.1",
  "fields": [
    {
        "name": "alertId", "type": "long", "doc": "unique alert identifier"},
    {
        "name": "diaSourceId", "type": "long", "doc": "id of source that triggered this classification"},
    {
        "name": "elasticcPublishTimestamp",
        "type": {"type": "long", "logicalType": "timestamp-millis"},
        "doc": "timestamp from originating ELAsTiCC alert"
    },
    {
        "name": "brokerIngestTimestamp",
        "type": ["null", {"type": "long", "logicalType": "timestamp-millis"}],
        "doc": "timestamp of broker ingestion of ELAsTiCC alert"
    },
    {"name": "brokerName", "type": "string", "doc": "Name of broker (never changes)"},
    {"name": "brokerVersion", "type": "string", "doc": "Version/Release of broker's software"},
    {"name": "classifications", "type": {
        "type": "array",
        "items": {
          "type": "record",
          "name": "classificationDict",
          "fields": [
            {
                "name": "classifierName",
                "type": "string",
                "doc": "Name of classifier broker is using, including software version"
            },
            {
                "name": "classifierParams",
                "type": "string",
                "doc": "Any classifier parameter information worth noting for this classification"
            },
            {"name": "classId", "type": "int", "doc": "See https://github.com/LSSTDESC/elasticc/tree/main/taxonomy/taxonomy.ipynb for specification"},
            {"name": "probability",  "type": "float", "doc": "0-1"}
          ]
        }
      }
     }
  ]
}
