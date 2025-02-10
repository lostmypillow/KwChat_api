from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Depends
import sqlite3
from sqlalchemy import text
from typing import List, Dict, Any
import asyncio
from database.async_operations import async_engine, exec_sql


async def lifespan(app: FastAPI):
    """Disposes SQLAlchemy engine
    """
    yield
    if async_engine:
        await async_engine.dispose()
app = FastAPI(lifespan=lifespan)

# In-memory storage for connected WebSockets
active_connections: Dict[str, WebSocket] = {}


# Custom SQL execution function

@app.post("/chatrooms/")
async def create_chatroom(user1_id: int, user2_id: int):
    await exec_sql(
        'commit',
        'create_chat',
        user1_id=user1_id,
        user2_id=user2_id
    )
    return {"message": "Chat created"}


@app.get("/chatrooms/{user_id}")
async def get_chatrooms(user_id: int):
    return await exec_sql('all', 'get_chats', user_id=user_id)


@app.get("/messages/{chat_id}")
async def get_messages(chat_id: int):
    return await exec_sql('all', 'get_msgs', chat_id=chat_id)


@app.websocket("/ws/{username}")
async def websocket_endpoint(websocket: WebSocket, username: str):
    await websocket.accept()
    active_connections[username] = websocket

    try:
        while True:
            data = await websocket.receive_json()
            sender = data["sender"]
            receiver = data["receiver"]
            message = data["message"]

            # Save message to the database
            exec_sql(
                "commit",
                "INSERT INTO messages (sender, receiver, message) VALUES (:sender, :receiver, :message)",
                {"sender": sender, "receiver": receiver, "message": message},
            )

            # If the receiver is online, send the message
            if receiver in active_connections:
                await active_connections[receiver].send_json({"sender": sender, "message": message})

    except WebSocketDisconnect:
        del active_connections[username]
