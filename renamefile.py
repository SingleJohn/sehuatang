import os
import shutil
import pymongo
from log_util import TNLog

log = TNLog()


def get_file_info(path):
    file_info_list = []
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(".mp4"):
                file_info = {}
                # print(file.split("-C")[0])
                file_info["file_name"] = file.split("-C")[0]
                # print(os.path.join(root, file))
                file_info["file_path"] = root
                file_info["file_path_name"] = os.path.join(root, file)
                file_info_list.append(file_info)
    return file_info_list


def get_mongo_info():
    # 查询mongodb中的文件名，通过字符串查询
    client = pymongo.MongoClient(
        "mongodb+srv://dong:6f9j27Kn6cDvHCne@cluster0.8mosa.mongodb.net/Cluster0?retryWrites=true&w=majority"
    )
    db = client.sehuatang
    collection = db.hd_chinese_subtitles
    # res = collection.find({}, {"_id": 0, "number": 1, "title": 1}).sort("_id", pymongo.DESCENDING).limit(50)
    res = collection.find({}, {"_id": 0, "number": 1, "title": 1})

    return res


def rename_file_name(file_info_list, res):
    ll = []
    # 重命名文件
    for i in res:
        for j in file_info_list:
            # 不区分大小写
            if i["number"].lower() == j["file_name"].lower():
                ld = {}
                name = i["number"].lower() + "-C " + i["title"]
                print(i["title"])
                print(j["file_path_name"])
                # 获取文件修改时间
                file_time = os.path.getmtime(j["file_path_name"])
                # 获取文件创建时间
                file_create_time = os.path.getctime(j["file_path_name"])

                change_path_name = os.path.join(j["file_path"], name + ".mp4")

                # 重命名文件
                shutil.move(j["file_path_name"], change_path_name)
                # 重命名时间
                os.utime(change_path_name, (file_time, file_create_time))
                ld["number"] = j["file_name"].lower() + "-C"
                ld["file_name"] = name
                ll.append(ld)
    return ll


def get_dirs(path):
    # 获取所有文件夹
    dir_info_list = []
    root, dirs, _ = os.walk(path).__next__()
    for dir_name in dirs:
        dir_info = {}
        # dir_path = os.path.join(root, dir_name)
        dir_info["dir_name"] = dir_name
        dir_info["dir_path"] = root
        dir_info_list.append(dir_info)
    return dir_info_list


def rename_dir_name(dir_info_list, old_new):
    # 重命名文件夹
    for i in dir_info_list:
        for j in old_new:
            if i["dir_name"].lower() == j["number"].lower():
                dir_old_path_name = os.path.join(i["dir_path"], i["dir_name"])
                dir_new_path_name = os.path.join(i["dir_path"], j["file_name"])
                print(dir_old_path_name)
                print(dir_new_path_name)
                # 重命名文件夹
                shutil.move(dir_old_path_name, dir_new_path_name)
    pass


def main():
    path = r"Y:\aria2_downloaded"

    file_info_list = get_file_info(path)

    res = get_mongo_info()

    old_new = rename_file_name(file_info_list, res)

    dir_info_list = get_dirs(path)

    rename_dir_name(dir_info_list, old_new)


if __name__ == "__main__":
    main()
