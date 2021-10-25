from db_plugins.db import models as generic_models
from pymongo import (
    TEXT,
    GEOSPHERE,
    IndexModel,
    DESCENDING,
    ASCENDING,
)
from db_plugins.db.mongo.orm import base_creator, Field, SpecialField

Base = base_creator()


def create_extra_fields(Model, **kwargs):
    if "extra_fields" in kwargs:
        return kwargs["extra_fields"]
    else:
        for field in Model._meta.fields:
            try:
                kwargs.pop(field)
            except (KeyError):
                pass
        return kwargs


class Object(generic_models.Object, Base):
    """Mongo implementation of the Object class.

    Contains definitions of indexes and custom attributes like loc.
    """

    def loc_definition(**kwargs):
        return {
            "type": "Point",
            "coordinates": [kwargs["meanra"], kwargs["meandec"]],
        }

    aid = Field() # ALeRCE candidate id (unique id of object in the ALeRCE database)
    oid = Field() # Object id should include objects id of all surveys (same survey can provide different object ids)
    lastmjd = Field()
    firstmjd = Field()
    ndet = Field()
    loc = SpecialField(loc_definition)
    meanra = Field()
    meandec = Field()
    extra_fields = SpecialField(create_extra_fields)

    __table_args__ = [
        IndexModel([("aid", TEXT)]),
        IndexModel([("oid", TEXT)]),
        IndexModel([("lastmjd", DESCENDING)]),
        IndexModel([("firstmjd", DESCENDING)]),
        IndexModel([("loc", GEOSPHERE)]),
        IndexModel([("meanra", ASCENDING)]),
        IndexModel([("meandec", ASCENDING)]),
    ]
    __tablename__ = "object"


class Detection(Base, generic_models.Detection):

    tid = Field() # Telescope id (this gives the spatial coordinates of the observatory, e.g. ZTF, ATLAS-HKO, ATLAS-MLO)
    aid = Field()
    candid = Field()
    mjd = Field()
    fid = Field()
    ra = Field()
    dec = Field()
    rb = Field()
    mag = Field()
    sigmag = Field()
    rfid = Field()
    e_ra = Field() 
    e_dec = Field()
    sigmag = Field()
    isdiffpos = Field()
    magpsf_corr = Field()
    sigmapsf_corr = Field()
    sigmapsf_corr_ext = Field()
    corrected = Field()
    dubious = Field()
    parent_candid = Field()
    has_stamp = Field()
    step_id_corr = Field()
    rb = Field()
    rbversion = Field()
    extra_fields = SpecialField(create_extra_fields)
    __table_args__ = [IndexModel([("aid", TEXT)])]
    __tablename__ = "detection"


class NonDetection(Base, generic_models.NonDetection):

    aid = Field()
    tid = Field()
    mjd = Field()
    diffmaglim = Field()
    fid = Field()
    extra_fields = SpecialField(create_extra_fields)

    __table_args__ = [
        IndexModel([("aid", TEXT)]),
        IndexModel([("tid", TEXT)]),
        IndexModel([("mjd", DESCENDING)]),
        IndexModel([("fid", ASCENDING)]),
    ]
    __tablename__ = "non_detection"
