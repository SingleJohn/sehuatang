# 色花堂BT区页面爬取脚本

1. 使用方式
   1. `pip install -r requirements.txt` 安装依赖
   2. 将 `config_bak.yaml` 文件改为 `config.yaml`
   3. 修改配置项，运行 `main.py` 即可


2. 目前实现的功能
   - 按板块抓取指定日期的信息
   - 将数据存入 MongoDB
   - 判断数据是否存在，存在则跳过

3. 当前功能基本够用，可能会改进的地方
   - 异步并发
   - 导出数据到 Excel
