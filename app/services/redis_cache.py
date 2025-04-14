import redis.asyncio as redis
import os
from dotenv import load_dotenv
import json

load_dotenv()

redis_host= os.getenv("REDIS_DEV_HOST")
redis_port = int(os.getenv("REDIS_DEV_PORT"))
redis_password= os.getenv("REDIS_DEV_PASSWORD")

redis_client= redis.Redis(host=redis_host, port=redis_port,password=redis_password, ssl=True, decode_responses=True)

'''Get user from cache'''
async def get_user_from_cache(token:str):
    try:
        user = await redis_client.get(f"user:{token}")
        return json.loads(user)
    except Exception as e:
        print("Something went wrong with Redis get.", e)

'''Set user in cache'''
async def set_user_in_cache(token:str, user_data:dict):
    try:
        await redis_client.setex(f"user:{token}", 3600, json.dumps(user_data))
    except Exception as e:
        print("Something went wrong with Redis set.", e)
