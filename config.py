import yaml
import os

dir = os.path.dirname(__file__)
config_path = os.path.join(dir, "config.yaml")

# 读取配置文件
def read_config(config_path):
    with open(config_path, "r", encoding="utf-8") as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
    return data


# 配置获取函数，支持二级配置，供其他模块调用
def get_config(key=None):
    if key is None:
        return read_config(config_path)
    data = read_config(config_path)
    if key in data:
        return data[key]
    else:
        for i in data:
            if key in data[i]:
                return data[i][key]
    return None

