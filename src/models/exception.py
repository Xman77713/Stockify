class InvalidFileTypeError(Exception):
    """Exception raised for non-authorized file type"""

    def __init__(self, message="Invalid file type."):
        self.message = message
        super().__init__(self.message)


class WrongPasswordError(Exception):
    """Exception raised for Wrong password"""

    def __init__(self, message="Wrong password."):
        self.message = message
        super().__init__(self.message)
