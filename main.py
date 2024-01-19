# created by xiao 
import sys
from PySide2.QtWidgets import QApplication
from func.newDataPage import NewDataPage
# from func.loadPage import loadPage


def main():
    app = QApplication()
    w = NewDataPage()
    w.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()