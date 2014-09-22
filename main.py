#!/usr/bin/env python2.7
import sys

from PyQt4 import QtGui, QtCore

from paperless_window import PaperlessWindow

def main():
    QtCore.QCoreApplication.setOrganizationName('Poorlytyped')
    QtCore.QCoreApplication.setApplicationName('Paperless')

    app = QtGui.QApplication(sys.argv)

    window = PaperlessWindow()
    window.show()

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()

