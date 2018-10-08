from websocket import create_connection

# url = "wss://pocketmsg.ru:8888/v1/ws/"
url = "ws://127.0.0.1:8888/v1/ws/"

ws = create_connection(url, header=['token:d53e124e6b31e34d'])
print("Sending some message...")
msg = ''
while msg != 'exit':
    msg = input('Enter message to send: ')
    ws.send(msg)
    print("Sent")

    print("Reсeiving...")
    result = ws.recv()
    print("Received '%s'" % result)

ws.close()
