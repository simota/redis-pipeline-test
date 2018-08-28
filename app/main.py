import time
import redis
import random


redis_client = redis.StrictRedis(host='redis', port=6379, db=0)


def measurement(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        func(*args, **kwargs)
        elapsed_time = time.time() - start_time
        print("{}:{} sec".format(func.__name__, elapsed_time))
    return wrapper


def setup_keys():
    redis_client.flushdb()
    value = '*' * 10000
    prefix = '_' * 255

    keys = ['{}_key_{}'.format(prefix, i) for i in range(0, 20000)]
    [redis_client.set(key, value) for key in keys]
    return random.sample(keys, 3000)


@measurement
def delete_keys_use_pipeline(keys):
    pipe = redis_client.pipeline(transaction=False)
    for key in keys:
        pipe.delete(key)
    pipe.execute()


@measurement
def delete_keys(keys):
    for key in keys:
        redis_client.delete(key)


if __name__ == '__main__':
    delete_keys(setup_keys())
    delete_keys_use_pipeline(setup_keys())
