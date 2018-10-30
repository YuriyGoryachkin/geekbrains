from handlers.json_util import JsonHandler
from database_tools.alchemy import CUsers, CContacts

class SearchHandlers(JsonHandler):
    def prepare(self):
        super().prepare()
        self.check_result = self._token_check()

    # def get(self):
    #     if self.check_result:
    #         try:
    #             contact = self.json_data['search']
    #             search_contact = self.db.query(CUsers).filter(CUsers.email == contact).all()
    #             if search_contact is None:
    #                 self.set_status(404, 'User not found')
    #             else:
    #                 self.set_status(201, 'Found')
    #                 self.response['found_username'] = search_contact.username
    #                 self.write_json()
    #         except:
    #             self.send_error(400, reason='No or bad request body')
    def get(self):
        if self.check_result:
            try:
                contact = self.json_data['search']
                search_email = self.db.query(CUsers).filter(CUsers.email == contact).all()
                search_username = self.db.query(CUsers).filter(CUsers.username == contact).all()
                if search_email:
                    search_contact = search_email
                    self.set_status(201, 'Found')
                    self.response['found_username'] = search_contact.username
                    self.write_json()

                elif search_username:
                    search_contact = search_username
                    self.set_status(201, 'Found')
                    self.response['found_username'] = search_contact.username
                    self.write_json()

                else:
                    self.set_status(404, 'User not found')
            except:
                self.send_error(400, reason='No or bad request body')
