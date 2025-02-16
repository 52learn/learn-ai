from MyLogger import logger
# 缓存装饰器
def cacheFunc(f):
    cache={}
    def wrapper(*args, **kwargs):
        cache_key = f"{f.__name__}_{args}_{kwargs}"
        logger.debug(f"cache_key:{cache_key}")
        if cache_key in cache:
            return cache[cache_key]
        result = f(*args, **kwargs)
        cache[cache_key] = result
        return result
    return wrapper