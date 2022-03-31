import yaml

# 读取配置文件
def read_config(file_name):
    with open(file_name, "r", encoding="utf-8") as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
    return data


# 配置获取函数，支持二级配置，供其他模块调用
def get_config(key=None):
    if key is None:
        return read_config("config.yaml")
    data = read_config("config.yaml")
    if key in data:
        return data[key]
    else:
        for i in data:
            if key in data[i]:
                return data[i][key]
    return None


# def get_config(key):
#     data = read_config("config.yaml")
#     return data[key]


if __name__ == "__main__":
    print(get_config("domain_name000"))
    print(get_config("domain_name"))
    print(get_config())
