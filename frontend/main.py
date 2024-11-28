import sys
import os
from base64 import b64encode
from PyQt5.QtWidgets import QComboBox,QCheckBox,QApplication,QFormLayout, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTextEdit, QLineEdit, QScrollArea, QFrame, QPushButton
from PyQt5.QtCore import Qt, QMimeData, QPoint, QRect
from PyQt5.QtGui import QDrag, QDragEnterEvent, QDropEvent
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
                new_y = self.y() + delta.y()

                if self.scroll_area:
                    visible_rect = self.scroll_area.viewport().rect()

                    if new_y >= 0 and new_y + self.height() <= visible_rect.height():
                        self.move(self.x(), new_y)

                    self.last_mouse_move_position = event.pos()

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


class DropLabel(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAlignment(Qt.AlignCenter)
        self.setStyleSheet("border: 2px dashed black; font-size: 10pt; padding: 20px; background-color: lightgreen;")
        self.setText("Drag and Drop File Here")
        self.setAcceptDrops(True)

    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dragMoveEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event: QDropEvent):
        if event.mimeData().hasUrls():
            for url in event.mimeData().urls():
                file_path = url.toLocalFile()
                self.parent().read_file_hex(file_path)
            event.acceptProposedAction()


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


class DropWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Integrated Drag and Drop Example')
        self.setFixedSize(1920, 1200)  # 固定窗口大小

        main_layout = QHBoxLayout()

        # 左侧布局（移除了拖放显示相关代码）
        left_layout = QVBoxLayout()
        left_label = QLabel('Single  Machine  Mode')
        left_label.setStyleSheet("background-color: lightblue; padding: 20px;")
        left_layout.addWidget(left_label)

        # 添加搜索框
        self.search_input = QLineEdit(self)
        self.search_input.setPlaceholderText("Search for encryption/decryption/conversion modes...")
        self.search_input.textChanged.connect(self.update_search_results)
        left_layout.addWidget(self.search_input)

        # 创建三个QScrollArea用于存放不同类别的标签
        self.scroll_areas = {
            'Encryption': self.create_scroll_area(),
            'Decryption': self.create_scroll_area(),
            'Conversion': self.create_scroll_area()
        }

        for category, (scroll_area, _, _) in self.scroll_areas.items():
            left_layout.addWidget(QLabel(f"{category} Modes:"))
            left_layout.addWidget(scroll_area)  # 添加QScrollArea对象而不是元组

        main_layout.addLayout(left_layout, 2)

        # 中间布局（用于显示拖放相关信息以及原有的自定义组件等）
        middle_layout = QVBoxLayout()

        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)

        self.scroll_widget = ScrollAreaWidget(self.scroll_area)
        self.scroll_area.setWidget(self.scroll_widget)

        # 添加一个新的QLabel用于显示拖放相关信息（这里可根据实际需求进一步美化样式等）
        self.drop_info_label = QLabel(self)
        self.drop_info_label.setStyleSheet("background-color: lightyellow; padding: 10px;")
        self.drop_info_label.setWordWrap(True)  # 允许自动换行
        middle_layout.addWidget(self.drop_info_label)

        middle_layout.addWidget(self.scroll_area)
        
        #todo 记得添加执行内容 submit 函数将当前获取的内容转化成json
        add_button = QPushButton('Start', self)
        add_button.clicked.connect(self.submit)
        middle_layout.addWidget(add_button)
        main_layout.addLayout(middle_layout, 3)

        # 右侧布局（原第一段代码中的右侧布局，保持不变）
        right_layout = QVBoxLayout()
        self.label = DropLabel(self)
        self.label.setFixedHeight(100)
        right_layout.addWidget(self.label)

        self.text_edit_input = QTextEdit(self)
        self.text_edit_input.setPlaceholderText("请在这里输入想要加密的文本，如果是拖入的文件，将会在此处显示16进制内容……")
        self.text_edit_input.textChanged.connect(self.update_hex_content)
        right_layout.addWidget(self.text_edit_input)

        self.text_edit_output = QTextEdit(self)
        self.text_edit_output.setReadOnly(True)
        self.text_edit_output.setPlaceholderText("加密后的结果将会显示在这里……")
        right_layout.addWidget(self.text_edit_output)

        main_layout.addLayout(right_layout, 5)

        self.setLayout(main_layout)

        # 更改拖放事件处理绑定到中间布局的对应组件
        self.scroll_area.setAcceptDrops(True)
        self.scroll_area.dragEnterEvent = self.dragEnterEvent
        self.scroll_area.dragMoveEvent = self.dragMoveEvent
        self.scroll_area.dropEvent = self.dropEvent


        # 初始化所有标签
        self.labels = {
            'Encryption': [
                'Caesar',
                'Keyword',
                'Affine',
                'Multiliteral',
                'Vigenere',
                'Autokey ciphertext',
                'Autokey plaintext',
                'Playfair',
                'Permutation',
                'Column permutation',
                'Double-Transposition',
                'RC4 Encryption',
                'CA Encryption',
                'DES Encryption',
                'AES Encryption',
                'RSA Encryption',
                'ECC Encryption',
                'Auto ECC Key',
                'Auto RSA Key'
            ],
            'Decryption': [
                'deCaesar',
                'deKeyword',
                'deAffine',
                'deMultiliteral',
                'deVigenere',
                'deAutokey ciphertext',
                'deAutokey plaintext',
                'dePlayfair',
                'dePermutation',
                'deColumn permutation',
                'deDouble-Transposition',
                'RC4 Decryption',
                'CA Decryption',
                'DES Decryption',
                'AES Decryption',
                'RSA Decryption',
                'ECC Decryption'
            ],
            'Conversion': [
                'From Base64',
                'To Base64',
                'To Hex',
                'From Hex',
                'MD5 Hashing'
            ]
        }

        self.update_search_results()

    def create_scroll_area(self):
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        scroll_area.setWidget(content_widget)
        return (scroll_area, content_widget, content_layout)

    def update_search_results(self):
        search_text = self.search_input.text().strip().lower()
        for category, (scroll_area, content_widget, content_layout) in self.scroll_areas.items():
            # 清除旧的内容
            while content_layout.count():
                child = content_layout.takeAt(0)
                if child.widget():
                    child.widget().deleteLater()

            for label_text in self.labels[category]:
                if search_text in label_text.lower():
                    draggable_label = DraggableLabel(label_text)
                    draggable_label.setStyleSheet("background-color: lightblue; border: 1px solid black; padding: 10px;")
                    content_layout.addWidget(draggable_label)

    def dragEnterEvent(self, event):
        if event.mimeData().hasText():
            event.acceptProposedAction()

    def dragMoveEvent(self, event):
        if event.mimeData().hasText():
            event.acceptProposedAction()

    def dropEvent(self, event):
        if event.mimeData().hasText():
            text = event.mimeData().text()
            self.output_content(text)
            self.add_new_widget(text)
            event.acceptProposedAction()

    def output_content(self, text):
        # 在中间布局的新QLabel中显示拖放相关信息
        self.drop_info_label.setText(f"Selected Mode: {text}")

    def resizeEvent(self,event):  # 更新 QScrollArea 的宽度
        try:
            total_width = self.width()
            left_width = self.layout().itemAt(0).geometry().width()
            right_width = self.layout().itemAt(2).geometry().width()
            middle_width = (total_width - left_width - right_width) * 3 / 8  # 伸缩因子为3
            self.scroll_area.setFixedWidth(middle_width)
            self.scroll_widget.update_child_widths()  # 更新子控件宽度
        except Exception as e:
            print(f"Error in resizeEvent: {e}")
            traceback.print_exc()

    def read_file_hex(self, file_path):
        try:
            with open(file_path, 'rb') as file:
                content = file.read()
                hex_content = content.hex()
                self.text_edit_input.setPlainText(hex_content)
        except Exception as e:
            self.text_edit_output.setPlainText(f"Error reading file: {e}")

    #当收到返回内容的时候在这里更新  TODO 最终记得修改
    def update_hex_content(self):
        input_text = self.text_edit_input.toPlainText()
        hex_content = input_text.encode('utf-8').hex()
        #self.text_edit_output.setPlainText(hex_content)
    def get_custom_widgets_info(self):
        # 检查 self.scroll_widget 是否存在且不为 None
        if not self.scroll_widget or not self.scroll_widget.layout:
            print("Error: self.scroll_widget or its layout is None or not initialized.")
            return []

        widgets_info = []
        for index, widget in enumerate(self.scroll_widget.get_widgets_in_order()):
            if isinstance(widget, DraggableWidget):
                try:
                    # print(f"Processing widget {index} of type {widget.__class__.__name__}")
                    if hasattr(widget, 'get_contents'):
                       widgets_info.append(widget.get_contents())
                    else:
                        print(f"Warning: {widget.__class__.__name__} does not have a get_contents method.")
                        widgets_info.append({"Error": "Widget does not have a get_contents method"})
                except Exception as e:
                    print(f"Error occurred while getting info for widget {widget.label.text()} of type {widget.__class__.__name__}: {e}")
                    traceback.print_exc()
                    widgets_info.append({"Error": "Failed to retrieve contents"})
        return widgets_info
    def get_right_input_text(self):
         return self.text_edit_input.toPlainText()
    def add_new_widget(self, text):
        # TODO 这里还有两个RSA和ECC的加密算法，需要单独处理
        if text == "Affine" or text =="Double-Transposition":
            widget_to_add = WidgetTypeA(text, self.scroll_widget, self.scroll_area)
        elif text == "RC4 Encryption" or text == "Keyword" or text == "Caesar" or text == "Multiliteral" or text == "Vigenere" or text == "Autokey ciphertext" or text == "Autokey plaintext" or text == "Playfair" or text == "Permutation" or text == "Column permutation":
            widget_to_add = WidgetTypeB(text, self.scroll_widget, self.scroll_area)
        elif text == "CA Encryption":
            widget_to_add = WidgetTypeC(text, self.scroll_widget, self.scroll_area)
        elif text == "Auto ECC Key" or text == "Auto RSA Key":
            widget_to_add = WidgetTypeD(text, self.scroll_widget, self.scroll_area)
        elif text == "AES Encryption" or text == "DES Encryption":
            widget_to_add = WidgetTypeE(text, self.scroll_widget, self.scroll_area)
        elif text == "deAffine" or text =="deDouble-Transposition":
            widget_to_add = WidgetTypeG(text, self.scroll_widget, self.scroll_area)
        elif text == "RSA Encryption" or text == "ECC Encryption":
            widget_to_add = WidgetTypeF(text, self.scroll_widget, self.scroll_area)
        elif text == "RC4 Decryption" or text == "deKeyword" or text == "deCaesar" or text == "deMultiliteral" or text == "deVigenere" or text == "deAutokey ciphertext" or text == "deAutokey plaintext" or text == "dePlayfair" or text == "dePermutation" or text == "deColumn permutation":
            widget_to_add = WidgetTypeH(text, self.scroll_widget, self.scroll_area)
        elif text == "CA Decryption":
            widget_to_add = WidgetTypeI(text, self.scroll_widget, self.scroll_area)
        elif text == "AES Decryption" or text == "DES Decryption":
            widget_to_add = WidgetTypeJ(text, self.scroll_widget, self.scroll_area)
        elif text == "RSA Decryption" or text == "ECC Decryption":
            widget_to_add = WidgetTypeK(text, self.scroll_widget, self.scroll_area)
        elif text == "From Base64" or text == "To Base64" or text == "To Hex" or text == "From Hex" or text == "MD5 Hashing":
            widget_to_add = WidgetTypeL(text, self.scroll_widget, self.scroll_area)
        else:
            widget_to_add = DraggableWidget(text, self.scroll_widget, self.scroll_area)  # 默认添加普通的DraggableWidget

        self.scroll_widget.layout.addWidget(widget_to_add)
        self.scroll_widget.update_child_widths()
        
    @staticmethod
    def standardize_algorithm_names(array):
        print("进入到 standardize_algorithm_names函数")
        
        # 定义加密和解密算法的映射
        algorithm_mapping = {
            'Caesar': 'Caesar',
            'Keyword': 'Keyword',
            'Affine': 'Affine',
            'Multiliteral': 'Multiliteral',
            'Vigenere': 'Vigenere',
            'Autokey ciphertext': 'Autokey ciphertext',
            'Autokey plaintext': 'Autokey plaintext',
            'Playfair': 'Playfair',
            'Permutation': 'Permutation',
            'Column permutation': 'Column permutation',
            'Double-Transposition': 'Double-Transposition',
            'RC4 Encryption': 'RC4',
            'CA Encryption': 'CA',
            'DES Encryption': 'DES',
            'AES Encryption': 'AES',
            'RSA Encryption': 'RSA',
            'ECC Encryption': 'ECC',
            'deCaesar': 'Caesar',
            'deKeyword': 'Keyword',
            'deAffine': 'Affine',
            'deMultiliteral': 'Multiliteral',
            'deVigenere': 'Vigenere',
            'deAutokey ciphertext': 'Autokey ciphertext',
            'deAutokey plaintext': 'Autokey plaintext',
            'dePlayfair': 'Playfair',
            'dePermutation': 'Permutation',
            'deColumn permutation': 'Column permutation',
            'deDouble-Transposition': 'Double-Transposition',
            'RC4 Decryption': 'RC4',
            'CA Decryption': 'CA',
            'DES Decryption': 'DES',
            'AES Decryption': 'AES',
            'RSA Decryption': 'RSA',
            'ECC Decryption': 'ECC'
        }

        print("尝试遍历并更改")
        
        # 遍历每个字典并更新算法名称
        for dic in array:  # 假设 array 是一个包含字典的列表
            if 'algorithm' in dic:
                original_name = dic['algorithm']
                if original_name in algorithm_mapping:
                    dic['algorithm'] = algorithm_mapping[original_name]

        return array  # 返回整个处理过的数组
    def submit(self):
        print("Submit button clicked1")
        custom_widgets_info = self.get_custom_widgets_info()
        print("get_custom_widgets_info")
        print("自定义控件信息:", custom_widgets_info)
        custom_widgets_info2 = self.standardize_algorithm_names(custom_widgets_info)
        right_input_text = self.get_right_input_text()
        print("Submit button clicked2")
        print("自定义控件信息:", custom_widgets_info2)
        print("右侧用户输入内容:", right_input_text)
        
        self.text_edit_output.setPlainText("啊啦啦啦啦")
    
    
#下面就是各种自定义的标签了 以及main函数
class WidgetTypeA(DraggableWidget):
    def __init__(self, text, parent=None, scroll_area=None):
        super().__init__(text, parent, scroll_area)
        self.setFixedSize(300, 200)
        self.label.setText(f"{text}")
        
        # 创建一个表单布局
        form_layout = QFormLayout()
        
        # 创建新的标签和输入框部件
        self.name_edit = QLineEdit(self)
        self.name_edit.setPlaceholderText("请输入密钥1")
        self.name_edit.setStyleSheet("QLineEdit { background-color: white; }")
        form_layout.addRow(self.name_edit)
        
        self.key_edit = QLineEdit(self)
        self.key_edit.setPlaceholderText("请输入密钥2")
        self.key_edit.setStyleSheet("QLineEdit { background-color: white; }")
        form_layout.addRow(self.key_edit)
        
        # 创建包含两个下拉菜单的水平布局
        combo_layout = QHBoxLayout()
        self.input_type = QComboBox(self)
        self.input_type.addItems(["Hex", "Raw"])
        self.input_type.setStyleSheet("QComboBox { background-color: white; }")
        self.output_type = QComboBox(self)
        self.output_type.addItems(["Hex", "Raw"])
        self.output_type.setStyleSheet("QComboBox { background-color: white; }")
        combo_layout.addWidget(self.input_type)
        combo_layout.addWidget(self.output_type)
        
        # 将水平布局添加到表单布局中，作为一行
        form_layout.addRow("Input/Output", combo_layout)
        
        # 获取父类原有的垂直布局（也可以选择创建新的外层布局，这里以使用原布局为例）
        layout = self.layout()
        # 将表单布局添加到原垂直布局中，它会在垂直方向上位于合适位置（排在原有QLabel下方等情况）
        layout.addLayout(form_layout)
    
    def get_contents(self):
        return {
            "algorithm":self.label.text(),
            "key": [self.name_edit.text(),self.key_edit.text()],
            "mode":"encrypt",
            "key_type": "",
            "input_type": self.input_type.currentText(),
            "output_type": self.output_type.currentText()
        }
        
class WidgetTypeF(DraggableWidget):
    def __init__(self, text, parent=None, scroll_area=None):
        super().__init__(text, parent, scroll_area)
        self.setFixedSize(300, 200)
        self.label.setText(f"{text}")
        
        # 创建一个表单布局
        form_layout = QFormLayout()
        
        # 创建新的标签和输入框部件
        self.name_edit = QLineEdit(self)
        self.name_edit.setPlaceholderText("请输入公钥模数n")
        self.name_edit.setStyleSheet("QLineEdit { background-color: white; }")
        form_layout.addRow(self.name_edit)
        
        self.key_edit = QLineEdit(self)
        self.key_edit.setPlaceholderText("请输入公钥底数e")
        self.key_edit.setStyleSheet("QLineEdit { background-color: white; }")
        form_layout.addRow(self.key_edit)
        
        # 创建包含两个下拉菜单的水平布局
        combo_layout = QHBoxLayout()
        self.input_type = QComboBox(self)
        self.input_type.addItems(["Hex", "Raw"])
        self.input_type.setStyleSheet("QComboBox { background-color: white; }")
        self.output_type = QComboBox(self)
        self.output_type.addItems(["Hex", "Raw"])
        self.output_type.setStyleSheet("QComboBox { background-color: white; }")
        combo_layout.addWidget(self.input_type)
        combo_layout.addWidget(self.output_type)
        
        # 将水平布局添加到表单布局中，作为一行
        form_layout.addRow("Input/Output", combo_layout)
        
        # 获取父类原有的垂直布局（也可以选择创建新的外层布局，这里以使用原布局为例）
        layout = self.layout()
        # 将表单布局添加到原垂直布局中，它会在垂直方向上位于合适位置（排在原有QLabel下方等情况）
        layout.addLayout(form_layout)

    def get_contents(self):
        return {
            "algorithm":self.label.text(),
            "key": {
                "public_key":[self.name_edit.text(),self.key_edit.text()],
                "private_key":["",""]
            },
            "mode":"encrypt",
            "key_type": "",
            "input_type": self.input_type.currentText(),
            "output_type": self.output_type.currentText()
        }   
        
class WidgetTypeK(DraggableWidget):
    def __init__(self, text, parent=None, scroll_area=None):
        super().__init__(text, parent, scroll_area)
        self.setFixedSize(300, 200)
        self.label.setText(f"{text}")
        
        # 创建一个表单布局
        form_layout = QFormLayout()
        
        # 创建新的标签和输入框部件
        self.name_edit = QLineEdit(self)
        self.name_edit.setPlaceholderText("请输入私钥模数n")
        self.name_edit.setStyleSheet("QLineEdit { background-color: lightyellow; }")
        form_layout.addRow(self.name_edit)
        
        self.key_edit = QLineEdit(self)
        self.key_edit.setPlaceholderText("请输入私钥底数d")
        self.key_edit.setStyleSheet("QLineEdit { background-color: lightyellow; }")
        form_layout.addRow(self.key_edit)
        
        # 创建包含两个下拉菜单的水平布局
        combo_layout = QHBoxLayout()
        self.input_type = QComboBox(self)
        self.input_type.addItems(["Hex", "Raw"])
        self.input_type.setStyleSheet("QComboBox { background-color: lightyellow; }")
        self.output_type = QComboBox(self)
        self.output_type.addItems(["Hex", "Raw"])
        self.output_type.setStyleSheet("QComboBox { background-color: lightyellow; }")
        combo_layout.addWidget(self.input_type)
        combo_layout.addWidget(self.output_type)
        
        # 将水平布局添加到表单布局中，作为一行
        form_layout.addRow("Input/Output", combo_layout)
        
        # 获取父类原有的垂直布局（也可以选择创建新的外层布局，这里以使用原布局为例）
        layout = self.layout()
        # 将表单布局添加到原垂直布局中，它会在垂直方向上位于合适位置（排在原有QLabel下方等情况）
        layout.addLayout(form_layout)

    def get_contents(self):
        return {
            "algorithm":self.label.text(),
            "key": {
                "public_key":["",""],
                "private_key":[self.name_edit.text(),self.key_edit.text()]
            },
            "mode":"decrypt",
            "key_type": "",
            "input_type": self.input_type.currentText(),
            "output_type": self.output_type.currentText()
        }   
class WidgetTypeG(DraggableWidget):
    def __init__(self, text, parent=None, scroll_area=None):
        super().__init__(text, parent, scroll_area)
        self.setFixedSize(300, 200)
        self.label.setText(f"{text}")
        
        # 创建一个表单布局
        form_layout = QFormLayout()
        
        # 创建新的标签和输入框部件
        self.name_edit = QLineEdit(self)
        self.name_edit.setPlaceholderText("请输入密钥1")
        self.name_edit.setStyleSheet("QLineEdit { background-color: lightyellow; }")
        form_layout.addRow(self.name_edit)
        
        self.key_edit = QLineEdit(self)
        self.key_edit.setPlaceholderText("请输入密钥2")
        self.key_edit.setStyleSheet("QLineEdit { background-color: lightyellow; }")
        form_layout.addRow(self.key_edit)
        
        # 创建包含两个下拉菜单的水平布局
        combo_layout = QHBoxLayout()
        self.input_type = QComboBox(self)
        self.input_type.addItems(["Hex", "Raw"])
        self.input_type.setStyleSheet("QComboBox { background-color: lightyellow; }")
        self.output_type = QComboBox(self)
        self.output_type.addItems(["Hex", "Raw"])
        self.output_type.setStyleSheet("QComboBox { background-color: lightyellow; }")
        combo_layout.addWidget(self.input_type)
        combo_layout.addWidget(self.output_type)
        
        # 将水平布局添加到表单布局中，作为一行
        form_layout.addRow("Input/Output", combo_layout)
        
        # 获取父类原有的垂直布局（也可以选择创建新的外层布局，这里以使用原布局为例）
        layout = self.layout()
        # 将表单布局添加到原垂直布局中，它会在垂直方向上位于合适位置（排在原有QLabel下方等情况）
        layout.addLayout(form_layout)

    def get_contents(self):
        return {
            "algorithm":self.label.text(),
            "key": [self.name_edit.text(),self.key_edit.text()],
            "mode":"decrypt",
            "key_type": "",
            "input_type": self.input_type.currentText(),
            "output_type": self.output_type.currentText()
        }

class WidgetTypeB(DraggableWidget):
    def __init__(self, text, parent=None, scroll_area=None):
        super().__init__(text, parent, scroll_area)
        self.setFixedSize(300, 160)
        # 设置标签文本
        self.label.setText(f"{text}")
        # 创建一个表单布局
        form_layout = QFormLayout()
        # 创建新的标签和输入框部件
        self.name_edit = QLineEdit(self)  # 保存为实例属性
        self.name_edit.setPlaceholderText("请输入密钥")
        self.name_edit.setStyleSheet("QLineEdit { background-color: white; }")
        form_layout.addRow(self.name_edit)
        # 创建包含两个下拉菜单的水平布局
        combo_layout = QHBoxLayout()
        self.input_type = QComboBox(self)  # 保存为实例属性
        self.input_type.addItems(["Hex", "Raw"])
        self.input_type.setStyleSheet("QComboBox { background-color: white; }")
        self.output_type = QComboBox(self)  # 保存为实例属性
        self.output_type.addItems(["Hex", "Raw"])
        self.output_type.setStyleSheet("QComboBox { background-color: white; }")
        combo_layout.addWidget(self.input_type)
        combo_layout.addWidget(self.output_type)
        # 将水平布局添加到表单布局中，作为一行
        form_layout.addRow("Input/Output", combo_layout)
        # 获取父类原有的垂直布局（也可以选择创建新的外层布局，这里以使用原布局为例）
        layout = self.layout()
        # 将表单布局添加到原垂直布局中，它会在垂直方向上位于合适位置（排在原有QLabel下方等情况）
        layout.addLayout(form_layout)
    def get_contents(self):
        return {
            "algorithm":self.label.text(),
            "key": [self.name_edit.text()],
            "mode":"encrypt",
            "key_type": "",
            "input_type": self.input_type.currentText(),
            "output_type": self.output_type.currentText()
        }

class WidgetTypeH(DraggableWidget):
    def __init__(self, text, parent=None, scroll_area=None):
        super().__init__(text, parent, scroll_area)
        self.setFixedSize(300, 160)
        self.label.setText(f"{text}")
        
        # 创建一个表单布局
        form_layout = QFormLayout()
        
        # 创建新的标签和输入框部件
        self.name_edit = QLineEdit(self)
        self.name_edit.setPlaceholderText("请输入密钥")
        self.name_edit.setStyleSheet("QLineEdit { background-color: lightyellow; }")
        form_layout.addRow(self.name_edit)
        
        # 创建包含两个下拉菜单的水平布局
        combo_layout = QHBoxLayout()
        self.input_type = QComboBox(self)
        self.input_type.addItems(["Hex", "Raw"])
        self.input_type.setStyleSheet("QComboBox { background-color: lightyellow; }")
        self.output_type = QComboBox(self)
        self.output_type.addItems(["Hex", "Raw"])
        self.output_type.setStyleSheet("QComboBox { background-color: lightyellow; }")
        combo_layout.addWidget(self.input_type)
        combo_layout.addWidget(self.output_type)
        
        # 将水平布局添加到表单布局中，作为一行
        form_layout.addRow("Input/Output", combo_layout)
        
        # 获取父类原有的垂直布局（也可以选择创建新的外层布局，这里以使用原布局为例）
        layout = self.layout()
        # 将表单布局添加到原垂直布局中，它会在垂直方向上位于合适位置（排在原有QLabel下方等情况）
        layout.addLayout(form_layout)

    def get_contents(self):
        return {
            "algorithm":self.label.text(),
            "key": [self.name_edit.text()],
            "mode":"decrypt",
            "key_type": "",
            "input_type": self.input_type.currentText(),
            "output_type": self.output_type.currentText()
        }
        
class WidgetTypeC(DraggableWidget):
    def __init__(self, text, parent=None, scroll_area=None):
        super().__init__(text, parent, scroll_area)
        self.setFixedSize(300, 230)
        self.label.setText(f"{text}")
        
        # 创建一个表单布局
        form_layout = QFormLayout()
        
        # 创建新的标签和输入框部件
        self.name_edit = QLineEdit(self)
        self.name_edit.setPlaceholderText("初始状态")
        self.name_edit.setStyleSheet("QLineEdit { background-color: white; }")
        form_layout.addRow(self.name_edit)
        
        self.key_edit = QLineEdit(self)
        self.key_edit.setPlaceholderText("密钥转移规则")
        self.key_edit.setStyleSheet("QLineEdit { background-color: white; }")
        form_layout.addRow(self.key_edit)
        
        self.key_edit2 = QLineEdit(self)
        self.key_edit2.setPlaceholderText("密钥位置")
        self.key_edit2.setStyleSheet("QLineEdit { background-color: white; }")
        form_layout.addRow(self.key_edit2)
        
        # 创建包含两个下拉菜单的水平布局
        combo_layout = QHBoxLayout()
        self.input_type = QComboBox(self)
        self.input_type.addItems(["Hex", "Raw"])
        self.input_type.setStyleSheet("QComboBox { background-color: white; }")
        self.output_type = QComboBox(self)
        self.output_type.addItems(["Hex", "Raw"])
        self.output_type.setStyleSheet("QComboBox { background-color: white; }")
        combo_layout.addWidget(self.input_type)
        combo_layout.addWidget(self.output_type)
        
        # 将水平布局添加到表单布局中，作为一行
        form_layout.addRow("Input/Output", combo_layout)
        
        # 获取父类原有的垂直布局（也可以选择创建新的外层布局，这里以使用原布局为例）
        layout = self.layout()
        # 将表单布局添加到原垂直布局中，它会在垂直方向上位于合适位置（排在原有QLabel下方等情况）
        layout.addLayout(form_layout)

    def get_contents(self):
        return {
            "algorithm":self.label.text(),
            "key": [self.name_edit.text(),self.key_edit.text(),self.key_edit2.text()],
            "mode":"encrypt",
            "key_type": "",
            "input_type": self.input_type.currentText(),
            "output_type": self.output_type.currentText()
        }

        
class WidgetTypeI(DraggableWidget):
    def __init__(self, text, parent=None, scroll_area=None):
        super().__init__(text, parent, scroll_area)
        self.setFixedSize(300, 230)
        self.label.setText(f"{text}")
        
        # 创建一个表单布局
        form_layout = QFormLayout()
        
        # 创建新的标签和输入框部件
        self.name_edit = QLineEdit(self)
        self.name_edit.setPlaceholderText("初始状态")
        self.name_edit.setStyleSheet("QLineEdit { background-color: lightyellow; }")
        form_layout.addRow(self.name_edit)
        
        self.key_edit = QLineEdit(self)
        self.key_edit.setPlaceholderText("密钥转移规则")
        self.key_edit.setStyleSheet("QLineEdit { background-color: lightyellow; }")
        form_layout.addRow(self.key_edit)
        
        self.key_edit2 = QLineEdit(self)
        self.key_edit2.setPlaceholderText("密钥位置")
        self.key_edit2.setStyleSheet("QLineEdit { background-color: lightyellow; }")
        form_layout.addRow(self.key_edit2)
        
        # 创建包含两个下拉菜单的水平布局
        combo_layout = QHBoxLayout()
        self.input_type = QComboBox(self)
        self.input_type.addItems(["Hex", "Raw"])
        self.input_type.setStyleSheet("QComboBox { background-color: lightyellow; }")
        self.output_type = QComboBox(self)
        self.output_type.addItems(["Hex", "Raw"])
        self.output_type.setStyleSheet("QComboBox { background-color: lightyellow; }")
        combo_layout.addWidget(self.input_type)
        combo_layout.addWidget(self.output_type)
        
        # 将水平布局添加到表单布局中，作为一行
        form_layout.addRow("Input/Output", combo_layout)
        
        # 获取父类原有的垂直布局（也可以选择创建新的外层布局，这里以使用原布局为例）
        layout = self.layout()
        # 将表单布局添加到原垂直布局中，它会在垂直方向上位于合适位置（排在原有QLabel下方等情况）
        layout.addLayout(form_layout)

    def get_contents(self):
        return {
            "algorithm":self.label.text(),
            "key": [self.name_edit.text(),self.key_edit.text(),self.key_edit2.text()],
            "mode":"decrypt",
            "key_type": "",
            "input_type": self.input_type.currentText(),
            "output_type": self.output_type.currentText()
        }
class WidgetTypeD(DraggableWidget):
    def __init__(self, text, parent=None, scroll_area=None):
        super().__init__(text, parent, scroll_area)
        self.setFixedSize(300, 110)
        self.label.setText(f"{text}")
        
        # 创建一个表单布局
        form_layout = QFormLayout()
        
        # 创建新的标签和输入框部件
        self.name_edit = QLineEdit(self)
        self.name_edit.setPlaceholderText("请输入密钥长度，限制1024及以内")
        self.name_edit.setStyleSheet("QLineEdit { background-color: white; }")
        form_layout.addRow(self.name_edit)
        
        # # 创建包含两个下拉菜单的水平布局
        # combo_layout = QHBoxLayout()
        # self.input_type = QComboBox(self)
        # self.input_type.addItems(["Raw", "Hex"])
        # self.input_type.setStyleSheet("QComboBox { background-color: white; }")
        # self.output_type = QComboBox(self)
        # self.output_type.addItems(["Raw", "Hex"])
        # self.output_type.setStyleSheet("QComboBox { background-color: white; }")
        # combo_layout.addWidget(self.input_type)
        # combo_layout.addWidget(self.output_type)
        
        # # 将水平布局添加到表单布局中，作为一行
        # form_layout.addRow("Input/Output", combo_layout)
        
        # 获取父类原有的垂直布局（也可以选择创建新的外层布局，这里以使用原布局为例）
        layout = self.layout()
        # 将表单布局添加到原垂直布局中，它会在垂直方向上位于合适位置（排在原有QLabel下方等情况）
        layout.addLayout(form_layout)

    def get_contents(self):
        return {
            "algorithm":self.label.text(),
            "key": [self.name_edit.text()],
            "mode":"encrypt",
            "key_type": "",
            "input_type": "",
            "output_type": ""
        }
        
class WidgetTypeE(DraggableWidget):
    def __init__(self, text, parent=None, scroll_area=None):
        super().__init__(text, parent, scroll_area)
        self.setFixedSize(300, 160)
        self.label.setText(f"{text}")
        
        # 创建一个表单布局
        form_layout = QFormLayout()
        
        # 创建新的标签和输入框部件
        self.name_edit = QLineEdit(self)
        self.name_edit.setPlaceholderText("请输入密钥")
        self.name_edit.setStyleSheet("QLineEdit { background-color: white; }")
        form_layout.addRow(self.name_edit)
        
        # 创建包含三个下拉菜单的水平布局
        combo_layout = QHBoxLayout()
        self.input_type = QComboBox(self)
        self.input_type.addItems(["Hex", "Raw"])
        self.input_type.setStyleSheet("QComboBox { background-color: white; }")
        self.output_type = QComboBox(self)
        self.output_type.addItems(["Hex", "Raw"])
        self.output_type.setStyleSheet("QComboBox { background-color: white; }")
        self.key_type = QComboBox(self)
        self.key_type.addItems(["Hex", "Raw"])
        self.key_type.setStyleSheet("QComboBox { background-color: white; }")
        combo_layout.addWidget(self.input_type)
        combo_layout.addWidget(self.output_type)
        combo_layout.addWidget(self.key_type)
        
        # 将水平布局添加到表单布局中，作为一行
        form_layout.addRow("In/Out/Type", combo_layout)
        
        # 获取父类原有的垂直布局（也可以选择创建新的外层布局，这里以使用原布局为例）
        layout = self.layout()
        # 将表单布局添加到原垂直布局中，它会在垂直方向上位于合适位置（排在原有QLabel下方等情况）
        layout.addLayout(form_layout)

    def get_contents(self):
        return {
            "algorithm":self.label.text(),
            "key": [self.name_edit.text()],
            "mode":"encrypt",
            "key_type": self.key_type.currentText(),
            "input_type": self.input_type.currentText(),
            "output_type": self.output_type.currentText()
        }
        
class WidgetTypeJ(DraggableWidget):
    def __init__(self, text, parent=None, scroll_area=None):
        super().__init__(text, parent, scroll_area)
        self.setFixedSize(300, 160)
        self.label.setText(f"{text}")
        
        # 创建一个表单布局
        form_layout = QFormLayout()
        
        # 创建新的标签和输入框部件
        self.name_edit = QLineEdit(self)
        self.name_edit.setPlaceholderText("请输入密钥")
        self.name_edit.setStyleSheet("QLineEdit { background-color: lightyellow; }")
        form_layout.addRow(self.name_edit)
        
        # 创建包含三个下拉菜单的水平布局
        combo_layout = QHBoxLayout()
        self.input_type = QComboBox(self)
        self.input_type.addItems(["Hex", "Raw"])
        self.input_type.setStyleSheet("QComboBox { background-color: lightyellow; }")
        self.output_type = QComboBox(self)
        self.output_type.addItems(["Hex", "Raw"])
        self.output_type.setStyleSheet("QComboBox { background-color: lightyellow; }")
        self.key_type = QComboBox(self)
        self.key_type.addItems(["Hex", "Raw"])
        self.key_type.setStyleSheet("QComboBox { background-color: lightyellow; }")
        combo_layout.addWidget(self.input_type)
        combo_layout.addWidget(self.output_type)
        combo_layout.addWidget(self.key_type)
        
        # 将水平布局添加到表单布局中，作为一行
        form_layout.addRow("In/Out/Type", combo_layout)
        
        # 获取父类原有的垂直布局（也可以选择创建新的外层布局，这里以使用原布局为例）
        layout = self.layout()
        # 将表单布局添加到原垂直布局中，它会在垂直方向上位于合适位置（排在原有QLabel下方等情况）
        layout.addLayout(form_layout)

    def get_contents(self):
        return {
            "algorithm":self.label.text(),
            "key": [self.name_edit.text()],
            "mode":"decrypt",
            "key_type": self.key_type.currentText(),
            "input_type": self.input_type.currentText(),
            "output_type": self.output_type.currentText()
        }
        
        
class WidgetTypeL(DraggableWidget):
    def __init__(self, text, parent=None, scroll_area=None):
        super().__init__(text, parent, scroll_area)

    def get_contents(self):
        return {
            "algorithm":self.label.text(),
            "key":"",
            "mode":"",
            "key_type": "",
            "input_type": "",
            "output_type": ""
        }
                
if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = DropWidget()
    widget.show()
    sys.exit(app.exec_())