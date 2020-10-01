from db_plugins.db.sql import (
    models,
    Pagination,
    SQLConnection,
    SQLQuery,
    Pagination,
    create_engine,
    Base,
    sessionmaker,
)
from sqlalchemy.engine.reflection import Inspector
import unittest
import json
import time
import datetime


class SQLConnectionTest(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        config = {
            "ENGINE": "postgresql",
            "HOST": "localhost",
            "USER": "postgres",
            "PASSWORD": "postgres",
            "PORT": 5432,
            "DB_NAME": "postgres",
        }
        self.config = {
            "SQLALCHEMY_DATABASE_URL": f"{config['ENGINE']}://{config['USER']}:{config['PASSWORD']}@{config['HOST']}:{config['PORT']}/{config['DB_NAME']}"
        }
        self.session_options = {
            "autocommit": False,
            "autoflush": True,
        }
        self.db = SQLConnection()

    def tearDown(self):
        if self.db.Base and self.db.engine:
            self.db.Base.metadata.drop_all(bind=self.db.engine)

    def test_connect_not_scoped(self):
        self.db.connect(self.config, session_options=session_options, use_scoped=False)
        self.assertIsNotNone(self.db.engine)
        self.assertIsNotNone(self.db.session)

    def test_connect_scoped(self):
        session_options = self.session_options
        session_options["autoflush"] = False
        self.db.connect(self.config, session_options=session_options, use_scoped=True)
        self.assertIsNotNone(self.db.engine)
        self.assertIsNotNone(self.db.session)

    def test_create_session(self):
        engine = create_engine(self.config["SQLALCHEMY_DATABASE_URL"])
        Session = sessionmaker(bind=engine, **self.session_options)
        self.db.Session = Session
        self.db.create_session()
        self.assertIsNotNone(self.db.session)

    def test_create_scoped_session(self):
        engine = create_engine(self.config["SQLALCHEMY_DATABASE_URL"])
        session_options = self.session_options
        session_options["autoflush"] = False
        Session = sessionmaker(bind=engine, **session_options)
        self.db.Session = Session
        self.db.Base = Base
        self.db.create_scoped_session()
        self.assertIsNotNone(self.db.session)

    def test_create_db(self):
        engine = create_engine(self.config["SQLALCHEMY_DATABASE_URL"])
        self.db.engine = engine
        self.db.Base = Base
        self.db.create_db()
        inspector = Inspector.from_engine(engine)
        self.assertGreater(len(inspector.get_table_names()), 0)

    def test_drop_db(self):
        engine = create_engine(self.config["SQLALCHEMY_DATABASE_URL"])
        self.db.engine = engine
        self.db.Base = Base
        self.db.Base.metadata.create_all(bind=self.db.engine)
        self.db.drop_db()
        inspector = Inspector.from_engine(engine)
        self.assertEqual(len(inspector.get_table_names()), 0)

    def test_query(self):
        query = self.db.query()
        print(query)


class SQLQueryTest(unittest.TestCase):
    pass
