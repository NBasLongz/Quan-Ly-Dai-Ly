# frontend/ui/controllers/loai_daily_controller.py
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QWidget, QTableWidgetItem, QMessageBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from decimal import Decimal

from frontend.api_client import DjangoAPIClient, APIError
from frontend.utils.helpers import AlertHelper, IconManager
from frontend.utils.validators import ValidationHelper


class LoaiDaiLyController(QWidget):
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
        title_label = QtWidgets.QLabel("QUẢN LÝ LOẠI ĐẠI LÝ")
        title_label.setStyleSheet("font-size: 24px; font-weight: bold;")
        layout.addWidget(title_label, alignment=Qt.AlignCenter)

        # Create form and table layout
        content_layout = QtWidgets.QHBoxLayout()

        # Form panel
        form_panel = QtWidgets.QGroupBox("THÔNG TIN LOẠI ĐẠI LÝ")
        form_layout = QtWidgets.QFormLayout(form_panel)

        # Form fields
        self.txt_ma_loai = QtWidgets.QLineEdit()
        self.txt_ma_loai.setEnabled(False)
        form_layout.addRow("Mã loại:", self.txt_ma_loai)

        self.txt_ten_loai = QtWidgets.QLineEdit()
        form_layout.addRow("Tên loại:", self.txt_ten_loai)

        self.txt_no_toi_da = QtWidgets.QLineEdit()
        form_layout.addRow("Nợ tối đa:", self.txt_no_toi_da)

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
        table_panel = QtWidgets.QGroupBox("DANH SÁCH LOẠI ĐẠI LÝ")
        table_layout = QtWidgets.QVBoxLayout(table_panel)

        # Table
        self.table_loai = QtWidgets.QTableWidget()
        self.table_loai.setColumnCount(4)
        self.table_loai.setHorizontalHeaderLabels(["Mã loại", "Tên loại", "Nợ tối đa", "Số đại lý"])
        self.table_loai.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.table_loai.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)

        table_layout.addWidget(self.table_loai)

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
        self.table_loai.itemSelectionChanged.connect(self.on_table_selection_changed)

    def refresh_table_data(self):
        try:
            loai_list = self.api_client.get_all_loaidaily()
            self.populate_table(loai_list)
        except APIError as e:
            AlertHelper.show_api_error(self, e, "Lỗi tải dữ liệu")

    def populate_table(self, loai_list):
        self.table_loai.setRowCount(0)
        for i, loai in enumerate(loai_list):
            self.table_loai.insertRow(i)
            self.table_loai.setItem(i, 0, QTableWidgetItem(str(loai['id'])))
            self.table_loai.setItem(i, 1, QTableWidgetItem(loai['ten_loai_dai_ly']))
            self.table_loai.setItem(i, 2, QTableWidgetItem(f"{loai['no_toi_da']:,.0f}"))
            self.table_loai.setItem(i, 3, QTableWidgetItem(str(loai['so_dai_ly'])))

        # Auto adjust column widths
        self.table_loai.resizeColumnsToContents()

    def on_table_selection_changed(self):
        # Get selected row
        selected_rows = self.table_loai.selectedItems()
        if not selected_rows:
            return

        # Get row index
        row = selected_rows[0].row()

        # Get data from the row
        ma_loai = self.table_loai.item(row, 0).text()
        ten_loai = self.table_loai.item(row, 1).text()
        no_toi_da = self.table_loai.item(row, 2).text().replace(',', '')

        # Set data to form fields
        self.txt_ma_loai.setText(ma_loai)
        self.txt_ten_loai.setText(ten_loai)
        self.txt_no_toi_da.setText(no_toi_da)

        # Enable/disable buttons
        self.btn_them.setEnabled(False)
        self.btn_sua.setEnabled(True)
        self.btn_xoa.setEnabled(True)

    def handle_them_button(self):
        # Validate input
        error = self.validate_input()
        if error:
            AlertHelper.show_error_alert(self, "Lỗi", error)
            return

        # Get form data
        ten_loai = self.txt_ten_loai.text().strip()
        no_toi_da = Decimal(self.txt_no_toi_da.text().strip().replace(',', ''))

        try:
            # Add new distributor type
            result = self.api_client.add_loaidaily(ten_loai, no_toi_da)

            AlertHelper.show_success_alert(self, "Thành công", "Thêm loại đại lý mới thành công!")
            self.refresh_table_data()
            self.reset_form()
        except APIError as e:
            AlertHelper.show_api_error(self, e, "Lỗi thêm loại đại lý")

    def handle_sua_button(self):
        # Check if distributor type is selected
        if not self.txt_ma_loai.text():
            AlertHelper.show_error_alert(self, "Lỗi", "Vui lòng chọn loại đại lý cần sửa!")
            return

        # Validate input
        error = self.validate_input()
        if error:
            AlertHelper.show_error_alert(self, "Lỗi", error)
            return

        # Get form data
        ma_loai = int(self.txt_ma_loai.text())
        ten_loai = self.txt_ten_loai.text().strip()
        no_toi_da = Decimal(self.txt_no_toi_da.text().strip().replace(',', ''))

        try:
            # Update distributor type
            result = self.api_client.update_loaidaily(ma_loai, ten_loai, no_toi_da)

            AlertHelper.show_success_alert(self, "Thành công", "Cập nhật loại đại lý thành công!")
            self.refresh_table_data()
            self.reset_form()
        except APIError as e:
            AlertHelper.show_api_error(self, e, "Lỗi cập nhật loại đại lý")

    def handle_xoa_button(self):
        # Check if distributor type is selected
        if not self.txt_ma_loai.text():
            AlertHelper.show_error_alert(self, "Lỗi", "Vui lòng chọn loại đại lý cần xóa!")
            return

        # Confirm deletion
        confirmed = AlertHelper.show_confirmation_dialog(
            self, "Xác nhận", "Bạn có chắc chắn muốn xóa loại đại lý này không?"
        )

        if not confirmed:
            return

        # Get distributor type ID
        ma_loai = int(self.txt_ma_loai.text())

        try:
            # Delete distributor type
            self.api_client.delete_loaidaily(ma_loai)

            AlertHelper.show_success_alert(self, "Thành công", "Xóa loại đại lý thành công!")
            self.refresh_table_data()
            self.reset_form()
        except APIError as e:
            AlertHelper.show_api_error(self, e, "Lỗi xóa loại đại lý")

            # Kiểm tra nếu lỗi liên quan đến đại lý đang sử dụng
            if "đang được sử dụng" in str(e):
                AlertHelper.show_error_alert(
                    self, "Lỗi",
                    "Không thể xóa loại đại lý này vì đang có đại lý thuộc loại này."
                )

    def handle_lam_moi_button(self):
        self.reset_form()
        self.refresh_table_data()

    def reset_form(self):
        # Clear form fields
        self.txt_ma_loai.clear()
        self.txt_ten_loai.clear()
        self.txt_no_toi_da.clear()

        # Reset button states
        self.btn_them.setEnabled(True)
        self.btn_sua.setEnabled(False)
        self.btn_xoa.setEnabled(False)

        # Clear table selection
        self.table_loai.clearSelection()

    def validate_input(self):
        # Get form data
        ten_loai = self.txt_ten_loai.text().strip()
        no_toi_da = self.txt_no_toi_da.text().strip()

        # Validate required fields
        ten_error = ValidationHelper.validate_required(ten_loai, "Tên loại đại lý")
        if ten_error:
            return ten_error

        # Validate maximum debt
        no_error = ValidationHelper.validate_positive_decimal(no_toi_da, "Nợ tối đa")
        if no_error:
            return no_error

        return None