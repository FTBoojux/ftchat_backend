from django_redis import get_redis_connection
import redis
import ftchat.applicationConf as conf
import jwt
from datetime import datetime

redis_client = redis.StrictRedis(host=conf.redis_host, port=conf.redis_port, password=conf.redis_password,db=0)

lua_script = """
local tokens = redis.call('lrange', KEYS[1], 0, -1)
for i, token in ipairs(tokens) do
    if ARGV[i] == 'true' then
        redis.call('lrem', KEYS[1], 1, token)
    end
end
redis.call('rpush', KEYS[1], ARGV[#ARGV])
"""

update_token_script = redis_client.register_script(lua_script)

def is_token_expired(token):
    try:
        decoded = jwt.decode(token,conf.jwt_security_key,algorithms='HS256')
    except jwt.exceptions.ExpiredSignatureError:
        return True
    expiration_date = datetime.utcfromtimestamp(decoded['exp'])
    return expiration_date < datetime.utcnow()


def token_add(uid,token,secrect_key=conf.jwt_security_key):
    lock = redis_client.lock(f'{uid}-lock')
    with lock:
        tokens = redis_client.lrange(f'{uid}-tokens',0,-1)
        expired = [str(is_token_expired(t)).lower() for t in tokens]
        update_token_script(keys=[f'{uid}-tokens'], args=expired+[token])

def token_delete(uid,token):
    lock = redis_client.lock(f'{uid}-lock')
    with lock:
        redis_client.lrem(f'{uid}-tokens',1,token)