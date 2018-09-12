# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'patch_select.ui'
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

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(329, 191)
        self.buttonBox = QtGui.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(-50, 110, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.label = QtGui.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(20, 40, 46, 13))
        self.label.setObjectName(_fromUtf8("label"))
        self.label_2 = QtGui.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(20, 70, 46, 13))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.spinBank1 = QtGui.QSpinBox(Dialog)
        self.spinBank1.setGeometry(QtCore.QRect(90, 40, 42, 22))
        self.spinBank1.setMaximum(2)
        self.spinBank1.setObjectName(_fromUtf8("spinBank1"))
        self.spinPatch1 = QtGui.QSpinBox(Dialog)
        self.spinPatch1.setGeometry(QtCore.QRect(90, 70, 42, 22))
        self.spinPatch1.setMaximum(127)
        self.spinPatch1.setObjectName(_fromUtf8("spinPatch1"))
        self.spinPatch1_2 = QtGui.QSpinBox(Dialog)
        self.spinPatch1_2.setGeometry(QtCore.QRect(240, 70, 42, 22))
        self.spinPatch1_2.setMaximum(127)
        self.spinPatch1_2.setObjectName(_fromUtf8("spinPatch1_2"))
        self.label_3 = QtGui.QLabel(Dialog)
        self.label_3.setGeometry(QtCore.QRect(170, 40, 46, 13))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.label_4 = QtGui.QLabel(Dialog)
        self.label_4.setGeometry(QtCore.QRect(170, 70, 46, 13))
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.spinBank1_2 = QtGui.QSpinBox(Dialog)
        self.spinBank1_2.setGeometry(QtCore.QRect(240, 40, 42, 22))
        self.spinBank1_2.setMaximum(2)
        self.spinBank1_2.setObjectName(_fromUtf8("spinBank1_2"))
        self.label_5 = QtGui.QLabel(Dialog)
        self.label_5.setGeometry(QtCore.QRect(20, 10, 46, 13))
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.label_6 = QtGui.QLabel(Dialog)
        self.label_6.setGeometry(QtCore.QRect(170, 10, 46, 13))
        self.label_6.setObjectName(_fromUtf8("label_6"))

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), Dialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Patch Select", None))
        self.label.setText(_translate("Dialog", "Bank", None))
        self.label_2.setText(_translate("Dialog", "Patch", None))
        self.label_3.setText(_translate("Dialog", "Bank", None))
        self.label_4.setText(_translate("Dialog", "Patch", None))
        self.label_5.setText(_translate("Dialog", "Patch 1", None))
        self.label_6.setText(_translate("Dialog", "Patch 2", None))

