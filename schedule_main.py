import asyncio
import schedule
import time

from main import main
from util.log_util import log
from util.config import schedule_time


def get_schedule_time():
    log.info("计划任务时间为：" + " ".join(schedule_time))
    return schedule_time


def run_schedule():
    time_list = get_schedule_time()
    for i in time_list:
        schedule.every().day.at(i).do(asyncio.run(main()))
    asyncio.run(main())
    while True:
        schedule.run_pending()
        time.sleep(1)

