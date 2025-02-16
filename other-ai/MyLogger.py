import logging
import os
from logging.handlers import RotatingFileHandler

global logger

# 创建 logger
logger = logging.getLogger("my_logger")
logger.setLevel(logging.DEBUG)

# 创建控制台处理器
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

log_dir="/log"
# 检查目录是否存在，如果不存在则创建
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

# 创建文件处理器
#file_handler = logging.FileHandler(log_dir+"/ai.log")

# 创建按大小轮转的日志处理器
file_handler = RotatingFileHandler(log_dir+"/ai.log", maxBytes=1024 * 1024 * 10, backupCount=5)  # 每个文件最大 10MB，保留 5 个备份

file_handler.setLevel(logging.DEBUG)


# 定义日志格式
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
console_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

# 添加处理器到 logger
logger.addHandler(console_handler)
logger.addHandler(file_handler)

if __name__ == "__main__":
    logger.debug("调试信息 %s","1111111111")
    logger.info("普通信息")
    logger.warning("警告信息")
    logger.error("错误信息")
    logger.critical("严重错误信息")
 