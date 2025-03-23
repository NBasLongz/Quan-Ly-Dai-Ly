#!/usr/bin/env python3
import os
import subprocess
import sys

def run_backend():
    os.chdir(os.path.join(os.path.dirname(__file__), 'backend'))
    args = ['python', 'manage.py', 'runserver', '8000']
    return subprocess.call(args)

if __name__ == '__main__':
    sys.exit(run_backend())