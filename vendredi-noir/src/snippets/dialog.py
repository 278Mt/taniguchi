import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QInputDialog

"""
部屋番号確認ダイアログ(WIP)
@author: wakame-tech
"""

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)

        self.openDialog()

    def openDialog(self):
        text, ok = QInputDialog.getInt(self, 'Dialog', '部屋番号?')

        if ok:
            print(str(text))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myapp = MainWindow()
    myapp.show()
    sys.exit(app.exec_())