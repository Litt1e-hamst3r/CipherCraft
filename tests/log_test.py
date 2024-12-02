import logging
from datetime import datetime
import os

# 这个还是加在前端吧

def setup_logger(name):
    # 创建一个logger
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)  # 设置最低的日志级别为DEBUG

    # 创建一个handler用于写入日志文件
    now = datetime.now()
    log_filename = f"./log/app_{now.strftime('%Y%m%d_%H%M%S')}.log"
    
    # 确保日志目录存在
    log_dir = os.path.dirname(log_filename)
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    file_handler = logging.FileHandler(log_filename)
    file_handler.setLevel(logging.DEBUG)

    # 创建一个handler用于输出到控制台
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    # 定义handler的输出格式
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # 给logger添加handler
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger

if __name__ == "__main__":
        # 获取logger实例
    logger = setup_logger("test_logger")

    # 记录一条debug级别的日志
    logger.debug("This is a debug message")

    # 记录一条info级别的日志
    logger.info("This is an info message")

    # 记录一条warning级别的日志
    logger.warning("This is a warning message")

    try:
        x = 1 / 0
    except ZeroDivisionError as e:
        # 记录一条error级别的日志
        logger.error("An error occurred: %s", e)

    # 记录一条critical级别的日志
    logger.critical("This is a critical message")