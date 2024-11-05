from ftchat.applicationConf import redis_password, redis_host, redis_port

REDIS_URL = 'redis://:{}@{}:{}/0'.format(redis_password,redis_host,redis_port)
CELERY_BROKER_URL = REDIS_URL  # 使用 Redis 作为消息代理
CELERY_RESULT_BACKEND = REDIS_URL