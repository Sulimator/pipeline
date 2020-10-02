import logging
import io
import pandas as pd
from apf.core.step import GenericStep
import sys
import os
import requests
import operator
import datetime
from db_plugins.db.sql.models import Object, Probability, Step
from db_plugins.db.sql import SQLConnection


DIRNAME = os.path.dirname(__file__)
MODEL = os.path.join(DIRNAME, "../model")
sys.path.append(MODEL)

from deployment import StampClassifier


class EarlyClassifier(GenericStep):
    """EarlyClassifier Description

    Parameters
    ----------
    consumer : GenericConsumer
        Description of parameter `consumer`.
    **step_args : type
        Other args passed to step (DB connections, API requests, etc.)

    """

    def __init__(
        self,
        consumer=None,
        config=None,
        db_connection=None,
        request_session=None,
        stamp_classifier=None,
        level=logging.INFO,
        **step_args,
    ):
        super().__init__(consumer, config=config, level=level)
        self.db = db_connection or SQLConnection()
        self.db.connect(self.config["DB_CONFIG"]["SQL"])
        if not step_args.get("test_mode", False):
            self.insert_step_metadata()
        self.requests_session = request_session or requests.Session()
        self.model = stamp_classifier or StampClassifier()

    def insert_step_metadata(self):
        self.db.query(Step).get_or_create(
            filter_by={"step_id": self.config["STEP_METADATA"]["STEP_ID"]},
            name=self.config["STEP_METADATA"]["STEP_NAME"],
            version=self.config["STEP_METADATA"]["STEP_VERSION"],
            comments=self.config["STEP_METADATA"]["STEP_COMMENTS"],
            date=datetime.datetime.now(),
        )


    def get_probabilities(self,message):
        oid = message["objectId"]
        template = message["cutoutTemplate"]["stampData"]
        science = message["cutoutScience"]["stampData"]
        difference = message["cutoutDifference"]["stampData"]
        df = pd.DataFrame([{
            "science": science,
            "template": template,
            "diff": difference,
            **message["candidate"]
        }], index = [oid])
        try:
            probabilities = self.model.execute(df).iloc[0].to_dict()
        except Exception as e:
            self.logger.critical(str(e))
            probabilities = None
        return probabilities

    def execute(self, message):
        oid = message["objectId"]
        probabilities = self.get_probabilities(message)
        if probabilities is not None:
            object_data = self.get_default_object_values(message)
            self.insert_db(probabilities, oid, object_data)

    def insert_db(self, probabilities, oid, object_data):
        """
        Inserts probabilities returned by the stam classifier into the database.

        Parameters
        ----------
        probabilities : dict
            Should contain the probability name as key and probability as value.
            Something like:
            {
                "AGN": 1,
                "SN": 2,
                "bogus": 3,
                "asteroid": 4,
                "VS": 5,
            }
        oid : str
            Object ID of the object that is being classified. It is used to search
            the database for a specific object and get its instance
        object_data : dict
            Values to use if the object needs to be created. Keys in this dictionary
            should have every attribute of the object table other than `oid`
        """
        probabilities = self.get_ranking(probabilities)
        obj, _ = self.db.query(Object).get_or_create(
            filter_by={"oid": oid}, **object_data
        )
        for prob in probabilities:
            filter_by = {
                "oid": oid,
                "class_name": prob,
                "classifier_name": self.config["STEP_METADATA"]["CLASSIFIER_NAME"],
                "classifier_version": self.config["STEP_METADATA"][
                    "CLASSIFIER_VERSION"
                ],
            }
            prob_data = {
                "probability": probabilities[prob]["probability"],
                "ranking": probabilities[prob]["ranking"],
            }
            probability, created = self.db.query(Probability).get_or_create(
                filter_by=filter_by,
                **prob_data,
            )
            if not created:
                self.logger.info("Probability already exists. Skipping insert")
                break

    def get_ranking(self, probabilities):
        """
        Transforms the probabilities dictionary returned by the model to a dictionary
        that has the probability and ranking for each class.

        Parameters
        ----------
        probabilities : dict
            Something like:
            {
                "AGN": 1,
                "SN": 2,
                "bogus": 3,
                "asteroid": 4,
                "VS": 5,
            }
        Return
        ------
        probabilities : dict
            A dictionary with probability and ranking for each class.
            Something like:
            {
                "AGN": {"probability": 1, "ranking": 5},
                "SN": {"probability": 2, "ranking": 4},
                "bogus": {"probability": 3, "ranking": 3},
                "asteroid": {"probability": 4, "ranking": 2},
                "VS": {"probability": 5, "ranking": 1},
            }

        """
        sorted_classes = sorted(probabilities.items(), key=lambda x: x[1], reverse=True)
        for x in range(len(sorted_classes)):
            probabilities[sorted_classes[x][0]] = {
                "probability": probabilities[sorted_classes[x][0]],
                "ranking": x + 1,
            }
        return probabilities

    def get_default_object_values(
        self,
        alert: dict,
    ) -> dict:
        """
        Returns default values for creating an `object` in the database

        Parameters
        ----------
        alert : dict
            The whole alert from the stream that has the `candidate` key.

        Return
        ------
        data : dict
            Dictionary with default values for an object
        """

        data = {}
        data["ndethist"] = alert["candidate"]["ndethist"]
        data["ncovhist"] = alert["candidate"]["ncovhist"]
        data["mjdstarthist"] = alert["candidate"]["jdstarthist"] - 2400000.5
        data["mjdendhist"] = alert["candidate"]["jdendhist"] - 2400000.5
        data["firstmjd"] = alert["candidate"]["jd"] - 2400000.5
        data["lastmjd"] = data["firstmjd"]
        data["ndet"] = 1
        data["deltajd"] = 0
        data["meanra"] = alert["candidate"]["ra"]
        data["meandec"] = alert["candidate"]["dec"]
        data["step_id_corr"] = "0.0.0"
        data["corrected"] = False
        data["stellar"] = False

        return data
