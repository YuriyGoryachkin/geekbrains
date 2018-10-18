from handlers.json_util import JsonHandler
from database_tools.alchemy import CUsers, CContacts
from database_tools.work_with_db import ServerStorage



class ContactsHandler(JsonHandler):
    def prepare(self):
        super().prepare()
        self.check_result = self._token_check()

    def post(self):
        if self.check_result:
            contact = self.json_data['contact']
            exists_contact = self.db.query(CUsers).filter(CUsers.email == contact).one_or_none()        ###
            exists_contact = ServerStorage().check_email_one_or_none(contact)        ###
            if exists_contact is None:
                self.set_status(404, 'User does not exists')
            else:
                result = self.db.query(CContacts).filter(CContacts.user_id == self.check_result.uid,
                                                         CContacts.contact == exists_contact.uid).first()       ###
                result = ServerStorage().check_contact_first(user=self.check_result, exists_contact=exists_contact)      ###
                if result is None:
                    # new_contact = CContacts(user_id=self.check_result.uid, contact=exists_contact.uid)
                    # self.db.add(new_contact)
                    # self.db.commit()
                    ServerStorage().add_contact_list(uid=self.check_result.uid, contact=exists_contact.uid)     ###
                    self.set_status(201, 'Added')
                else:
                    self.set_status(409, 'Contact already in list')

    def delete(self):
        if self.check_result:
            contact = self.json_data['contact']
            result = self.db.query(CUsers).filter(CUsers.email == contact).one_or_none()        ###
            result = ServerStorage().check_name_one_or_none(contact)        ###
            result_db = self.db.query(CContacts).filter(CContacts.user_id == self.check_result.uid,
                                                        CContacts.contact == result.uid).delete()       ###
            result_db = ServerStorage().check_delete_contact(check_result=self.check_result, result=result)       ###
            if not result_db:
                self.set_status(404, 'Not in your contact list')
            else:
                self.db.commit()        ###
                result_db.commit()      ###
                self.set_status(200)
                self.response['deleted_contact_id'] = result.uid
                self.response['deleted_contact_username'] = result.username
                self.write_json()
        else:
            self.send_error(400)

    def get(self):
        if self.check_result:
            contacts = self.db.query(CContacts, CUsers).filter(CContacts.user_id == self.check_result.uid)      ###
            contacts = ServerStorage().check_contacts(self.check_result)
            query = contacts.join(CUsers, CUsers.uid == CContacts.contact)      ###
            query = ServerStorage().contacts_join(contacts)     ###
            records = query.all()
            for i in range(len(records)):
                self.response[i] = records[i].CUsers.username
            self.write_json()
