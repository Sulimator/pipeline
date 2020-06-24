import abc
from math import ceil

class DatabaseConnection(abc.ABC):
    """
    Main database connection interface declares common functionality
    to all databases
    """

    @abc.abstractmethod
    def start(self):
        """
        Initiates the database connection.
        """
        pass

    @abc.abstractmethod
    def create_db(self):
        """
        Creates database collections or tables
        """
        pass

    @abc.abstractmethod
    def drop_db(self):
        """
        Removes database collections or tables
        """
        pass

    @abc.abstractmethod
    def query(self, *args):
        """
        Gets a query object
        """
        pass

class BaseQuery(abc.ABC):
    @abc.abstractmethod
    def check_exists(self, model, filter_by):
        """
        Checks if a model exists in the database
        """
        pass

    @abc.abstractmethod
    def get_or_create(self, model, filter_by, **kwargs):
        """
        Creates a model if it doesn't exist in the database.
        It always returns a model instance and whether it was created or not.
        """
        pass

    @abc.abstractmethod
    def update(self, instance, args):
        """
        Updates a model instance with specified args
        """
        pass

    @abc.abstractmethod
    def paginate(self, page=1, per_page=10, count=True):
        """
        Returns a pagination object from this query
        """
        pass

    @abc.abstractmethod
    def bulk_insert(self, objects, model):
        """
        Inserts multiple objects to the database
        """
        pass

    # @abc.abstractmethod
    # def find_all(self):
    #     """
    #     Retrieves all items from the result of this query
    #     """
    #     pass

    # @abc.abstractmethod
    # def find_one(self):
    #     """
    #     Retrieves only one item from the result of this query.
    #     Returns None if result is empty.
    #     """
    #     pass


class Pagination:
    def __init__(self, query, page, per_page, total, items):
        self.query = query
        self.page = page
        self.per_page = per_page
        self.total = total
        self.items = items

    @property
    def pages(self):
        """The total number of pages"""
        if self.per_page == 0 or self.total is None:
            pages = 0
        else:
            pages = int(ceil(self.total / float(self.per_page)))
        return pages

    def prev(self):
        """Returns a :class:`Pagination` object for the previous page."""
        assert (
            self.query is not None
        ), "a query object is required for this method to work"
        return self.query.paginate(self.page - 1, self.per_page)

    @property
    def prev_num(self):
        """Number of the previous page."""
        if not self.has_prev:
            return None
        return self.page - 1

    @property
    def has_prev(self):
        """True if a previous page exists"""
        return self.page > 1

    def next(self):
        """Returns a :class:`Pagination` object for the next page."""
        assert (
            self.query is not None
        ), "a query object is required for this method to work"
        return self.query.paginate(self.page + 1, self.per_page)

    @property
    def has_next(self):
        """True if a next page exists."""
        return self.page < self.pages

    @property
    def next_num(self):
        """Number of the next page"""
        if not self.has_next:
            return None
        return self.page + 1



class AbstractClass:
    """
    Abstract Class model

    Attributes
    ----------
    name : str
        the class name
    acronym : str
        the short class name
    """

    name = None
    acronym = None

    def get_taxonomies(self):
        """
        Gets the taxonomies that the class instance belongs to
        """
        pass

    def get_classifications(self):
        """
        Gets all classifications with the class
        """
        pass


class AbstractTaxonomy:
    """
    Abstract Taxonomy model

    Attributes
    ----------
    name : str
        the taxonomy name
    """

    name = None

    def get_classes(self):
        """
        Gets the classes that a taxonomy uses
        """
        pass

    def get_classifiers(self):
        """
        Gets the classifiers using the taxonomy
        """
        pass


class AbstractClassifier:
    """
    Abstract Classifier model

    Attributes
    ----------
    name : str
        name of the classifier
    """

    name = None

    def get_classifications(self):
        """
        Gets classifications done by the classifier
        """
        pass

    def get_taxonomy(self):
        """
        Gets the taxonomy the classifier is using
        """
        pass


class AbstractAstroObject:
    """
    Abstract Object model

    Attributes
    ----------
    oid: str
        object identifier
    nobs: str
        number of observations
    lastmjd: float
        date (in mjd) of the last observation
    firstmjd: float
        date (in mjd) of the first observation
    meanra: float
        mean right ascension coordinates
    meandec: float
        mean declination coordinates
    sigmara: float
        error for right ascension coordinates
    sigmadec: float
        error for declination coordinates
    deltajd: float
        difference between last and first mjd
    """

    oid = None
    nobs = None
    lastmjd = None
    meanra = None
    meandec = None
    sigmara = None
    sigmadec = None
    deltajd = None
    firstmjd = None

    def get_classifications(self):
        """
        Gets all classifications on the object
        """
        pass

    def get_magnitude_statistics(self):
        """
        Gets magnitude statistics for the object
        """
        pass

    def get_xmatches(self):
        """
        Gets crossmatch information for the object
        """
        pass

    def get_features(self):
        """
        Gets features associated with the object
        """
        pass

    def get_detections(self):
        """
        Gets all detections of the object
        """
        pass

    def get_non_detections(self):
        """
        Gets all non_detections of the object
        """
        pass

    def get_lightcurve(self):
        """
        Gets the lightcurve of the object
        """
        pass


class AbstractXmatch:
    """
    Abstract Crossmatch model

    Attributes
    ----------
    catalog_id : str
        name identifying the catalog
    catalog_object_id : str
        the catalog's name identifier for the object
    """

    catalog_id = None
    catalog_object_id = None

    def get_object(self):
        """
        Gets the object referring to the crossmatch
        """
        pass


class AbstractMagnitudeStatistics:
    """
    Abstract Magnitude Statistics model

    Attributes
    ----------
    magnitude_type : str
        the type of the magnitude, could be psf or ap
    fid : int
        magnitude band identifier, 1 for red, 2 for green
    mean : float
        mean magnitude meassured
    median : float
        median of the magnitude
    max_mag : float
        maximum value of magnitude meassurements
    min_mag : float
        minimum value of magnitude meassurements
    sigma : float
        error of magnitude meassurements
    last : float
        value for the last magnitude meassured
    first : float
        value for the first magnitude meassured
    """

    magnitude_type = None
    fid = None
    mean = None
    median = None
    max_mag = None
    min_mag = None
    sigma = None
    last = None
    first = None

    def get_object(self):
        """
        Gets the object associated with the stats
        """
        pass


class AbstractClassification:
    """
    Abstract Classification model

    Attributes
    ----------
    class_name : str
        name of the class
    probability : float
        probability of the classification
    probabilities : json
        probabilities for each class
    """

    probability = None
    probabilities = None

    def get_class(self):
        """
        Gets the class of the classification
        """
        pass

    def get_object(self):
        """
        Gets the object classifified
        """
        pass

    def get_classifier(self):
        """
        Gets the classifier used
        """
        pass


class AbstractFeatures:
    """
    Abstract Features model

    Attributes
    ---------
    version : str
        name of the version used for features
    """

    version = None


class AbstractNonDetection:
    """
    Abstract model for non detections

    Attributes
    ----------
    mjd : float
        date of the non detection in mjd
    diffmaglim: float
        magnitude of the non detection
    fid : int
        band identifier 1 for red, 2 for green
    """

    mjd = None
    diffmaglim = None
    fid = None

    def get_object(self):
        """
        Gets the object related
        """
        pass


class AbstractDetection:
    """
    Abstract model for detections

    Attributes
    ----------
    candid : str
        candidate identifier
    mjd : float
        date of the detection in mjd
    fid : int
        band identifier, 1 for red, 2 for green
    ra : float
        right ascension coordinates
    dec : float
        declination coordinates
    rb : int
        real bogus
    magap : float
        ap magnitude
    magpsf : float
        psf magnitude
    sigmapsf : float
        error for psf magnitude
    sigmagap : float
        error for ap magnitude
    magpsf_corr : float
        magnitude correction for magpsf
    magap_corr : float
        magnitude correction for magap
    sigmapsf_corr : float
        correction for sigmapsf
    sigmagap_corr : float
        correction for sigmagap
    avro : string
        url for avro file in s3
    """

    candid = None
    mjd = None
    fid = None
    ra = None
    dec = None
    rb = None
    magap = None
    magpsf = None
    sigmapsf = None
    sigmagap = None
    alert = None
    magap_corr = None
    magpsf_corr = None
    sigmapsf_corr = None
    sigmagap_corr = None
    avro = None

    def get_object(self):
        """
        Gets the object related
        """
        pass


class AbstractOutlierDetector:
    """
    Abstract class for outlier detection models

    Attributes
    ------------
    name : str
        a name for identifying the model
    """

    name = None

    def get_outlier_scores(self):
        """
        Gets all the outlier scores produced by the detector
        """
        pass


class AbstractOutlierScore:
    """
    Abstract class for outlier scores

    Attributes
    ----------
    score : float
        the main metric for identifying outliers
    scores : json
        other scoring metrics for outliers
    """

    score = None
    scores = None
