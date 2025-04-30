from .base import CustomAPIException


class DuplicateTransactionException(CustomAPIException):
    def __init__(self, transaction_id):
        message = f"Transaction with ID {transaction_id} already exists."
        details = {"transaction_id": transaction_id}
        super().__init__(message=message, code=409, details=details)
