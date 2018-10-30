from database_tools.alchemy import CUsers
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_tools.db_config import POSTGRES_LOGIN, POSTGRES_PASS, POSTGRES_SERVER, POSTGRES_PORT, POSTGRES_BASE
from datetime import datetime, timedelta


def token_expiration():
    today = datetime.now()
    days = timedelta(days=5)
    token_expire = (today + days)
    return token_expire

db_address = 'postgresql+psycopg2://{0}:{1}@{2}:{3}/{4}'.format(POSTGRES_LOGIN, POSTGRES_PASS, POSTGRES_SERVER,
                                                       POSTGRES_PORT,
                                                       POSTGRES_BASE)

engine = create_engine(db_address)
Session = sessionmaker(bind=engine)
session = Session()

name = 'tester3'
password = 'qwerty'
email = 'mte@gmail.com'
token = 'd53e124e6b31e34d'
status = 1
role = 1
time = token_expiration()



add_user = CUsers(username=name, password=password, email=email, token=token, tokenexp=time, status_id=status, role_id=role)
session.add(add_user)
session.commit()
