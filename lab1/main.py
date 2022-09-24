import sys

from PyQt6.QtWidgets import *


def main():
    app = QApplication(sys.argv)
    widget = QWidget()

    textLabel = QLabel(widget)
    textLabel.setText("Hello, world!")
    textLabel.move(110, 85)

    widget.setGeometry(50, 50, 320, 200)
    widget.setWindowTitle("PyQt6 Example")
    widget.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
