import time
from MyLogger import logger
def timer(f):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = f(*args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time
        logger.debug(f"func_name:{f.__name__} Execution time: {execution_time} seconds")
        return result
    return wrapper