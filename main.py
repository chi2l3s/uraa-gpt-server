from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import g4f

app = FastAPI()

# Разрешаем CORS для всех источников
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Разрешаем доступ с любых источников
    allow_credentials=True,
    allow_methods=["*"],  # Разрешаем любые методы (GET, POST и т.д.)
    allow_headers=["*"],  # Разрешаем любые заголовки
)

class Message(BaseModel):
    message: str

@app.post("/chat")
async def chat_with_gpt(message: Message):
    response = g4f.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": message.message}],  # Используем пользовательское сообщение
        stream=True,
    )
    full_message = ''
    for m in response:
        full_message += m

    return {"reply": full_message}  # Возвращаем ответ в формате JSON

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
