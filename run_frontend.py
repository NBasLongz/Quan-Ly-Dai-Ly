#!/usr/bin/env python3
import sys
import os

# Thêm thư mục gốc vào PATH
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from frontend.main import main

if __name__ == '__main__':
    sys.exit(main())