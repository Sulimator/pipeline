import json
from unittest import mock

from .data.messages import data
from scripts.run_step import step_factory

from pprint import pprint


def test_execute_multistream(env_variables):
    step = step_factory()
    formatted_data = step.pre_execute(data)
    result = step.execute(formatted_data)
    result = result["multistream"]
    for d in data:
        assert d["aid"] in result
        assert "meanra" in result[d["aid"]]
        assert "meandec" in result[d["aid"]]
        assert "magstats" in result[d["aid"]]
        assert "oid" in result[d["aid"]]
        assert "tid" in result[d["aid"]]
        assert "firstmjd" in result[d["aid"]]
        assert "lastmjd" in result[d["aid"]]
        assert "ndet" in result[d["aid"]]
        assert "sigmara" in result[d["aid"]]
        assert "sigmadec" in result[d["aid"]]


def test_scribe_message_multistream(env_variables):
    step = step_factory()
    formatted_data = step.pre_execute(data)
    result = step.execute(formatted_data)
    # Necessary because creation in step_factory gives dictionary of config which is interpreted as spec for dict
    step.scribe_producer = mock.MagicMock()

    step.post_execute(result)
    result = result["multistream"]
    for d in data:
        to_write = result[d["aid"]]
        to_write.update(
            {
                "loc": {
                    "type": "Point",
                    "coordinates": [
                        to_write["meanra"] - 180,
                        to_write["meandec"],
                    ],
                }
            }
        )
        command = {
            "collection": "object",
            "type": "update",
            "criteria": {"_id": d["aid"]},
            "data": to_write,
            "options": {"upsert": True},
        }
        step.scribe_producer.produce.assert_any_call(
            {"payload": json.dumps(command)}
        )


def test_execute_ztf(env_variables):
    step = step_factory()
    formatted_data = step.pre_execute(data)
    result = step.execute(formatted_data)
    result = result["ztf"]
    for d in data:
        if not any([det["sid"] == "ZTF" for det in d["detections"]]):
            continue
        assert d["aid"] in result
        assert "meanra" in result[d["aid"]]
        assert "meandec" in result[d["aid"]]
        assert "magstats" in result[d["aid"]]
        assert "oid" in result[d["aid"]]
        assert "tid" in result[d["aid"]]
        assert "firstmjd" in result[d["aid"]]
        assert "lastmjd" in result[d["aid"]]
        assert "ndet" in result[d["aid"]]
        assert "sigmara" in result[d["aid"]]
        assert "sigmadec" in result[d["aid"]]
