import sys
from func.loadPage import *
from func.historyPage import *

def main():
    app = QApplication()
    w = loadPage()
    w.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()