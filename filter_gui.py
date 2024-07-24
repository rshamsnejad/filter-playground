import sys
import os
from PyQt6.QtWidgets import QApplication
from lib.MainWindow import MainWindow

if __name__ == '__main__':

    if os.name == 'nt':
        # Workaround to get the app icon in the taskbar on Windows
        import ctypes
        myappid = 'mycompany.myproduct.subproduct.version' # arbitrary string
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

    app = QApplication(sys.argv)

    window = MainWindow()

    sys.exit(app.exec())