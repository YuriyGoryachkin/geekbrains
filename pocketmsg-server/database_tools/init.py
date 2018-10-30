from sqlalchemy import Table, Column, Integer, String, ForeignKey, MetaData, DateTime
from sqlalchemy import create_engine
from database_tools.db_connect import POSTGRES_SERVER, POSTGRES_PORT, POSTGRES_LOGIN, POSTGRES_PASS, POSTGRES_BASE

from database_tools.alchemy import CUserStatus, CUserRoles
from sqlalchemy.orm import sessionmaker

engine = create_engine(
    'postgresql+psycopg2://{0}:{1}@{2}:{3}/{4}'.format(POSTGRES_LOGIN, POSTGRES_PASS, POSTGRES_SERVER,
                                                       POSTGRES_PORT,
                                                       POSTGRES_BASE))
meta = MetaData(bind=engine)

users = Table('users', meta,
              Column('uid', Integer, primary_key=True),
              Column('username', String),
              Column('password', String),
              Column('email', String),
              Column('token', String),
              Column('tokenexp', DateTime),
              Column('status_id', Integer),
              Column('role_id', Integer)
              )

messages = Table('messages', meta,
                 Column('mid', Integer, primary_key=True),
                 Column('to_id', Integer, ForeignKey('users.uid')),
                 Column('from_id', Integer, ForeignKey('users.uid')),
                 Column('message', String),
                 Column('dtime', DateTime))

contacts = Table('contacts', meta,
                 Column('cid', Integer, primary_key=True),
                 Column('user_id', Integer, ForeignKey('users.uid')),
                 Column('contact', Integer, ForeignKey('users.uid')))

#-------------------------------------------------------------------
groups = Table('groups', meta,
              Column('gid', Integer, primary_key=True),
              Column('groupname', String),
              Column('creation_date', DateTime),
              Column('creater_user_id', Integer))

user_groups = Table('user_groups', meta,
              Column('userid', Integer, ForeignKey('users.uid')),
              Column('groupid', Integer, ForeignKey('groups.gid')))

#---------------------------------------------------roles
user_roles = Table('user_roles', meta,
              Column('roleid', Integer, primary_key=True),
              Column('role_name', String))

status_of_user = Table('status_of_user', meta,
                       Column('usid', Integer, primary_key=True),
                       Column('status_name', String))

meta.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

session.add_all([CUserRoles(role_name='admin'),
                 CUserRoles(role_name='teacher'),
                 CUserRoles(role_name='student'),
                 CUserRoles(role_name='admin_group'),
                 CUserRoles(role_name='user'),
                 CUserStatus(status_name='online'),
                 CUserStatus(status_name='offline'),
                 CUserStatus(status_name='banned'),
                 CUserStatus(status_name='not confirmed'),
                 ])
session.commit()
