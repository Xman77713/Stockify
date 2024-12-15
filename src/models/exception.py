class WrongPasswordError(Exception):
    """Exception raised for wrong password"""

    def __init__(self, message="Wrong password."):
        self.message = message
        super().__init__(self.message)

class SecurityError(Exception):
    """Exception raised because of security checks"""

    def __init__(self, message="Data compromised."):
        self.message = message
        super().__init__(self.message)

class IncorrectMailError(Exception):
    """Exception raised for incorrect mail"""

    def __init__(self, message="Mail is incorrect."):
        self.message = message
        super().__init__(self.message)

class IncorrectTimeError(Exception):
    """Exception raised for incorrect time"""

    def __init__(self, message="Time must be positive and wittren like: 1, 1.2, 1.0."):
        self.message = message
        super().__init__(self.message)

class mailNotReached(Exception):
    """Exception raised for incorrect time"""

    def __init__(self, message="The mail does not reach the receiver. Please try later."):
        self.message = message
        super().__init__(self.message)