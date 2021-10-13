import click
import sys
import os
from db_plugins.db.sql import (
    init as init_sql,
    make_migrations as make_sql_migrations,
    migrate as migrate_sql,
)


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
        init_sql
        click.echo("Database created with credentials from {}".format(settings_path))

    elif "MONGO" in DB_CONFIG:
        pass

    else:
        raise Exception("Invalid settings file")


@cli.command()
@click.option("--settings_path", default=".", help="settings.py path")
def make_migrations(settings_path):
    if not os.path.exists(settings_path):
        raise Exception("Settings file not found")
    sys.path.append(os.path.abspath(settings_path))

    from settings import DB_CONFIG

    if "SQL" in DB_CONFIG:
        make_sql_migrations()
        click.echo("Migrations made with config from {}".format(settings_path))

    else:
        raise Exception("Invalid settings file")


@cli.command()
@click.option("--settings_path", default=".", help="settings.py path")
def migrate(settings_path):
    if not os.path.exists(settings_path):
        raise Exception("Settings file not found")
    sys.path.append(os.path.abspath(settings_path))

    from settings import DB_CONFIG

    if "SQL" in DB_CONFIG:
        migrate_sql()
        click.echo("Migrated database with config from {}".format(settings_path))

    else:
        raise Exception("Invalid settings file")
