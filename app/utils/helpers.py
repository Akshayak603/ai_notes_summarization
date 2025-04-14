import google.generativeai as genai
import os
import asyncio
import time
from functools import partial
from fastapi import HTTPException
from models import User

# Initialize Gemini with an api key
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

async def call_gemini(prompt:str):
    # Call Gemini with the prompt
    try:
        loop = asyncio.get_event_loop()
        model= genai.GenerativeModel("gemini-2.0-flash")
        '''same as model.generate_content(prompt)'''
        func= partial(model.generate_content, prompt)
        '''to run synchronous as asynchronous for non blocking thread''' 
        response= await loop.run_in_executor(None, func)

        return response.text.strip() if response.text else "No summary generated"
    
    except Exception as e:
        print(f"An error occurred: {e}")
        return  "Failed to generate summary"
    
'''Model Object to dictionary'''
def user_obj_to_dict(user:User):
    return {
        "username": user.username,
        "email": user.email,
        "id": user.id
    }

"""Rate limiting our gemini requests"""
async def rate_limited_gemini_call(redis_client, user_id:int, max_requests: int=1, window_seconds:int=60):
    key= f"rate_limit:{user_id}"
    current_time= int(time.time())

    async with redis_client.pipeline(transaction=True) as pipe:
        # remove old timestamps which exceeds 60 seconds
        pipe.zremrangebyscore(key, 0, current_time - window_seconds)
        # count request in the window
        pipe.zcard(key)
        # add current request
        pipe.zadd(key,  {str(current_time): current_time})
        # clean window if user stops sending request
        pipe.expire(key, window_seconds)
        # get the count of requests in the window
        result = await pipe.execute()

        current_count= result[1]

        if current_count>= max_requests:
            raise HTTPException(
            status_code=429,
            detail="Too many requests. Please try again later."
        )


