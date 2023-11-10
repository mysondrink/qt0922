# created by xiao 
import sys
from func.loadPage import *
from func.aboutPage import *

def main():
    app = QApplication()
    w = aboutPage()
    w.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()