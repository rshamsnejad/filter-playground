from PyQt6.QtCore import QDir, QAbstractItemModel
from PyQt6.QtWidgets import QTreeView, QApplication
from PyQt6.QtGui import QFileSystemModel, QStandardItemModel, QStandardItem

import sys

if __name__ == '__main__':
    app = QApplication(sys.argv)

    # model = QFileSystemModel()
    # model.setRootPath(QDir.currentPath())

    model = QStandardItemModel()
    parentItem = model.invisibleRootItem()
    for i in range(4):
        item = QStandardItem("item %d" % i)
        parentItem.appendRow(item)
        parentItem = item

    tree = QTreeView()
    tree.setModel(model)

    tree.show()

    sys.exit(app.exec())
