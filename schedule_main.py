import asyncio
import schedule
import time

from main import main
from util.read_config import get_config
from util.log_util import TNLog
log = TNLog()


def get_schedule_time():
    schedule_time = get_config("schedule_time")
    log.info("计划任务时间为：" + " ".join(schedule_time))
    return schedule_time


def run_schedule():
    schedule_time = get_schedule_time()
    for i in schedule_time:
        schedule.every().day.at(i).do(asyncio.run(main()))
    asyncio.run(main())
    while True:
        schedule.run_pending()
        time.sleep(1)

