
class ErrorResponse(Exception):
    
    def __init__(self, reason: str, status_code: int = 500) -> None:
        self.reason = reason
        self.status_code = status_code
        super().__init__()