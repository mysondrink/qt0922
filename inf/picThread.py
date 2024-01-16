from PySide2.QtCore import QThread, Signal, QDateTime
import frozen as frozen
import time
from inf.img_acquire import Image_Acquire
from inf.img_process import Image_Processing
import datetime
import sys
import traceback

#   定位点圈定区域，可修改
roi_position = [
    [0, 700], [0, 2500]  # [startY, endY] [StartX, endX]
]


class MyPicThread(QThread):
    update_progress = Signal(int)
    update_fail = Signal()
    update_success = Signal()
    finished = Signal(str)
    update_log = Signal(str)

    """
    @detail 初始化线程，同时创建记录异常的信息
    @detail 构造函数
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        sys.excepthook = self.HandleException
        self.gray_aver = []
        self.imgAcq = None
        self.imgPro = None

    """
    @detail 捕获及输出异常类
    @param excType: 异常类型
    @param excValue: 异常对象
    @param tb: 异常的trace back
    """
    def HandleException(self, excType, excValue, tb):
        sys.__excepthook__(excType, excValue, tb)
        err_msg = ''.join(traceback.format_exception(excType, excValue, tb))
        self.update_log.emit(err_msg)

    """
    @detail 发送异常信息
    @detail 在正常抛出异常时使用
    @detail 未使用
    """
    def sendException(self):
        exc_type, exc_value, exc_traceback = sys.exc_info()
        err_msg = ''.join(traceback.format_exception(exc_type, exc_value, exc_traceback))
        self.update_log.emit(err_msg)

    """
    @detail 线程运行函数
    @detail 进行图片的获取和图片pixel的获取
    """
    def run(self):
        pic_path = QDateTime.currentDateTime().toString('yyyy-MM-dd')
        time_now = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
        path_cache = frozen.app_path() + r'/inf/pic_cache/'
        path_save = frozen.app_path() + r'/inf/picture/'
        self.imgAcq = Image_Acquire(
            path_cache=path_cache,
            path_save=path_save
        )

        self.imgPro = Image_Processing(
            roi_position=roi_position
        )
        # for i in range(101):
        #     self.update_progress.emit(i)
        #     time.sleep(0.1)
        # self.update_success.emit()

        self.imgAcq.img_acquire(time_now)

        # pic_name = 'img_final'
        # flag, gray_aver = self.imgPro.process(path_read=frozen.app_path() + r'/inf/picture/' + pic_name + '.jpeg',
        #                                       path_write=frozen.app_path() + r'/inf/img_out/', reagent=(8, 5),
        #                                       radius=40)
        item_type = "检测组合" + self.item_type
        judge_flag, self.gray_aver, self.nature_aver = self.imgPro.process(path_read=frozen.app_path() + r'/inf/picture/' + time_now + '.jpeg',
                                                                     path_write=frozen.app_path() + r'/inf/img_out/', combina=item_type, radius=40)
        w, h = self.nature_aver.shape
        print(w, h)
        self.antibody_test_results = []
        self.antibody_test_points = []
        self.nature_aver_str = ""
        self.gray_aver_str = ""
        for i in range(w):
            for j in range(h):
                self.nature_aver_str += "," + self.nature_aver[i][j] 
                self.gray_aver_str += "," + str(self.gray_aver[i][j])
                # if (i * h + j) % 2 != 0:
                #     self.antibody_test_points.append(self.gray_aver[i + 1][j])
                # else:
                #     self.antibody_test_results.append(self.nature_aver[i][j])
        # print(self.gray_aver)
        # print(self.nature_aver)
        for k in range(h):
            self.gray_aver_str += "," + str(self.gray_aver[w][k])
        # print(self.nature_aver_str)
        # print(self.gray_aver_str)
        print("finished!")
        self.finished.emit(time_now)
        self.judge_flag = judge_flag

    """
    @detail 获取图片pixel信息
    """     
    def getGrayAver(self):
        return self.judge_flag, self.gray_aver, self.nature_aver, self.gray_aver_str, self.nature_aver_str
    
    def setType(self, item_type):
        self.item_type = item_type