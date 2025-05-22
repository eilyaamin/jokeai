import asyncio
import websockets
import json
from config.settings import setup_logging
from utils.translator import translate

# Process a single message: translate the joke and send the result back
async def process_message(data, websocket, logger):
    try:
        joke_id, joke_text = data["id"], data["joke"]
        result = await translate(joke_id, joke_text, logger)
        logger.info(f"Client: {result}")
        await websocket.send(json.dumps(result))
    except KeyError as e:
        logger.error(f"Missing expected data field: {e}")
    except Exception as e:
        logger.error(f"Error during processing: {e}")

# Main coroutine to handle the websocket connection and message processing
async def handle_connection():
    logger = setup_logging()
    uri = "ws://server:8000/ws"
    tasks = set()  # Track all running tasks for processing messages

    # Retry connection up to 3 times if it fails
    for attempt in range(3):
        try:
            async with websockets.connect(uri) as websocket:
                logger.info("✅ Connected to server.")

                # Receive and process up to 5 messages from the server
                for _ in range(5):
                    try:
                        message = await websocket.recv()
                        data = json.loads(message)
                        logger.info(f"Received data: {data}")

                        # Start processing the message in a background task
                        task = asyncio.create_task(process_message(data, websocket, logger))
                        tasks.add(task)
                        # Remove completed tasks from the set
                        tasks = {t for t in tasks if not t.done()}

                    except websockets.exceptions.ConnectionClosed:
                        logger.info("🔒 Server closed the connection.")
                        break
                    except Exception as e:
                        logger.error(f"Error during receiving: {e}")
                        break

                # Wait for all processing tasks to finish before exiting
                if tasks:
                    await asyncio.gather(*tasks)

                break  # Exit retry loop after successful connection
        except Exception as e:
            logger.error(f"❌ Connection failed (attempt {attempt+1}): {e}")
            await asyncio.sleep(2)
