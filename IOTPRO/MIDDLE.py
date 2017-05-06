import socket
import asyncio
import websockets
import threading
import json
import datetime
from config import RedisHelper, LOG
import os
os.system("title 中间件---TCP服务")#修改命令行的显示标题
current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

obj = RedisHelper()
logger = LOG.middle()

def server_socket(conn, addr):
    logger.debug("接入客户端的ip地址：{}".format(addr))
    while 1:
        res = conn.recv(1024)
        recv_json = res.decode()
        if not len(res):
            conn.close()

        logger.debug("当前时间：{}".format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        logger.debug("TcpServer接收到的数据：{}".format(recv_json))

        obj.publish(recv_json)
        logger.debug("发布者 发布：{}".format(recv_json))

def main():
    s = socket.socket()
    s.bind(("0.0.0.0", 9876))
    s.listen(5)
    while 1:
        conn, addr = s.accept()
        t1 = threading.Thread(target=server_socket, args=(conn, addr))
        t1.start()

if __name__ == "__main__":
    main()
