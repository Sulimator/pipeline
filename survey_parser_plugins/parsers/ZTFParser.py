from survey_parser_plugins.core import SurveyParser


class ZTFParser(SurveyParser):
    _source = "ZTF"
    _exclude_keys = ["candid", "jd", "fid", "ra", "dec", "rb", "magpsf", "sigmapsf", "aimage", "bimage"]

    @classmethod
    def parse_message(cls, message, extra_fields=False):
        oid = message["objectId"]
        message = message["candidate"].copy()
        return {
            "survey_id": oid,
            "candid": message['candid'],
            "mjd": message['jd'] - 2400000.5,
            "fid": message['fid'],
            "ra": message['ra'],
            "dec": message['dec'],
            "rb": message['rb'],
            "mag": message['magpsf'],
            "sigmag": message["sigmapsf"],
            "aimage": message["aimage"],
            "bimage": message["bimage"],
            "extra_fields": {
                k: message[k]
                for k in message.keys()
                if k not in cls._exclude_keys
            } if extra_fields else None
        }

    @classmethod
    def get_source(cls):
        return cls._source

    @classmethod
    def can_parse(cls, message: dict) -> bool:
        return 'publisher' in message.keys() and cls._source in message["publisher"]
