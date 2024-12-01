class InvalidFileTypeError(Exception):
    """
    Exception raised in case of non-authorized extension
    """

    def __init__(self, message="Invalid file type."):
        self.message = message
        super().__init__(self.message)
