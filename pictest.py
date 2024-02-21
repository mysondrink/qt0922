from inf.picThread import MyPicThread
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
import os
import datetime
import cProfile

class Test():
    def __init__(self) -> None:
        pass
    
    def startTest(self):
        self.mypicthread = MyPicThread()
        self.mypicthread.finished.connect(self.takePicture)
        self.mypicthread.start()

    def takePicture(self, msg):
        cur_time = QDateTime.currentDateTime().toString('yyyy-MM-dd hh:mm:ss')
        time_now = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
        pic_path = QDateTime.currentDateTime().toString('yyyy-MM-dd')
        self.ui.photoLabel.setText(cur_time)
        time_now = msg
        gray_aver = self.mypicthread.getGrayAver()
        print(gray_aver)
        print(msg)
        print(cur_time)

def main():
    mytest = Test()
    mytest.startTest()

if __name__ == "__main__":
    cProfile.run('main()')
