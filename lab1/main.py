import ast
import logging
import requests
import sys

from envdata import *
from mainwindow import Ui_MainWindow
from PyQt6.QtWidgets import *

env_data = load_env_data()

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter("[%(asctime)s: %(levelname)s] %(message)s"))
logger.addHandler(handler)


def yandex_translate_text(texts, target_language):
    body = {
        "targetLanguageCode": target_language,
        "texts": texts,
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Api-Key {env_data['YANDEX_API_KEY']}"
    }

    response = requests.post('https://translate.api.cloud.yandex.net/translate/v2/translate',
                             json=body,
                             headers=headers
                             )
    response_dict = ast.literal_eval(response.text)
    result = []
    if "translations" in response_dict:
        logger.debug(f"response_dict={response_dict}")
        result = [translation.get('text', "") for translation in response_dict['translations']]
    else:
        logger.error(f"возникла ошибка API, был возвращен ответ: {response_dict}")
    return result


class MyMainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

    def translateText(self):
        text = self.ui.plainTextEdit.toPlainText()
        texts = text.split('\n')
        logger.debug(f"texts={texts}")
        index = self.ui.comboBox.currentIndex()
        langs = ["en", "es", "de", "ru", "fr"]
        if index < 0 or index > len(langs):
            logger.error("индекс combobox за пределами")
            return
        result = yandex_translate_text(texts=texts, target_language=langs[index])
        logger.debug(f"result={result}")
        self.ui.textBrowser.setText(str.join('\n', result))


def main():
    app = QApplication(sys.argv)
    mainWindow = MyMainWindow()
    mainWindow.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
