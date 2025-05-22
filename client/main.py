from services.client import handle_connection
import asyncio

if __name__ == "__main__":
    asyncio.run(handle_connection())
