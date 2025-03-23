# frontend/utils/helpers.py
import os
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtGui import QIcon


class IconManager:
    """Helper class to manage icons"""
    ICONS_PATH = os.environ.get('ICONS_PATH', os.path.join(os.path.dirname(os.path.dirname(
        os.path.dirname(os.path.abspath(__file__)))), 'shared', 'icons'))

    @staticmethod
    def get_icon(icon_name):
        """Get icon by name"""
        icon_path = os.path.join(IconManager.ICONS_PATH, f"{icon_name}.png")
        if os.path.exists(icon_path):
            return QIcon(icon_path)
        return QIcon()  # Empty icon if not found


class AlertHelper:
    """Helper class for showing alerts and message boxes"""

    @staticmethod
    def show_success_alert(parent, title, message):
        """Display a success information message box"""
        QMessageBox.information(parent, title, message)

    @staticmethod
    def show_error_alert(parent, title, message):
        """Display an error message box"""
        QMessageBox.critical(parent, title, message)

    @staticmethod
    def show_warning_alert(parent, title, message):
        """Display a warning message box"""
        QMessageBox.warning(parent, title, message)

    @staticmethod
    def show_confirmation_dialog(parent, title, message):
        """Display a confirmation dialog and return True if OK is clicked"""
        result = QMessageBox.question(
            parent,
            title,
            message,
            QMessageBox.Ok | QMessageBox.Cancel,
            QMessageBox.Cancel
        )
        return result == QMessageBox.Ok

    @staticmethod
    def show_api_error(parent, error, default_title="Lỗi API"):
        """Display API error message"""
        if hasattr(error, 'message'):
            AlertHelper.show_error_alert(parent, default_title, error.message)
        else:
            AlertHelper.show_error_alert(parent, default_title, str(error))


# frontend/utils/validators.py
import re
from decimal import Decimal, DecimalException


class ValidationHelper:
    """Helper class for validating inputs"""

    PHONE_REGEX = r"^\d{10,11}$"
    EMAIL_REGEX = r"^[A-Za-z0-9+_.-]+@[A-Za-z0-9.-]+$"

    @staticmethod
    def validate_required(value, field_name):
        """Check if string is not empty"""
        if not value or not value.strip():
            return f"{field_name} không được để trống."
        return None

    @staticmethod
    def validate_phone(phone):
        """Check if phone number is valid"""
        if not phone or not phone.strip():
            return "Số điện thoại không được để trống."

        if not re.match(ValidationHelper.PHONE_REGEX, phone):
            return "Số điện thoại không hợp lệ (phải có 10-11 chữ số)."

        return None

    @staticmethod
    def validate_email(email):
        """Check if email is valid"""
        if not email or not email.strip():
            return None  # Email is optional

        if not re.match(ValidationHelper.EMAIL_REGEX, email):
            return "Email không hợp lệ."

        return None

    @staticmethod
    def validate_positive_integer(input_value, field_name):
        """Check if input is a positive integer"""
        if not input_value or not input_value.strip():
            return f"{field_name} không được để trống."

        try:
            value = int(input_value)
            if value <= 0:
                return f"{field_name} phải là số nguyên dương."
        except ValueError:
            return f"{field_name} phải là số nguyên."

        return None

    @staticmethod
    def validate_positive_decimal(input_value, field_name):
        """Check if input is a positive decimal"""
        if not input_value or not input_value.strip():
            return f"{field_name} không được để trống."

        try:
            value = Decimal(input_value.replace(',', ''))
            if value <= 0:
                return f"{field_name} phải là số dương."
        except (ValueError, DecimalException):
            return f"{field_name} phải là số."

        return None