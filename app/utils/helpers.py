import google.generativeai as genai
import os
import asyncio
from functools import partial

# Initialize Gemini with an api key
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

async def call_gemini(prompt:str):
    # Call Gemini with the prompt
    try:
        loop = asyncio.get_event_loop()
        model= genai.GenerativeModel("gemini-pro")
        '''same as model.generate_content(prompt)'''
        func= partial(model.generate_content, prompt)
        '''to run synchronous as asynchronous for non blocking thread''' 
        response= await loop.run_in_executor(None, func)

        return response.text.strip() if response.text else "No summary generated"
    
    except Exception as e:
        print(f"An error occurred: {e}")
        return  "Failed to generate summary"
