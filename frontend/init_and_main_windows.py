from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QStackedWidget
import sys
from .single_dropWidget import DropWidget
from .double_windows2 import Window2
import os
import PyQt5.QtGui as QtGui

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.stacked_widget = QStackedWidget()
        
        self.window1 = DropWidget(self.switch_window)
        self.window2 = Window2(self.switch_window)

        self.setWindowTitle("CipherCraft: "+str(self.window2.port))
        self.init_icon()
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

    def init_icon(self):
        # 设置窗口图标
        ico_path = os.path.join(os.path.dirname(__file__), './src/cc.ico')
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(ico_path), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.setWindowIcon(icon)
        # 设置任务栏图标
        import ctypes
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("CipherCraft")
def run():
    
    app = QApplication(sys.argv)
    qss_file = os.path.join(os.path.dirname(__file__), './src/style.qss')
    qss_style = open(qss_file, 'r', encoding='utf-8').read()
    app.setStyleSheet(qss_style) 
    # apply_stylesheet(app, theme='dark_teal.xml')
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    run()
    # app = QApplication(sys.argv)
    # main_window = MainWindow()
    # main_window.show()
    # sys.exit(app.exec_())