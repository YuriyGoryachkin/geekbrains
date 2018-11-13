from database_tools.alchemy import CGroups, CUserStatus, CCollGroup, CCategoryGroup, CUserRoles, CUsers, CContacts, CGroupsUsers, CMessages
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_tools.db_connect import POSTGRES_SERVER, POSTGRES_PORT, POSTGRES_LOGIN, POSTGRES_PASS, POSTGRES_BASE

engine = create_engine(
    'postgresql+psycopg2://{0}:{1}@{2}:{3}/{4}'.format(POSTGRES_LOGIN, POSTGRES_PASS, POSTGRES_SERVER,
                                                       POSTGRES_PORT,
                                                       POSTGRES_BASE))


Session = sessionmaker(bind=engine)
session = Session()

out = session.query(CUsers).filter(CUsers.username == 'tester3').one()



print('out - {}'.format(out))

print('uid - {}'.format(out.uid))

print('email - {}'.format(out.email))
