from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QStackedWidget
import sys
from .single_dropWidget import DropWidget
from .double_windows2 import Window2

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.stacked_widget = QStackedWidget()
        
        self.window1 = DropWidget(self.switch_window)
        self.window2 = Window2(self.switch_window)

        self.setWindowTitle("CipherCraft: "+str(self.window2.port))
        # 将两个窗口添加到堆栈窗口
        self.stacked_widget.addWidget(self.window1)
        self.stacked_widget.addWidget(self.window2)

        # 设置主窗口的布局
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)  # 设置布局的边距为0
        layout.setSpacing(0)  # 设置布局的间距为0
        layout.addWidget(self.stacked_widget)
        self.setLayout(layout)
        
        self.setFixedSize(1920, 1200)  # 设置固定大小为1920x1200像素

        # self.setWindowTitle('端口号是这个：')

    def switch_window(self, index):
        self.stacked_widget.setCurrentIndex(index)

def run():
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    run()
    # app = QApplication(sys.argv)
    # main_window = MainWindow()
    # main_window.show()
    # sys.exit(app.exec_())