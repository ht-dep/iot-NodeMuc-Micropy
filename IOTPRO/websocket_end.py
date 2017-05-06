import socket
import asyncio
import websockets
import threading
import datetime
import json
from config import RedisHelper, LOG

logger = LOG.end()
sd = []
sensor_dt = {}
flag = False


def sub():
    obj = RedisHelper()
    redis_sub = obj.subscribe()  # 调用订阅方法
    global sensor_dt
    while True:
        msg = redis_sub.parse_response()[2]
        # logger.debug(msg)
        try:
            message = json.loads(msg.decode("utf8"))
            # logger.debug(type(message))
            current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            logger.debug("订阅者得到消息：{}   {}".format(message, current_time))
            sensor_dt["tem"] = message[0]
            sensor_dt["wet"] = message[1]
            sensor_dt["time"] = current_time
        except Exception as e:
            logger.debug("*********************************")
            logger.debug("原始数据：{}".format(msg))
            logger.debug("订阅者遇到错误：{}".format(e))
            logger.debug("*********************************")


def check_key(json_data):
    key = json.loads(json_data)
    if key["key"] == "rinpo":
        return True
    return False


async def hello(websocket, path):
    while True:
        # logger.debug("websokcet服务端发送的数据:{}".format(sensor_dt))
        data_json = json.dumps(sensor_dt, ensure_ascii=False)
        await websocket.send(data_json)
        logger.debug(">>>发送数据 {}".format(data_json))
        await asyncio.sleep(5)


if __name__ == "__main__":
    t1 = threading.Thread(target=sub)
    t1.start()
    start_server = websockets.serve(hello, '0.0.0.0', 9999)
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()
