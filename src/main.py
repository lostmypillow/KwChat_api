from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from typing import Dict

app = FastAPI()

# A dictionary to store active connections identified by a unique ID
active_connections: Dict[str, WebSocket] = {}

@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    # Add the new client to the connection pool
    active_connections[client_id] = websocket
    await websocket.accept()

    try:
        while True:
            # Receive a message from the client
            data = await websocket.receive_text()
            # Extract target client ID and the message
            if "|" in data:  # Example message format: "target_id|Hello!"
                target_id, message = data.split("|", 1)

                # Check if the target client exists
                if target_id in active_connections:
                    target_ws = active_connections[target_id]
                    await target_ws.send_text(f"{client_id}: {message}")
                    
            else:
                await websocket.send_text("Invalid message format. Use 'target_id|message'.")
    except WebSocketDisconnect:
        # Remove the disconnected client from the pool
        del active_connections[client_id]
        print(f"Client {client_id} disconnected.")
