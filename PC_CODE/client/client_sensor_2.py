import socket
import time
import threading
import random
import json

a=[19,23,35,56,77,66,37,28]
b=[67,77,79,59,69]
c=[323,325,326,327,328]

def cli_recv(cli):
    while 1:
        data = cli.recv(1024)
        print("接收到数据：", data.decode())


def cli_send(cli):
    while 1:
        cli.send(json.dumps([random.choice(a),random.choice(b),"模拟网关2"]).encode())
        time.sleep(5)


cli = socket.socket()
cli.connect(("127.0.0.1", 10002))
cli_send(cli)
# while 1:
# cli.send("hello".encode())
# time.sleep(5)
# t1 = threading.Thread(target=cli_send, args=(cli,))
# t2 = threading.Thread(target=cli_recv, args=(cli,))
# t1.start()
# t2.start()

# cli.close()
