# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'SaveWarning.ui'
#
# Created: Tue Jul 12 15:22:40 2016
#      by: PyQt4 UI code generator 4.10.4
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

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(493, 87)
        self.horizontalLayout = QtGui.QHBoxLayout(Dialog)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.pushButton = QtGui.QPushButton(Dialog)
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.horizontalLayout.addWidget(self.pushButton)
        self.pushButton_2 = QtGui.QPushButton(Dialog)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8("share/rcmanager/1465394415_floppy.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_2.setIcon(icon)
        self.pushButton_2.setObjectName(_fromUtf8("pushButton_2"))
        self.horizontalLayout.addWidget(self.pushButton_2)
        self.pushButton_3 = QtGui.QPushButton(Dialog)
        self.pushButton_3.setAutoDefault(True)
        self.pushButton_3.setDefault(True)
        self.pushButton_3.setObjectName(_fromUtf8("pushButton_3"))
        self.horizontalLayout.addWidget(self.pushButton_3)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Dialog", None))
        self.pushButton.setText(_translate("Dialog", "Don\'t Save", None))
        self.pushButton_2.setText(_translate("Dialog", "Save", None))
        self.pushButton_3.setText(_translate("Dialog", "Cancel", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    Dialog = QtGui.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())

