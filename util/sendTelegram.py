import telebot
from telebot.types import InputMediaPhoto
from telebot.util import antiflood
import time
from util.log_util import log
from util.config import get_config


bot_token = get_config("tg_bot_token")
chat_id = get_config("tg_chat_id")
bot = telebot.TeleBot(bot_token)



def special_char_sub(text):
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
    for i in range(len(old_strs)):
        text = text.replace(old_strs[i], new_strs[i])
    return text

fid_name_dict = {
    103: "高清中文字幕",
    104: "素人有码系列",
    37: "亚洲有码原创",
    36: "亚洲无码原创",
    39: "动漫原创",
    160: "vr",
    151: "4k",
    2: "国产原创",
    38: "欧美无码",
    107: "三级写真",
    152: "韩国主播",
}


def send_media_group(data_list, fid):
    for data in data_list:
        if fid in fid_name_dict:
            tag_name = fid_name_dict[fid]
        else:
            tag_name = "other"
        magnet = data["magnet"]
        magnet_115 = data["magnet_115"]
        title = data["title"]
        num = data["number"]
        post_time = data["post_time"]
        image_list = data["img"]
        if magnet_115 is None:
            content = f"\n{num} {title}\n\n磁力链接：\n{magnet}\n\n发布时间：{post_time}\n\n #{tag_name}"
        else:
            content = f"\n{num} {title}\n\n磁力链接：\n{magnet}\n防115屏蔽压缩包磁链：\n{magnet_115}\n\n发布时间：{post_time}\n\n #{tag_name}"
        content = special_char_sub(content)
        media_group = []
        for image in image_list:
            index = image_list.index(image)
            if index == len(image_list) - 1:
                media_group.append(InputMediaPhoto(media=image, caption=content, parse_mode="markdownV2"))
            else:
                media_group.append(InputMediaPhoto(media=image))
        antiflood(bot.send_media_group, chat_id=chat_id, media=media_group)
        log.debug(f"send_media_group: {content}")
    if len(data_list) > 0:
        name_list = [data["number"] + " " + data["title"] for data in data_list]
        time_str = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        send_message_text = f"#{tag_name} 抓取完成。\n\n本次抓取共抓取{len(data_list)}个资源 \n\n抓取时间：{time_str} \n\n抓取结果: \n"
        name_str = "\n".join(name_list)
        send_message_text += name_str

        antiflood(bot.send_message, chat_id=chat_id, text=send_message_text)
        log.info(f"send telegram message success: {send_message_text}")




if __name__ == '__main__':
    pass



