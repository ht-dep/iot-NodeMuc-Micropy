import socket
import time
import threading
import random
import json

a=[19,23,35,36,41,38,37,28]
b=[55,66,77,65,76,52]
c=[77,72,73,75,78]
d=["bad","middle",'good',"better"]

def cli_recv(cli):
    while 1:
        data = cli.recv(1024)
        print("接收到数据：", data.decode())


def cli_send(cli):
    while 1:
        cli.send(json.dumps([random.choice(a),random.choice(b),"模拟网关1",random.choice(c),random.choice(d)]).encode())
        time.sleep(5)


cli = socket.socket()
# cli.connect(("127.0.0.1", 10001))
cli.connect(("192.168.199.72", 10001))
# cli.connect(("47.90.92.56", 59962))
cli_send(cli)
# while 1:
# cli.send("hello".encode())
# time.sleep(5)
# t1 = threading.Thread(target=cli_send, args=(cli,))
# t2 = threading.Thread(target=cli_recv, args=(cli,))
# t1.start()
# t2.start()

# cli.close()
