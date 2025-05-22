# import pytest
# import asyncio
# import json
# from unittest.mock import AsyncMock, MagicMock, patch
# from client.services.client import process_message



# @pytest.mark.asyncio
# async def test_process_message_success():
#     data = {"id": 1, "joke": "Why did the chicken cross the road?"}
#     websocket = AsyncMock()
#     logger = MagicMock()
#     result = {"id": 1, "translated": "Warum hat das Huhn die Straße überquert?"}

#     with patch("client.services.client.translate", return_value=result):
#         await process_message(data, websocket, logger)

#     logger.info.assert_called_with(f"Client: {result}")
#     websocket.send.assert_awaited_once_with(json.dumps(result))

# @pytest.mark.asyncio
# async def test_process_message_missing_field():
#     data = {"joke": "No id here"}
#     websocket = AsyncMock()
#     logger = MagicMock()

#     await process_message(data, websocket, logger)

#     logger.error.assert_any_call("Missing expected data field: 'id'")

# @pytest.mark.asyncio
# async def test_process_message_translate_exception():
#     data = {"id": 2, "joke": "Knock knock"}
#     websocket = AsyncMock()
#     logger = MagicMock()

#     with patch("client.services.client.translate", side_effect=Exception("fail")):
#         await process_message(data, websocket, logger)

#     logger.error.assert_any_call("Error during processing: fail")