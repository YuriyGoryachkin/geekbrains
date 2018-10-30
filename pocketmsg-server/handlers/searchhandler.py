from handlers.json_util import JsonHandler
from database_tools.alchemy import CUsers

class SearchHandlers(JsonHandler):
    def prepare(self):
        super().prepare()
        self.check_result = self._token_check()

    def post(self):
        if self.check_result:
            try:
                search = self.json_data['search']
                if search.count('@'):
                    search_email = self.db.query(CUsers).filter(CUsers.email == search).all()
                    self.set_status(201, 'Found')
                    self.response['result'] = search_email
                    self.write_json()

                else:
                    search_username = self.db.query(CUsers).filter(CUsers.username == search).all()
                    if search_username:
                        self.set_status(201, 'Found')
                        self.response['result'] = search_username
                        self.write_json()

                    else:
                        self.set_status(404, 'User not found')
            except:
                self.send_error(400, reason='No or bad request body')