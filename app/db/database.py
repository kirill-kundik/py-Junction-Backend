from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import app
from app.utilities import Singleton


class Database(metaclass=Singleton):
    def __init__(self):
        self.engine = create_engine(app.Config.DATABASE_URI)
        self.Session = sessionmaker(bind=self.engine)

    @contextmanager
    def _session_scope(self):
        session = self.Session(expire_on_commit=False)
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()
