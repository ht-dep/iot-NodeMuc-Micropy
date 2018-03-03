import redis
# coding=utf-8
from pymongo import MongoClient
import datetime
import logging

logging.basicConfig(level=logging.DEBUG, format='[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s')

def getDate():
    now = datetime.datetime.now().strftime("%Y%m%d")
    return now


def getTime():
    now = datetime.datetime.now().strftime("%Y-%m-%d ")
    return now


class LOG:

    @staticmethod #中间件--tcp服务
    def middle():
        logger=logging.getLogger('%s:%d' % ("MIDDLE", 9876))
        return logger

    @staticmethod #后台---websocket服务
    def end():
        logger=logging.getLogger('%s:%d' % ('END', 9999))
        return logger

    @staticmethod #后台---web服务
    def web():
        logger=logging.getLogger('%s:%d' % ('WEB', 9999))
        return logger


class DBSENSOR:
    '''
    存储数据模型,此模型只适合用来存储数据，不适合记录下载图片情形
    {"date":"2017-03-06",
   "data":
            {
             "id":"",
             "tem":"",
             "wet":"",
             "time":"",}
        }
    '''

    def __init__(self):
        self.time = getTime()
        self.table = "sensor" + getDate()
        self.MONGODB_URI = "mongodb://localhost:27017/"
        self.client = MongoClient(self.MONGODB_URI)
        self.db = self.client["sensor"]
        self.collection = self.db[self.table]

    def save(self, record):
        self.collection.save(record)

    def query(self):
        try:
            res = {}
            # todo find({"flag":true})验证  再做数据修改{"flag":false}
            rc = self.collection.find_one()
            r = rc[self.table]
            res["tem"] = r["tem"]
            res["wet"] = r["wet"]
            res["time"] = r["time"]
            print(res)
        except Exception as e:
            print("查询出错")
            res = {self.time: {}}
        return res


# class DBSENSOR:
#     '''
#     存储数据模型
#     一天一个表 table20170306
#     {
#     "id":"",
#     "tem":"",
#     "wet":""，
#     "datetime":""
#     "flag":True
#     }
#     '''
#
#     def __init__(self):
#         self.date = "sensor" + getDate()
#         self.MONGODB_URI = "mongodb://localhost:27017/"
#         self.client = MongoClient(self.MONGODB_URI)
#         self.db = self.client["sensordb"]
#         self.collection = self.db[self.date]
#
#     def insert(self, record):
#         # 数据在外部查询结束后，再插入数据库
#         self.collection.insert(record)
#
#     def insert_many(self, recordList):
#         self.collection.insert_many(recordList)
#
#     def count(self):
#         count = self.collection.count()
#         return count
#
#     def tcheck(self):
#         # 针对一条记录存储所有数据list
#         # 判断数据是否存在，判断key的存在，再判断value的长度
#         # self.collection.
#         pass
#
#     def query(self):
#         results = []
#         try:
#             records = self.collection.find()
#             # 可以再优化
#             for r in records:
#                 print(r)
#                 res = {}
#                 res["tem"] = r["tem"]
#                 res["wet"] = r["wet"]
#                 res["datetime"] = r["datetime"]
#                 res["flag"]=r["flag"]
#                 results.append(res)
#             return results
#         except Exception as e:
#             print("DBHistory query error:{}".format(e))
#     def check(self):
#
#         print("start")
#         try:
#             num = self.collection.find().count()
#             print(num)
#             if num == 0:
#                 return saveHistory()
#             else:
#                 return self.query()
#         except Exception as e:
#             print(e)

class RedisHelper(object):
    def __init__(self):
        self.__conn = redis.Redis(host='127.0.0.1', port=6379)  # 连接Redis
        self.channel = 'monitor'  # 定义名称
        self.video_channel="video"  #摄像头监控主题

    def publish(self, msg):  # 定义发布方法
        self.__conn.publish(self.channel, msg)
        return True

    def publish_video(self, msg):  # 摄像头监控发布方法
        self.__conn.publish(self.video_channel, msg)
        return True

    def subscribe(self):  # 定义订阅方法
        pub = self.__conn.pubsub()
        pub.subscribe(self.channel)
        pub.parse_response()
        return pub
    def subscribe_video(self):  # 定义订阅方法
        pub = self.__conn.pubsub()
        pub.subscribe(self.video_channel)
        pub.parse_response()
        return pub


if __name__ == "__main__":
    pass
    # data={"tem":"tem","wet":"wet","time":getTime(),"flag":True}
    # data = {DBSENSOR().table: {"tem": "tem", "wet": "wet", "time": getTime(), "flag": True}}
    # DBSENSOR().save(data)
    DBSENSOR().query()
