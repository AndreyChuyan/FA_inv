from fastapi import HTTPException, status
from fastapi.responses import RedirectResponse


class RedirectException(HTTPException):
    def __init__(self, url: str):
        super().__init__(
            status_code=status.HTTP_307_TEMPORARY_REDIRECT, detail="Temporary redirect"
        )
        self.headers = {"Location": url}


# дубликат
class DuplicateObjectException(HTTPException):
    def __init__(self, detail: str = "Object already exists"):
        super().__init__(status_code=409, detail=detail)

# неверный формат данных
class InvalidDataException(HTTPException):
    def __init__(self, detail: str = "Invalid data provided"):
        super().__init__(status_code=400, detail=detail)

# едостаточные права доступа
class UnauthorizedException(HTTPException):
    def __init__(self, detail: str = "Unauthorized"):
        super().__init__(status_code=401, detail=detail)