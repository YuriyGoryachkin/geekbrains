from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, Unicode, UniqueConstraint, ForeignKey, MetaData

engine = create_engine(
    'postgresql+psycopg2://{0}:{1}@{2}:{3}/{4}'.format('test_user', 'qwerty', '127.0.0.1',
                                                       '5432',
                                                       'test_database'), echo=True)
Session = sessionmaker(bind=engine)

session = Session()

CBase = declarative_base()


class CUsers(CBase):
    __tablename__ = 'users'

    uid = Column(Integer(), primary_key=True)
    username = Column(Unicode())
    password = Column(Unicode())
    email = Column(Unicode())
    token = Column(Unicode())
    check_1 = UniqueConstraint('username')
    check_2 = UniqueConstraint('email')

    def __init__(self, username, password, email, token):
        self.username = username
        self.password = password
        self.email = email
        self.token = token

    def __repr__(self):
        return 'CUsers: uid = %d, account_name = %s, email = %s, token = %s' % (self.uid, self.username, self.email, self.token)



# session.add(CUsers("tester3", "qwerty", "monguste@gmail.com", "d53e124e6b31e34d"))
#
# session.commit()

q_user = session.query(CUsers).filter_by(username="tester3").all()
print(q_user)

session.close()