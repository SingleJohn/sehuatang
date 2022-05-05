# python3
# -*- coding: utf-8 -*-
import requests
import time
import json
import config



class SendMessage:
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
        res = requests.get(url, params).json()
        # config.set_config("wework", "access_token", res["access_token"])
        # config.set_config("wework", "update_time", str(time.time()))
        self.access_token = res["access_token"]

    def get_application_list(self):
        if config.get_config("wework", "agent_id") is not None:
            return
        url = "https://qyapi.weixin.qq.com/cgi-bin/agent/list"
        params = {"access_token": config.get_config("wework", "access_token")}
        res = requests.get(url, params).json()
        config.set_config("wework", "agent_id", str(res["agentlist"][0]["agentid"]))
        config.set_config("wework", "agent_name", res["agentlist"][0]["name"])

    # def get_application_info(self):
    #     url = "https://qyapi.weixin.qq.com/cgi-bin/agent/get"
    #     params = {
    #         "access_token": config.get_config("wework", "access_token"),
    #         "agentid": config.get_config("wework", "agent_id"),
    #     }
    #     res = requests.get(url, params).json()
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
        res = requests.post(self.send_url, params=params, data=send_msgs).json()
        if res["errcode"] == 0:
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


def main():
    wework = SendMessage()
    # wework.get_access_token()
    wework.send_message("测试54321", "测试666", "mpnews")
    # wework.get_application_info()


if __name__ == "__main__":
    main()