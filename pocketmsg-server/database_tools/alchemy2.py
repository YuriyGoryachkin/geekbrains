from sqlalchemy import Column, Integer, Unicode, UniqueConstraint, ForeignKey, MetaData
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Table, Column, Integer, String, ForeignKey, MetaData, DateTime
from sqlalchemy import create_engine
# from .db_connect import POSTGRES_SERVER, POSTGRES_PORT, POSTGRES_LOGIN, POSTGRES_PASS, POSTGRES_BASE

engine = create_engine(
    'postgresql+psycopg2://{0}:{1}@{2}:{3}/{4}'.format('test_user', 'qwerty', '127.0.0.1',
                                                       '5432',
                                                       'test_database'), echo=True)
meta = MetaData(bind=engine)
CBase = declarative_base()


class CUsers(CBase):
    __tablename__ = 'users'

    uid = Column(Integer(), primary_key=True)
    username = Column(Unicode())
    password = Column(Unicode())
    email = Column(Unicode())
    token = Column(Unicode())
    # check_1 = UniqueConstraint('username')
    # check_2 = UniqueConstraint('email')

    def __init__(self, username, password, email, token):
        self.username = username
        self.password = password
        self.email = email
        self.token = token

    def __repr__(self):
        return 'CUsers: uid = %d, account_name = %s, email = %s' % (self.uid, self.username, self.email)


class CMessages(CBase):
    __tablename__ = 'messages'

    mid = Column(Integer(), primary_key=True)
    message = Column(Unicode())
    from_id = Column(Integer(), ForeignKey('users.uid'))
    to_id = Column(Integer(), ForeignKey('users.uid'))
    dtime = Column(Unicode())

    p_from_id = relationship('CUsers', foreign_keys=[from_id])
    p_to_id = relationship('CUsers', foreign_keys=[to_id])

    def __repr__(self):
        return 'CMessages<mid = %d, from_id = %d, to_id = %d, message = %s' % (
            self.mid, self.from_id, self.to_id, self.message)


class CContacts(CBase):
    __tablename__ = 'contacts'
    cid = Column(Integer(), primary_key=True)
    user_id = Column(Integer(), ForeignKey('users.uid'))
    contact = Column(Integer(), ForeignKey('users.uid'))

    def __repr__(self):
        return 'CContacts<cid = %d, user_id = %d, contact = %d' % (self.cid, self.user_id, self.contact)

CBase.metadata.create_all(engine)