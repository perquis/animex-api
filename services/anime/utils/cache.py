import json

from services.redis import redis_client


def use_redis_cache(redis_id: str, callback) -> bool:
    if redis_client.exists(redis_id):
        return json.loads(redis_client.get(redis_id))
    
    data = callback()
    redis_client.set(redis_id, json.dumps(data), ex=3600)
    return data