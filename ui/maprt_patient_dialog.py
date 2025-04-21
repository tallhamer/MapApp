# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'maprt_patient_dialog.ui'
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
    QDialogButtonBox, QGridLayout, QLabel, QLineEdit,
    QSizePolicy, QSpacerItem, QWidget)

class Ui_MapRTPatientDialog(object):
    def setupUi(self, MapRTPatientDialog):
        if not MapRTPatientDialog.objectName():
            MapRTPatientDialog.setObjectName(u"MapRTPatientDialog")
        MapRTPatientDialog.resize(294, 82)
        self.gridLayout = QGridLayout(MapRTPatientDialog)
        self.gridLayout.setObjectName(u"gridLayout")
        self.w_le_patient_id = QLineEdit(MapRTPatientDialog)
        self.w_le_patient_id.setObjectName(u"w_le_patient_id")

        self.gridLayout.addWidget(self.w_le_patient_id, 0, 1, 1, 1)

        self.label = QLabel(MapRTPatientDialog)
        self.label.setObjectName(u"label")

        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer, 2, 0, 1, 1)

        self.buttonBox = QDialogButtonBox(MapRTPatientDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.StandardButton.Cancel|QDialogButtonBox.StandardButton.Ok)

        self.gridLayout.addWidget(self.buttonBox, 3, 0, 1, 2)

        self.label_2 = QLabel(MapRTPatientDialog)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)

        self.w_cb_patient_orientation = QComboBox(MapRTPatientDialog)
        self.w_cb_patient_orientation.setObjectName(u"w_cb_patient_orientation")

        self.gridLayout.addWidget(self.w_cb_patient_orientation, 1, 1, 1, 1)


        self.retranslateUi(MapRTPatientDialog)
        self.buttonBox.accepted.connect(MapRTPatientDialog.accept)
        self.buttonBox.rejected.connect(MapRTPatientDialog.reject)

        QMetaObject.connectSlotsByName(MapRTPatientDialog)
    # setupUi

    def retranslateUi(self, MapRTPatientDialog):
        MapRTPatientDialog.setWindowTitle(QCoreApplication.translate("MapRTPatientDialog", u"MapRT Patient ID", None))
        self.label.setText(QCoreApplication.translate("MapRTPatientDialog", u"Patient ID:", None))
        self.label_2.setText(QCoreApplication.translate("MapRTPatientDialog", u"Orientation:", None))
    # retranslateUi

