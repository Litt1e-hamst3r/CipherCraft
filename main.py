import os
import sys
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# 将项目根目录添加到 sys.path
sys.path.append(project_root)
from frontend import init_and_main_windows as ui_main

if __name__ == "__main__":
    ui_main.run()