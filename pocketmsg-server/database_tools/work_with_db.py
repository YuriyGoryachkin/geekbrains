from sqlalchemy.orm import sessionmaker
from database_tools.alchemy import CUsers, CContacts, CMessages
from database_tools.init import engine
from datetime import datetime

dtime = datetime.now()


class ServerStorage:

    def __init__(self):
        Session = sessionmaker(bind=engine)
        session = Session()
        self.session = session

    def __commit(self):
        self.session.commit()

    def _get_client_by_username(self, username):
        """ Возвращает клиента с username """
        client = self.session.query(CUsers).filter(CUsers.username == username).first()
        return client

    def check_email_all(self, email):
        result = self.session.query(CUsers.email).filter(CUsers.email == email).all()
        return result

    def check_email_one_or_none(self, contact):
        result = self.session.query(CUsers).filter(CUsers.email == contact).one_or_none()
        return result

    def check_name_one_or_none(self, name):
        result = self.session.query(CUsers.username).filter(CUsers.username == name).one_or_none()
        return result

    def check_token_one_or_none(self, check_result):
        result = self.session.query(CUsers).filter(CUsers.uid == check_result.uid).one_or_none()
        return result

    def check_contact_first(self, user, exists_contact):
        result = self.session.query(CContacts).filter(CContacts.user_id == user.uid,
                                                 CContacts.contact == exists_contact.uid).first()
        return result

    def check_contacts(self, check_result):
        result = self.session.query(CContacts, CUsers).filter(CContacts.user_id == check_result.uid)
        return result

    def contacts_join(self, contacts):
        query = contacts.join(CUsers, CUsers.uid == CContacts.contact)
        return query



    def add_user(self, username, password, email, token, tokenexp):
        verify = CUsers(username=username, password=password, email=email, token=token, tokenexp=tokenexp)
        self.session.add(verify)
        self.__commit()

    def add_history(self, from_id, to_id, message):
        if from_id and to_id:
            history = CMessages(message=message, from_id=from_id, to_id=to_id, dtime=dtime)
            self.session.add(history)
            self.__commit()
        else:
            pass

    def add_contact_list(self, uid, contact):
        client = self._get_client_by_username(contact)
        if uid and client:
            contact_list = CContacts(user_id=uid, contact=client.uid)
            self.session.add(contact_list)
            self.__commit()
        else:
            pass

    def delete_user(self, username, password):
        pass

    def check_delete_contact(self, check_result, result):
        result_db = self.session.query(CContacts).filter(CContacts.user_id == check_result.uid,
                                                    CContacts.contact == result.uid).delete()
        return result_db