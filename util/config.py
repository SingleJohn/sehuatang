import time
from util.read_config import get_config


mongodb = get_config('mongodb')
mongodb_enable = mongodb.get('enable')
mongodb_host = mongodb.get('db_host')
mongodb_port = mongodb.get('db_port')
mongodb_conn_str = mongodb.get('connection_string')
mongodb_use_conn_str = mongodb.get('use_conn_str')

mysql = get_config('mysql')
mysql_enable = mysql.get('enable')
mysql_host = mysql.get('host')
mysql_port = mysql.get('port')
mysql_user = mysql.get('user')
mysql_passwd = mysql.get('password')
mysql_db = mysql.get('db')

domain = get_config('domain_name')
fid_json = get_config('fid')
fid_list = [key for key in fid_json]
fid_value_list = [fid_json[key] for key in fid_json]
page_num = get_config('page_num')

proxy = get_config('proxy')
proxy_url = proxy.get('proxy_url')
proxy_enable = proxy.get('proxy_enable')

if proxy_enable:
    proxy = proxy_url
else:
    proxy = None

send_msg = get_config('sendMessage')
tg_enable = send_msg.get('send_telegram_enable')
tg_bot_token = send_msg.get('tg_bot_token')
tg_chat_id = send_msg.get('tg_chat_id')


date = get_config("date")
if date is None:
    date = time.strftime("%Y-%m-%d", time.localtime())
else:
    date = date.__str__()

schedule_time = get_config("schedule_time")