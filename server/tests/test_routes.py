import pytest
import asyncio
from unittest.mock import AsyncMock, MagicMock, patch
from fastapi import WebSocketDisconnect
from server.routes.websocket import websocket_joke


@pytest.mark.asyncio
async def test_websocket_joke():
    mock_websocket = AsyncMock()
    mock_websocket.client = "client"
    mock_websocket.receive_json = AsyncMock(side_effect=WebSocketDisconnect())
    mock_websocket.send_json = AsyncMock()
    mock_ws_manager = MagicMock()
    mock_logger = MagicMock()
    mock_generate_joke = AsyncMock(return_value="joke")

    with patch("server.routes.websocket.ws_manager", mock_ws_manager), \
         patch("server.routes.websocket.logger", mock_logger), \
         patch("server.routes.websocket.generate_joke", mock_generate_joke):

        await websocket_joke(mock_websocket)

    mock_websocket.accept.assert_awaited_once()
    mock_ws_manager.add_client.assert_called_once_with(mock_websocket)
    mock_ws_manager.remove_client.assert_called_once_with(mock_websocket)
    mock_logger.info.assert_any_call("WebSocket /ws connected: client")
    mock_logger.info.assert_any_call("WebSocket /ws disconnected: client")