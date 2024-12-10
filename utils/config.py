from os import getenv
from pathlib import Path

from dotenv import load_dotenv


class EnvVariableNotFound(Exception):
    pass


class Config:

    lang_settings_list = {
        "en": {
            "stt_lang": "en-GB",
            "tts_lang": "en-GB",
            "voice": "Polly.Emma-Neural"
        },
        "ar": {
            "stt_lang": "ar-LB",
            "tts_lang": "ar-XA",
            "voice": "Google.ar-XA-Wavenet-A"
        }
    }
    supported_languages = ["en", "ar"]
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
        self.ANTHROPIC_API_KEY = self.get_var("ANTHROPIC_API_KEY")
        self.DATA_FILE_PATH = Path(self.get_var("DATA_FILE_PATH"))
        self.LANGUAGE = self.get_var("LANGUAGE")
        if self.LANGUAGE not in self.supported_languages:
            raise ValueError("Unsupported language specified. See README.md")
        self.lang_settings = self.lang_settings_list[self.LANGUAGE]

    @staticmethod
    def get_var(item: str, optional: bool = False):
        var = getenv(item)
        if not var and not optional:
            raise EnvVariableNotFound(f"Environment variable {item} not found")
        return var


config = Config()
