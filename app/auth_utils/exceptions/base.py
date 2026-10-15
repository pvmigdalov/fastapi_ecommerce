class BaseAuthException(Exception):
    @property
    def message(self):
        return "An unknown error has occurred"


class BaseUserException(BaseAuthException):
    @property
    def message(self):
        return "An unknown user authenticate error has occurred"


class BaseJWTException(BaseAuthException):
    token_types = (
        "access",
        "refresh",
    )

    @property
    def message(self):
        return "An uknown JWT decoding error has occurred"
