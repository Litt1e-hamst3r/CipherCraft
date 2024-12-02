from PyQt5.QtWidgets import QLineEdit, QFormLayout, QHBoxLayout, QComboBox
from .single_draggable_widget import DraggableWidget

#下面就是各种自定义的标签了
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
        
class  WidgetTypeK(DraggableWidget):
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
        
class WidgetTypeEccDe(DraggableWidget):
    def __init__(self, text, parent=None, scroll_area=None):
        super().__init__(text, parent, scroll_area)
        self.setFixedSize(300, 240)
        self.label.setText(f"{text}")
        
        # 创建一个表单布局
        form_layout = QFormLayout()
        
        # 创建新的标签和输入框部件
        self.C1x = QLineEdit(self)
        self.C1x.setPlaceholderText("请输入私钥模数n")
        self.C1x.setStyleSheet("QLineEdit { background-color: lightyellow; }")
        form_layout.addRow(self.C1x)
        
        self.C1y = QLineEdit(self)
        self.C1y.setPlaceholderText("请输入私钥模数n")
        self.C1y.setStyleSheet("QLineEdit { background-color: lightyellow; }")
        form_layout.addRow(self.C1y)
        
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
                "private_key":[self.C1x.text(),self.C1y.text(),self.key_edit.text()]
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
        self.name_edit.setPlaceholderText("初始状态，不得为空")
        self.name_edit.setStyleSheet("QLineEdit { background-color: white; }")
        form_layout.addRow(self.name_edit)
        
        self.key_edit = QLineEdit(self)
        self.key_edit.setPlaceholderText("密钥转移规则，不能大于255")
        self.key_edit.setStyleSheet("QLineEdit { background-color: white; }")
        form_layout.addRow(self.key_edit)
        
        self.key_edit2 = QLineEdit(self)
        self.key_edit2.setPlaceholderText("密钥位置，需要小于 len(初始状态)")
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
        self.name_edit.setPlaceholderText("初始状态,不得为空")
        self.name_edit.setStyleSheet("QLineEdit { background-color: lightyellow; }")
        form_layout.addRow(self.name_edit)
        
        self.key_edit = QLineEdit(self)
        self.key_edit.setPlaceholderText("密钥转移规则,不能大于255")
        self.key_edit.setStyleSheet("QLineEdit { background-color: lightyellow; }")
        form_layout.addRow(self.key_edit)
        
        self.key_edit2 = QLineEdit(self)
        self.key_edit2.setPlaceholderText("密钥位置，需要小于 len(初始状态)")
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