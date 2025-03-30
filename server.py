"""WebSocket сервер для совместного рисования."""
import asyncio
import json
from typing import List

from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI(title="Совместное рисование")

# Подключаем статические файлы
app.mount("/static", StaticFiles(directory="static"), name="static")

# Хранилище активных подключений
active_connections: List[WebSocket] = []


@app.get("/favicon.ico")
async def favicon():
    """Обработчик запроса favicon.ico."""
    return {"status": "ok"}


@app.get("/", response_class=HTMLResponse)
async def get():
    """Возвращает главную страницу приложения."""
    with open("static/index.html", encoding="utf-8") as f:
        return f.read()


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """Обработчик WebSocket соединений.
    
    Args:
        websocket: WebSocket соединение
    """
    await websocket.accept()
    active_connections.append(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            # Отправляем данные всем подключенным клиентам
            for connection in active_connections:
                await connection.send_text(data)
    except Exception as e:
        print(f"Error: {e}")
    finally:
        active_connections.remove(websocket)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
