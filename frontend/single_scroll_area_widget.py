from PyQt5.QtWidgets import QWidget, QVBoxLayout
from PyQt5.QtCore import Qt
from .single_draggable_widget import *

class ScrollAreaWidget(QWidget):
    def __init__(self, scroll_area=None):
        super(ScrollAreaWidget, self).__init__()
        self.scroll_area = scroll_area
        self.layout = QVBoxLayout()
        self.layout.setSpacing(10)  # 设置布局间距为10
        self.layout.setAlignment(Qt.AlignTop)  # 设置布局内子部件的对齐方式为顶部对齐，这是关键修改点
        self.setLayout(self.layout)

        # 维护一个列表来记录所有添加的控件
        self.widgets_list = []

    def add_widget(self, text):
        widget = DraggableWidget(text, self, self.scroll_area)
        self.layout.addWidget(widget)
        self.update_child_widths()  # 更新子控件宽度

    def update_child_widths(self):
        for i in range(self.layout.count()):
            widget = self.layout.itemAt(i).widget()
            if isinstance(widget, DraggableWidget):
                widget.setFixedWidth(500)  # 设置宽度为300
    
    def get_widgets_in_order(self):
        # 返回按添加顺序排列的控件列表
        return self.widgets_list
    
    def remove_widget(self, widget):
        if widget in self.widgets_list:
            self.widgets_list.remove(widget)
        self.layout.removeWidget(widget)
        widget.deleteLater()