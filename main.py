from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import g4f

app = FastAPI()

# Разрешенные источники (Origin)
origins = [
    "https://uraa-gpt.vercel.app/",  # Ваш фронтенд-домен
    "http://localhost:3000"  # Если вы тестируете локально
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Разрешаемые домены
    allow_credentials=True,
    allow_methods=["*"],  # Разрешаемые методы (GET, POST и т.д.)
    allow_headers=["*"],  # Разрешаемые заголовки
)

class Message(BaseModel):
    message: str

@app.post("/chat")
async def chat_with_gpt(message: Message):
    response = g4f.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": message.message}],
        stream=True,
    )
    message = ''
    for m in response:
        message += m

    return {"response": message}