from datetime import datetime, timedelta

from passlib.context import CryptContext
from jose import JWTError, jwt

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


# These should be set to your desired values
SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# верификацию токена доступа в формате JSON Web Token (JWT).
# используется механизм генерации исключений для обработки ошибок верификации токена.
def verify_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_name: int = payload.get("sub")
        if user_name is None:
            raise credentials_exception
        return user_name
    except JWTError:
        raise credentials_exception


# функцию которая выполняет верификацию токена доступа
# В случае успешной верификации токена и декодирования его содержимого, функция возвращает идентификатор пользователя
def verify_token_not_exception(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_name: int = payload.get("sub")
        if user_name is None:
            return
        return user_name
    except JWTError:
        return
