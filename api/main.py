import uvicorn
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import google.generativeai as genai
import json
import time
from openai import OpenAI

app = FastAPI()
app.add_middleware(CORSMiddleware,
                   allow_credentials=True,
                   allow_origins=["*"],
                   allow_methods=["*"],
                   allow_headers=["*"]
                   )


@app.post("/gemini/chat", tags=["API"], summary="GEMINI")
def gemini_chat(data: dict):
    prompt = data.get('prompt')
    api_key= data.get('api_key')
    history=data.get('history')
    model_version=data.get('model_version')
    if history is None:
        history=[]  
    try:
        # genai.configure(api_key=api_key,transport='rest')
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel(model_version)
        chat = model.start_chat(history=history)
        response = chat.send_message(prompt)
        text=response.text
        response = {"content": text}
        # for message in chat.history:
        #     print(f'**{message.role}**')
        return response
    except Exception as e:
        print("gemini_chat:",e)
        return None

@app.post("/openai/chat", tags=["API"], summary="OPENAI")
def openai_chat(data: dict):
    prompt = data.get('prompt')
    api_key= data.get('api_key')
    history=data.get('history')
    model_version=data.get('model_version')
    if history is None:
        history=[]  
    try:
        client =OpenAI(api_key =api_key)

        completion = client.chat.completions.create(
        model=model_version,
        messages=[
            {"role": "user", "content": prompt}
        ]
        )
        response=completion.choices[0].message
        #response = {"content": text}
        return response
    except Exception as e:
        print("openai_chat:",e)
        return None
    
if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1",workers=1)