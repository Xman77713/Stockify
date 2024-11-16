class InvalidFileTypeError(Exception):
    """Exception levée pour les types de fichiers non autorisés."""

    def __init__(self, message="Invalid file type."):
        self.message = message
        super().__init__(self.message)
