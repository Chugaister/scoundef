from os import getenv
from dotenv import load_dotenv


class EnvVariableNotFound(Exception):
    pass


class Config:

    def __init__(self):
        load_dotenv()
        self.HOST = self.get_var("HOST")
        self.PORT = int(self.get_var("PORT"))
        self.PUBLIC_URL = self.get_var("PUBLIC_URL")
        self.ACCOUNT_SID = self.get_var("ACCOUNT_SID")
        self.PHONE_NUMBER_SID = self.get_var("PHONE_NUMBER_SID")
        self.AUTH_TOKEN = self.get_var("AUTH_TOKEN")
        self.SSL_CERTFILE_PATH = self.get_var("SSL_CERTFILE_PATH", optional=True)
        self.SSL_KEYFILE_PATH = self.get_var("SSL_KEYFILE_PATH", optional=True)
        self.SSL_CA_BUNDLE_FILE_PATH = self.get_var("SSL_CA_BUNDLE_FILE_PATH", optional=True)
        self.NGROK_AUTH_TOKEN = self.get_var("NGROK_AUTH_TOKEN", optional=True)

    @staticmethod
    def get_var(item: str, optional: bool = False):
        var = getenv(item)
        if not var and not optional:
            raise EnvVariableNotFound(f"Environment variable {item} not found")
        return var


config = Config()
