import ast
import logging
import requests
import sys

from mainwindow import Ui_MainWindow
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter("[%(asctime)s: %(levelname)s]: {%(funcName)s: %(lineno)d} %(message)s"))
logger.addHandler(handler)


def continue_phrase(text):
    body = {
        "text": text,
    }

    headers = {
        'Connection': 'keep-alive',
        'Accept': 'application/json',
        'Server': 'istio-envoy',
        'Accept-encoding': 'gzip, deflate, br',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/96.0.4664.110 Safari/537.36 OPR/82.0.4227.43',
        'Content-Type': 'application/json',
        'Origin': 'https://russiannlp.github.io',
        'Referer': 'https://russiannlp.github.io/',
        'Sec-Fetch-Site': 'same-site',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Accept-Language': 'en-US,en;q=0.9,es-AR;q=0.8,es;q=0.7',
    }

    response = requests.post("https://api.aicloud.sbercloud.ru/public/v1/public_inference/gpt3/predict",
                             json=body,
                             headers=headers
                             )
    response_dict = ast.literal_eval(response.text)
    result = []
    if "predictions" in response_dict:
        logger.debug(f"response_dict={response_dict}")
        result = response_dict["predictions"]
    else:
        logger.error(f"возникла ошибка API, был возвращен ответ: {response_dict}")
    return result


class MyMainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.progressBar.hide()

    def translateText(self):
        text = self.ui.plainTextEdit.toPlainText()
        self.thread = QThread()
        self.worker = Worker(text)
        self.worker.moveToThread(self.thread)

        self.thread.started.connect(self._onRun)
        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.thread.quit)

        self.worker.resulted.connect(self.ui.textBrowser.setText)
        self.thread.finished.connect(self._onFinished)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)

        self.thread.start()

    def _onRun(self):
        logger.debug("Начат процесс генерации")
        self.ui.textBrowser.setText("")
        self.ui.progressBar.show()
        self.ui.pushButton.setEnabled(False)
        self.ui.plainTextEdit.setTextInteractionFlags(Qt.TextInteractionFlags.NoTextInteraction)

    def _onFinished(self):
        logger.debug("Закончен процесс генерации")
        self.ui.progressBar.hide()
        self.ui.pushButton.setEnabled(True)
        self.ui.plainTextEdit.setTextInteractionFlags(Qt.TextInteractionFlags.TextEditorInteraction)


class Worker(QObject):
    def __init__(self, text):
        super().__init__()
        self.text = text

    resulted = pyqtSignal(str)
    finished = pyqtSignal()

    def run(self):
        logger.debug(f"text={self.text}")
        result = continue_phrase(self.text)
        logger.debug(f"Type of result = {type(result)}")
        self.resulted.emit(result)
        self.finished.emit()


def main():
    app = QApplication(sys.argv)
    mainWindow = MyMainWindow()
    mainWindow.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
