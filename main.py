# created by xiao 
import sys
from PySide2.QtWidgets import QApplication
# from func.newDataPage import NewDataPage
from func.loadPage import loadPage
from inf.uploadThread import UploadThread

def main():
    thread = UploadThread()
    thread.run()
    # app = QApplication()
    # w = loadPage()
    # w.show()
    # sys.exit(app.exec_())


if __name__ == "__main__":
    main()