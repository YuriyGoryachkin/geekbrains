import argparse
from socket import *
import sys
import select
import json
import time

from jim_message.jim_message import JIMMessageServer
from log import log_config

"""
Проблема с JSON

1. Запустить сервер
2. Запуск последовательно 3-х клиентов(без выбора режима работы)
3. Выбор режима msg в первом клиенте
4. Выбор режима receiver во втором клиенте
5. Выбор режима receiver в третьем клиенте
Ошибка:
Проблема с JSON!!!
raise JSONDecodeError("Expecting value", s, err.value) from None
json.decoder.JSONDecodeError: Expecting value: line 1 column 1 (char 0)
"""


def create_parser(Default_Port, Default_Host, Default_Block):
    parser_serv = argparse.ArgumentParser(prog='server', description='сервер', epilog='(C)2018')
    parser_serv.add_argument('-p', '--port', type=int, default=Default_Port, help='порт')
    parser_serv.add_argument('-a', '--host', type=str, default=Default_Host, help='IP-адрес')
    parser_serv.add_argument('-b', '--blocking', type=int, default=Default_Block, help='блокировка сокета')
    return parser_serv


class Clients_Base:
    """ Класс работает с базой клиентов """
    def __init__(self):
        self.base = []

    @log_config.log(__qualname__)
    def add_client(self, new_client):
        """ Добавление клиента в базу """
        self.base.append(new_client)
        return '\nclient app: {}\n'.format(new_client)

    @log_config.log(__qualname__)
    def remove_client(self, del_client):
        """ Удаление клиента из базы """
        self.base.remove(del_client)
        return '\nclient del: {}\n'.format(del_client)


class JIM_Server:
    """ Класс должен обрабатывать полученные сообщения от клиента и ответы сервера """

    def __init__(self, obj_Server):
        self.protocol = JIMMessageServer()
        self.server = obj_Server
        self.clients = Clients_Base()

    @staticmethod
    def __deserialization_msg(data):
        """ Декодирует полученное сообщение """
        return json.loads(data.decode('utf-8'))

    @log_config.log(__qualname__)
    def receive_response(self, client, data):
        """ проверка по action """
        w_clients = self.clients.base
        try:
            response = self.__deserialization_msg(data)
            # log_config.log_server.debug('[Server]:'
            #                             ' receive_response:'
            #                             ' response:\n{}'.format(response))
            if response.get('action').startswith('presence'):
                # log_config.log_server.debug('[Server]:'
                #                             ' receive_response(presence):'
                #                             ' response:\n{}'.format(response))
                self.clients.add_client(client)
                client.sendall(self.protocol.good_response())
            elif response.get('action').startswith('msg'):
                user = response['user']
                msg = response['message']
                # log_config.log_server.debug('[Server]:'
                #                             ' receive_response(msg):'
                #                             ' response:\n{}'.format(response))
                for s_client in w_clients:
                    try:
                        s_client.sendall(
                            self.protocol.response_6xx(600, user['account_name'], msg))
                        # log_config.log_server.debug('[Server]:'
                        #                             ' receive_response600:'
                        #                             ' response:\n{}'.format(json.loads(self.protocol.response_6xx(600, user['account_name'], msg).decode('utf-8'), encoding='utf-8')))
                    except:
                        pass
                # return '\nsend:\n{}\n'.format(msg)
            elif response.get('action').startswith('quit'):
                # log_config.log_server.debug('[Server]:'
                #                             ' receive_response(quit):'
                #                             ' response:\n{}'.format(response))
                self.clients.remove_client(client)
                log_config.log_server.debug('[Server]:'
                                            ' receive_response:'
                                            ' client {}'
                                            ' offline'.format(client))
                client.close()
                user = response['user']
                msg = response['message']
                for s_client in w_clients:
                    try:
                        s_client.sendall(self.protocol.response_6xx(600, user['account_name'], msg))
                    except:
                        pass
            else:
                log_config.log_server.info('[Server]:'
                                           ' Сообщение содержит'
                                           ' неверный /response/')
                pass
            # response = {}
        except:
            """
            1. Запустить сервер
            2. Запуск последовательно 3-х клиентов(без выбора режима работы)
            3. Выбор режима msg в первом клиенте
            4. Выбор режима receiver во втором клиенте
            5. Выбор режима receiver в третьем клиенте
            Ошибка:
            Проблема с JSON!!!
            raise JSONDecodeError("Expecting value", s, err.value) from None
            json.decoder.JSONDecodeError: Expecting value: line 1 column 1 (char 0)
            """
            log_config.log_server.debug('[Server]:'
                                        ' receive_response(data):'
                                        ' response:\n{}'.format(self.__deserialization_msg(data)))
            time.sleep(2)


class Server:
    def __init__(self, server_host, server_port):
        self.address = (server_host, server_port)

    @log_config.log(__qualname__)
    def start_JIM(self, JIM_server):
        try:
            self.protocol = JIM_server()
            return True, 'JIM protocol: OK'
        except:
            log_config.log_server.error('[Server]: JIM protocol: FAIL')
            return False, '\nJIM protocol: FAIL\n'

    @log_config.log(__qualname__)
    def stop(self):
        """ Остановка сервера """
        self.__stop()
        log_config.log_server.debug('[Server]: shutdown')
        sys.exit()  # Вызавает ошибку unittest_server

    @log_config.log(__qualname__)
    def __stop_non_socket(self, e):
        """ Остановка без создания сервера """
        log_config.log_server.warning('[Server]: stop, error,'
                                      ' non socket: {}'.format(e))
        self.__stop()
        sys.exit()

    @log_config.log(__qualname__)
    def __stop_is_error(self, e):
        """ Остановка сервера из-за ошибки """
        log_config.log_server.error('[Server]: stop, error: {}'.format(e))
        self.__stop()
        sys.exit()

    @log_config.log(__qualname__)
    def make_tcp_socket(self, blocking_sock=0):
        """ Запуск сервера """
        try:
            self.sock = socket(AF_INET, SOCK_STREAM)
            self.sock.setblocking(blocking_sock)
            self.sock.bind(self.address)
            sock_start = True
        except ConnectionError as e:
            log_config.log_server.error('[Server]: stop, error,'
                                        ' non socket: {}'.format(e))
            self.__stop_non_socket(e)
        except PermissionError as e:
            log_config.log_server.error('[Server]: stop, error: {}'.format(e))
            log_config.log_server.debug('[Server]: ошибка запуска сервера,'
                                        ' у вас нет прав '
                                        'на запуск сервера: {}'.format(self.address))
            log_config.log_server.debug('[Server]: измените настройки'
                                        ' (хост/порт) или обратитесь'
                                        ' к администратору')
            self.__stop_non_socket(e)
        except OSError as e:
            log_config.log_server.error('[Server]: stop, error: {}'.format(e))
            log_config.log_server.debug('[Server]: ошибка запуска сервера,'
                                        ' адрес уже используется: {}'.format(self.address))
            log_config.log_server.debug('[Server]: измените настройки'
                                        ' (хост/порт)')
            self.__stop_non_socket(e)
        else:
            self.sock.listen(5)
            self.sock.settimeout(0.2)
            self.handler = JIM_Server(self.sock)
            log_config.log_server.debug('[Server]: start')
            return sock_start

    def connect_clients(self):
        """ Подключение клиентов """
        while True:
            try:
                client, client_host = self.sock.accept()
                data = client.recv(MAX_DATA)  #
                print('\ndata: {}\n'.format(data))
                self.handler.receive_response(client=client, data=data)
            except OSError:
                pass
            except KeyboardInterrupt:
                self.stop()
            else:
                client_base = self.handler.clients.base
            finally:
                r = []
                w = []
                try:
                    r, w, e = select.select(client_base, client_base, [], 0)
                except:
                    pass
                request_msg = self.read_request(r)
                self.write_request(request_msg)

    @log_config.log(__qualname__)
    def _remove_client(self, client):
        """ Удаление клиента из списка """
        self.handler.clients.remove_client(client)
        return '\n{} remove\n'.format(client)

    @staticmethod
    def read_request(r_clients):
        """ Чтение запросов из списка клиентов """
        messages = []
        for client in r_clients:
            try:
                data = client.recv(MAX_DATA)
                messages.append((client, data))
            except OSError:
                # log_config.log_server.debug('[Server]: read_request:'
                #                             ' client {}'
                #                             ' offline'.format(client))
                # self._remove_client(client)
                # self.handler.clients.remove_client(client)
                pass

            except:
                log_config.log_server.error('[Server]:'
                                            ' read_request:'
                                            ' ERROR')
                pass
        return messages

    def write_request(self, messages):
        """ Эхо-ответ сервера клиентам """
        for message in messages:
            self.responses(message[0], message[1])

    def responses(self, client, data):
        self.handler.receive_response(client=client, data=data)

    def __stop(self):
        self.sock.shutdown(SHUT_RDWR)


if __name__ == '__main__':
    from config.config import *

    DH = DEFAULT_HOST
    DP = DEFAULT_PORT
    DB = DEFAULT_BLOCKING
    JIM = JIMMessageServer
    MC = MAX_CLIENT

    parser = create_parser(DP, DH, DB)
    namespace = parser.parse_args(sys.argv[1:])
    host = namespace.host
    port = namespace.port
    blocking = namespace.blocking
    server = Server(host, port)
    if server.make_tcp_socket(blocking):
        if server.start_JIM(JIM):
            server.connect_clients()
