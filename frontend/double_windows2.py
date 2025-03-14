import random
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QLineEdit, QScrollArea, QPushButton, QTextEdit
from PyQt5.QtCore import Qt
from PyQt5.QtCore import pyqtSignal
import traceback
from .single_scroll_area_widget import ScrollAreaWidget
from .single_drop_drag_label import DraggableLabel, DropLabel
from .single_draggable_widget import DraggableWidget
from .double_history_widget import CustomHistoryWidget
import os
import sys
import threading 

import socket

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# 将项目根目录添加到 sys.path
sys.path.append(project_root)
from backend.client import send_once
from backend.server import receive_once
from backend.network import NetworkHandler
from .log_msg import setup_logger
import random

class Window2(QWidget):
    data_received = pyqtSignal(str)  # 定义一个信号，传递字符串数据
    data_error = pyqtSignal(dict)    # 定义一个信号，传递错误信息
    addr_received = pyqtSignal(tuple)

    def __init__(self, switch_window_callback):
        super().__init__()
        self.logger = setup_logger("double_windows")
        self.switch_window = switch_window_callback
        self.initUI()
        self.port = 12345
        self.start_receive_thread('0.0.0.0', self.port)
        self.data_received.connect(self.handle_data_received)  # 连接信号到槽函数
        self.data_error.connect(self.handle_data_received)
        self.addr_received.connect(self.handle_addr_received)
        # 设置一些默认值（用户应该按照业务配置）
        self.ip_edit.setText("127.0.0.1")
        self.port_edit.setText("12345")

    def handle_addr_received(self, addr):
        ip, port = addr
        self.ip_edit.setText(ip)
        self.port_edit.setText(str(port))

    def handle_data_received(self, data):
        if isinstance(data, dict) and 'error_code' in data and 'error_message' in data:
            self.show_popup_message(f"Error: {data['error_message']}")
        else:
            print("Received data:", data)
            self.add_new_widget2(data, "type2")
    
    def initUI(self):
        self.setWindowTitle('Integrated Drag and Drop Example')
        self.setFixedSize(1920, 1200)  # 固定窗口大小

        main_layout = QHBoxLayout()

        # 左侧布局（移除了解密相关代码）
        left_layout = QVBoxLayout()
        horizontal_layout = QHBoxLayout()
        left_label = QLabel('Double Machine', self)
        left_label.setStyleSheet("background-color: lightblue; padding: 20px;")
        horizontal_layout.addWidget(left_label)

        # 创建一个 QLabel
        right_button = QPushButton('Change Mode', self)
        right_button.setStyleSheet("""
            padding: 20px;

        """)
        right_button.clicked.connect(lambda: self.switch_window(0))
        # right_label = QLabel('Change Mode', self)
        # right_label.setStyleSheet("""
        #     background-color: lightblue;
        #     padding: 20px;

        # """)
        
        # right_label.mousePressEvent = self.on_left_label_click
        # right_label.mouseGrabber = self.on_left_label_movein
        
        horizontal_layout.addWidget(right_button)
        left_layout.addLayout(horizontal_layout)

        self.search_input = QLineEdit(self)
        self.search_input.setPlaceholderText("Type here to search……")
        self.search_input.textChanged.connect(self.update_search_results)
        left_layout.addWidget(self.search_input)

        self.scroll_areas = {
            'Encryption': self.create_scroll_area()
        }

        for category, (scroll_area, _, _) in self.scroll_areas.items():
            left_layout.addWidget(QLabel(f"{category} Modes:"))
            left_layout.addWidget(scroll_area)

        main_layout.addLayout(left_layout, 2)

        # 中间布局（替换为包含输入接收方IP和端口号的控件布局）
        middle_layout = QVBoxLayout()
        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_widget = ScrollAreaWidget(self.scroll_area)
        self.scroll_area.setWidget(self.scroll_widget)

        # 创建接收方IP输入相关布局
        ip_port_layout = QVBoxLayout()
        ip_label = QLabel("接收方IP:", self)
        self.ip_edit = QLineEdit(self)
        self.ip_edit.setPlaceholderText("请输入接收方IP地址")
        port_label = QLabel("端口号:", self)
        self.port_edit = QLineEdit(self)
        self.port_edit.setPlaceholderText("请输入端口号")
        ip_port_layout.addWidget(ip_label)
        ip_port_layout.addWidget(self.ip_edit)
        ip_port_layout.addWidget(port_label)
        ip_port_layout.addWidget(self.port_edit)

        middle_layout.addLayout(ip_port_layout)
        middle_layout.addWidget(self.scroll_area)

        add_button = QPushButton('Start', self)
        add_button.clicked.connect(self.submit)
        middle_layout.addWidget(add_button)
        main_layout.addLayout(middle_layout, 3)

        # 右侧布局修改
        right_layout = QVBoxLayout()

        # 创建水平布局放置两个输入框
        right_input_layout = QHBoxLayout()
        self.label = DropLabel(self)
        self.label.setFixedHeight(100)
        right_layout.addWidget(self.label)

        self.text_edit_input = QTextEdit(self)
        self.text_edit_input.setPlaceholderText("请在这里输入想要加密的文本，如果是拖入的文件，将会在此处显示16进制内容……")
        right_input_layout.addWidget(self.text_edit_input)

        self.text_edit_output = QTextEdit(self)
        self.text_edit_output.setReadOnly(True)
        self.text_edit_output.setPlaceholderText("加密后的结果将会显示在这里……")
        right_input_layout.addWidget(self.text_edit_output)

        right_layout.addLayout(right_input_layout)

        # 添加用于记录发送和接收原文内容的 QScrollArea
        self.history_scroll_area = QScrollArea(self)
        self.history_scroll_area.setWidgetResizable(True)
        self.history_content_widget = QWidget()
        self.history_layout = QVBoxLayout(self.history_content_widget)
        self.history_layout.setAlignment(Qt.AlignTop)  # 设置此布局内的内容为顶部对齐
        self.history_scroll_area.setWidget(self.history_content_widget)
        right_layout.addWidget(self.history_scroll_area)

        main_layout.addLayout(right_layout, 5)

        self.setLayout(main_layout)

        self.scroll_area.setAcceptDrops(True)
        self.scroll_area.dragEnterEvent = self.dragEnterEvent
        self.scroll_area.dragMoveEvent = self.dragMoveEvent
        self.scroll_area.dropEvent = self.dropEvent

        # 初始化标签（只保留加密和转换相关的标签）
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
                'RC4',
                'CA',
                'DES',
                'AES',
                'RSA',
                'ECC'
            ]
        }

        self.update_search_results()

    def on_left_label_click(self, event):
        print("Left label clicked!")
        self.switch_window(0)

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
            self.add_new_widget(text)
            event.acceptProposedAction()

    def read_file_hex(self, file_path):
        try:
            with open(file_path, 'rb') as file:
                content = file.read()
                hex_content = content.hex()
                self.text_edit_input.setPlainText(hex_content)
        except Exception as e:
            self.text_edit_output.setPlainText(f"Error reading file: {e}")

    def update_hex_content(self):
        input_text = self.text_edit_input.toPlainText()
        hex_content = input_text.encode('utf-8').hex()
    def get_custom_widgets_info(self):
        if not self.scroll_widget or not self.scroll_widget.layout:
            print("Error: self.scroll_widget or its layout is None or not initialized.")
            return []

        widgets_info = []
        for index, widget in enumerate(self.scroll_widget.get_widgets_in_order()):
            if isinstance(widget, DraggableWidget):
                try:
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
        widget_to_add = DraggableWidget(text, self.scroll_widget, self.scroll_area)
        self.scroll_widget.layout.addWidget(widget_to_add)
        self.scroll_widget.update_child_widths()
    
    def add_new_widget2(self, text, widget_type):
        widget_to_add = CustomHistoryWidget(text, widget_type)
        self.history_layout.addWidget(widget_to_add)
        self.history_layout.setSpacing(10)  
        self.history_content_widget.updateGeometry()  

    def show_popup_message(self, message):
        """
        弹出包含指定消息内容的弹窗

        参数:
        message (str): 要在弹窗中显示的消息内容
        """
        from PyQt5.QtWidgets import QMessageBox
        msg_box = QMessageBox()
        msg_box.setText(message)
        msg_box.exec_()
    def submit(self):
        try:
            IPinfo = self.ip_edit.text()
            PortInfo = self.port_edit.text()
            right_input_text = self.get_right_input_text()
            custom_widgets_info = self.get_custom_widgets_info()
            self.logger.info(f"Sending to {IPinfo}:{PortInfo}, alogorithm: {custom_widgets_info}")
            error = send_once(self.port, IPinfo, int(PortInfo), right_input_text.encode(), custom_widgets_info)
            if isinstance(error, dict) and 'error_code' in error and 'error_message' in error:
                self.logger.warning(f"Error: {error['error_message']}")
                self.show_popup_message(f"Error: {error['error_message']}")
            elif isinstance(error, bytes) or isinstance(error, bytearray):
                self.logger.info(f"Send success: {right_input_text}, encrypted: {error}")
                self.add_new_widget2(right_input_text, "type1")
                self.text_edit_output.setPlainText(str(error))
            else:
                self.logger.error(f"Error: {error}")
                self.show_popup_message(f"Error: {error}")
        except Exception as e:
            self.logger.error(str(e))
            self.show_popup_message(str(e))

    def receive_thread(self, ip, port):
        while True:
            # 接受连接
            network_handler = NetworkHandler(ip, port)
            network_handler.socket.listen(1)
            server_socket = network_handler.socket
            client_socket, addr = network_handler.socket.accept()
            network_handler.socket = client_socket
            print(f"Server started on {network_handler.host}:{network_handler.port}")
            print(f"Connected to {addr}")

            ip, _ = addr
            target_port, dec = receive_once(network_handler)
            self.addr_received.emit((ip, target_port))
            self.logger.info(f"Connected to {addr}, Target addr: {ip}:{target_port}")

            if isinstance(dec, dict) :
                self.logger.error(f"Error: {dec['error_message']}")
                self.data_error.emit(dec)
            if isinstance(dec, str):
                self.logger.info(f"Received data: {dec}")
            else:
                try:
                    self.logger.info(f"Received data: {dec.decode()}")
                    self.data_received.emit(dec.decode())  # 发射信号，传递解码后的数据
                except: 
                    self.logger.error(f"Error: {dec}")

            # 关闭连接
            server_socket.close()
            client_socket.close()

    def is_port_in_use(self, port):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            return s.connect_ex(('127.0.0.1', port)) == 0

    def start_receive_thread(self, ip, port):
        while True:
            if self.is_port_in_use(port):
                self.logger.warning(f"Port {port} is already in use. Trying the next port...")
                port += 1
            else:
                break
        
        self.port = port
        self.logger.info(f"Server started on {ip}:{port}, receive thread started on port {port}")
        
        # 创建线程对象并传递 self 作为参数
        self.receive_thread_obj = threading.Thread(target=self.receive_thread, args=(ip, port))
        # 设置线程为守护线程
        self.receive_thread_obj.daemon = True
        # 启动线程
        self.receive_thread_obj.start()
        return self.receive_thread_obj