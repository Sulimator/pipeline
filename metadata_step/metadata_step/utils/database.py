import itertools
from contextlib import contextmanager
from typing import Callable, ContextManager, Dict, List

from sqlalchemy import create_engine, select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import sessionmaker, Session
from db_plugins.db.sql.models import Reference, Gaia_ztf, Ss_ztf, Dataquality, Ps1_ztf


class PSQLConnection:
    def __init__(self, config: dict) -> None:
        url = self.__format_db_url(config)
        self._engine = create_engine(url, echo=True)
        self._session_factory = sessionmaker(
            self._engine,
        )

    def __format_db_url(self, config):
        return f"postgresql://{config['USER']}:{config['PASSWORD']}@{config['HOST']}:{config['PORT']}/{config['DB_NAME']}"

    @contextmanager
    def session(self) -> Callable[..., ContextManager[Session]]:
        session: Session = self._session_factory()
        try:
            yield session
        except Exception as e:
            session.rollback()
            raise
        finally:
            session.close()

def _parse_sql_dict(d: Dict):
    return {k: v for k, v in d.items() if not k.startswith("_")}

def get_ps1_catalog(session: Session, oids: List):
    stmt = select(Ps1_ztf).where(Ps1_ztf.oid.in_(oids))
    catalog = session.execute(stmt).all()
    return [_parse_sql_dict(c[0].__dict__) for c in catalog]


def get_gaia_catalog(session: Session, oids: List):
    stmt = select(Gaia_ztf).where(Gaia_ztf.oid.in_(oids))
    catalog = session.execute(stmt).all()
    return [_parse_sql_dict(c[0].__dict__) for c in catalog]



def insert_metadata(session: Session, data: List):
    def accumulate(accumulator, el):
        keys = ["ss", "reference", "dataquality", "gaia", "ps1"]
        return {k: [*accumulator[k], {"oid": el["oid"], **el[k]}] for k in keys}

    accumulated_metadata = itertools.accumulate(
        data,
        accumulate,
        {"ss": [], "reference": [], "dataquality": [], "gaia": [], "ps1": []},
    )

    # Reference
    reference_stmt = insert(Reference).values(accumulated_metadata["reference"])
    reference_stmt = reference_stmt.on_conflict_do_update(
        constraint="reference_pkey", set_=dict(oid=reference_stmt.excluded.oid)
    )
    session.connection().execute(reference_stmt)

    # SS
    ss_stmt = insert(Ss_ztf).values(accumulated_metadata["ss"])
    ss_stmt = ss_stmt.on_conflict_do_update(
        constraint="ss_ztf_pkey", set_=dict(oid=ss_stmt.excluded.oid)
    )
    session.connection().execute(ss_stmt)

    # Dataquality
    dataquality_stmt = insert(Dataquality).values(accumulated_metadata["dataquality"])
    dataquality_stmt = dataquality_stmt.on_conflict_do_update(
        constraint="dataquality_pkey", set_=dict(oid=dataquality_stmt.excluded.oid)
    )
    session.connection().execute(dataquality_stmt)

    # GAIA
    gaia_stmt = insert(Gaia_ztf).values(accumulated_metadata["gaia"])
    gaia_stmt = gaia_stmt.on_conflict_do_update(
        constraint="gaia_ztf_pkey", set_=dict(unique1=gaia_stmt.excluded.unique1)
    )
    session.connection().execute(gaia_stmt)

    # PS1
    ps1_stmt = insert(Ps1_ztf).values(accumulated_metadata["ps1"])
    ps1_stmt = ps1_stmt.on_conflict_do_update(
        constraint="ps1_ztf_pkey",
        set_=dict(
            unique1=ps1_stmt.excluded.unique1,
            unique2=ps1_stmt.excluded.unique2,
            unique3=ps1_stmt.excluded.unique3,
        ),
    )
    session.connection().execute(ps1_stmt)
