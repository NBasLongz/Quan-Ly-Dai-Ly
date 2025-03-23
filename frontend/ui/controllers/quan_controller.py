# frontend/ui/controllers/quan_controller.py
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QWidget, QTableWidgetItem, QMessageBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon

from frontend.api_client import DjangoAPIClient, APIError
from frontend.utils.helpers import AlertHelper, IconManager
from frontend.utils.validators import ValidationHelper


class QuanController(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        # Initialize API client
        self.api_client = DjangoAPIClient()

        # Setup UI
        self.setup_ui()

        # Connect signals to slots
        self.connect_signals()

        # Load initial data
        self.refresh_table_data()

    def setup_ui(self):
        # Create main layout
        layout = QtWidgets.QVBoxLayout(self)

        # Page title
        title_label = QtWidgets.QLabel("QUẢN LÝ QUẬN")
        title_label.setStyleSheet("font-size: 24px; font-weight: bold;")
        layout.addWidget(title_label, alignment=Qt.AlignCenter)

        # Create form and table layout
        content_layout = QtWidgets.QHBoxLayout()

        # Form panel
        form_panel = QtWidgets.QGroupBox("THÔNG TIN QUẬN")
        form_layout = QtWidgets.QFormLayout(form_panel)

        # Form fields
        self.txt_ma_quan = QtWidgets.QLineEdit()
        self.txt_ma_quan.setEnabled(False)
        form_layout.addRow("Mã quận:", self.txt_ma_quan)

        self.txt_ten_quan = QtWidgets.QLineEdit()
        form_layout.addRow("Tên quận:", self.txt_ten_quan)

        # Action buttons
        btn_layout = QtWidgets.QHBoxLayout()

        self.btn_them = QtWidgets.QPushButton("Thêm")
        self.btn_them.setIcon(IconManager.get_icon("add"))
        self.btn_them.setStyleSheet("background-color: #3498db; color: white;")
        btn_layout.addWidget(self.btn_them)

        self.btn_sua = QtWidgets.QPushButton("Sửa")
        self.btn_sua.setIcon(IconManager.get_icon("edit"))
        self.btn_sua.setStyleSheet("background-color: #f39c12; color: white;")
        self.btn_sua.setEnabled(False)
        btn_layout.addWidget(self.btn_sua)

        self.btn_xoa = QtWidgets.QPushButton("Xóa")
        self.btn_xoa.setIcon(IconManager.get_icon("delete"))
        self.btn_xoa.setStyleSheet("background-color: #e74c3c; color: white;")
        self.btn_xoa.setEnabled(False)
        btn_layout.addWidget(self.btn_xoa)

        self.btn_lam_moi = QtWidgets.QPushButton("Làm mới")
        self.btn_lam_moi.setIcon(IconManager.get_icon("refresh"))
        self.btn_lam_moi.setStyleSheet("background-color: #9b59b6; color: white;")
        btn_layout.addWidget(self.btn_lam_moi)

        form_layout.addRow("", btn_layout)

        # Table panel
        table_panel = QtWidgets.QGroupBox("DANH SÁCH QUẬN")
        table_layout = QtWidgets.QVBoxLayout(table_panel)

        # Table
        self.table_quan = QtWidgets.QTableWidget()
        self.table_quan.setColumnCount(3)
        self.table_quan.setHorizontalHeaderLabels(["Mã quận", "Tên quận", "Số đại lý"])
        self.table_quan.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.table_quan.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)

        table_layout.addWidget(self.table_quan)

        # Add panels to content layout
        content_layout.addWidget(form_panel, 1)
        content_layout.addWidget(table_panel, 2)

        # Add content layout to main layout
        layout.addLayout(content_layout)

    def connect_signals(self):
        # Connect buttons to their handlers
        self.btn_them.clicked.connect(self.handle_them_button)
        self.btn_sua.clicked.connect(self.handle_sua_button)
        self.btn_xoa.clicked.connect(self.handle_xoa_button)
        self.btn_lam_moi.clicked.connect(self.handle_lam_moi_button)

        # Connect table selection change
        self.table_quan.itemSelectionChanged.connect(self.on_table_selection_changed)

    def refresh_table_data(self):
        try:
            quan_list = self.api_client.get_all_quan()
            self.populate_table(quan_list)
        except APIError as e:
            AlertHelper.show_api_error(self, e, "Lỗi tải dữ liệu")

    def populate_table(self, quan_list):
        self.table_quan.setRowCount(0)
        for i, quan in enumerate(quan_list):
            self.table_quan.insertRow(i)
            self.table_quan.setItem(i, 0, QTableWidgetItem(str(quan['id'])))
            self.table_quan.setItem(i, 1, QTableWidgetItem(quan['ten_quan']))
            self.table_quan.setItem(i, 2, QTableWidgetItem(str(quan['so_dai_ly'])))

        # Auto adjust column widths
        self.table_quan.resizeColumnsToContents()

    def on_table_selection_changed(self):
        # Get selected row
        selected_rows = self.table_quan.selectedItems()
        if not selected_rows:
            return

        # Get row index
        row = selected_rows[0].row()

        # Get data from the row
        ma_quan = self.table_quan.item(row, 0).text()
        ten_quan = self.table_quan.item(row, 1).text()

        # Set data to form fields
        self.txt_ma_quan.setText(ma_quan)
        self.txt_ten_quan.setText(ten_quan)

        # Enable/disable buttons
        self.btn_them.setEnabled(False)
        self.btn_sua.setEnabled(True)
        self.btn_xoa.setEnabled(True)

    def handle_them_button(self):
        # Validate input
        ten_quan = self.txt_ten_quan.text().strip()

        error = ValidationHelper.validate_required(ten_quan, "Tên quận")
        if error:
            AlertHelper.show_error_alert(self, "Lỗi", error)
            return

        try:
            # Add new district
            result = self.api_client.add_quan(ten_quan)

            AlertHelper.show_success_alert(self, "Thành công", "Thêm quận mới thành công!")
            self.refresh_table_data()
            self.reset_form()
        except APIError as e:
            AlertHelper.show_api_error(self, e, "Lỗi thêm quận")

    def handle_sua_button(self):
        # Check if district is selected
        if not self.txt_ma_quan.text():
            AlertHelper.show_error_alert(self, "Lỗi", "Vui lòng chọn quận cần sửa!")
            return

        # Validate input
        ten_quan = self.txt_ten_quan.text().strip()

        error = ValidationHelper.validate_required(ten_quan, "Tên quận")
        if error:
            AlertHelper.show_error_alert(self, "Lỗi", error)
            return

        # Get district ID
        ma_quan = int(self.txt_ma_quan.text())

        try:
            # Update district
            result = self.api_client.update_quan(ma_quan, ten_quan)

            AlertHelper.show_success_alert(self, "Thành công", "Cập nhật quận thành công!")
            self.refresh_table_data()
            self.reset_form()
        except APIError as e:
            AlertHelper.show_api_error(self, e, "Lỗi cập nhật quận")

    def handle_xoa_button(self):
        # Check if district is selected
        if not self.txt_ma_quan.text():
            AlertHelper.show_error_alert(self, "Lỗi", "Vui lòng chọn quận cần xóa!")
            return

        # Confirm deletion
        confirmed = AlertHelper.show_confirmation_dialog(
            self, "Xác nhận", "Bạn có chắc chắn muốn xóa quận này không?"
        )

        if not confirmed:
            return

        # Get district ID
        ma_quan = int(self.txt_ma_quan.text())

        try:
            # Delete district
            self.api_client.delete_quan(ma_quan)

            AlertHelper.show_success_alert(self, "Thành công", "Xóa quận thành công!")
            self.refresh_table_data()
            self.reset_form()
        except APIError as e:
            AlertHelper.show_api_error(self, e, "Lỗi xóa quận")

    def handle_lam_moi_button(self):
        self.reset_form()
        self.refresh_table_data()

    def reset_form(self):
        # Clear form fields
        self.txt_ma_quan.clear()
        self.txt_ten_quan.clear()

        # Reset button states
        self.btn_them.setEnabled(True)
        self.btn_sua.setEnabled(False)
        self.btn_xoa.setEnabled(False)

        # Clear table selection
        self.table_quan.clearSelection()