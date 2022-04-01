# -*- coding: utf-8 -*-
import os
import time
import logging
import inspect
from logging.handlers import RotatingFileHandler

dir = os.path.dirname(__file__)
dir_time = time.strftime("%Y-%m-%d", time.localtime())

if os.path.exists(dir + "/logs") is False:
    os.mkdir(dir + "/logs")


handlers = {
    logging.NOTSET: os.path.join(dir, "logs/notset.log"),
    logging.DEBUG: os.path.join(dir, "logs/debug.log"),
    logging.INFO: os.path.join(dir, "logs/info.log"),
    logging.WARNING: os.path.join(dir, "logs/warning.log"),
    logging.ERROR: os.path.join(dir, "logs/error.log"),
    logging.CRITICAL: os.path.join(dir, "logs/critical.log"),
}


def createHandlers():
    logLevels = handlers.keys()

    for level in logLevels:
        path = os.path.abspath(handlers[level])
        handlers[level] = RotatingFileHandler(
            path, maxBytes=10000000, backupCount=2, encoding="utf-8"
        )


# 加载模块时创建全局变量

createHandlers()


class TNLog(object):
    def printfNow(self):
        return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    def __init__(self, level=logging.NOTSET):
        self.__loggers = {}

        logLevels = handlers.keys()

        for level in logLevels:
            logger = logging.getLogger(str(level))

            # 如果不指定level，获得的handler似乎是同一个handler?

            logger.addHandler(handlers[level])

            logger.setLevel(level)

            self.__loggers.update({level: logger})

    def getLogMessage(self, level, message):
        frame, filename, lineNo, functionName, code, unknowField = inspect.stack()[2]

        """日志格式：[时间] [类型] [记录代码] 信息"""

        return "[%s] [%s] [%s - %s - %s] %s" % (
            self.printfNow(),
            level,
            filename,
            lineNo,
            functionName,
            message,
        )

    def info(self, message):
        message = self.getLogMessage("info", message)

        self.__loggers[logging.INFO].info(message)

    def error(self, message):
        message = self.getLogMessage("error", message)

        self.__loggers[logging.ERROR].error(message)

    def warning(self, message):
        message = self.getLogMessage("warning", message)

        self.__loggers[logging.WARNING].warning(message)

    def debug(self, message):
        message = self.getLogMessage("debug", message)

        self.__loggers[logging.DEBUG].debug(message)

    def critical(self, message):
        message = self.getLogMessage("critical", message)

        self.__loggers[logging.CRITICAL].critical(message)


if __name__ == "__main__":
    logger = TNLog()

    logger.debug("debug")
    logger.info("info")
    logger.warning("warning")
    logger.error("error")
    logger.critical("critical")
