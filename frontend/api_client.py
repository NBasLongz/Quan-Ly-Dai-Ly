# frontend/api_client.py
import requests
from decimal import Decimal
from datetime import datetime, date
from typing import List, Dict, Any, Optional, Union
from shared.config import API_BASE_URL, DEFAULT_TIMEOUT


class APIError(Exception):
    """Exception raised for API errors"""

    def __init__(self, message, status_code=None, response=None):
        self.message = message
        self.status_code = status_code
        self.response = response
        super().__init__(self.message)


class DjangoAPIClient:
    """Client class to interact with Django REST API"""

    def __init__(self, base_url=API_BASE_URL):
        self.base_url = base_url

    def _handle_response(self, response, expected_status=200):
        """Handle API response and errors"""
        if response.status_code == expected_status:
            return response.json() if response.content else None

        # Handle error
        try:
            error_data = response.json()
            error_message = error_data.get('error', 'Unknown API error')
        except:
            error_message = f"API error: HTTP {response.status_code}"

        raise APIError(error_message, response.status_code, response)

    # Quan (District) API methods
    def get_all_quan(self) -> List[Dict]:
        """Get all districts"""
        response = requests.get(f"{self.base_url}/quan/", timeout=DEFAULT_TIMEOUT)
        return self._handle_response(response)

    def get_quan_by_id(self, id_: int) -> Dict:
        """Get district by ID"""
        response = requests.get(f"{self.base_url}/quan/{id_}/", timeout=DEFAULT_TIMEOUT)
        return self._handle_response(response)

    def add_quan(self, ten_quan: str) -> Dict:
        """Add new district"""
        data = {"ten_quan": ten_quan}
        response = requests.post(f"{self.base_url}/quan/", json=data, timeout=DEFAULT_TIMEOUT)
        return self._handle_response(response, 201)

    def update_quan(self, id_: int, ten_quan: str) -> Dict:
        """Update district"""
        data = {"ten_quan": ten_quan}
        response = requests.put(f"{self.base_url}/quan/{id_}/", json=data, timeout=DEFAULT_TIMEOUT)
        return self._handle_response(response)

    def delete_quan(self, id_: int) -> None:
        """Delete district"""
        response = requests.delete(f"{self.base_url}/quan/{id_}/", timeout=DEFAULT_TIMEOUT)
        return self._handle_response(response, 204)

    def count_daily_by_quan(self, id_: int) -> int:
        """Count distributors in district"""
        try:
            response = requests.get(f"{self.base_url}/quan/{id_}/dai_lys/", timeout=DEFAULT_TIMEOUT)
            data = self._handle_response(response)
            return len(data)
        except:
            return 0

    # LoaiDaiLy (Distributor Type) API methods
    def get_all_loaidaily(self) -> List[Dict]:
        """Get all distributor types"""
        response = requests.get(f"{self.base_url}/loaidaily/", timeout=DEFAULT_TIMEOUT)
        return self._handle_response(response)

    def get_loaidaily_by_id(self, id_: int) -> Dict:
        """Get distributor type by ID"""
        response = requests.get(f"{self.base_url}/loaidaily/{id_}/", timeout=DEFAULT_TIMEOUT)
        return self._handle_response(response)

    def add_loaidaily(self, ten_loai: str, no_toi_da: Decimal) -> Dict:
        """Add new distributor type"""
        data = {
            "ten_loai_dai_ly": ten_loai,
            "no_toi_da": float(no_toi_da)
        }
        response = requests.post(f"{self.base_url}/loaidaily/", json=data, timeout=DEFAULT_TIMEOUT)
        return self._handle_response(response, 201)

    def update_loaidaily(self, id_: int, ten_loai: str, no_toi_da: Decimal) -> Dict:
        """Update distributor type"""
        data = {
            "ten_loai_dai_ly": ten_loai,
            "no_toi_da": float(no_toi_da)
        }
        response = requests.put(f"{self.base_url}/loaidaily/{id_}/", json=data, timeout=DEFAULT_TIMEOUT)
        return self._handle_response(response)

    def delete_loaidaily(self, id_: int) -> None:
        """Delete distributor type"""
        response = requests.delete(f"{self.base_url}/loaidaily/{id_}/", timeout=DEFAULT_TIMEOUT)
        return self._handle_response(response, 204)

    # DaiLy (Distributor) API methods
    def get_all_daily(self) -> List[Dict]:
        """Get all distributors"""
        response = requests.get(f"{self.base_url}/daily/", timeout=DEFAULT_TIMEOUT)
        return self._handle_response(response)

    def get_daily_by_id(self, id_: int) -> Dict:
        """Get distributor by ID"""
        response = requests.get(f"{self.base_url}/daily/{id_}/", timeout=DEFAULT_TIMEOUT)
        return self._handle_response(response)

    def search_daily(self, keyword: str) -> List[Dict]:
        """Search distributors"""
        response = requests.get(f"{self.base_url}/daily/search/?keyword={keyword}", timeout=DEFAULT_TIMEOUT)
        return self._handle_response(response)

    def add_daily(self, ten_daily: str, dien_thoai: str, dia_chi: str,
                  quan_id: int, loaidaily_id: int, email: Optional[str] = None) -> Dict:
        """Add new distributor"""
        data = {
            "ten_dai_ly": ten_daily,
            "dien_thoai": dien_thoai,
            "dia_chi": dia_chi,
            "quan": quan_id,
            "loai_dai_ly": loaidaily_id,
            "email": email
        }
        response = requests.post(f"{self.base_url}/daily/", json=data, timeout=DEFAULT_TIMEOUT)
        return self._handle_response(response, 201)

    def update_daily(self, id_: int, ten_daily: str, dien_thoai: str, dia_chi: str,
                     quan_id: int, loaidaily_id: int, email: Optional[str] = None) -> Dict:
        """Update distributor"""
        data = {
            "ten_dai_ly": ten_daily,
            "dien_thoai": dien_thoai,
            "dia_chi": dia_chi,
            "quan": quan_id,
            "loai_dai_ly": loaidaily_id,
            "email": email
        }
        response = requests.put(f"{self.base_url}/daily/{id_}/", json=data, timeout=DEFAULT_TIMEOUT)
        return self._handle_response(response)

    def update_tien_no(self, id_: int, tien_no: Decimal) -> Dict:
        """Update distributor's debt"""
        daily = self.get_daily_by_id(id_)
        daily["tien_no"] = float(tien_no)

        response = requests.put(f"{self.base_url}/daily/{id_}/", json=daily, timeout=DEFAULT_TIMEOUT)
        return self._handle_response(response)

    def delete_daily(self, id_: int) -> None:
        """Delete distributor"""
        response = requests.delete(f"{self.base_url}/daily/{id_}/", timeout=DEFAULT_TIMEOUT)
        return self._handle_response(response, 204)

    # QuyDinh (Regulation) API methods
    def get_all_quydinh(self) -> List[Dict]:
        """Get all regulations"""
        response = requests.get(f"{self.base_url}/quydinh/", timeout=DEFAULT_TIMEOUT)
        return self._handle_response(response)

    def get_quydinh_by_name(self, name: str) -> Optional[Dict]:
        """Get regulation by name"""
        try:
            response = requests.get(f"{self.base_url}/quydinh/by_name/?name={name}", timeout=DEFAULT_TIMEOUT)
            return self._handle_response(response)
        except APIError:
            return None

    def get_or_create_quydinh(self, name: str, default_value: str, mo_ta: Optional[str] = None) -> Dict:
        """Get regulation by name or create if not exists"""
        try:
            quydinh = self.get_quydinh_by_name(name)
            if quydinh:
                return quydinh
        except:
            pass

        # Create new regulation
        data = {
            "ten_quy_dinh": name,
            "gia_tri": default_value,
            "mo_ta": mo_ta
        }
        response = requests.post(f"{self.base_url}/quydinh/", json=data, timeout=DEFAULT_TIMEOUT)
        return self._handle_response(response, 201)

    def update_quydinh(self, id_: int, gia_tri: str, mo_ta: Optional[str] = None) -> Dict:
        """Update regulation"""
        quydinh = self.get_quydinh_by_id(id_)
        quydinh["gia_tri"] = gia_tri
        if mo_ta is not None:
            quydinh["mo_ta"] = mo_ta

        response = requests.put(f"{self.base_url}/quydinh/{id_}/", json=quydinh, timeout=DEFAULT_TIMEOUT)
        return self._handle_response(response)

    def get_quydinh_by_id(self, id_: int) -> Dict:
        """Get regulation by ID"""
        response = requests.get(f"{self.base_url}/quydinh/{id_}/", timeout=DEFAULT_TIMEOUT)
        return self._handle_response(response)