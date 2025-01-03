import redis
from django.conf import settings

def get_redis_client():
    return redis.StrictRedis(host=settings.REDIS_HOST,
                               port=settings.REDIS_PORT,
                                decode_responses=True)
