from apf.core.step import GenericStep
from apf.producers import KafkaProducer
from db_plugins.db.sql.models import Object, Detection, NonDetection
from db_plugins.db.sql import SQLConnection
from lc_correction.compute import apply_correction, DISTANCE_THRESHOLD

import numpy as np
import logging

logging.getLogger("GP").setLevel(logging.WARNING)
np.seterr(divide='ignore')

DET_KEYS = ['avro', 'oid', 'candid', 'jd', 'fid', 'pid', 'diffmaglim', 'isdiffpos', 'nid', 'ra', 'dec', 'magpsf',
            'sigmapsf', 'magap', 'sigmagap', 'distnr', 'rb', 'rbversion', 'drb', 'drbversion', 'magapbig', 'sigmagapbig',
            'rfid', 'magpsf_corr', 'sigmapsf_corr', 'sigmapsf_corr_ext', 'corrected', 'dubious', 'parent_candid',
            'has_stamp', 'step_id_corr']
COR_KEYS = ["magpsf_corr", "sigmapsf_corr", "sigmapsf_corr_ext"]


class Correction(GenericStep):
    """Correction Description

    Parameters
    ----------
    consumer : GenericConsumer
        Description of parameter `consumer`.
    **step_args : type
        Other args passed to step (DB connections, API requests, etc.)

    """
    def __init__(self, consumer=None, level=logging.INFO, config=None, **step_args):
        super().__init__(consumer, level=level, config=config, **step_args)
        self.producer = KafkaProducer(config["PRODUCER_CONFIG"])
        self.driver = SQLConnection()
        self.driver.connect(config["DB_CONFIG"]["SQL"])

    def get_object(self, alert: dict) -> Object:
        data = {
            "oid": alert["objectId"]
        }
        return self.driver.session.query().get_or_create(Object, data)

    def get_detection(self, candidate: dict) -> Detection:
        filters = {
            "candid": candidate["candid"]
        }
        data = {key: candidate[key] for key in DET_KEYS if key in candidate.keys()}
        return self.driver.session.query().get_or_create(Detection, filter_by=filters, **data)

    def set_object_values(self, alert: dict, obj: Object) -> Object:
        obj.ndethist = alert["candidate"]["ndethist"]
        obj.ncovhist = alert["candidate"]["ncovhist"]
        obj.jdstarthist = alert["candidate"]["jdstarthist"] - 2400000.5
        obj.jdendhist = alert["candidate"]["jdendhist"] - 2400000.5
        obj.firstmjd = alert["candidate"]["jd"] - 2400000.5
        return obj

    def preprocess_alert(self, alert: dict) -> None:
        alert["candidate"]["mjd"] = alert["candidate"]["jd"] - 2400000.5
        alert["candidate"]["isdiffpos"] = 1 if alert["candidate"]["isdiffpos"] in ["t", "1"] else -1
        alert["candidate"]["corrected"] = alert["candidate"]["distnr"] < DISTANCE_THRESHOLD
        alert["candidate"]["candid"] = str(alert["candidate"]["candid"])
        for k in ["cutoutDifference", "cutoutScience", "cutoutTemplate"]:
            alert.pop(k, None)

    def do_correction(self, alert: dict, inplace=False) -> dict:
        values = apply_correction(alert["candidate"])
        result = dict(zip(COR_KEYS, values))
        if inplace:
            alert.update(result)
        return result

    def process_lightcurve(self, alert: dict, obj: Object) -> None:
        detection, created = self.get_detection(alert["candidate"])
        print(detection, created)

    def execute(self, message):
        obj, created = self.get_object(message)
        self.preprocess_alert(message)
        self.do_correction(message, inplace=True)
        self.process_lightcurve(message, obj)
        # First observation of the object
        if created:
            self.set_object_values(message, obj)

        # Another case


        self.logger.info(f"{obj} -> {created}")
        self.driver.session.commit()

        #self.producer.produce(write)