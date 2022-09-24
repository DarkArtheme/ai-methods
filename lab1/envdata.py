import os
from dotenv import load_dotenv


def load_env_data():
    load_dotenv(dotenv_path=".env")
    data = dict()
    data['YANDEX_API_KEY'] = os.getenv('YANDEX_API_KEY')
    data['YANDEX_FOLDER_ID'] = os.getenv('YANDEX_FOLDER_ID')
    return data
