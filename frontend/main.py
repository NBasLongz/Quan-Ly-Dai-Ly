#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Quản lý Đại Lý - Distributor Management System (Frontend)
"""
import sys
import os
from PyQt5.QtWidgets import QApplication


def main():
    # Thêm thư mục gốc vào PATH
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if project_root not in sys.path:
        sys.path.insert(0, project_root)

    # Thiết lập thư mục icons
    icons_path = os.path.join(project_root, 'shared', 'icons')
    os.environ['ICONS_PATH'] = icons_path

    # Import MainWindow ở đây để tránh circular import
    from frontend.ui.controllers.main_controller import MainWindow

    # Tạo ứng dụng
    app = QApplication(sys.argv)

    # Tạo và hiển thị cửa sổ chính
    window = MainWindow()
    window.show()

    # Chạy ứng dụng
    return app.exec_()


if __name__ == "__main__":
    sys.exit(main())