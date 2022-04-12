# 连接mongodb

import pymongo
import time
from config import get_config
from log_util import TNLog

log = TNLog()

host = get_config("db_host")
port = get_config("db_port")
date = get_config("date")
if date is None:
    date = time.strftime("%Y-%m-%d", time.localtime())
else:
    date = date.__str__()

use_conn_str = get_config("use_conn_str")
if use_conn_str:
    client = pymongo.MongoClient(get_config("connection_string"))
else:
    client = pymongo.MongoClient(host, port)

db = client.sehuatang


# 枚举，通过fid获取板块名称
def get_plate_name(fid):
    if fid == 103:
        return "hd_chinese_subtitles"
    elif fid == 104:
        return "vegan_with_mosaic"
    elif fid == 37:
        return "asia_mosaic_originate"
    elif fid == 36:
        return "asia_codeless_originate"
    elif fid == 39:
        return "anime_originate"
    elif fid == 160:
        return "vr_video"
    else:
        return "other"


# 保存数据(已存在的数据不保存)
def save_data(data_list, fid):
    """
    :param data: 字典
    """
    collection_name = get_plate_name(fid)
    collection = db[collection_name]
    tid_list = find_data_tid(collection_name, date)
    data_list_new = compare_data(data_list, tid_list)
    if len(data_list_new) > 0:
        collection.insert_many(data_list_new)
        log.info("保存数据成功, 共存入数据库{}条".format(len(data_list_new)))
    else:
        log.info("未查询到新数据")


# 查询数据, 拿到已存在的数据id
def find_data_tid(collection_name, date):
    """
    :param data: 字典
    """
    collection = db[collection_name]
    # 构造查询条件
    query = {"post_time": {"$regex": "^" + date}}
    # 查询数据, 返回指定的字段
    res = collection.find(query, {"_id": 0, "date": 1, "tid": 1})
    # 将查询结果中的id提取出来
    tid_list = []
    for i in res:
        tid_list.append(i["tid"])
    return tid_list


# 比对tid，将不存在的信息筛选出来
def compare_data(data_list, id_list):
    """
    :param data: 字典
    """
    data_list_new = []
    for i in data_list:
        if i["tid"] not in id_list:
            data_list_new.append(i)
    return data_list_new


# 筛选不存在的tids
def compare_tid(tid_list, fid):
    collection_name = get_plate_name(fid)
    id_list = find_data_tid(collection_name, date)

    tid_list_new = []
    for i in tid_list:
        if i not in id_list:
            tid_list_new.append(i)
    return tid_list_new
