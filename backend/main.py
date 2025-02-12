from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Depends, HTTPException
import sqlite3
from sqlalchemy import text
from typing import List, Dict, Any
import asyncio
from database.async_operations import async_engine, exec_sql


async def lifespan(app: FastAPI):
    """Disposes SQLAlchemy engine
    """
    await exec_sql('commit', 'schema/users')
    await exec_sql('commit', 'schema/rooms')
    await exec_sql('commit', 'schema/room_users')
    await exec_sql('commit', 'schema/messages')
    await exec_sql('commit', 'schema/message_recipient')
    await exec_sql('commit', 'placeholder_users')
    yield
    if async_engine:
        await async_engine.dispose()


app = FastAPI(lifespan=lifespan)

# In-memory storage for connected WebSockets
active_connections: Dict[str, WebSocket] = {}


@app.post('/user/{name}')
async def create_user(name: str):
    existing_user = await exec_sql('one', 'user/get_by_name', name=name)
    if existing_user is None:
        await exec_sql('commit', 'user/create', name=name, image='/'+name)
        return await exec_sql('one', 'user/get_by_name', name=name)
    else:
        return existing_user


@app.get('/users/{name}')
async def get_all_users(name: str):
    existing_user = await exec_sql('one', 'user/get_by_name', name=name)
    if existing_user is None:
        raise HTTPException(404, 'User not registered!')
    else:
        return await exec_sql('all', 'user/get_not_you', name=name)


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
