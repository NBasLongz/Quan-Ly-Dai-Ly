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

    @staticmethod
    def validate_max_value(input_value, max_value, field_name):
        """Check if input value does not exceed max value"""
        try:
            value = Decimal(input_value.replace(',', ''))
            if value > max_value:
                return f"{field_name} không được vượt quá {max_value:,.0f}."
        except (ValueError, DecimalException):
            return f"{field_name} phải là số."

        return None

    @staticmethod
    def format_currency(value):
        """Format number to currency string"""
        if isinstance(value, str):
            try:
                value = Decimal(value.replace(',', ''))
            except:
                return value

        return f"{value:,.0f}"

    @staticmethod
    def parse_currency(value):
        """Parse currency string to Decimal"""
        if not value:
            return Decimal('0')

        if isinstance(value, (int, float, Decimal)):
            return Decimal(str(value))

        try:
            return Decimal(value.replace(',', ''))
        except:
            return Decimal('0')