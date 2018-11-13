from database_tools.alchemy import CGroups, CUserStatus, CCollGroup, CCategoryGroup, CUserRoles, CUsers, CContacts, CGroupsUsers, CMessages, CBase
from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
from database_tools.db_connect import POSTGRES_SERVER, POSTGRES_PORT, POSTGRES_LOGIN, POSTGRES_PASS, POSTGRES_BASE
from datetime import datetime

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
print('date - {}'.format(datetime.utcnow()))
#
category_multi = session.query(CCategoryGroup).filter(CCategoryGroup.category_name == 'Multi').first()
category_single = session.query(CCategoryGroup).filter(CCategoryGroup.category_name == 'Single').first()
print('category - {}'.format(category_multi))
#
# supergroup = CGroups(creation_date=datetime.utcnow(),
#                      group_name='test_group3',
#                      creater_user_id=out.uid,
#                      category_group=category.category_id)
#
# session.add(supergroup)
# session.commit()
out_group = session.query(CGroups).filter(CGroups.creater_user_id == out.uid).all()
print('out_group - {}'.format(out_group))

grand_group = session.query(CGroups).filter(CGroups.category_group == category_multi.category_id).first()
add_group = session.query(CGroups).filter(CGroups.category_group == category_single.category_id).first()
coll_gr = CCollGroup(collgroup_id=grand_group.gid,
                     group_id=add_group.gid)
session.add(coll_gr)
session.commit()

''' Удаление таблиц '''
# CBase.metadata.drop_all(engine)
