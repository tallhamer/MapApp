# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'app_settings_dialog.ui'
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
    QGridLayout, QGroupBox, QLabel, QLineEdit,
    QPushButton, QSizePolicy, QSpacerItem, QSpinBox,
    QTextEdit, QVBoxLayout, QWidget)

class Ui_SettingsDialog(object):
    def setupUi(self, SettingsDialog):
        if not SettingsDialog.objectName():
            SettingsDialog.setObjectName(u"SettingsDialog")
        SettingsDialog.setWindowModality(Qt.WindowModality.ApplicationModal)
        SettingsDialog.resize(431, 619)
        SettingsDialog.setMinimumSize(QSize(400, 600))
        self.verticalLayout = QVBoxLayout(SettingsDialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.groupBox_2 = QGroupBox(SettingsDialog)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.gridLayout_2 = QGridLayout(self.groupBox_2)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.label_4 = QLabel(self.groupBox_2)
        self.label_4.setObjectName(u"label_4")

        self.gridLayout_2.addWidget(self.label_4, 0, 0, 1, 1)

        self.w_le_dicom_directory = QLineEdit(self.groupBox_2)
        self.w_le_dicom_directory.setObjectName(u"w_le_dicom_directory")

        self.gridLayout_2.addWidget(self.w_le_dicom_directory, 0, 1, 1, 1)

        self.w_pb_dicom_directory = QPushButton(self.groupBox_2)
        self.w_pb_dicom_directory.setObjectName(u"w_pb_dicom_directory")
        self.w_pb_dicom_directory.setMinimumSize(QSize(25, 0))
        self.w_pb_dicom_directory.setMaximumSize(QSize(25, 16777215))

        self.gridLayout_2.addWidget(self.w_pb_dicom_directory, 0, 2, 1, 1)

        self.label_5 = QLabel(self.groupBox_2)
        self.label_5.setObjectName(u"label_5")

        self.gridLayout_2.addWidget(self.label_5, 1, 0, 1, 1)

        self.w_sb_arc_check_resolution = QSpinBox(self.groupBox_2)
        self.w_sb_arc_check_resolution.setObjectName(u"w_sb_arc_check_resolution")
        self.w_sb_arc_check_resolution.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)
        self.w_sb_arc_check_resolution.setMinimum(1)
        self.w_sb_arc_check_resolution.setMaximum(10)

        self.gridLayout_2.addWidget(self.w_sb_arc_check_resolution, 1, 1, 1, 1)


        self.verticalLayout.addWidget(self.groupBox_2)

        self.groupBox = QGroupBox(SettingsDialog)
        self.groupBox.setObjectName(u"groupBox")
        self.gridLayout = QGridLayout(self.groupBox)
        self.gridLayout.setObjectName(u"gridLayout")
        self.label_3 = QLabel(self.groupBox)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 2)

        self.label = QLabel(self.groupBox)
        self.label.setObjectName(u"label")

        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)

        self.w_le_api_url = QLineEdit(self.groupBox)
        self.w_le_api_url.setObjectName(u"w_le_api_url")

        self.gridLayout.addWidget(self.w_le_api_url, 0, 2, 1, 3)

        self.w_pb_test_connection = QPushButton(self.groupBox)
        self.w_pb_test_connection.setObjectName(u"w_pb_test_connection")

        self.gridLayout.addWidget(self.w_pb_test_connection, 3, 4, 1, 1)

        self.horizontalSpacer = QSpacerItem(207, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer, 3, 3, 1, 1)

        self.w_le_api_token = QLineEdit(self.groupBox)
        self.w_le_api_token.setObjectName(u"w_le_api_token")

        self.gridLayout.addWidget(self.w_le_api_token, 1, 2, 1, 3)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_2, 3, 1, 1, 2)

        self.w_le_api_user_agent = QLineEdit(self.groupBox)
        self.w_le_api_user_agent.setObjectName(u"w_le_api_user_agent")

        self.gridLayout.addWidget(self.w_le_api_user_agent, 2, 2, 1, 3)

        self.label_2 = QLabel(self.groupBox)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 2)

        self.w_te_test_connectio_results = QTextEdit(self.groupBox)
        self.w_te_test_connectio_results.setObjectName(u"w_te_test_connectio_results")
        self.w_te_test_connectio_results.setReadOnly(True)

        self.gridLayout.addWidget(self.w_te_test_connectio_results, 4, 0, 1, 5)


        self.verticalLayout.addWidget(self.groupBox)

        self.buttonBox = QDialogButtonBox(SettingsDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.StandardButton.Cancel|QDialogButtonBox.StandardButton.Ok)

        self.verticalLayout.addWidget(self.buttonBox)


        self.retranslateUi(SettingsDialog)
        self.buttonBox.accepted.connect(SettingsDialog.accept)
        self.buttonBox.rejected.connect(SettingsDialog.reject)

        QMetaObject.connectSlotsByName(SettingsDialog)
    # setupUi

    def retranslateUi(self, SettingsDialog):
        SettingsDialog.setWindowTitle(QCoreApplication.translate("SettingsDialog", u"Map App Settings", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("SettingsDialog", u"DICOM", None))
        self.label_4.setText(QCoreApplication.translate("SettingsDialog", u"Data Directory:", None))
        self.w_pb_dicom_directory.setText(QCoreApplication.translate("SettingsDialog", u"...", None))
        self.label_5.setText(QCoreApplication.translate("SettingsDialog", u"Arc Check Resolution:", None))
        self.groupBox.setTitle(QCoreApplication.translate("SettingsDialog", u"MapRT API", None))
        self.label_3.setText(QCoreApplication.translate("SettingsDialog", u"User-Agent:", None))
        self.label.setText(QCoreApplication.translate("SettingsDialog", u"URL:", None))
        self.w_pb_test_connection.setText(QCoreApplication.translate("SettingsDialog", u"Test Connection", None))
        self.label_2.setText(QCoreApplication.translate("SettingsDialog", u"Token:", None))
    # retranslateUi

