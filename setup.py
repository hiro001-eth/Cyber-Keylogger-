# setup.py

from setuptools import setup, find_packages

setup(
    name="CyberKeylogger",
    version="1.0.0",
    description="Enterprise-grade, privacy-compliant keylogger and monitoring suite",
    author="Your Name",
    packages=find_packages(),
    install_requires=[
        "pynput", "psutil", "flask", "mss", "Pillow", "pyperclip", "websockets", "pywin32", "pyobjc"
    ],
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "cyberkeylogger=main:main"
        ]
    }
)
