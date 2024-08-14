#!/usr/bin/python

import sys
import os

if os.name == 'nt':
    # Workaround to get the app icon in the taskbar on Windows
    import ctypes
    myappid = 'mycompany.myproduct.subproduct.version' # arbitrary string
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

    # Workaround to make this script run without a terminal window
    if sys.executable.endswith("pythonw.exe"):
        sys.stdout = open(os.path.join(os.getenv("TEMP"), os.path.basename(sys.argv[0]) + "-stdout"), 'w')
        sys.stderr = open(os.path.join(os.getenv("TEMP"), os.path.basename(sys.argv[0]) + "-stderr"), 'w')

from PyQt6.QtWidgets import QApplication, QStyleFactory
from lib.MainWindow import MainWindow

if __name__ == '__main__':

    style = QStyleFactory()

    app = QApplication(sys.argv)
    app.setStyle(style.create('Fusion'))

    window = MainWindow()

    sys.exit(app.exec())