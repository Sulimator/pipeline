from db_plugins.db.sql import DatabaseConnection
from db_plugins.db.sql.models import Base
import alembic.config
import click
import os, sys


MANAGE_PATH = os.path.dirname(os.path.abspath(__file__))
MIGRATIONS_PATH = os.path.abspath(os.path.join(MANAGE_PATH, "../db/sql/"))


@click.group()
def cli():
    pass


@cli.command()
@click.option("--settings_path", default=".", help="settings.py path")
def initdb(settings_path):
    if not os.path.exists(settings_path):
        raise Exception("Settings file not found")
    sys.path.append(os.path.dirname(os.path.expanduser(settings_path)))
    from settings import DB_CONFIG

    if "SQL" in DB_CONFIG:
        db_config = DB_CONFIG["SQL"]
    else:
        db_config = {"SQLALCHEMY_DATABASE_URL": "sqlite:///:memory:"}
    db = DatabaseConnection(db_config)
    db.create_db()
    os.chdir(MIGRATIONS_PATH)
    alembic.config.main(["stamp", "head"])
    click.echo("Database created with credentials from {}".format(settings_path))


@cli.command()
@click.option("--settings_path", default=".", help="settings.py path")
def make_migrations(settings_path):
    if not os.path.exists(settings_path):
        raise Exception("Settings file not found")
    sys.path.append(os.path.abspath(settings_path))

    os.chdir(MIGRATIONS_PATH)
    alembicArgs = ["--raiseerr", "revision", "--autogenerate", "-m", "tables"]
    alembic.config.main(alembicArgs)


@cli.command()
@click.option("--settings_path", default=".", help="settings.py path")
def migrate(settings_path):
    if not os.path.exists(settings_path):
        raise Exception("Settings file not found")
    sys.path.append(os.path.abspath(settings_path))

    os.chdir(MIGRATIONS_PATH)
    alembicArgs = ["--raiseerr", "upgrade", "head"]
    alembic.config.main(alembicArgs)
