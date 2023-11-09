from PySide2.QtCore import QThread, Signal, QDateTime
import frozen as frozen
import time
from inf.img_acquire import Image_Acquire
from inf.img_process import Image_Processing

#   试剂区域圈定区域，可修改
roi_agentia = [
    [0, 700], [0, 2500]
]

#   定位点圈定区域，可修改
roi_position = [
    [0, 700], [0, 2500]  # [startY, endY] [StartX, endX]
]

#   试剂点，相对位置；可修改
matrix_agentia = [
    [
        [260, 310], [590, 310], [920, 310], [1250, 310], [1580, 310]
    ],
    [
        [260, 640], [590, 640], [920, 640], [1250, 640], [1580, 640]
    ],
    [
        [260, 970], [590, 970], [920, 970], [1250, 970], [1580, 970]
    ],
    [
        [260, 1300], [590, 1300], [920, 1300], [1250, 1300], [1580, 1300]
    ],
    [
        [260, 1630], [590, 1630], [920, 1630], [1250, 1630], [1580, 1630]
    ],
    [
        [260, 1960], [590, 1960], [920, 1960], [1250, 1960], [1580, 1960]
    ],
    [
        [260, 2290], [590, 2290], [920, 2290], [1250, 2290], [1580, 2290]
    ],
    [
        [-640, 3320], [-310, 3320], [20, 3320], [350, 3320], [680, 3320]
    ]
]


class MyPicThread(QThread):
    update_progress = Signal(int)
    update_fail = Signal()
    update_success = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)

    def run(self):
        pic_path = QDateTime.currentDateTime().toString('yyyy-MM-dd')

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

    def takePicture(self, time_now):
        try:
            time.sleep(2)
        except Exception as e:
            print(str(e))

        self.imgAcq.img_acquire(time_now)

        # pic_name = 'img_final'
        # flag, gray_aver = self.imgPro.process(path_read=frozen.app_path() + r'/inf/picture/' + pic_name + '.jpeg',
        #                                       path_write=frozen.app_path() + r'/inf/img_out/', reagent=(8, 5),
        #                                       radius=40)
        flag, gray_aver = self.imgPro.process(path_read=frozen.app_path() + r'/inf/picture/' + time_now + '.jpeg',
                                              path_write=frozen.app_path() + r'/inf/img_out/', reagent=(8, 5),
                                              radius=40)

        return gray_aver