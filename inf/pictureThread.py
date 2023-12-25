from PySide2.QtCore import QThread


"""
@detail 图片获取线程
@detail 弃用
"""


class pictureThread(QThread):
    """
    @detail 初始化线程
    @detail 构造函数
    """
    def __init__(self):
        super().__init__()

    def run(self):
        pass