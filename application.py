import sys
from PyQt5.QtWidgets import QApplication

from ui.window import ImageCipherApp


def application():
    app = QApplication(sys.argv)
    m = ImageCipherApp()
    m.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    application()
