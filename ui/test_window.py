# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'test_window.ui'
##
## Created by: Qt User Interface Compiler version 6.8.2
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
from PySide6.QtWidgets import (QApplication, QGridLayout, QGroupBox, QHBoxLayout,
    QLabel, QLineEdit, QMainWindow, QMenuBar,
    QPushButton, QSizePolicy, QSpacerItem, QStatusBar,
    QVBoxLayout, QWidget)

from vtkmodules.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(958, 600)
        MainWindow.setMinimumSize(QSize(0, 0))
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.horizontalLayout = QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.groupBox = QGroupBox(self.centralwidget)
        self.groupBox.setObjectName(u"groupBox")
        self.verticalLayout = QVBoxLayout(self.groupBox)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.widget = QWidget(self.groupBox)
        self.widget.setObjectName(u"widget")
        self.gridLayout = QGridLayout(self.widget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.label = QLabel(self.widget)
        self.label.setObjectName(u"label")

        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)

        self.label_2 = QLabel(self.widget)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)

        self.w_pb_obj_file = QPushButton(self.widget)
        self.w_pb_obj_file.setObjectName(u"w_pb_obj_file")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.w_pb_obj_file.sizePolicy().hasHeightForWidth())
        self.w_pb_obj_file.setSizePolicy(sizePolicy1)
        self.w_pb_obj_file.setMaximumSize(QSize(25, 16777215))

        self.gridLayout.addWidget(self.w_pb_obj_file, 1, 3, 1, 1)

        self.w_le_dicom_file = QLineEdit(self.widget)
        self.w_le_dicom_file.setObjectName(u"w_le_dicom_file")
        self.w_le_dicom_file.setMinimumSize(QSize(100, 0))

        self.gridLayout.addWidget(self.w_le_dicom_file, 0, 1, 1, 2)

        self.w_pb_dicom_file = QPushButton(self.widget)
        self.w_pb_dicom_file.setObjectName(u"w_pb_dicom_file")
        sizePolicy1.setHeightForWidth(self.w_pb_dicom_file.sizePolicy().hasHeightForWidth())
        self.w_pb_dicom_file.setSizePolicy(sizePolicy1)
        self.w_pb_dicom_file.setMaximumSize(QSize(25, 16777215))

        self.gridLayout.addWidget(self.w_pb_dicom_file, 0, 3, 1, 1)

        self.w_le_obj_file = QLineEdit(self.widget)
        self.w_le_obj_file.setObjectName(u"w_le_obj_file")
        self.w_le_obj_file.setMinimumSize(QSize(100, 0))

        self.gridLayout.addWidget(self.w_le_obj_file, 1, 1, 1, 2)


        self.verticalLayout.addWidget(self.widget)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)


        self.horizontalLayout.addWidget(self.groupBox)

        self.groupBox_2 = QGroupBox(self.centralwidget)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.horizontalLayout_2 = QHBoxLayout(self.groupBox_2)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.vtk_widget = QVTKRenderWindowInteractor(self.groupBox_2)
        self.vtk_widget.setObjectName(u"vtk_widget")
        sizePolicy.setHeightForWidth(self.vtk_widget.sizePolicy().hasHeightForWidth())
        self.vtk_widget.setSizePolicy(sizePolicy)
        self.vtk_widget.setMinimumSize(QSize(400, 400))
        self.vtk_widget.setMaximumSize(QSize(16777215, 16777215))

        self.horizontalLayout_2.addWidget(self.vtk_widget)


        self.horizontalLayout.addWidget(self.groupBox_2)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 958, 33))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.groupBox.setTitle(QCoreApplication.translate("MainWindow", u"Test Area 1", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"DICOM Structure Set File", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"OBJ File", None))
        self.w_pb_obj_file.setText(QCoreApplication.translate("MainWindow", u"...", None))
        self.w_pb_dicom_file.setText(QCoreApplication.translate("MainWindow", u"...", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("MainWindow", u"Test Area 2", None))
    # retranslateUi

