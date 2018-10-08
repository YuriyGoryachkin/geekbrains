from database_tools.alchemy import CUsers
from database_tools.init import engine
from sqlalchemy.orm import sessionmaker

Session = sessionmaker()
Session.configure(bind=engine)
session = Session()

addUser = CUsers('tester3', 'qwerty', 'monguste@gmail.com', 'd53e124e6b31e34d')

session.add(addUser)

q_user = session.query(CUsers).filter_by(username="tester3").all()
print(q_user)

session.commit()