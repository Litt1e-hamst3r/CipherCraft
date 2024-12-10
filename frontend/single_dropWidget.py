from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QLineEdit, QScrollArea, QPushButton, QTextEdit
from PyQt5.QtCore import Qt
import traceback
from .single_scroll_area_widget import ScrollAreaWidget
from .single_drop_drag_label import DraggableLabel, DropLabel
from .single_draggable_widget import DraggableWidget
from .single_custom_widgets import *
import os
import sys
import json
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# 将项目根目录添加到 sys.path
sys.path.append(project_root)
from backend.CipherProcessor import CipherProcessor
from .log_msg import setup_logger

class DropWidget(QWidget):
    
    def __init__(self, switch_window_callback):
        super().__init__()
        self.switch_window = switch_window_callback
        self.initUI()
        self.logger = setup_logger("single_window")
        # self.file_path = None  # 用于存储文件路径

    def initUI(self):
        # self.setWindowTitle('Integrated Drag and Drop Example')
        self.setFixedSize(1920, 1200)  # 固定窗口大小

        main_layout = QHBoxLayout()

        # 左侧布局（移除了拖放显示相关代码）
        # 创建垂直布局
        left_layout = QVBoxLayout()
        # 创建水平布局
        horizontal_layout = QHBoxLayout()
        # 创建标签
        left_label = QLabel('Single Machine', self)
        left_label.setStyleSheet("background-color: lightblue; padding: 20px;")
        # left_label.mousePressEvent = self.on_left_label_click  # 添加点击事件
        horizontal_layout.addWidget(left_label)

        # 创建按钮
        #button = QPushButton('Click Me', self)
                # 创建一个 QLabel
        right_button = QPushButton('Change Mode', self)
        right_button.setStyleSheet("""padding: 20px;""")
        right_button.clicked.connect(lambda: self.switch_window(1))
        # right_label = QLabel('Change Mode', self)
        # right_label.setStyleSheet("background-color: lightblue; padding: 20px;")
        # right_label.mousePressEvent = self.on_left_label_click
        horizontal_layout.addWidget(right_button)

        # 将水平布局添加到垂直布局中
        left_layout.addLayout(horizontal_layout)

        # 添加搜索框
        self.search_input = QLineEdit(self)
        self.search_input.setPlaceholderText("Type here to search……")
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

    # def on_left_label_click(self, event):
    #     print("Left label clicked!")
    #     self.switch_window(1)
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
        elif text == "Keyword" or text == "Caesar" or text == "Multiliteral" or text == "Vigenere" or text == "Autokey ciphertext" or text == "Autokey plaintext" or text == "Playfair" or text == "Permutation" or text == "Column permutation":
            widget_to_add = WidgetTypeB(text, self.scroll_widget, self.scroll_area)
        elif text == "CA Encryption":
            widget_to_add = WidgetTypeC(text, self.scroll_widget, self.scroll_area)
        elif text == "Auto ECC Key" or text == "Auto RSA Key":
            widget_to_add = WidgetTypeD(text, self.scroll_widget, self.scroll_area)
        elif text == "RC4 Encryption" or text == "AES Encryption" or text == "DES Encryption":
            widget_to_add = WidgetTypeE(text, self.scroll_widget, self.scroll_area)
        elif text == "deAffine" or text =="deDouble-Transposition":
            widget_to_add = WidgetTypeG(text, self.scroll_widget, self.scroll_area)
        elif text == "RSA Encryption" or text == "ECC Encryption":
            widget_to_add = WidgetTypeF(text, self.scroll_widget, self.scroll_area)
        elif  text == "deKeyword" or text == "deCaesar" or text == "deMultiliteral" or text == "deVigenere" or text == "deAutokey ciphertext" or text == "deAutokey plaintext" or text == "dePlayfair" or text == "dePermutation" or text == "deColumn permutation":
            widget_to_add = WidgetTypeH(text, self.scroll_widget, self.scroll_area)
        elif text == "CA Decryption":
            widget_to_add = WidgetTypeI(text, self.scroll_widget, self.scroll_area)
        elif text == "RC4 Decryption" or text == "AES Decryption" or text == "DES Decryption":
            widget_to_add = WidgetTypeJ(text, self.scroll_widget, self.scroll_area)
        elif text == "RSA Decryption":
            widget_to_add = WidgetTypeK(text, self.scroll_widget, self.scroll_area)
        elif text == "ECC Decryption":
            widget_to_add = WidgetTypeEccDe(text, self.scroll_widget, self.scroll_area)
        elif text == "From Base64" or text == "To Base64" or text == "To Hex" or text == "From Hex" or text == "MD5 Hashing":
            widget_to_add = WidgetTypeL(text, self.scroll_widget, self.scroll_area)
        else:
            widget_to_add = DraggableWidget(text, self.scroll_widget, self.scroll_area)  # 默认添加普通的DraggableWidget

        self.scroll_widget.layout.addWidget(widget_to_add)
        self.scroll_widget.update_child_widths()
        
    @staticmethod
    def standardize_algorithm_names(array):
        # print("进入到 standardize_algorithm_names函数")
        
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

        # print("尝试遍历并更改")
        
        # 遍历每个字典并更新算法名称
        for dic in array:  # 假设 array 是一个包含字典的列表
            if 'algorithm' in dic:
                original_name = dic['algorithm']
                if original_name in algorithm_mapping:
                    dic['algorithm'] = algorithm_mapping[original_name]

        return array  # 返回整个处理过的数组
    
    # def handle_file_dropped(self, file_path):
    #     print(f"File dropped: {file_path}")
    #     self.file_path = file_path  # 存储文件路径
    
    def submit(self):
        # 获取拖拽文件地址相关信息
        path_info = self.label.return_file_path()
        print(path_info)
        custom_widgets_info = self.get_custom_widgets_info()
        # print("get_custom_widgets_info")
        # print("自定义控件信息:", custom_widgets_info)
        custom_widgets_info2 = self.standardize_algorithm_names(custom_widgets_info)
        right_input_text = self.get_right_input_text()
        # print("Submit button clicked2")
        # print("自定义控件信息:", custom_widgets_info2)
        # print("右侧用户输入内容:", right_input_text)
        self.logger.info(f"{right_input_text}")
        cipher_processor = CipherProcessor(right_input_text, custom_widgets_info2)
        # print("custom_widgets_info2", custom_widgets_info2)
        result = cipher_processor.process()
        if isinstance(result, dict):
            result = json.dumps(result, ensure_ascii=False)
            self.logger.warning(f"{result}")
        elif isinstance(result, tuple):
            result = json.dumps(result, ensure_ascii=False)
            self.logger.info(f"{result}")
        else:
            self.logger.info(f"result: {result}")
        if isinstance(result, list):
            result = json.dumps(result, ensure_ascii=False)
        self.text_edit_output.setPlainText(result)