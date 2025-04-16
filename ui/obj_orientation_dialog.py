# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'obj_orientation_dialog.ui'
##
## Created by: Qt User Interface Compiler version 6.8.3
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QAbstractButton, QApplication, QComboBox, QDialog,
    QDialogButtonBox, QFormLayout, QLabel, QSizePolicy,
    QVBoxLayout, QWidget)

class Ui_OrientationDialog(object):
    def setupUi(self, OrientationDialog):
        if not OrientationDialog.objectName():
            OrientationDialog.setObjectName(u"OrientationDialog")
        OrientationDialog.resize(300, 100)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(OrientationDialog.sizePolicy().hasHeightForWidth())
        OrientationDialog.setSizePolicy(sizePolicy)
        OrientationDialog.setMinimumSize(QSize(300, 100))
        OrientationDialog.setMaximumSize(QSize(300, 100))
        self.verticalLayout = QVBoxLayout(OrientationDialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.widget = QWidget(OrientationDialog)
        self.widget.setObjectName(u"widget")
        self.formLayout = QFormLayout(self.widget)
        self.formLayout.setObjectName(u"formLayout")
        self.label = QLabel(self.widget)
        self.label.setObjectName(u"label")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.label)

        self.w_cb_obj_surface_orientation = QComboBox(self.widget)
        self.w_cb_obj_surface_orientation.setObjectName(u"w_cb_obj_surface_orientation")

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.w_cb_obj_surface_orientation)


        self.verticalLayout.addWidget(self.widget)

        self.buttonBox = QDialogButtonBox(OrientationDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.StandardButton.Cancel|QDialogButtonBox.StandardButton.Ok)

        self.verticalLayout.addWidget(self.buttonBox)


        self.retranslateUi(OrientationDialog)
        self.buttonBox.accepted.connect(OrientationDialog.accept)
        self.buttonBox.rejected.connect(OrientationDialog.reject)

        QMetaObject.connectSlotsByName(OrientationDialog)
    # setupUi

    def retranslateUi(self, OrientationDialog):
        OrientationDialog.setWindowTitle(QCoreApplication.translate("OrientationDialog", u"File Surface Orientation", None))
        self.label.setText(QCoreApplication.translate("OrientationDialog", u"Patient Orientation", None))
    # retranslateUi

