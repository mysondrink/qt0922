from PySide2.QtCore import QThread, Signal, QStorageInfo


class MyProbe(QThread):
    update_progress = Signal()
    def __init__(self, parent=None):
        super().__init__(parent)

    def run(self):
        self.memorystr = QStorageInfo().root()
        mem_total = self.memorystr.bytesTotal() / (1024 * 1024 * 1024)
        mem_avail = self.memorystr.bytesAvailable() / (1024 * 1024 * 1024)
        mem_progress = mem_avail / mem_total
        if mem_progress < 0.02:
            self.update_progress.emit()