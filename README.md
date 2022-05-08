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
   - 推送到企业微信
   - 推送到telegram（带封面图），效果可见 https://t.me/sehuatang_crawler

3. 当前功能基本够用，可能会改进的地方
   - 导出数据到 Excel


4. 常见问题
   1. cloudflare 防护绕过
      - 可以使用 cloudflare 的 workers ，对网站进行反向代理，然后爬取域名设置为 workers 的域名即可
      - workers 代码参考 ：[production.js](util/production.js)
   2. ~~telegram 频道条目不全~~(应该已经修复)
      - telegram api 限制单条消息的大小，如图片过大，则会导致发送的消息过大，报错--()
      - 完整数据在 mongodb 中


5. 其他
   - `main` 、 `dev` 分支都是过渡版本(应该不会再维护了)，最新版本为`async`分支
   - 一个公共的mongodb库(权限只读)
      - `mongodb+srv://readonly:cS9NSuiJ1ebHnUL0@cluster0.8mosa.mongodb.net/Cluster0?retryWrites=true&w=majority`
   - 有使用问题可以提issues
   - 为避免原站压力过大，建议直接订阅上面的 telegram 频道，或使用上方提供的公共数据库查看数据
   - 预览图可见：[effect picture](effect%20picture)
