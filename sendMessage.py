# python3
# -*- coding: utf-8 -*-
import time
from time import sleep

import httpx
import json
import config
import telegram
from telegram import InputMediaPhoto

from log_util import TNLog

log = TNLog()


class SendWeCom:
    def __init__(self):
        self.access_token = None
        self.agent_id = config.get_config("agent_id")
        self.corp_id = config.get_config("corp_id")
        self.app_secret = config.get_config("corp_secret")
        self.send_url = "https://qyapi.weixin.qq.com/cgi-bin/message/send"

    def get_access_token(self) -> None:
        """获取鉴权token"""
        url = "https://qyapi.weixin.qq.com/cgi-bin/gettoken"
        params = {"corpid": self.corp_id, "corpsecret": self.app_secret}
        res = httpx.get(url, params=params).json()
        log.info("send_wecom_message.get_access_token: {}".format(res))
        # config.set_config("wework", "access_token", res["access_token"])
        # config.set_config("wework", "update_time", str(time.time()))
        self.access_token = res["access_token"]

    def get_application_list(self):
        if config.get_config("wework", "agent_id") is not None:
            return
        url = "https://qyapi.weixin.qq.com/cgi-bin/agent/list"
        params = {"access_token": config.get_config("wework", "access_token")}
        res = httpx.get(url, params=params).json()
        config.set_config("wework", "agent_id", str(res["agentlist"][0]["agentid"]))
        config.set_config("wework", "agent_name", res["agentlist"][0]["name"])

    # def get_application_info(self):
    #     url = "https://qyapi.weixin.qq.com/cgi-bin/agent/get"
    #     params = {
    #         "access_token": config.get_config("wework", "access_token"),
    #         "agentid": config.get_config("wework", "agent_id"),
    #     }
    #     res = httpx.get(url, params).json()
    #     config.set_config("wework", "agent_name", res["name"])
    #     config.set_config("wework", "agent_id", res["agentid"])
    #     # print(res)

    def send_text_message(self, title, content="", touser="@all"):
        if title != "":
            content = title + "\n" + content
        data = {
            "agentid": self.agent_id,
            "touser": touser,
            "msgtype": "text",
            "text": {"content": content},
        }
        self.send_request(data)

    def send_markdown_message(self, title, content, touser="@all"):
        data = {
            "touser": touser,
            "msgtype": "markdown",
            "agentid": self.agent_id,
            "markdown": {"content": content},
        }
        self.send_request(data)

    def send_mpnews_message(self, title, content, touser="@all"):
        if config.get_config("media_id") is None:
            self.send_text_message(title, content)
            return
        data = {
            "touser": touser,
            "msgtype": "mpnews",
            "agentid": self.agent_id,
            "mpnews": {
                "articles": [
                    {
                        "title": title,
                        "thumb_media_id": config.get_config("media_id"),
                        "author": "Author",
                        "content_source_url": "URL",
                        "content": content.replace("\n", "<br>"),
                        "digest": content,
                    }
                ]
            },
            "safe": 0,
            "enable_id_trans": 0,
            "enable_duplicate_check": 0,
            "duplicate_check_interval": 1800,
        }
        self.send_request(data)

    def send_request(self, data):
        send_msgs = bytes(json.dumps(data), "utf-8")
        params = {"access_token": self.access_token}
        res = httpx.post(self.send_url, params=params, data=send_msgs).json()
        log.info("send_wecom_message.send_request: {}".format(res))
        if res["errcode"] == 0:
            log.info("send_wecom_message: success")
            return True, res["errmsg"]
        else:
            return False, res["errmsg"]

    # def update_access_token(self):
    #     if config.get_config("wework", "update_time") is None:
    #         self.get_access_token()
    #         return
    #     if time.time() - float(config.get_config("wework", "update_time")) > 7200:
    #         self.get_access_token()
    #         return

    def send_message(self, title: str, content: str, type: str = "text"):
        self.get_access_token()
        touser = config.get_config("to_user")
        # self.get_application_list()
        if type == "text":
            self.send_text_message(title, content, touser)
        elif type == "markdown":
            self.send_markdown_message(title, content, touser)
        elif type == "mpnews":
            self.send_mpnews_message(title, content, touser)


class SendTelegram:
    def __init__(self):
        self.chat_id = config.get_config("tg_chat_id")
        self.token = config.get_config("tg_bot_token")
        self.proxy_host = config.get_config("proxy_host")
        if config.get_config("proxy_enable"):
            self.proxy = telegram.utils.request.Request(proxy_url=self.proxy_host)
        else:
            self.proxy = None
        self.bot = telegram.Bot(token=self.token, request=self.proxy)

    def send_message(self, message):
        self.bot.send_message(chat_id=self.chat_id, text=message)

    def send_photo(self, photo_url, caption=None):
        self.bot.send_photo(chat_id=self.chat_id, photo=photo_url, caption=caption)

    def send_media_group(self, media_list):
        self.bot.send_media_group(chat_id=self.chat_id, media=media_list)


bot = SendTelegram()


def send_telegram_request(content: str):
    proxy_enable = config.get_config("proxy_enable")
    if proxy_enable:
        proxy = config.get_config("proxy_host")
    else:
        proxy = None
    url = "https://api.telegram.org/bot{}/sendMessage".format(
        config.get_config("tg_bot_token")
    )
    data = {
        "chat_id": config.get_config("tg_chat_id"),
        "text": content,
        "parse_mode": "markdownV2",
        "disable_notification": True,
    }
    res = httpx.post(url, data=data, proxies=proxy).json()
    # print(res)
    if res["ok"]:
        return True
    else:
        log.error(data)
        log.error("send telegram message error: {}".format(res))
        return False


def send_tg(data_list, fid):
    if config.get_config("tg_bot_token") is None:
        log.info("tg_bot_token is None")
        return
    if config.get_config("tg_chat_id") is None:
        log.info("tg_chat_id is None")
        return
    tag_name = get_chinese_name(fid)
    for data in data_list:
        magnet = data["magnet"]
        title = data["title"]
        num = data["number"]
        post_time = data["post_time"]
        image_str = data["img"][0]
        old_strs = [
            "_",
            "*",
            "[",
            "]",
            "(",
            ")",
            "~",
            "`",
            ">",
            "#",
            "+",
            "-",
            "=",
            "|",
            "{",
            "}",
            ".",
            "!",
        ]
        new_strs = [
            "\_",
            "\*",
            "\[",
            "\]",
            "\(",
            "\)",
            "\~",
            "\`",
            "\>",
            "\#",
            "\+",
            "\-",
            "\=",
            "\|",
            "\{",
            "\}",
            "\.",
            "\!",
        ]

        content = f"{num} {title}\n\n{magnet}\n\n发布时间：{post_time} \n{image_str}\n\n #{tag_name}"
        # 替换特殊字符
        for i in range(len(old_strs)):
            content = content.replace(old_strs[i], new_strs[i])
        if send_telegram_request(content):
            log.info(f"send telegram message success: {title} {num}")
        sleep(3)


def send_tg_message(data, tag_name):
    magnet = data["magnet"]
    title = data["title"]
    num = data["number"]
    post_time = data["post_time"]
    image_str = data["img"][0]
    old_strs = [
        "_",
        "*",
        "[",
        "]",
        "(",
        ")",
        "~",
        "`",
        ">",
        "#",
        "+",
        "-",
        "=",
        "|",
        "{",
        "}",
        ".",
        "!",
    ]
    new_strs = [
        "\_",
        "\*",
        "\[",
        "\]",
        "\(",
        "\)",
        "\~",
        "\`",
        "\>",
        "\#",
        "\+",
        "\-",
        "\=",
        "\|",
        "\{",
        "\}",
        "\.",
        "\!",
    ]

    content = (
        f"{num} {title}\n\n{magnet}\n\n发布时间：{post_time} \n{image_str}\n\n #{tag_name}"
    )
    # 替换特殊字符
    for i in range(len(old_strs)):
        content = content.replace(old_strs[i], new_strs[i])
    if send_telegram_request(content):
        log.info(f"send telegram message success: {title} {num}")
    else:
        log.error(f"second send telegram message error: {title} {num}")
    sleep(3)


def send_tg_media_group(data_list, fid):
    if config.get_config("tg_bot_token") is None:
        log.error("tg_bot_token is None")
        return
    if config.get_config("tg_chat_id") is None:
        log.error("tg_chat_id is None")
        return
    tag_name = get_chinese_name(fid)

    for data in data_list:
        magnet = data["magnet"]
        title = data["title"]
        num = data["number"]
        post_time = data["post_time"]
        image_list = data["img"]
        old_strs = [
            "_",
            "*",
            "[",
            "]",
            "(",
            ")",
            "~",
            "`",
            ">",
            "#",
            "+",
            "-",
            "=",
            "|",
            "{",
            "}",
            ".",
            "!",
        ]
        new_strs = [
            "\_",
            "\*",
            "\[",
            "\]",
            "\(",
            "\)",
            "\~",
            "\`",
            "\>",
            "\#",
            "\+",
            "\-",
            "\=",
            "\|",
            "\{",
            "\}",
            "\.",
            "\!",
        ]
        content = f"\n{num} {title}\n\n{magnet}\n\n发布时间：{post_time}\n\n #{tag_name}"
        # 替换特殊字符
        for i in range(len(old_strs)):
            content = content.replace(old_strs[i], new_strs[i])
        media_group = []
        for image_str in image_list:
            index = image_list.index(image_str)
            if index == len(image_list) - 1:
                media_group.append(
                    InputMediaPhoto(
                        media=image_str, parse_mode="markdownV2", caption=content
                    )
                )
            else:
                media_group.append(InputMediaPhoto(media=image_str))
        try:
            bot.send_media_group(media_group)
            log.info(f"send telegram message success: {num} {title}")
        except Exception as e:
            log.error(f"send telegram message error: {num} {title}")
            log.error(e)
            # mediaGroup 发送失败是，尝试调用普通发送
            send_tg_message(data, tag_name)
        # 延迟10秒，原因见 https://telegra.ph/So-your-bot-is-rate-limited-01-26
        sleep(10)
    if len(data_list) > 0:
        sleep(10)
        try:
            name_list = [data["number"] + " " + data["title"] for data in data_list]
            time_str = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            send_message_text = f"#{tag_name} 抓取完成。\n\n本次抓取共抓取{len(data_list)}个资源 \n\n 抓取时间：{time_str} \n\n 抓取结果: \n "
            name_str = "\n".join(name_list)
            send_message_text += name_str
            # send_telegram_request(send_message_text)
            bot.send_message(send_message_text)
            log.info(f"send telegram message success: {send_message_text}")
        except Exception as e:
            log.error(f"send text error" + e)


def get_chinese_name(fid):
    if fid == 103:
        return "高清中文字幕"
    elif fid == 104:
        return "素人有码系列"
    elif fid == 37:
        return "亚洲有码原创"
    elif fid == 36:
        return "亚洲无码原创"
    elif fid == 39:
        return "动漫原创"
    elif fid == 160:
        return "vr"
    elif fid == 151:
        return "4k"
    else:
        return "other"


def main():
    # wework = SendMessage()
    # wework.get_access_token()
    # wework.send_message("测试54321", "测试666", "mpnews")
    # wework.get_application_info()
    # content = '[图片](https://i.imgur.com/KaiskSW.jpeg)\n[图片2](https://i.imgur.com/KaiskSW.jpeg)'

    content = """
    <a href="https://i.imgur.com/KaiskSW.jpeg"> </a>
    <a href="https://i.imgur.com/u31nq0Q.jpeg"> </a>
    <b>bold</b>, <strong>bold</strong>
    <i>italic</i>, <em>italic</em>
    <pre><code class="language-python">pre-formatted fixed-width code block written in the Python programming language</code></pre>
    """

    test_data_list = []

    # send_telegram_request(content)

    # send_tg(datalist, 103)

    send_tg_media_group(test_data_list, 104)


if __name__ == "__main__":
    main()
