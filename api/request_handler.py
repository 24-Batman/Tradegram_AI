from typing import Dict, Any

class RequestHandler:
    def __init__(self):
        self.handlers = {}
        
    def process_request(self, request_type: str, data: Dict[str, Any]):
        handler = self.handlers.get(request_type)
        if handler:
            return handler(data)
        raise ValueError(f"Unknown request type: {request_type}") 