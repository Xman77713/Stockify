class WrongPasswordError(Exception):
    """Exception raised for Wrong password"""

    def __init__(self, message="Wrong password."):
        self.message = message
        super().__init__(self.message)
