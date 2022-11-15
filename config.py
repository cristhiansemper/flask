from dotenv import load_dotenv
load_dotenv()

from os import environ

class Config():
    DB_HOST = environ.get("DB_HOST")
    DB_PORT = int(environ.get("DB_PORT"))
    DB_USER = environ.get("DB_USER")
    DB_PASSWORD = environ.get("DB_PASSWORD")
    DB_NAME = environ.get("DB_NAME")


class SecretKey():
    JWT_SECRET_KEY = environ.get("JWT_SECRET_KEY")


class Host():
    URL_APP = 'http://127.0.0.1:3007'
