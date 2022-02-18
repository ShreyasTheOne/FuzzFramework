class HTTPMethodNotAccepted(Exception):
    """
    Raised when HTTP Method is not valid
    """

    def __init__(self, invalid_method):
        self.invalid_method = invalid_method
    
    def __str__(self):
        return f"Unrecognised or unaccepted HTTP Method {self.invalid_method}"

class HTTPMethod:
    """
    Defines the accepted types of HTTP Methods
    """
    
    OPTIONS = 'OPTIONS'
    GET = 'GET'
    POST = 'POST'
    PATCH = 'PATCH'
    PUT = 'PUT'
    DELETE = 'DELETE'

    METHODS = [
        OPTIONS,
        GET,
        POST,
        PATCH,
        PUT,
        DELETE
    ]

    @classmethod
    def validate(cls, method, silent=True):
        """
        Checks if method is a valid HTTP method

        :param method: Method who's validity is checked
        :return: Boolean value representing whether HTTP Method is valid
        """
        method = method.upper()
        if method in [m.upper() for m in cls.METHODS]:
            return method
        if silent:
            return False
        raise HTTPMethodNotAccepted(method)
