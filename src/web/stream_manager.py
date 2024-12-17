import queue
import threading
from dataclasses import dataclass
from typing import Set, Dict, Any

@dataclass
class StreamClient:
    """Represents a client connection"""
    queue: queue.Queue
    active: bool = True

class StreamManager:
    """Manages client connections and message broadcasting"""
    def __init__(self):
        self._clients: Set[StreamClient] = set()
        self._lock = threading.Lock()

    def add_client(self) -> StreamClient:
        """Create and register new client"""
        client = StreamClient(queue.Queue(maxsize=10))
        with self._lock:
            self._clients.add(client)
        return client

    def remove_client(self, client: StreamClient):
        """Remove client from active set"""
        with self._lock:
            self._clients.discard(client)
            client.active = False

    def broadcast(self, data: Dict[str, Any]):
        """Broadcast data to all active clients"""
        with self._lock:
            for client in list(self._clients):
                try:
                    client.queue.put_nowait(data)
                except queue.Full:
                    self.remove_client(client)