from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker, load_only, scoped_session, Query
from sqlalchemy.ext.declarative import declarative_base
from math import ceil
from ..generic import DatabaseConnection


class BaseModel:
    query = None


Base = declarative_base(cls=BaseModel)
from db_plugins.db.sql.models import *


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


class BaseQuery(Query):
    def query(
        self,
        models,
        offset=None,
        limit=None,
        total=None,
        sort_by=None,
        sort_desc="DESC",
        *params
    ):
        sql_query = self.session.query(*models).filter(*params)
        total = sql_query.order_by(None).count() if not total else None
        if sort_by is not None:
            sql_query = (
                sql_query.order_by(sort_by.desc())
                if sort_desc == "DESC"
                else sql_query.order_by(sort_by.asc())
            )
        results = sql_query[offset:limit]
        return {"total": total, "results": results}

    def check_exists(self, model=None, filter_by=None):
        """
        Check if record exists in database.

        :param session: The connection session
        :param model: The class of the model to be instantiated
        :param dict filter_by: attributes used to find object in the database
        :param dict kwargs: attributes used to create the object that are not used in filter_by

        :returns: True if object exists else False

        """
        model = self._entities[0].mapper.class_ if self._entities else model
        query = self.session.query(model) if not self._entities else self
        return self.session.query(query.filter_by(**filter_by).exists()).scalar()

    def get_or_create(self, model=None, filter_by=None, **kwargs):
        """
        Initializes a model by creating it or getting it from the database if it exists
        Parameters
        ----------
        session : Session
            The connection session
        model : Model
            The class of the model to be instantiated
        filter_by : dict
            attributes used to find object in the database
        kwargs : dict
            attributes used to create the object that are not used in filter_by
        Returns
        ----------
        instance, created
            Tuple with the instanced object and wether it was created or not
        """
        model = self._entities[0].mapper.class_ if self._entities else model
        query = self.session.query(model) if not self._entities else self
        instance = (
            query.options(load_only(*filter_by.keys())).filter_by(**filter_by).first()
        )
        if instance:
            return instance, False
        else:
            filter_by.update(kwargs)
            instance = model(**filter_by)
            self.session.add(instance)
            return instance, True

    def update(self, instance, args):
        """
        Updates an object

        Parameter
        -----------

        instance : Model
            Object to be updated
        args : dict
            Attributes updated

        Returns
        ----------
        instance
            The updated object instance
        """
        for key in args.keys():
            setattr(instance, key, args[key])
        return instance

    def bulk_insert(self, objects, model):
        """
        Inserts multiple objects to the database improving performance

        Parameters
        -----------

        objects : list
            Objects to be added
        model: Model
            Class of the model to be added
        session: Session
            Session instance 
        """
        self.session.bulk_insert_mappings(model, objects)

    def paginate(self, page=1, per_page=10, count=True):
        if page < 1:
            page = 1
        if per_page < 0:
            per_page = 10
        items = self.limit(per_page).offset((page - 1) * per_page).all()
        if not count:
            total = None
        else:
            total = self.order_by(None).count()
        return Pagination(self, page, per_page, total, items)


class SQLConnection(DatabaseConnection):
    def __init__(self):
        self.config = None
        self.engine = None
        self.Base = None
        self.Session = None
        self.session = None

    def start(self, config, base=None, session_options=None, use_scoped=False, scope_func=None):
        self.config = config
        self.engine = create_engine(config["SQLALCHEMY_DATABASE_URL"])
        self.Base = base or Base
        session_options = session_options or {}
        session_options["query_cls"] = BaseQuery
        self.Session = sessionmaker(bind=self.engine, **session_options)
        if not use_scoped:
            self.create_session()
        else:
            self.create_scoped_session(scope_func)

    def create_session(self):
        self.session = self.Session()

    def create_scoped_session(self, scope_func=None):
        self.session = scoped_session(self.Session, scopefunc=scope_func)
        self.Base.query = self.session.query_property(query_cls=BaseQuery)

    def create_db(self):
        self.Base.metadata.create_all(bind=self.engine)

    def drop_db(self):
        self.Base.metadata.drop_all(bind=self.engine)
