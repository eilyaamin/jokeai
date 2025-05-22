import logging
from fastapi import WebSocket

class WebSocketManager:
    def __init__(self):
        self.clients = set()
        self.jokes_sent = []
        self.translations_received = []
        self.translation_times = []
        self.logger = logging.getLogger(__name__)

    def add_client(self, websocket: WebSocket):
        self.clients.add(websocket)
        self.logger.info(f"Client added: {websocket.client}")

    def remove_client(self, websocket: WebSocket):
        self.clients.discard(websocket)
        self.logger.info(f"Client removed: {websocket.client}")

    def record_joke_sent(self, joke):
        self.jokes_sent.append(joke)

    def record_translation(self, translation, time_taken):
        self.translations_received.append(translation)
        self.translation_times.append(time_taken)

    def get_stats(self):
        return {
            "jokes_sent": self.jokes_sent,
            "translations_received": self.translations_received,
            "avg_translation_time": self.translation_times
        }