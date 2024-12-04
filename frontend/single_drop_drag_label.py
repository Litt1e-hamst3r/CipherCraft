from PyQt5.QtWidgets import QLabel,QApplication
from PyQt5.QtCore import Qt,QMimeData,pyqtSignal
from PyQt5.QtGui import QDrag,QDragEnterEvent,QDropEvent

class DropLabel(QLabel):
    # fileDropped = pyqtSignal(str)  # 定义一个自定义信号
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAlignment(Qt.AlignCenter)
        self.setStyleSheet("border: 2px dashed black; padding: 20px; background-color: lightgreen;")
        self.setText("Drag and Drop File Here")
        self.setAcceptDrops(True)
        self.file_path = None

    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dragMoveEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event: QDropEvent):
        if event.mimeData().hasUrls():
            for url in event.mimeData().urls():
                self.file_path = url.toLocalFile()
                # 在这里打印了拖入文件的信息
                # print(self.file_path)
                # self.fileDropped.emit(file_path)  # 发射信号
                self.parent().read_file_hex(self.file_path)
            event.acceptProposedAction()
            
    def return_file_path(self):
        #  print(self.file_path)
        return self.file_path


class DraggableLabel(QLabel):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setAlignment(Qt.AlignCenter)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_start_position = event.pos()

    def mouseMoveEvent(self, event):
        if not (event.buttons() & Qt.LeftButton):
            return
        if (event.pos() - self.drag_start_position).manhattanLength() < QApplication.startDragDistance():
            return
        drag = QDrag(self)
        mime_data = QMimeData()
        mime_data.setText(self.text())
        drag.setMimeData(mime_data)
        drag.exec_(Qt.CopyAction | Qt.MoveAction)