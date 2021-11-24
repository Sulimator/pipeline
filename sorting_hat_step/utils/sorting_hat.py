import numpy as np
import pandas as pd

from scipy.spatial import cKDTree
from typing import List

from db_plugins.db.mongo.models import Object
from db_plugins.db.mongo.connection import MongoConnection


# https://media.giphy.com/media/JDAVoX2QSjtWU/giphy.gif
class SortingHat:
    def __init__(self, db: MongoConnection, radius: float = 1.5):
        self.radius = radius
        self.db = db

    @classmethod
    def wgs_scale(cls, lat: float) -> float:
        """
        Get scaling to convert degrees to meters at a given geodetic latitude (declination)
        :param lat: geodetic latitude (declination)
        :return:
        """

        # Values from WGS 84
        a = 6378137.000000000000  # Semi-major axis of Earth
        e = 0.081819190842600  # eccentricity
        angle = np.radians(1.0)

        # Compute radius of curvature along meridian (see https://en.wikipedia.org/wiki/Meridian_arc)
        rm = a * (1 - np.power(e, 2)) / np.power((1 - np.power(e, 2) * np.power(np.sin(np.radians(lat)), 2)), 1.5)

        # Compute length of arc at this latitude (meters/degree)
        arc = rm * angle
        return arc

    def cone_search(self, ra: float, dec: float) -> List[dict]:
        """
        Cone search to database given a ra, dec and radius. Returns a list of objects sorted by distance.
        :param ra: right ascension
        :param dec: declination
        :return:
        """
        radius = self.radius / 3600
        scaling = self.wgs_scale(dec)
        meter_radius = radius * scaling
        lon, lat = ra - 180., dec
        objects = self.db.query(model=Object)
        cursor = objects.find(
            {
                'loc': {
                    '$nearSphere': {
                        '$geometry':
                            {
                                'type': 'Point',
                                'coordinates': [lon, lat]
                            },
                        '$maxDistance': meter_radius,
                    }
                },
            },
            {
                "aid": 1  # only return alerce_id
            }
        )
        spatial = [i for i in cursor]
        return spatial

    def oid_query(self, oid: list) -> int or None:
        """
        Query to database if the oids has an alerce_id
        :param oid: oid of any survey
        :return: existing aid if exists else is None
        """
        objects = self.db.query(model=Object)
        cursor = objects.find(
            {
                "oid": {
                    "$in": oid
                }
            },
            {
                "_id": 0,
                "aid": 1
            }
        )
        data = [i["aid"] for i in cursor]
        if len(data):
            return data[0]
        return None

    @classmethod
    def id_generator(cls, ra: float, dec: float) -> int:
        """
        Method that create an identifier of 19 digits given its ra, dec.
        :param ra: right ascension in degrees
        :param dec: declination in degrees
        :return: alerce id
        """
        # 19 Digit ID - two spare at the end for up to 100 duplicates
        aid = 1000000000000000000

        # 2013-11-15 KWS Altered code to fix the negative RA problem
        if ra < 0.0:
            ra += 360.0

        if ra > 360.0:
            ra -= 360.0

        # Calculation assumes Decimal Degrees:
        ra_hh = int(ra / 15)
        ra_mm = int((ra / 15 - ra_hh) * 60)
        ra_ss = int(((ra / 15 - ra_hh) * 60 - ra_mm) * 60)
        ra_ff = int((((ra / 15 - ra_hh) * 60 - ra_mm) * 60 - ra_ss) * 100)

        if dec >= 0:
            h = 1
        else:
            h = 0
            dec = dec * -1

        dec_deg = int(dec)
        dec_mm = int((dec - dec_deg) * 60)
        dec_ss = int(((dec - dec_deg) * 60 - dec_mm) * 60)
        dec_f = int(((((dec - dec_deg) * 60 - dec_mm) * 60) - dec_ss) * 10)

        aid += (ra_hh * 10000000000000000)
        aid += (ra_mm * 100000000000000)
        aid += (ra_ss * 1000000000000)
        aid += (ra_ff * 10000000000)

        aid += (h * 1000000000)
        aid += (dec_deg * 10000000)
        aid += (dec_mm * 100000)
        aid += (dec_ss * 1000)
        aid += (dec_f * 100)

        return aid

    def internal_cross_match(self, data: pd.DataFrame, ra_col="ra", dec_col="dec"):
        """
        Do a internal cross match in data input (batch vs batch) to get closest objects. This method uses cKDTree class
        to get nearest object. Returns a dictionary where assign indexes of the same object. If the output is a empty
        dictionary indicates that doesn't exists nearest object in the batch.
        :param data:
        :param ra_col:
        :param dec_col:
        :return:
        """
        radius = self.radius / 3600
        values = data[[ra_col, dec_col]].to_numpy()
        tree = cKDTree(values)
        sdm = tree.sparse_distance_matrix(tree, radius, output_type="coo_matrix")  # get sparse distance matrix
        same_objects = {}
        for core, neighbour in zip(sdm.row, sdm.col):
            if neighbour in same_objects:
                same_objects[core] = same_objects[neighbour]
            elif core not in same_objects:
                same_objects[core] = core
                same_objects[neighbour] = core
        return same_objects

    def _to_name(self, group_of_alerts: pd.Series) -> pd.Series:
        """
        Generate alerce_id to a group of alerts of the same object. This method has three options:
        1) First Hit: The alert has an oid existing in database
        2) Second Hit: The alert has a ra, dec closest to object in database (radius of 1.5")
        3) Miss: Create a new aid given its ra, dec
        :param group_of_alerts: alerts of the same object.
        :return:
        """
        oids = group_of_alerts["oid"].unique().tolist()
        first_alert = group_of_alerts.iloc[0]
        # 1) First Hit: Exists at least one aid to this oid
        existing_oid = self.oid_query(oids)
        if existing_oid:
            aid = existing_oid
        else:
            # 2) Second Hit: cone search return objects sorted. So first response is closest.
            near_objects = self.cone_search(first_alert["ra"], first_alert["dec"])
            if len(near_objects):
                aid = near_objects[0]["aid"]
            # 3) Miss generate a new ALeRCE identifier
            else:
                aid = self.id_generator(first_alert["ra"], first_alert["dec"])
        response = {"aid": aid}
        return pd.Series(response)

    def to_name(self, alerts: pd.DataFrame) -> pd.DataFrame:
        """
        Generate an alerce_id to a batch of alerts given its oid, ra, dec and radius.
        :param alerts: Dataframe of alerts
        :return: Dataframe of alerts with a new column called `aid` (alerce_id)
        """
        # Internal cross match that identifies same objects in own batch: create a new column named 'tmp_id'
        indexes = self.internal_cross_match(alerts)
        alerts["tmp_id"] = alerts.index.map(lambda x: indexes[x] if x in indexes else x)
        # Interaction with database: group all alerts with the same tmp_id and find/create alerce_id
        tmp_id_aid = alerts.groupby("tmp_id").apply(self._to_name)
        # Join the tuple tmp_id-aid with batch of alerts
        alerts = alerts.set_index("tmp_id").join(tmp_id_aid)
        # Get alerce_id in long representation
        alerts["aid"] = alerts["aid"].astype(np.long)
        # Remove column tmp_id (really is a index) for ever
        alerts.reset_index(inplace=True, drop=True)
        return alerts
