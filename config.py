class Config():
    DB_HOST = os.getenv("DB_HOST")
    DB_PORT = os.getenv("DB_PORT")
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_NAME = os.getenv("DB_NAME")


class SecretKey():
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")


class Host():
    URL_APP = 'http://127.0.0.1:3007'
