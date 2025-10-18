class CryptographyServiceError(Exception):
    def __init__(self, message: str = "Service is not available", headers=None):
        self.message = message
        self.headers = headers
        super().__init__(self.message)


class ResourceNotFound(CryptographyServiceError):
    ...
