from sqlalchemy import (
    Column,
    Integer,
    String,
    Table,
    ForeignKey,
    Float,
    Boolean,
    JSON,
    Index,
    DateTime,
)
from sqlalchemy.orm import relationship
from .. import generic

from db_plugins.db.sql import Base


taxonomy_class = Table(
    "taxonomy_class",
    Base.metadata,
    Column("class_name", String, ForeignKey("class.name")),
    Column("taxonomy_name", String, ForeignKey("taxonomy.name")),
)


class Commons:
    def __getitem__(self, field):
        return self.__dict__[field]


class Class(Base, generic.AbstractClass):
    __tablename__ = "class"

    name = Column(String, primary_key=True)
    acronym = Column(String)
    taxonomies = relationship(
        "Taxonomy", secondary=taxonomy_class, back_populates="classes"
    )
    classifications = relationship("Classification")

    def __repr__(self):
        return "<Class(name='%s', acronym='%s')>" % (self.name, self.acronym)


class Taxonomy(Base, generic.AbstractTaxonomy):
    __tablename__ = "taxonomy"

    name = Column(String, primary_key=True)
    classes = relationship(
        "Class", secondary=taxonomy_class, back_populates="taxonomies"
    )
    classifiers = relationship("Classifier")

    def __repr__(self):
        return "<Taxonomy(name='%s')>" % (self.name)


class Classifier(Base, generic.AbstractClassifier):
    __tablename__ = "classifier"
    name = Column(String, primary_key=True)
    taxonomy_name = Column(String, ForeignKey("taxonomy.name"))
    classifications = relationship("Classification")

    def __repr__(self):
        return "<Classifier(name='%s')>" % (self.name)


class Object(Base, generic.AbstractObject):
    __tablename__ = "object"

    oid = Column(String, primary_key=True)
    ndethist = Column(Integer)
    ncovhist = Column(Integer)
    mjdstarthist = Column(Float)
    mjdendhist = Column(Float)
    corrected = Column(Boolean)
    stellar = Column(Boolean)
    ndet = Column(Integer)
    g_r_max = Column(Float)
    g_r_max_corr = Column(Float)
    g_r_mean = Column(Float)
    g_r_mean_corr = Column(Float)
    meanra = Column(Float)
    meandec = Column(Float)
    sigmara = Column(Float)
    sigmadec = Column(Float)
    deltamjd = Column(Float)
    firstmjd = Column(Float)
    lastmjd = Column(Float)
    step_id_corr = Column(String)

    __table_args__ = (
        Index("object_ndet", "ndet", postgresql_using="btree"),
        Index("object_firstmjd", "firstmjd", postgresql_using="btree"),
        Index("object_lastmjd", "lastmjd", postgresql_using="btree"),
    )

    xmatches = relationship("Xmatch")
    magnitude_statistics = relationship("MagnitudeStatistics", uselist=True)
    classifications = relationship("Classification")
    non_detections = relationship("NonDetection")
    detections = relationship("Detection")
    features = relationship("FeaturesObject")

    def get_lightcurve(self):
        return {
            "detections": self.detections,
            "non_detections": self.non_detections,
        }

    def __repr__(self):
        return "<Object(oid='%s')>" % (self.oid)


class Classification(Base, generic.AbstractClassification):
    __tablename__ = "classification"

    object = Column(String, ForeignKey("object.oid"), primary_key=True)
    classifier_name = Column(String, ForeignKey("classifier.name"), primary_key=True)
    class_name = Column(String, ForeignKey("class.name"), primary_key=True)
    probability = Column(Float)
    probabilities = Column(JSON)

    classes = relationship("Class", back_populates="classifications")
    objects = relationship("Object", back_populates="classifications")
    classifiers = relationship("Classifier", back_populates="classifications")

    def __repr__(self):
        return (
            "<Classification(class_name='%s', probability='%s', object='%s', classifier_name='%s')>"
            % (
                self.class_name,
                self.probability,
                self.object,
                self.classifier_name,
            )
        )


class Xmatch(Base, generic.AbstractXmatch):
    __tablename__ = "xmatch"

    oid = Column(String, ForeignKey("object.oid"))
    catalog_id = Column(String, primary_key=True)
    catalog_oid = Column(String, primary_key=True)


class MagnitudeStatistics(Base, generic.AbstractMagnitudeStatistics):
    __tablename__ = "magnitude_statistics"

    oid = Column(String, ForeignKey('object.oid'), primary_key=True)
    fid = Column(Integer)
    stellar = Column(Boolean)
    corrected = Column(Boolean)
    ndet = Column(Integer)
    ndubious = Column(Integer)
    dmdt_first = Column(Float)
    dm_first = Column(Float)
    sigmadm_first = Column(Float)
    dt_first = Column(Float)
    magmean = Column(Float)
    magmedian = Column(Float)
    magmax = Column(Float)
    magmin = Column(Float)
    magsigma = Column(Float)
    maglast = Column(Float)
    magfirst = Column(Float)
    firstmjd = Column(Float)
    lastmjd = Column(Float)
    step_id_corr = Column(String)

    __table_args__ = (
        Index("mag_mean", "magmean", postgresql_using="btree"),
        Index("mag_median", "magmedian", postgresql_using="btree"),
        Index("mag_min", "magmin", postgresql_using="btree"),
        Index("mag_max", "magmax", postgresql_using="btree"),
        Index("mag_first", "magfirst", postgresql_using="btree"),
        Index("mag_last", "maglast", postgresql_using="btree"),
    )


class Features(Base, generic.AbstractFeatures):
    __tablename__ = "features"

    version = Column(String, primary_key=True)


class FeaturesObject(Base):
    __tablename__ = "features_object"

    object_id = Column(String, ForeignKey("object.oid"), primary_key=True)
    features_version = Column(String, ForeignKey("features.version"), primary_key=True)
    data = Column(JSON)
    features = relationship("Features")


class NonDetection(Base, generic.AbstractNonDetection, Commons):
    __tablename__ = "non_detection"

    oid = Column(String, ForeignKey("object.oid"), primary_key=True)
    fid = Column(Integer, primary_key=True)
    datetime = Column(DateTime, primary_key=True)
    mjd = Column(Float)
    diffmaglim = Column(Float)
    __table_args__ = (Index("non_det_oid", "oid", postgresql_using="hash"),)


class Detection(Base, generic.AbstractDetection, Commons):
    __tablename__ = "detection"

    candid = Column(String, primary_key=True)
    oid = Column(String, ForeignKey("object.oid"))
    avro = Column(String)
    mjd = Column(Float)
    fid = Column(Integer)
    pid = Column(Float)
    diffmaglim = Column(Float)
    isdiffpos = Column(Integer)
    nid = Column(Integer)
    ra = Column(Float)
    dec = Column(Float)
    magpsf = Column(Float)
    sigmapsf = Column(Float)
    magap = Column(Float)
    sigmagap = Column(Float)
    distnr = Column(Float)
    rb = Column(Float)
    rbversion = Column(String)
    drb = Column(Float)
    drbversion = Column(String)
    magapbig = Column(Float)
    sigmagapbig = Column(Float)
    rfid = Column(Integer)
    magpsf_corr = Column(Float)
    sigmapsf_corr = Column(Float)
    sigmapsf_corr_ext = Column(Float)
    corrected = Column(Boolean)
    dubious = Column(Boolean)
    parent_candid = Column(String)
    has_stamp = Column(Boolean)
    step_id_corr = Column(String)

    __table_args__ = (
        Index("object_id", "oid", postgresql_using="hash"),)

    def __repr__(self):
        return "<Detection(candid='%s', fid='%i', oid='%s')>" % (self.candid, self.fid, self.oid)

class OutlierDetector(Base, generic.AbstractOutlierDetector):
    __tablename__ = "outlier_detector"

    name = Column(String, primary_key=True)


class OutlierScore(Base, generic.AbstractOutlierScore):
    __tablename__ = "outlier_score"
    object_ = Column("object", String, ForeignKey("object.oid"), primary_key=True)
    detector_name = Column(
        String, ForeignKey("outlier_detector.name"), primary_key=True
    )
    score = Column(Float, primary_key=True)
    scores = Column(JSON)


class Dataquality(Base, generic.AbstractDataquality):
    __tablename__ = 'dataquality'

    candid = Column(String, primary_key=True)
    oid = Column(String)
    fid = Column(Integer)
    xpos = Column(Float, nullable=False)
    ypos = Column(Float, nullable=False)
    chipsf = Column(Float, nullable=False)
    sky = Column(Float, nullable=False)
    fwhm = Column(Float, nullable=False)
    classtar = Column(Float, nullable=False)
    mindtoedge = Column(Float, nullable=False)
    seeratio = Column(Float, nullable=False)
    aimage = Column(Float, nullable=False)
    bimage = Column(Float, nullable=False)
    aimagerat = Column(Float, nullable=False)
    bimagerat = Column(Float, nullable=False)
    nneg = Column(Integer, nullable=False)
    nbad = Column(Integer, nullable=False)
    sumrat = Column(Float, nullable=False)
    scorr = Column(Float, nullable=False)
    dsnrms = Column(Float, nullable=False)
    ssnrms = Column(Float, nullable=False)
    magzpsci = Column(Float, nullable=False)
    magzpsciunc = Column(Float, nullable=False)
    magzpscirms = Column(Float, nullable=False)
    nmatches = Column(Integer, nullable=False)
    clrcoeff = Column(Float, nullable=False)
    clrcounc = Column(Float, nullable=False)
    zpclrcov = Column(Float, nullable=False)
    zpmed = Column(Float, nullable=False)
    clrmed = Column(Float, nullable=False)
    clrrms = Column(Float, nullable=False)
    exptime = Column(Float, nullable=False)

    __table_args__ = (

        Index('index_candid', 'candid', postgresql_using='btree'),
        Index('index_fid', 'fid', postgresql_using='btree'))


class Gaia_ztf(Base, generic.AbstractGaia_ztf):
    __tablename__ = 'gaia_ztf'

    oid = Column(String, primary_key=True)
    candid = Column(String, primary_key=True)
    neargaia = Column(Float, nullable=False)
    neargaiabright = Column(Float, nullable=False)
    maggaia = Column(Float, nullable=False)
    maggaiabright = Column(Float, nullable=False)
    unique = Column(Boolean)


class Ss_ztf(Base, generic.AbstractSs_ztf):
    __tablename__ = 'ss_ztf'

    oid = Column(String, primary_key=True)
    candid = Column(String)
    ssdistnr = Column(Float, nullable=False)
    ssmagnr = Column(Float, nullable=False)
    ssnamenr = Column(String)


class Ps1_ztf(Base, generic.AbstractPs1_ztf):
    __tablename__ = 'ps1_ztf'

    oid = Column(String, primary_key=True)
    candid = Column(Integer, primary_key=True)
    objectidps1 = Column(Float, nullable=False)
    sgmag1 = Column(Float, nullable=False)
    srmag1 = Column(Float, nullable=False)
    simag1 = Column(Float, nullable=False)
    szmag1 = Column(Float, nullable=False)
    sgscore1 = Column(Float, nullable=False)
    distpsnr1 = Column(Float, nullable=False)
    objectidps2 = Column(Float, nullable=False)
    sgmag2 = Column(Float, nullable=False)
    srmag2 = Column(Float, nullable=False)
    simag2 = Column(Float, nullable=False)
    szmag2 = Column(Float, nullable=False)
    sgscore2 = Column(Float, nullable=False)
    distpsnr2 = Column(Float, nullable=False)
    objectidps3 = Column(Float, nullable=False)
    sgmag3 = Column(Float, nullable=False)
    srmag3 = Column(Float, nullable=False)
    simag3 = Column(Float, nullable=False)
    szmag3 = Column(Float, nullable=False)
    sgscore3 = Column(Float, nullable=False)
    distpsnr3 = Column(Float, nullable=False)
    nmtchps = Column(Integer)
    unique1 = Column(Boolean)


class Reference(Base, generic.AbstractReference):
    __tablename__ = 'reference'

    oid = Column(String, primary_key=True)
    rfid = Column(String)
    candiid = Column(String)
    fid = Column(Integer)
    rcid = Column(Integer, nullable=False)
    field = Column(Integer, nullable=False)
    magnr = Column(Float, nullable=False)
    sigmagnr = Column(Float, nullable=False)
    chinr = Column(Float, nullable=False)
    sharpnr = Column(Float, nullable=False)
    ranr = Column(Float)
    decnr = Column(Float)
    mjdstartref = Column(Float)
    mjdendref = Column(Float)
    nframesref = Column(Integer)


class Pipeline(Base, generic.AbstractPipeline):
    __tablename__ = 'pipeline'

    pipeline_id = Column(String, primary_key=True)
    step_id_corr = Column(String, nullable=False)
    step_id_feat = Column(String, nullable=False)
    step_id_clf = Column(String, nullable=False)
    step_id_out = Column(String, nullable=False)
    step_id_stamp = Column(String, nullable=False)
    date = Column(DateTime, nullable=False)


class Step(Base, generic.AbstractStep):
    __tablename__ = 'step'

    step_id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    version = Column(String, nullable=False)
    comments = Column(String, nullable=False)
    date = Column(DateTime, nullable=False)