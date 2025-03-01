from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.requests import Request
from typing import List

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (Change for production)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



# Load HTML templates
templates = Jinja2Templates(directory="templates")

# WebSocket connections list
connected_clients: List[WebSocket] = []

# Serve the index.html page
# Root route (Fixes Not Found error)
@app.get("/")
async def home():
    return {"message": "Fusion Chat Backend is Running!"}


# WebSocket endpoint for real-time chat
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    connected_clients.append(websocket)
    try:
        while True:
            message = await websocket.receive_text()
            # Broadcast message to all clients
            for client in connected_clients:
                await client.send_text(message)
    except:
        connected_clients.remove(websocket)
import uvicorn
import os

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))  # Get the correct port from Railway
    print(f"Starting server on port {port}...")  # Debugging message
    uvicorn.run("main:app", host="0.0.0.0", port=port)

