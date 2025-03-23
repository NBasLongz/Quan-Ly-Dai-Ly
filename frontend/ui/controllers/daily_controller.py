# frontend/ui/controllers/daily_controller.py
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QWidget, QTableWidgetItem, QMessageBox, QComboBox, QDateEdit, QLineEdit, QPushButton
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtGui import QIcon
from datetime import datetime
from decimal import Decimal

from frontend.api_client import DjangoAPIClient, APIError
from frontend.utils.helpers import AlertHelper, IconManager
from frontend.utils.validators import ValidationHelper


class DaiLyController(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        # Initialize API client
        self.api_client = DjangoAPIClient()

        # Setup UI
        self.setup_ui()

        # Connect signals to slots
        self.connect_signals()

        # Load initial data
        self.load_combobox_data()
        self.refresh_table_data()

    def setup_ui(self):
        # Create main layout
        layout = QtWidgets.QVBoxLayout(self)

        # Page title
        title_label = QtWidgets.QLabel("QUẢN LÝ ĐẠI LÝ")
        title_label.setStyleSheet("font-size: 24px; font-weight: bold;")
        layout.addWidget(title_label, alignment=Qt.AlignCenter)

        # Create form and table layout
        content_layout = QtWidgets.QHBoxLayout()

        # Form panel
        form_panel = QtWidgets.QGroupBox("THÔNG TIN ĐẠI LÝ")
        form_layout = QtWidgets.QFormLayout(form_panel)

        # Form fields
        self.txt_ma_daily = QtWidgets.QLineEdit()
        self.txt_ma_daily.setEnabled(False)
        form_layout.addRow("Mã đại lý:", self.txt_ma_daily)

        self.txt_ten_daily = QtWidgets.QLineEdit()
        form_layout.addRow("Tên đại lý:", self.txt_ten_daily)

        self.txt_dien_thoai = QtWidgets.QLineEdit()
        form_layout.addRow("Điện thoại:", self.txt_dien_thoai)

        self.txt_dia_chi = QtWidgets.QLineEdit()
        form_layout.addRow("Địa chỉ:", self.txt_dia_chi)

        self.txt_email = QtWidgets.QLineEdit()
        form_layout.addRow("Email:", self.txt_email)

        self.cbo_quan = QtWidgets.QComboBox()
        form_layout.addRow("Quận:", self.cbo_quan)
        self.cbo_loai_daily = QtWidgets.QComboBox()
        form_layout.addRow("Loại đại lý:", self.cbo_loai_daily)

        self.dp_ngay_tiep_nhan = QtWidgets.QDateEdit()
        self.dp_ngay_tiep_nhan.setCalendarPopup(True)
        self.dp_ngay_tiep_nhan.setDate(QDate.currentDate())
        self.dp_ngay_tiep_nhan.setEnabled(False)  # Disable as it's auto-set by backend
        form_layout.addRow("Ngày tiếp nhận:", self.dp_ngay_tiep_nhan)

        self.txt_tien_no = QtWidgets.QLineEdit()
        self.txt_tien_no.setEnabled(False)
        self.txt_tien_no.setText("0")
        form_layout.addRow("Tiền nợ:", self.txt_tien_no)

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

        # Right panel for table
        table_panel_widget = QtWidgets.QWidget()
        table_panel_layout = QtWidgets.QVBoxLayout(table_panel_widget)

        # Search layout
        search_layout = QtWidgets.QHBoxLayout()
        self.txt_tim_kiem = QtWidgets.QLineEdit()
        self.txt_tim_kiem.setPlaceholderText("Tìm kiếm đại lý...")
        search_layout.addWidget(self.txt_tim_kiem)

        self.btn_tim_kiem = QtWidgets.QPushButton("Tìm kiếm")
        self.btn_tim_kiem.setIcon(IconManager.get_icon("search"))
        self.btn_tim_kiem.setStyleSheet("background-color: #3498db; color: white;")
        search_layout.addWidget(self.btn_tim_kiem)

        table_panel_layout.addLayout(search_layout)

        # Table
        self.table_daily = QtWidgets.QTableWidget()
        self.table_daily.setColumnCount(9)
        self.table_daily.setHorizontalHeaderLabels([
            "Mã", "Tên đại lý", "Điện thoại", "Địa chỉ", "Quận",
            "Loại đại lý", "Ngày tiếp nhận", "Email", "Tiền nợ"
        ])
        self.table_daily.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.table_daily.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)

        table_panel_layout.addWidget(self.table_daily)

        # Add panels to content layout
        content_layout.addWidget(form_panel, 1)
        content_layout.addWidget(table_panel_widget, 2)

        # Add content layout to main layout
        layout.addLayout(content_layout)

    def connect_signals(self):
        # Connect buttons to their handlers
        self.btn_them.clicked.connect(self.handle_them_button)
        self.btn_sua.clicked.connect(self.handle_sua_button)
        self.btn_xoa.clicked.connect(self.handle_xoa_button)
        self.btn_lam_moi.clicked.connect(self.handle_lam_moi_button)
        self.btn_tim_kiem.clicked.connect(self.handle_tim_kiem_button)

        # Connect table selection change
        self.table_daily.itemSelectionChanged.connect(self.on_table_selection_changed)

    def load_combobox_data(self):
        try:
            # Load Quan data
            quan_list = self.api_client.get_all_quan()
            self.cbo_quan.clear()
            for quan in quan_list:
                self.cbo_quan.addItem(quan['ten_quan'], quan['id'])

            # Load LoaiDaiLy data
            loai_daily_list = self.api_client.get_all_loaidaily()
            self.cbo_loai_daily.clear()
            for loai in loai_daily_list:
                self.cbo_loai_daily.addItem(loai['ten_loai_dai_ly'], loai['id'])
        except APIError as e:
            AlertHelper.show_api_error(self, e, "Lỗi tải dữ liệu")

    def refresh_table_data(self):
        try:
            daily_list = self.api_client.get_all_daily()
            self.populate_table(daily_list)
        except APIError as e:
            AlertHelper.show_api_error(self, e, "Lỗi tải dữ liệu")

    def populate_table(self, daily_list):
        self.table_daily.setRowCount(0)
        for i, daily in enumerate(daily_list):
            self.table_daily.insertRow(i)
            self.table_daily.setItem(i, 0, QTableWidgetItem(str(daily['id'])))
            self.table_daily.setItem(i, 1, QTableWidgetItem(daily['ten_dai_ly']))
            self.table_daily.setItem(i, 2, QTableWidgetItem(daily['dien_thoai']))
            self.table_daily.setItem(i, 3, QTableWidgetItem(daily['dia_chi']))
            self.table_daily.setItem(i, 4, QTableWidgetItem(daily['ten_quan']))
            self.table_daily.setItem(i, 5, QTableWidgetItem(daily['ten_loai_dai_ly']))

            # Format date
            ngay_tiep_nhan = daily['ngay_tiep_nhan']
            date_obj = datetime.strptime(ngay_tiep_nhan, "%Y-%m-%d").date()
            formatted_date = date_obj.strftime("%d/%m/%Y")
            self.table_daily.setItem(i, 6, QTableWidgetItem(formatted_date))

            self.table_daily.setItem(i, 7, QTableWidgetItem(daily['email'] or ""))
            self.table_daily.setItem(i, 8, QTableWidgetItem(f"{daily['tien_no']:,.0f}"))

        # Auto adjust column widths
        self.table_daily.resizeColumnsToContents()

    def on_table_selection_changed(self):
        # Get selected row
        selected_rows = self.table_daily.selectedItems()
        if not selected_rows:
            return

        # Get row index
        row = selected_rows[0].row()

        # Get data from the row
        ma_daily = self.table_daily.item(row, 0).text()
        ten_daily = self.table_daily.item(row, 1).text()
        dien_thoai = self.table_daily.item(row, 2).text()
        dia_chi = self.table_daily.item(row, 3).text()
        quan = self.table_daily.item(row, 4).text()
        loai_daily = self.table_daily.item(row, 5).text()
        ngay_tiep_nhan = self.table_daily.item(row, 6).text()
        email = self.table_daily.item(row, 7).text()
        tien_no = self.table_daily.item(row, 8).text().replace(',', '')

        # Set data to form fields
        self.txt_ma_daily.setText(ma_daily)
        self.txt_ten_daily.setText(ten_daily)
        self.txt_dien_thoai.setText(dien_thoai)
        self.txt_dia_chi.setText(dia_chi)
        self.txt_email.setText(email)

        # Set combo box values
        self.cbo_quan.setCurrentText(quan)
        self.cbo_loai_daily.setCurrentText(loai_daily)

        # Set date
        date_parts = ngay_tiep_nhan.split('/')
        if len(date_parts) == 3:
            qdate = QDate(int(date_parts[2]), int(date_parts[1]), int(date_parts[0]))
            self.dp_ngay_tiep_nhan.setDate(qdate)

        # Set money value
        self.txt_tien_no.setText(tien_no)

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
        ten_daily = self.txt_ten_daily.text().strip()
        dien_thoai = self.txt_dien_thoai.text().strip()
        dia_chi = self.txt_dia_chi.text().strip()
        email = self.txt_email.text().strip() or None
        ma_quan = self.cbo_quan.currentData()
        ma_loai_daily = self.cbo_loai_daily.currentData()

        try:
            # Add new distributor
            result = self.api_client.add_daily(
                ten_daily, dien_thoai, dia_chi, ma_quan, ma_loai_daily, email
            )

            AlertHelper.show_success_alert(self, "Thành công", "Thêm đại lý mới thành công!")
            self.refresh_table_data()
            self.reset_form()
        except APIError as e:
            AlertHelper.show_api_error(self, e, "Lỗi thêm đại lý")

    def handle_sua_button(self):
        # Check if distributor is selected
        if not self.txt_ma_daily.text():
            AlertHelper.show_error_alert(self, "Lỗi", "Vui lòng chọn đại lý cần sửa!")
            return

        # Validate input
        error = self.validate_input()
        if error:
            AlertHelper.show_error_alert(self, "Lỗi", error)
            return

        # Get form data
        ma_daily = int(self.txt_ma_daily.text())
        ten_daily = self.txt_ten_daily.text().strip()
        dien_thoai = self.txt_dien_thoai.text().strip()
        dia_chi = self.txt_dia_chi.text().strip()
        email = self.txt_email.text().strip() or None
        ma_quan = self.cbo_quan.currentData()
        ma_loai_daily = self.cbo_loai_daily.currentData()

        try:
            # Update distributor
            result = self.api_client.update_daily(
                ma_daily, ten_daily, dien_thoai, dia_chi, ma_quan, ma_loai_daily, email
            )

            AlertHelper.show_success_alert(self, "Thành công", "Cập nhật đại lý thành công!")
            self.refresh_table_data()
            self.reset_form()
        except APIError as e:
            AlertHelper.show_api_error(self, e, "Lỗi cập nhật đại lý")

    def handle_xoa_button(self):
        # Check if distributor is selected
        if not self.txt_ma_daily.text():
            AlertHelper.show_error_alert(self, "Lỗi", "Vui lòng chọn đại lý cần xóa!")
            return

        # Confirm deletion
        confirmed = AlertHelper.show_confirmation_dialog(
            self, "Xác nhận", "Bạn có chắc chắn muốn xóa đại lý này không?"
        )

        if not confirmed:
            return

        # Get distributor ID
        ma_daily = int(self.txt_ma_daily.text())

        try:
            # Delete distributor
            self.api_client.delete_daily(ma_daily)

            AlertHelper.show_success_alert(self, "Thành công", "Xóa đại lý thành công!")
            self.refresh_table_data()
            self.reset_form()
        except APIError as e:
            AlertHelper.show_api_error(self, e, "Lỗi xóa đại lý")

    def handle_lam_moi_button(self):
        self.reset_form()
        self.refresh_table_data()

    def handle_tim_kiem_button(self):
        keyword = self.txt_tim_kiem.text().strip()

        if not keyword:
            self.refresh_table_data()
            return

        try:
            # Search distributors
            daily_list = self.api_client.search_daily(keyword)
            self.populate_table(daily_list)

            if not daily_list:
                AlertHelper.show_information_alert(
                    self, "Thông báo", f"Không tìm thấy đại lý phù hợp với từ khóa: {keyword}"
                )
        except APIError as e:
            AlertHelper.show_api_error(self, e, "Lỗi tìm kiếm")

    def reset_form(self):
        # Clear form fields
        self.txt_ma_daily.clear()
        self.txt_ten_daily.clear()
        self.txt_dien_thoai.clear()
        self.txt_dia_chi.clear()
        self.txt_email.clear()
        self.cbo_quan.setCurrentIndex(0)
        self.cbo_loai_daily.setCurrentIndex(0)
        self.dp_ngay_tiep_nhan.setDate(QDate.currentDate())
        self.txt_tien_no.setText("0")

        # Reset button states
        self.btn_them.setEnabled(True)
        self.btn_sua.setEnabled(False)
        self.btn_xoa.setEnabled(False)

        # Clear table selection
        self.table_daily.clearSelection()

    def validate_input(self):
        # Get form data
        ten_daily = self.txt_ten_daily.text().strip()
        dien_thoai = self.txt_dien_thoai.text().strip()
        dia_chi = self.txt_dia_chi.text().strip()
        email = self.txt_email.text().strip()

        # Validate required fields
        ten_error = ValidationHelper.validate_required(ten_daily, "Tên đại lý")
        if ten_error:
            return ten_error

        # Validate phone number
        phone_error = ValidationHelper.validate_phone(dien_thoai)
        if phone_error:
            return phone_error

        # Validate address
        dia_chi_error = ValidationHelper.validate_required(dia_chi, "Địa chỉ")
        if dia_chi_error:
            return dia_chi_error

        # Validate district
        if self.cbo_quan.currentIndex() < 0:
            return "Vui lòng chọn quận."

        # Validate distributor type
        if self.cbo_loai_daily.currentIndex() < 0:
            return "Vui lòng chọn loại đại lý."

        # Validate email
        email_error = ValidationHelper.validate_email(email)
        if email_error:
            return email_error

        return None