class SchemaError(Exception):
    def __init__(self, message, status):
        super().__init__(message, status)
        self.message = 'Invalid Schema given:' + message
        self.status = status


class ValidError(Exception):
    """Base class for exceptions in this module."""

    def __init__(self, message, status):
        super().__init__(message, status)
        self.message = message
        self.status = status


class MissingError(ValidError):
    pass


class RedundantError(ValidError):
    pass


class RegexError(ValidError):
    def __init__(self, message, status, regex):
        super().__init__(message, status)
        self.regex = regex


class TypeError(ValidError):
    def __init__(self, message, status, type):
        super().__init__(message, status)
        self.type = type


class RangeError(ValidError):
    def __init__(self, message, status, minimum=0, maximum=float('inf')):
        super().__init__(message, status)
        self.minimum = minimum
        self.maximum = maximum


"""=========== extend here like=================
    add new error like:

    class YOURError(ValidError):
    def __init__(self, message, status, YOUR_SPECIFIC_FEATURE):
        super().__init__(message, status)
        self.type = YOUR_SPECIFIC_FEATURE

"""