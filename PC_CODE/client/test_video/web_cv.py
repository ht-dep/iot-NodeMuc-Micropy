import socket
import asyncio
import websockets
import threading
import datetime
import json
import time
from config import RedisHelper, LOG
import os
import base64
import cv2
os.system("title 后台--WEBSOCKET服务")  # 修改命令行的显示标题
logger = LOG.end()

ids = set()  # flash.id列表
sensor_dt = {}
sdt = {}
sensor_CD={}
# sensor_CD = {"123":{"wet":"1","tem":"2","id":"3","time":"4","gateway":5},
#              "125":{"wet":"1","tem":"2","id":"3","time":"4","gateway":5},
#              }  # 所有的网关
flag = False
img=""

# 处理数据
# 接受传感器的数据以及mac地址
video_data = ""  # 视频字节流
video_dt = {}
video_CD = {}

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
            # 解析数据
            sensor_dt["tem"] = message[0]
            sensor_dt["wet"] = message[1]
            sensor_dt["id"] = message[2]  # 传感器的Flash_id
            sensor_dt["time"] = current_time
            # sensor_dt["gateway"] = ""
            # 待完善
            # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
            if len(message) > 3:
                sensor_dt["ph"] = message[3]
                sensor_dt["voc"] = message[4]
            else:
                sensor_dt["ph"] = "未传入"
                sensor_dt["voc"] = "未传入"
            # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
            id = message[2]
            ids = sensor_CD.keys()
            if id in ids:
                sensor_CD[id] = dict(sensor_CD[id], **sensor_dt)
                # logger.info("该传感器已存在：{}".format(sensor_CD[id]))
            else:
                sensor_num = len(ids)  # 集合转化为列表
                gw_name = "GATEWAY" + str(sensor_num + 1)
                logger.info("接入的第{}个传感器:{}".format(sensor_num + 1, gw_name))
                sensor_CD[id] = dict(sensor_dt, **{"gateway": gw_name})


        except Exception as e:
            logger.debug("*********************************")
            logger.debug("原始数据：{}".format(msg))
            logger.debug("订阅者遇到错误：{}".format(e))
            logger.debug("*********************************")


# 处理数据
# 接受摄像头监控的数据以及mac地址
def sub_video():
    obj = RedisHelper()
    redis_sub = obj.subscribe_video()  # 调用订阅方法
    global sensor_dt
    while True:
        data_byte = redis_sub.parse_response()[2]
        try:
            data = json.loads(data_byte.decode())
            # logger.info(data)
            s_img = "data:image/jpeg;base64," + data["img"]
            logger.info("base64 编码图片流")
            # logger.info(s_img)
            current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            logger.debug("摄像头监控订阅者得到消息：{}   {}".format("", current_time))
            video_dt["video"] = s_img
            video_dt["id"] = data["id"]  # 传感器的Flash_id//
            video_dt["time"] = current_time

            id = data["id"]
            ids = video_CD.keys()
            if id in ids:
                video_CD[id] = dict(video_CD[id], **video_dt)
                # logger.info("该视频监控已存在：{}".format(video_CD[id]))
            else:
                video_num = len(ids)  # 集合转化为列表
                gw_name = "视频监控" + str(video_num + 1)
                logger.info("接入的第{}个摄像头监控{}".format(video_num + 1, gw_name))
                video_CD[id] = dict(video_dt, **{"gateway": gw_name})

        except Exception as e:
            logger.debug("*********************************")
            logger.debug("摄像头监控订阅者遇到错误：{}".format(e))
            logger.debug("*********************************")

async def hello(websocket, path):
    while True:
        logger.info("*********************")
        video_LS = [video for video in video_CD.values()]
        # logger.info(video_LS)
        logger.info(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        sensor_LS = [sensor for sensor in sensor_CD.values()]
        data={"sensors":sensor_LS,"videos":video_LS}
        if not video_LS and not sensor_LS:
            logger.info("没有数据")
            await asyncio.sleep(5)


        else:
            await websocket.send(json.dumps(data))
            await asyncio.sleep(0.1)
        logger.info("<<<<<<<<<<<<<<<<<<<<<<<<<")
        # logger.debug(">>>发送数据 {}".format(data_json))



if __name__ == "__main__":
    t1 = threading.Thread(target=sub_video)
    t1.start()
    t2 = threading.Thread(target=sub)
    t2.start()
    start_server = websockets.serve(hello, '0.0.0.0', 8899)
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()
