class CustomAPIException(Exception):
    def __init__(self, message, code=400, details=None):
        self.message = message
        self.code = code
        self.details = details or {}
        super().__init__(message)

    def to_dict(self):
        return {
            "error": self.message,
            "code": self.code,
            "details": self.details,
        }
