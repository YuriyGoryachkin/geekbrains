from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
# from .db_config import POSTGRES_LOGIN, POSTGRES_PASS, POSTGRES_SERVER, POSTGRES_PORT, POSTGRES_BASE

db_address = 'postgresql+psycopg2://{0}:{1}@{2}:{3}/{4}'.format('test_user', 'qwerty', '127.0.0.1',
                                                       '5432',
                                                       'test_database')
engine = create_engine(db_address)
Session = sessionmaker(bind=engine)

Base = declarative_base()


def connect(dbname):
    db_address = 'postgresql+psycopg2://{0}:{1}@{2}:{3}/{4}'.format('test_user', 'qwerty', '127.0.0.1',
                                                       '5432',
                                                       'test_database')
    engine = create_engine(db_address)
    return engine
