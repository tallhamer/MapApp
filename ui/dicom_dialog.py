# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'dicom_dialog.ui'
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
from PySide6.QtWidgets import (QAbstractButton, QApplication, QDialog, QDialogButtonBox,
    QGridLayout, QLabel, QLineEdit, QPushButton,
    QSizePolicy, QWidget)

class Ui_DicomDialog(object):
    def setupUi(self, DicomDialog):
        if not DicomDialog.objectName():
            DicomDialog.setObjectName(u"DicomDialog")
        DicomDialog.resize(400, 150)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(DicomDialog.sizePolicy().hasHeightForWidth())
        DicomDialog.setSizePolicy(sizePolicy)
        DicomDialog.setMinimumSize(QSize(400, 150))
        DicomDialog.setMaximumSize(QSize(16777215, 150))
        self.gridLayout = QGridLayout(DicomDialog)
        self.gridLayout.setObjectName(u"gridLayout")
        self.label = QLabel(DicomDialog)
        self.label.setObjectName(u"label")

        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)

        self.w_le_dicom_plan_path = QLineEdit(DicomDialog)
        self.w_le_dicom_plan_path.setObjectName(u"w_le_dicom_plan_path")

        self.gridLayout.addWidget(self.w_le_dicom_plan_path, 0, 1, 1, 1)

        self.w_pb_dicom_plan_path = QPushButton(DicomDialog)
        self.w_pb_dicom_plan_path.setObjectName(u"w_pb_dicom_plan_path")
        self.w_pb_dicom_plan_path.setMinimumSize(QSize(25, 25))
        self.w_pb_dicom_plan_path.setMaximumSize(QSize(25, 25))

        self.gridLayout.addWidget(self.w_pb_dicom_plan_path, 0, 2, 1, 1)

        self.label_2 = QLabel(DicomDialog)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)

        self.w_le_dicom_structure_path = QLineEdit(DicomDialog)
        self.w_le_dicom_structure_path.setObjectName(u"w_le_dicom_structure_path")

        self.gridLayout.addWidget(self.w_le_dicom_structure_path, 1, 1, 1, 1)

        self.w_pb_dicom_structure_path = QPushButton(DicomDialog)
        self.w_pb_dicom_structure_path.setObjectName(u"w_pb_dicom_structure_path")
        self.w_pb_dicom_structure_path.setMinimumSize(QSize(25, 25))
        self.w_pb_dicom_structure_path.setMaximumSize(QSize(25, 25))

        self.gridLayout.addWidget(self.w_pb_dicom_structure_path, 1, 2, 1, 1)

        self.buttonBox = QDialogButtonBox(DicomDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.StandardButton.Cancel|QDialogButtonBox.StandardButton.Ok)

        self.gridLayout.addWidget(self.buttonBox, 2, 0, 1, 3)


        self.retranslateUi(DicomDialog)
        self.buttonBox.accepted.connect(DicomDialog.accept)
        self.buttonBox.rejected.connect(DicomDialog.reject)

        QMetaObject.connectSlotsByName(DicomDialog)
    # setupUi

    def retranslateUi(self, DicomDialog):
        DicomDialog.setWindowTitle(QCoreApplication.translate("DicomDialog", u"DICOM RT File Mode", None))
        self.label.setText(QCoreApplication.translate("DicomDialog", u"Plan File:", None))
        self.w_pb_dicom_plan_path.setText(QCoreApplication.translate("DicomDialog", u"...", None))
        self.label_2.setText(QCoreApplication.translate("DicomDialog", u"Structure Set File:", None))
        self.w_pb_dicom_structure_path.setText(QCoreApplication.translate("DicomDialog", u"...", None))
    # retranslateUi

