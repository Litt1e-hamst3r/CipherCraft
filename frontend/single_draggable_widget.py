from PyQt5.QtWidgets import QFrame,QVBoxLayout, QLabel, QFrame
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCursor
import traceback

class DraggableWidget(QFrame):
    def __init__(self, text, parent=None, scroll_area=None):
        super(DraggableWidget, self).__init__(parent)
        self.setFixedSize(300, 100)  # 初始宽度为300
        self.setStyleSheet("border: 1px solid black; background-color: lightblue;")
        self.normal_style = "border: 1px solid black; background-color: lightblue;"
        self.delete_style = "border: 1px solid black; background-color: red;"

        layout = QVBoxLayout()
        self.label = QLabel(text)
        layout.addWidget(self.label)
        self.setLayout(layout)

        self.drag_start_position = None
        self.is_dragging = False
        self.scroll_area = scroll_area
        self.delete_threshold = 200  # 横向移动超过200像素时删除控件
        self.last_mouse_move_position = None
        self.should_delete = False
        
        # 将新创建的控件添加到 widgets_list
        if self.scroll_area and self.scroll_area.widget():
            scroll_widget = self.scroll_area.widget()
            if hasattr(scroll_widget, 'widgets_list'):
                scroll_widget.widgets_list.append(self)

    def get_contents(self):
        return self.label.text()
        
    def mousePressEvent(self, event):
        try:
            if event.button() == Qt.LeftButton:
                self.drag_start_position = event.pos()
                self.is_dragging = True
                self.should_delete = False  # 重置删除标志
                self.setStyleSheet(self.normal_style)  # 重置样式
            super(DraggableWidget, self).mousePressEvent(event)
        except Exception as e:
            print(f"Error in mousePressEvent: {e}")
            traceback.print_exc()


    def mouseMoveEvent(self, event):
        try:
            if self.is_dragging:
                delta = event.pos() - self.drag_start_position
                # 保持x坐标不变
                new_x = self.x()
                new_y = self.y() + delta.y()

                # 获取鼠标在屏幕上的位置
                global_mouse_pos = QCursor.pos()
                # 将全局鼠标位置转换为相对于QScrollArea的局部位置
                local_mouse_pos = self.scroll_area.mapFromGlobal(global_mouse_pos)

                # 检查是否需要滚动
                if self.scroll_area:
                    visible_rect = self.scroll_area.viewport().rect()
                    viewport_height = visible_rect.height()
                    scroll_bar_v = self.scroll_area.verticalScrollBar()

                    # 计算滚动量
                    scroll_amount = 10

                    # 向上滚动
                    if local_mouse_pos.y() < 20 and scroll_bar_v.value() > 0:  # 鼠标距离顶部20像素内
                        # 如果小部件超出顶部，计算实际可以滚动的距离
                        actual_scroll_amount = min(scroll_amount, scroll_bar_v.value())
                        scroll_bar_v.setValue(scroll_bar_v.value() - actual_scroll_amount)
                        # 更新new_y以反映滚动
                        new_y += actual_scroll_amount
                    # 向下滚动
                    elif (local_mouse_pos.y() > (viewport_height - 20)) and \
                        scroll_bar_v.value() < scroll_bar_v.maximum():  # 鼠标距离底部20像素内
                        # 如果小部件超出底部，计算实际可以滚动的距离
                        actual_scroll_amount = min(scroll_amount, scroll_bar_v.maximum() - scroll_bar_v.value())
                        scroll_bar_v.setValue(scroll_bar_v.value() + actual_scroll_amount)
                        # 更新new_y以反映滚动
                        new_y -= actual_scroll_amount

                # 更新小部件位置
                self.move(new_x, new_y)

                # 检查水平移动距离是否超过阈值
                if abs(delta.x()) > self.delete_threshold:
                    self.setStyleSheet(self.delete_style)  # 标红
                    self.should_delete = True
                else:
                    self.setStyleSheet(self.normal_style)  # 重置样式
                    self.should_delete = False

            super(DraggableWidget, self).mouseMoveEvent(event)
        except Exception as e:
            print(f"Error in mouseMoveEvent: {e}")
            traceback.print_exc()
    def mouseReleaseEvent(self, event):
        try:
            if event.button() == Qt.LeftButton and self.is_dragging:
                self.is_dragging = False
                release_pos = event.globalPos()
                print(f"Mouse released at global position: {release_pos}")
                local_release_pos = self.mapFromGlobal(release_pos)
                print(f"Mouse released at local position: {local_release_pos}")

                if self.should_delete:
                    if self.scroll_area and self.scroll_area.widget():
                        scroll_widget = self.scroll_area.widget()
                        if hasattr(scroll_widget, 'remove_widget'):
                            scroll_widget.remove_widget(self)
                    print(f"Widget {self.label.text()} deleted")
                else:
                    self.rearrange_all_widgets()

            super(DraggableWidget, self).mouseReleaseEvent(event)
        except Exception as e:
            print(f"Error in mouseReleaseEvent: {e}")
            traceback.print_exc()

    def rearrange_all_widgets(self):
        # 获取所有兄弟控件
        siblings = [w for w in self.parent().children() if isinstance(w, DraggableWidget)]
        # 按照 y 坐标排序
        siblings.sort(key=lambda w: w.y())
        y_offset = 19  # 纵向偏移量
        for widget in siblings:
            widget.move(widget.x(), y_offset)  # 设置控件的位置
            y_offset += widget.height() + 10  # 增加偏移量，包括间距

        # 更新 ScrollAreaWidget 中的 widgets_list
        if self.scroll_area and self.scroll_area.widget():
            scroll_widget = self.scroll_area.widget()
            if hasattr(scroll_widget, 'widgets_list'):
                scroll_widget.widgets_list = siblings
            