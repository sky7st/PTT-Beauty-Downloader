# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'aboutApp.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_AboutAppDialog(object):
    def setupUi(self, AboutAppDialog):
        AboutAppDialog.setObjectName(_fromUtf8("AboutAppDialog"))
        AboutAppDialog.setWindowModality(QtCore.Qt.NonModal)
        AboutAppDialog.setEnabled(False)
        AboutAppDialog.resize(400, 300)
        AboutAppDialog.setSizeGripEnabled(False)
        AboutAppDialog.setModal(True)

        self.retranslateUi(AboutAppDialog)
        QtCore.QMetaObject.connectSlotsByName(AboutAppDialog)

    def retranslateUi(self, AboutAppDialog):
        AboutAppDialog.setWindowTitle(_translate("AboutAppDialog", "關於此APP", None))

