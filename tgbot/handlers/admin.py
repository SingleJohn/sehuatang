from telebot import TeleBot
from telebot.types import Message
from util.config import fid_list
from main import crawler
import asyncio


def admin_user(message: Message, bot: TeleBot):
    """
    You can create a function and use parameter pass_bot.
    """
    bot.send_message(message.chat.id, "Hello, admin!")


def crawl_plate(message: Message, bot: TeleBot):
    """
    You can create a function and use parameter pass_bot.
    """
    msg = message.json.get('text').split(' ')
    # 参数为空时，返回帮助信息
    if len(msg) != 2:
        bot.send_message(message.chat.id, "请输入正确的参数，如：/c 103")
        return

    fid = msg[1]

    # list中的数字转化为字符串
    fid_str = [str(i) for i in fid_list]
    if fid in fid_str:
        bot.send_message(message.chat.id, "正在爬取...，请稍后")
        rec_msg = asyncio.run(crawler(int(fid)))
        bot.send_message(message.chat.id, rec_msg)
    else:
        bot.send_message(message.chat.id, "fid不在配置文件中或者格式错误")



