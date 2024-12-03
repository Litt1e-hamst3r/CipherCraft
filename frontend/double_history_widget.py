from PyQt5.QtWidgets import QSizePolicy, QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QDateTimeEdit, QMessageBox, QDialog, QTextEdit, QFileDialog
from PyQt5.QtCore import Qt, QDateTime
from PyQt5.QtGui import QColor

# 定义文件类型的字典
FILE_TYPES = {
    b'\xFF\xD8\xFF': '.jpg',  # JPEG
    b'\x89\x50\x4E\x47\x0D\x0A\x1A\x0A': '.png',  # PNG
    b'\x47\x49\x46\x38\x39\x61': '.gif',  # GIF
    b'\x42\x4D': '.bmp',  # BMP
    b'\x49\x49\x2A\x00': '.tiff',  # TIFF (Intel byte order)
    b'\x4D\x4D\x00\x2A': '.tiff',  # TIFF (Motorola byte order)
    b'\x50\x4B\x03\x04': '.zip',  # ZIP
    b'\x52\x61\x72\x21\x1A\x07\x00': '.rar',  # RAR
    b'\x1F\x8B\x08': '.gz',  # GZIP
    b'\x4D\x5A': '.exe',  # EXE
    b'\x7F\x45\x4C\x46': '.elf',  # ELF
    b'\x50\x4B\x05\x06': '.zip',  # ZIP (central directory end)
    b'\x50\x4B\x07\x08': '.zip',  # ZIP (data descriptor)
    b'\x52\x61\x72\x21\x1A\x07\x01\x00': '.rar',  # RAR 5
    b'\x25\x50\x44\x46\x2D\x31': '.pdf',  # PDF
    b'\x52\x69\x66\x46': '.wav',  # WAV
    b'\x4F\x67\x67\x53': '.ogg',  # OGG
    b'\x46\x4C\x41\x43': '.flac',  # FLAC
    b'\x41\x52\x43\x48': '.arj',  # ARJ

}

def detect_file_type(hex_data):
    for magic_number, extension in FILE_TYPES.items():
        if hex_data.startswith(magic_number):
            return extension
    return None

class CustomHistoryWidget(QWidget):
    def __init__(self, text, widget_type):
        super().__init__()
        self.text = text
        self.widget_type = widget_type
        self.initUI()
        self.setFixedWidth(860)  # 设置固定宽度为860
        self.setFixedHeight(150)

    def initUI(self):
        main_layout = QHBoxLayout()  # 使用水平布局作为主布局

        # 创建左侧的垂直布局，用于显示文本
        left_layout = QVBoxLayout()
        left_layout.setContentsMargins(0, 0, 0, 0)  # 移除边距
        left_layout.setSpacing(0)  # 移除间距

        # 显示前100个字节内容的标签，设置为可点击并关联点击事件
        truncated_text = self.text[:50] if len(self.text) > 50 else self.text
        self.text_label = QLabel(truncated_text + "...")
        self.text_label.setCursor(Qt.PointingHandCursor)  # 设置鼠标指针样式为手型，表示可点击
        self.text_label.mousePressEvent = self.show_full_text  # 绑定点击事件到显示全部内容的方法
        self.text_label.setStyleSheet("border: 0; padding: 5px;")  # 去掉边框并添加内边距
        self.text_label.setWordWrap(True)  # 启用自动换行
        self.text_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)  # 设置大小策略
        left_layout.addWidget(self.text_label)

        # 根据类型设置背景颜色
        if self.widget_type == "type1":
            self.setStyleSheet("background-color: lightgray;")
            # 将删除按钮和时间标签放在左边
            right_layout = QVBoxLayout()
            right_layout.setContentsMargins(0, 0, 0, 0)  # 移除边距
            right_layout.setSpacing(0)  # 移除间距

            # 创建删除按钮
            delete_button = QPushButton("删除")
            delete_button.clicked.connect(self.delete_widget)
            delete_button.setStyleSheet("background-color: rgba(255, 255, 255, 0); padding: 5px;")  # 设置背景颜色为透明
            right_layout.addWidget(delete_button)

            # 显示创建时间的标签
            creation_time = QDateTime.currentDateTime()
            time_label = QLabel(f"{creation_time.toString('MM-dd hh:mm')}")
            time_label.setAlignment(Qt.AlignCenter)  # 居中对齐
            time_label.setStyleSheet("background-color: rgba(255, 255, 255, 0); padding: 5px;")  # 设置背景颜色为透明
            right_layout.addWidget(time_label)

            # 将左右布局添加到主布局中
            main_layout.addLayout(right_layout, 1)  # 右侧布局占10%
            main_layout.addLayout(left_layout, 9)  # 左侧布局占90%

        elif self.widget_type == "type2":
            self.setStyleSheet("background-color: lightyellow;")
            # 将删除按钮和时间标签放在右边
            right_layout = QVBoxLayout()
            right_layout.setContentsMargins(0, 0, 0, 0)  # 移除边距
            right_layout.setSpacing(0)  # 移除间距

            # 创建删除按钮
            delete_button = QPushButton("删除")
            delete_button.clicked.connect(self.delete_widget)
            delete_button.setStyleSheet("background-color: rgba(255, 255, 255, 0); padding: 5px;")  # 设置背景颜色为透明
            right_layout.addWidget(delete_button)

            # 显示创建时间的标签
            creation_time = QDateTime.currentDateTime()
            time_label = QLabel(f"{creation_time.toString('MM-dd hh:mm')}")
            time_label.setAlignment(Qt.AlignCenter)  # 居中对齐
            time_label.setStyleSheet("background-color: rgba(255, 255, 255, 0); padding: 5px;")  # 设置背景颜色为透明
            right_layout.addWidget(time_label)

            # 将左右布局添加到主布局中
            main_layout.addLayout(left_layout, 9)  # 左侧布局占90%
            main_layout.addLayout(right_layout, 1)  # 右侧布局占10%

        else:
            self.setStyleSheet("background-color: lightblue;")
            # 默认情况下，将删除按钮和时间标签放在右边
            right_layout = QVBoxLayout()
            right_layout.setContentsMargins(0, 0, 0, 0)  # 移除边距
            right_layout.setSpacing(0)  # 移除间距

            # 创建删除按钮
            delete_button = QPushButton("删除")
            delete_button.clicked.connect(self.delete_widget)
            delete_button.setStyleSheet("background-color: rgba(255, 255, 255, 0); padding: 5px;")  # 设置背景颜色为透明
            right_layout.addWidget(delete_button)

            # 显示创建时间的标签
            creation_time = QDateTime.currentDateTime()
            time_label = QLabel(f"{creation_time.toString('MM-dd hh:mm')}")
            time_label.setAlignment(Qt.AlignCenter)  # 居中对齐
            time_label.setStyleSheet("background-color: rgba(255, 255, 255, 0); padding: 5px;")  # 设置背景颜色为透明
            right_layout.addWidget(time_label)

            # 将左右布局添加到主布局中
            main_layout.addLayout(left_layout, 9)  # 左侧布局占90%
            main_layout.addLayout(right_layout, 1)  # 右侧布局占10%

        self.setLayout(main_layout)

    def show_full_text(self, event):
        # 这里只处理鼠标左键点击事件
        if event.button() == Qt.LeftButton:
            self.show_text_in_new_window()

    def show_text_in_new_window(self):
        # 创建一个新的对话框
        dialog = QDialog(self)
        dialog.setWindowTitle("完整文本")
        dialog.setFixedSize(800, 600)  # 设置对话框大小
        dialog.setStyleSheet("background-color: white;")  # 设置对话框背景颜色为白色

        # 创建一个 QTextEdit 控件来显示完整文本
        text_edit = QTextEdit(dialog)
        text_edit.setPlainText(self.text)
        text_edit.setReadOnly(True)  # 设置为只读
        text_edit.setStyleSheet("background-color: white; color: black; border: 1px solid #ccc; padding: 5px;")  # 设置 QTextEdit 背景颜色为白色，文字颜色为黑色，并添加边框和内边距

        # 创建一个按钮来保存文本
        save_button = QPushButton("保存为二进制文件")
        save_button.clicked.connect(lambda: self.save_text_as_binary_file(text_edit.toPlainText()))

        # 创建布局并将 QTextEdit 和按钮添加到对话框中
        layout = QVBoxLayout(dialog)
        layout.addWidget(text_edit)
        layout.addWidget(save_button)

        # 显示对话框
        dialog.exec_()

    def save_text_as_binary_file(self, text):
        try:
            # 将16进制文本转换为字节
            hex_text = text.strip()
            byte_array = bytes.fromhex(hex_text)

            # 检测文件类型并添加相应的扩展名
            file_extension = detect_file_type(byte_array)
            default_file_name = "untitled"
            if file_extension:
                default_file_name += file_extension

            # 弹出文件保存对话框
            file_name, _ = QFileDialog.getSaveFileName(self, "保存文件", default_file_name, "All Files (*)")

            if file_name:
                # 如果用户没有输入扩展名且检测到了扩展名，则添加扩展名
                if file_extension and not file_name.endswith(file_extension):
                    file_name += file_extension

                # 保存到文件
                with open(file_name, 'wb') as file:
                    file.write(byte_array)
                QMessageBox.information(self, "保存成功", f"文件已保存到 {file_name}")
        except Exception as e:
            QMessageBox.critical(self, "保存失败", f"保存文件时出错: {str(e)}")

    def delete_widget(self):
        # 获取父布局，从父布局中移除自身
        parent_layout = self.parentWidget().layout()
        if parent_layout:
            parent_layout.removeWidget(self)
            self.deleteLater()