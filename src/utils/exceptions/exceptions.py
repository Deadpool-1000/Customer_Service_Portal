class DataBaseException(Exception):
    """Custom exception class for database exception in the application."""
    pass


class ApplicationError(Exception):
    """Custom exception class for application related exceptions."""
    def __init__(self, message, code):
        self.message = message
        self.code = code
    
