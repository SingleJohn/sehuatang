import asyncio
import time
import random
import httpx
import bs4
import re

from mongo import save_data, compare_tid, filter_data
from config import get_config
from log_util import TNLog
from sendMessage import SendWeCom, send_tg2

log = TNLog()


# 获取帖子的id(访问板块)
async def get_plate_info(fid: int, page: int, proxy: str, date_time: str):
    """
    :param fid: 板块id
    :param page: 页码
    :param proxy: 代理服务器地址
    :param date_time: 日期，格式: 2019-01-01

    :return: info_list
    """
    log.info("Crawl the plate " + str(fid) + " page number " + str(page))
    url = "https://{}/".format(get_config("domain_name"))
    # 参数
    params = {
        "mod": "forumdisplay",
        "fid": fid,
        "page": page,
    }

    # 存放字典的列表
    info_list = []
    tid_list = []

    response = httpx.get(url, params=params, proxies=proxy)
    # 使用bs4解析
    soup = bs4.BeautifulSoup(response.text, "html.parser")
    # print(soup)
    all = soup.find_all(id=re.compile("^normalthread_"))
    try:
        for i in all:
            data = {}
            title_list = i.find("a", class_="s xst").get_text().split(" ")
            number = title_list[0]
            title_list.pop(0)
            title = " ".join(title_list)
            # date = i.find("span", attrs={"title": re.compile("^" + date_time)})
            date_td_em = i.find("td", class_="by").find("em")
            date_span = date_td_em.find(
                "span", attrs={"title": re.compile("^" + date_time)}
            )
            if date_span is not None:
                date = date_span.attrs["title"]
            else:
                flag = date_td_em.get_text().startswith(date_time)
                if flag:
                    date = date_td_em.get_text()
                else:
                    continue
            # print(date)
            if date is None:
                continue
            id = i.find(class_="showcontent y").attrs["id"].split("_")[1]
            data["number"] = number
            data["title"] = title
            data["date"] = date
            data["tid"] = id
            info_list.append(data)
            tid_list.append(id)
        log.debug("Crawl the plate " + str(fid) + " page number " + str(page))
        log.debug(" ".join(tid_list))
    except Exception as e:
        log.error(e)
    return info_list, tid_list


# 访问每个帖子的页面
async def get_page(tid, proxy, f_info):
    """
    :param tid: 帖子id
    :param proxy: 代理服务器地址
    :param f_info: 帖子信息
    """

    data = {}
    # log.info("Crawl the page " + tid)
    url = "https://{}/?mod=viewthread&tid={}".format(get_config("domain_name"), tid)

    try:
        response = httpx.get(url, proxies=proxy)
        soup = bs4.BeautifulSoup(response.text, "html.parser")
        # log.warning("Crawl the soup " + soup)
        # 获取帖子的标题
        title = soup.find("h1", class_="ts").find("span").get_text()
        # 楼主发布的内容
        info = soup.find("td", class_="t_f")
        # 存放图片的列表
        img_list = []
        for i in info.find_all("img"):
            img_list.append(i.attrs["file"])
        # 磁力链接
        magnet = soup.find("div", class_="blockcode").find("li").get_text()
        # 发布时间
        # post_time = (
        #     soup.find("img", class_="authicn vm")
        #     .parent.find("em")
        #     .find("span")
        #     .attrs["title"]
        # )
        post_time_em = soup.find("img", class_="authicn vm").parent.find("em")
        post_time_span = post_time_em.find("span")
        if post_time_span is not None:
            post_time = post_time_span.attrs["title"]
        else:
            post_time = post_time_em.get_text()[4:]

        data["title"] = title
        data["post_time"] = post_time
        data["img"] = img_list
        data["magnet"] = magnet
        log.debug("Crawl the page " + tid)
        log.debug(data.values())
        return data, f_info
    except Exception as e:
        log.error("Crawl the page " + tid + " failed.")
        log.error(e)


def main():
    # 获取配置
    config = get_config()
    fid_list = config["sehuatang"]["fid"]
    page_num = config["sehuatang"]["page_num"]
    date_time = config["sehuatang"]["date"]

    if date_time is None:
        date_time = time.strftime("%Y-%m-%d", time.localtime())
    else:
        date_time = date_time.__str__()

    proxy_enable = config["proxy"]["proxy_enable"]
    if proxy_enable:
        proxy = config["proxy"]["proxy_host"]
    else:
        proxy = None

    log.debug("日期: " + date_time)
    # 循环抓取所有页面
    for fid in fid_list:
        info_list_all = []
        tid_list_all = []
        for page in range(1, page_num + 1):
            try:
                info_list, tid_list = get_plate_info(fid, page, proxy, date_time)
                info_list_all.extend(info_list)
                tid_list_all.extend(tid_list)
            except Exception as e:
                log.error(e)
                continue
            finally:
                continue
        log.info("即将开始爬取的页面 " + " ".join(tid_list_all))
        tid_list_all = compare_tid(tid_list_all, fid)
        log.info("需要爬取的页面 " + " ".join(tid_list_all))
        data_list = []
        for i in info_list_all:
            try:
                data = get_page(i["tid"], proxy)
                data["number"] = i["number"]
                data["title"] = i["title"]
                data["date"] = i["date"]
                data["tid"] = i["tid"]
                post_time = data["post_time"]
                # 再次匹配发布时间（因为上级页面获取的时间可能不准确）
                if re.match("^" + date_time, post_time):
                    data_list.append(data)
            except Exception as e:
                log.error("Crawl the page " + " ".join(list(i.values())) + " failed.")
                log.error(e)
                continue
            finally:
                continue
        log.info("本次抓取的数据条数为：" + str(len(data_list)))
        log.info("开始写入数据库")
        save_data(data_list, fid)


async def main2():
    # 获取配置
    config = get_config()
    fid_list = config["sehuatang"]["fid"]
    page_num = config["sehuatang"]["page_num"]
    date_time = config["sehuatang"]["date"]

    if date_time is None:
        date_time = time.strftime("%Y-%m-%d", time.localtime())
    else:
        date_time = date_time.__str__()

    proxy_enable = config["proxy"]["proxy_enable"]
    if proxy_enable:
        proxy = config["proxy"]["proxy_host"]
    else:
        proxy = None

    log.debug("日期: " + date_time)

    for fid in fid_list:
        tasks = []  # 存放所有的任务
        for page in range(1, page_num + 1):
            tasks.append(
                # loop.run_in_executor(None, get_plate_info, fid, page, proxy, date_time)
                get_plate_info(fid, page, proxy, date_time)
            )
        # 开始执行协程
        results = await asyncio.gather(*tasks)

        # 将结果拼接
        info_list_all = []
        tid_list_all = []
        for result in results:
            info_list, tid_list = result
            info_list_all.extend(info_list)
            tid_list_all.extend(tid_list)
        log.info("即将开始爬取的页面 " + " ".join(tid_list_all))

        tid_list_new, info_list_new = compare_tid(tid_list_all, fid, info_list_all)
        log.info("需要爬取的页面 " + " ".join(tid_list_new))

        data_list = []
        tasks = []
        for i in info_list_new:
            tasks.append(get_page(i["tid"], proxy, i))
        results = await asyncio.gather(*tasks)
        results_new = [i for i in results if i is not None]
        for result in results_new:
            data, i = result
            data["number"] = i["number"]
            data["title"] = i["title"]
            data["date"] = i["date"]
            data["tid"] = i["tid"]
            post_time = data["post_time"]
            # 再次匹配发布时间（因为上级页面获取的时间可能不准确）
            if re.match("^" + date_time, post_time):
                data_list.append(data)
        log.info("本次抓取的数据条数为：" + str(len(data_list)))
        log.info("开始写入数据库")
        # data_list.reverse()
        data_list_new = filter_data(data_list, fid)
        save_data(data_list_new, fid)
        if get_config("send_telegram_enable"):
            send_tg2(data_list_new, fid)

    if get_config("send_wecom_enable"):
        send_message()


def send_message():
    wecom = SendWeCom()
    from mongo import get_send_context
    wecom.send_message("色花堂抓取结果", get_send_context(), "mpnews")


if __name__ == "__main__":
    # main()
    # 随机延时
    time.sleep(random.randint(10, 300))
    asyncio.run(main2())
    # asyncio.get_event_loop().run_until_complete(main2())
    # get_plate_info("103", 5, "http://127.0.0.1:11223", "2022-03")
    # get_page("819398", "http://127.0.0.1:11223", 2333)

