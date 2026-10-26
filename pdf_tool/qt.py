"""Select Qt 5 for Windows LTSB 1607, Qt 6 for current desktop systems.

PDF_MUHELY_QT=pyside2 allows exercising the legacy binding on a Linux test host.
A missing binding is an installation error, so do not silently switch versions.
"""
import os
import sys

BINDING = os.environ.get('PDF_MUHELY_QT', 'pyside2' if sys.platform == 'win32' else 'pyside6')
if BINDING == 'pyside2':
    from PySide2 import QtCore, QtGui, QtWidgets
elif BINDING == 'pyside6':
    from PySide6 import QtCore, QtGui, QtWidgets
else:
    raise ValueError(f'Unknown Qt binding: {BINDING}')
