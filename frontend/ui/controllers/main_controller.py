# frontend/ui/controllers/main_controller.py
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
import os

from frontend.ui.controllers.daily_controller import DaiLyController
from frontend.ui.controllers.quan_controller import QuanController
from frontend.ui.controllers.loai_daily_controller import LoaiDaiLyController
from frontend.utils.helpers import IconManager


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Setup UI
        self.setWindowTitle("Phần mềm Quản lý Đại lý")
        self.setMinimumSize(1024, 680)
        self.resize(1280, 720)

        # Set app icon
        app_icon = IconManager.get_icon("distributor")
        if not app_icon.isNull():
            self.setWindowIcon(app_icon)

        # Create layout
        self.central_widget = QtWidgets.QWidget()
        self.setCentralWidget(self.central_widget)

        # Main layout
        self.main_layout = QtWidgets.QHBoxLayout(self.central_widget)

        # Create menu panel
        self.setup_menu_panel()

        # Create content panel
        self.content_panel = QtWidgets.QStackedWidget()
        self.main_layout.addWidget(self.content_panel, 4)

        # Create controllers
        self.daily_controller = DaiLyController()
        self.quan_controller = QuanController()
        self.loai_daily_controller = LoaiDaiLyController()

        # Add controllers to content panel
        self.content_panel.addWidget(self.daily_controller)
        self.content_panel.addWidget(self.quan_controller)
        self.content_panel.addWidget(self.loai_daily_controller)

        # Show daily view by default
        self.set_active_button(self.btn_daily)

    def setup_menu_panel(self):
        # Menu panel
        menu_panel = QtWidgets.QWidget()
        menu_panel.setMinimumWidth(250)
        menu_panel.setMaximumWidth(250)
        menu_panel.setStyleSheet("background-color: #2c3e50;")

        menu_layout = QtWidgets.QVBoxLayout(menu_panel)
        menu_layout.setContentsMargins(0, 0, 0, 0)
        menu_layout.setSpacing(0)

        # Logo container
        logo_container = QtWidgets.QWidget()
        logo_container.setStyleSheet("background-color: #1a2530; padding: 20px;")
        logo_layout = QtWidgets.QVBoxLayout(logo_container)

        # Logo title
        logo_title = QtWidgets.QLabel("QUẢN LÝ ĐẠI LÝ")
        logo_title.setStyleSheet("color: white; font-size: 20px; font-weight: bold;")
        logo_title.setAlignment(Qt.AlignCenter)
        logo_layout.addWidget(logo_title)

        menu_layout.addWidget(logo_container)

        # Menu buttons
        self.btn_daily = self.create_menu_button("Đại Lý", "distributor")
        self.btn_daily.clicked.connect(self.show_daily_view)
        menu_layout.addWidget(self.btn_daily)

        self.btn_quan = self.create_menu_button("Quận", "district")
        self.btn_quan.clicked.connect(self.show_quan_view)
        menu_layout.addWidget(self.btn_quan)

        self.btn_loai_daily = self.create_menu_button("Loại Đại Lý", "distributor_type")
        self.btn_loai_daily.clicked.connect(self.show_loai_daily_view)
        menu_layout.addWidget(self.btn_loai_daily)

        self.btn_phieunhap = self.create_menu_button("Nhập Hàng", "receipt")
        # self.btn_phieunhap.clicked.connect(self.show_phieunhap_view)
        menu_layout.addWidget(self.btn_phieunhap)

        self.btn_phieuxuat = self.create_menu_button("Xuất Hàng", "issue")
        # self.btn_phieuxuat.clicked.connect(self.show_phieuxuat_view)
        menu_layout.addWidget(self.btn_phieuxuat)

        self.btn_phieuthu = self.create_menu_button("Thu Tiền", "payment")
        # self.btn_phieuthu.clicked.connect(self.show_phieuthu_view)
        menu_layout.addWidget(self.btn_phieuthu)

        self.btn_baocao = self.create_menu_button("Báo Cáo", "report")
        # self.btn_baocao.clicked.connect(self.show_baocao_view)
        menu_layout.addWidget(self.btn_baocao)

        self.btn_quydinh = self.create_menu_button("Quy Định", "regulation")
        # self.btn_quydinh.clicked.connect(self.show_quydinh_view)
        menu_layout.addWidget(self.btn_quydinh)

        # Spacer
        menu_layout.addStretch()

        # Footer
        footer = QtWidgets.QWidget()
        footer.setStyleSheet("background-color: #1a2530; padding: 10px;")
        footer_layout = QtWidgets.QVBoxLayout(footer)

        # API status
        self.api_status_label = QtWidgets.QLabel("API: Đã kết nối")
        self.api_status_label.setStyleSheet("color: #2ecc71;")
        self.api_status_label.setAlignment(Qt.AlignCenter)
        footer_layout.addWidget(self.api_status_label)

        # Footer text
        footer_text = QtWidgets.QLabel("Phần mềm Quản lý Đại lý")
        footer_text.setStyleSheet("color: white;")
        footer_text.setAlignment(Qt.AlignCenter)
        footer_layout.addWidget(footer_text)

        menu_layout.addWidget(footer)

        # Add menu panel to main layout
        self.main_layout.addWidget(menu_panel, 1)

    def create_menu_button(self, text, icon_name=None):
        btn = QtWidgets.QPushButton(text)
        if icon_name:
            btn.setIcon(IconManager.get_icon(icon_name))

        btn.setMinimumHeight(50)
        btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: white;
                font-size: 14px;
                padding: 15px 20px;
                text-align: left;
                border: none;
                border-radius: 0;
            }
            QPushButton:hover {
                background-color: #34495e;
            }
            QPushButton:pressed {
                background-color: #2980b9;
            }
        """)
        return btn

    def set_active_button(self, button):
        # Reset all buttons
        for btn in [self.btn_daily, self.btn_quan, self.btn_loai_daily, self.btn_phieunhap,
                    self.btn_phieuxuat, self.btn_phieuthu, self.btn_baocao, self.btn_quydinh]:
            btn.setStyleSheet("""
                QPushButton {
                    background-color: transparent;
                    color: white;
                    font-size: 14px;
                    padding: 15px 20px;
                    text-align: left;
                    border: none;
                    border-radius: 0;
                }
                QPushButton:hover {
                    background-color: #34495e;
                }
                QPushButton:pressed {
                    background-color: #2980b9;
                }
            """)

        # Set active button
        button.setStyleSheet("""
            QPushButton {
                background-color: #2980b9;
                color: white;
                font-size: 14px;
                padding: 15px 20px;
                text-align: left;
                border: none;
                border-radius: 0;
            }
        """)

    def show_daily_view(self):
        self.set_active_button(self.btn_daily)
        self.content_panel.setCurrentWidget(self.daily_controller)

    def show_quan_view(self):
        self.set_active_button(self.btn_quan)
        self.content_panel.setCurrentWidget(self.quan_controller)

    def show_loai_daily_view(self):
        self.set_active_button(self.btn_loai_daily)
        self.content_panel.setCurrentWidget(self.loai_daily_controller)

    def update_api_status(self, connected=True):
        if connected:
            self.api_status_label.setText("API: Đã kết nối")
            self.api_status_label.setStyleSheet("color: #2ecc71;")
        else:
            self.api_status_label.setText("API: Mất kết nối")
            self.api_status_label.setStyleSheet("color: #e74c3c;")