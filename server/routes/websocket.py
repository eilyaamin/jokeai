import asyncio
import time
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from core.websocket_manager import WebSocketManager
from utils.generate_joke import generate_joke
from config.logging_config import setup_logging

router = APIRouter()
ws_manager = WebSocketManager()
logger = setup_logging()

@router.websocket("/ws")
async def websocket_joke(websocket: WebSocket):
    """
    WebSocket endpoint for sending jokes and receiving translations.
    Each connected client receives jokes in a loop, and sends back translations.
    """
    await websocket.accept()
    ws_manager.add_client(websocket)
    logger.info(f"WebSocket /ws connected: {websocket.client}")

    try:
        idx = 0
        while True:
            idx = idx + 1
            # Fetch a new joke
            joke = await generate_joke(logger)
            # Record that a joke was sent
            ws_manager.record_joke_sent(joke)
            res = {"id": idx, "joke": joke}
            # Small delay between jokes
            start_time = time.time()
            # Send joke to client
            await asyncio.sleep(0.2)
            await websocket.send_json(res)

            # Wait for translation from client
            data = await websocket.receive_json()
            res_time = time.time()
            # Calculate response time
            duration = round(res_time - start_time, 4)

            # Record translation and duration
            ws_manager.record_translation(data.get('translated_joke', ''), duration)
            logger.info(f"Received translation: {data.get('translated_joke', '')}")

    except WebSocketDisconnect:
        logger.info(f"WebSocket /ws disconnected: {websocket.client}")
    finally:
        # Clean up client on disconnect
        ws_manager.remove_client(websocket)

@router.websocket("/status")
async def status_ws(websocket: WebSocket):
    """
    WebSocket endpoint for sending server status and statistics to clients.
    Sends stats every second.
    """
    await websocket.accept()
    ws_manager.add_client(websocket)
    logger.info(f"WebSocket /status connected: {websocket.client}")
    try:
        while True:
            # Get current server stats
            data = ws_manager.get_stats()
            # Send stats to client
            await websocket.send_json(data)
            # Send stats every second
            await asyncio.sleep(1)
    except WebSocketDisconnect:
        logger.info(f"WebSocket /status disconnected: {websocket.client}")
    finally:
        # Clean up client on disconnect
        ws_manager.remove_client(websocket)