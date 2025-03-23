# shared/config.py

# URL cơ sở của API
API_BASE_URL = "http://127.0.0.1:8000/api"  # Đảm bảo port đúng

# Thời gian timeout mặc định cho các request API (giây)
DEFAULT_TIMEOUT = 10

# Cấu hình ứng dụng
APP_NAME = "Quản lý Đại Lý"
APP_VERSION = "1.0.0"

# Đường dẫn thư mục icons
import os
ICONS_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'icons')