#!/usr/bin/env python3
"""
Script khởi chạy cả backend và frontend
"""
import subprocess
import threading
import time
import os
import sys


def run_backend():
    """Chạy Django backend trong thread riêng"""
    backend_script = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'run_backend.py')
    subprocess.call([sys.executable, backend_script])


def run_frontend():
    """Chạy PyQt5 frontend"""
    frontend_script = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'run_frontend.py')
    subprocess.call([sys.executable, frontend_script])


if __name__ == '__main__':
    # Chạy backend trong thread riêng
    backend_thread = threading.Thread(target=run_backend)
    backend_thread.daemon = True
    backend_thread.start()

    # Đợi server khởi động
    print("Đang khởi động Django server...")
    time.sleep(3)

    # Chạy frontend trong thread chính
    print("Đang khởi động PyQt5 frontend...")
    run_frontend()