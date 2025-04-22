import sys

from PyQt5.QtWidgets import QApplication, QLabel

from project.views.dashboard import MainWindow
from project.models import session

if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow(session)
    window.showMaximized()
    sys.exit(app.exec_())
