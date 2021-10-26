from ..core import GenericAlert, SurveyParser
from ..core.id_generator import id_generator


class ZTFParser(SurveyParser):
    _source = "ZTF"
    _celestial_sigmas = {
        1: 0.065,
        2: 0.085,
    }
    _generic_alert_message_key_mapping = {
        "candid": "candid",
        "mjd": "jd",
        "fid": "fid",
        "pid": "pid",
        "rfid": "rfid",
        "ra": "ra",
        "dec": "dec",
        "mag": "magpsf",
        "sigmag": "sigmapsf",
        "isdiffpos": "isdiffpos",
        "rb": "rb",
        "rbversion": "rbversion"
    }

    @classmethod
    def parse_message(cls, message) -> GenericAlert:
        try:
            oid = message["objectId"]
            prv_candidates = message["prv_candidates"]
            # get stamps
            stamps = {
                "cutoutScience": message["cutoutScience"]["stampData"],
                "cutoutTemplate": message["cutoutTemplate"]["stampData"],
                "cutoutDifference": message["cutoutDifference"]["stampData"]
            }

            candidate = message["candidate"]
            generic_alert_message = cls._generic_alert_message(candidate, cls._generic_alert_message_key_mapping)

            # inclusion of extra attributes
            generic_alert_message['oid'] = oid
            generic_alert_message['tid'] = cls._source
            generic_alert_message['aid'] = id_generator(candidate["ra"], candidate["dec"])
            generic_alert_message["extra_fields"]["prv_candidates"] = prv_candidates
            # inclusion of stamps
            generic_alert_message["stamps"] = stamps
            # attributes modification
            generic_alert_message["isdiffpos"] = 1 if generic_alert_message["isdiffpos"] in ["t", "1"] else -1
            generic_alert_message['mjd'] = generic_alert_message['mjd'] - 2400000.5

            # possible attributes
            sigmaradec = cls._celestial_sigmas[candidate["fid"]]
            generic_alert_message["sigmara"] = candidate["sigmara"] if "sigmara" in candidate else sigmaradec 
            generic_alert_message["sigmadec"] = candidate["sigmadec"] if "sigmadec" in candidate else sigmaradec 
            return GenericAlert(**generic_alert_message)
        except KeyError:
            raise KeyError("This parser can't parse message")

    @classmethod
    def can_parse(cls, message: dict) -> bool:
        return 'publisher' in message.keys() and cls._source in message[
            "publisher"]
