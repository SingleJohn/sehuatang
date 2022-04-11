# 色花堂BT区页面爬取脚本

1. 使用方式
   1. `pip install -r requirements.txt` 安装依赖
   2. 将 `config_bak.yaml` 文件改为 `config.yaml`
   3. 修改配置项，运行 `main.py` 即可


2. 目前实现的功能
   - 按板块抓取指定日期的信息
   - 将数据存入 MongoDB
   - 判断数据是否存在，存在则跳过
   - 异步并发

3. 当前功能基本够用，可能会改进的地方
   - 导出数据到 Excel


4. 常见问题
   1. cloudflare 防护绕过
      - 可以使用 cloudflare 的 workers ，对网站进行反向代理，然后爬取域名设置为 workers 的域名即可
      - workers 代码参考 ：production.js


5. 其他
   - 一个公共的mongodb库(权限只读)
      - `mongodb+srv://readonly:cS9NSuiJ1ebHnUL0@cluster0.8mosa.mongodb.net/Cluster0?retryWrites=true&w=majority`