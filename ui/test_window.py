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
from PySide6.QtWidgets import (QApplication, QComboBox, QFrame, QGridLayout,
    QGroupBox, QHBoxLayout, QLabel, QLineEdit,
    QMainWindow, QMenuBar, QPushButton, QRadioButton,
    QSizePolicy, QSpacerItem, QStatusBar, QVBoxLayout,
    QWidget)

from vtkmodules.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1086, 654)
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
        self.groupBox.setMaximumSize(QSize(400, 16777215))
        self.verticalLayout = QVBoxLayout(self.groupBox)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.groupBox_3 = QGroupBox(self.groupBox)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.gridLayout_2 = QGridLayout(self.groupBox_3)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.label_6 = QLabel(self.groupBox_3)
        self.label_6.setObjectName(u"label_6")

        self.gridLayout_2.addWidget(self.label_6, 0, 0, 1, 1)

        self.w_le_dicom_plan_file = QLineEdit(self.groupBox_3)
        self.w_le_dicom_plan_file.setObjectName(u"w_le_dicom_plan_file")
        self.w_le_dicom_plan_file.setMinimumSize(QSize(100, 0))
        self.w_le_dicom_plan_file.setReadOnly(True)

        self.gridLayout_2.addWidget(self.w_le_dicom_plan_file, 0, 1, 1, 1)

        self.w_pb_dicom_plan_file = QPushButton(self.groupBox_3)
        self.w_pb_dicom_plan_file.setObjectName(u"w_pb_dicom_plan_file")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.w_pb_dicom_plan_file.sizePolicy().hasHeightForWidth())
        self.w_pb_dicom_plan_file.setSizePolicy(sizePolicy1)
        self.w_pb_dicom_plan_file.setMaximumSize(QSize(25, 16777215))

        self.gridLayout_2.addWidget(self.w_pb_dicom_plan_file, 0, 2, 1, 1)

        self.label = QLabel(self.groupBox_3)
        self.label.setObjectName(u"label")

        self.gridLayout_2.addWidget(self.label, 1, 0, 1, 1)

        self.w_le_dicom_struct_file = QLineEdit(self.groupBox_3)
        self.w_le_dicom_struct_file.setObjectName(u"w_le_dicom_struct_file")
        self.w_le_dicom_struct_file.setMinimumSize(QSize(100, 0))
        self.w_le_dicom_struct_file.setDragEnabled(False)
        self.w_le_dicom_struct_file.setReadOnly(True)

        self.gridLayout_2.addWidget(self.w_le_dicom_struct_file, 1, 1, 1, 1)

        self.w_pb_dicom_struct_file = QPushButton(self.groupBox_3)
        self.w_pb_dicom_struct_file.setObjectName(u"w_pb_dicom_struct_file")
        sizePolicy1.setHeightForWidth(self.w_pb_dicom_struct_file.sizePolicy().hasHeightForWidth())
        self.w_pb_dicom_struct_file.setSizePolicy(sizePolicy1)
        self.w_pb_dicom_struct_file.setMaximumSize(QSize(25, 16777215))

        self.gridLayout_2.addWidget(self.w_pb_dicom_struct_file, 1, 2, 1, 1)

        self.label_3 = QLabel(self.groupBox_3)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout_2.addWidget(self.label_3, 2, 0, 1, 1)

        self.w_cb_dicom_color = QComboBox(self.groupBox_3)
        self.w_cb_dicom_color.setObjectName(u"w_cb_dicom_color")
        self.w_cb_dicom_color.setMinimumSize(QSize(100, 0))

        self.gridLayout_2.addWidget(self.w_cb_dicom_color, 2, 1, 1, 1)

        self.w_dicom_color_frame = QFrame(self.groupBox_3)
        self.w_dicom_color_frame.setObjectName(u"w_dicom_color_frame")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.w_dicom_color_frame.sizePolicy().hasHeightForWidth())
        self.w_dicom_color_frame.setSizePolicy(sizePolicy2)
        self.w_dicom_color_frame.setMaximumSize(QSize(25, 25))
        self.w_dicom_color_frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.w_dicom_color_frame.setFrameShadow(QFrame.Shadow.Raised)

        self.gridLayout_2.addWidget(self.w_dicom_color_frame, 2, 2, 1, 1)


        self.verticalLayout.addWidget(self.groupBox_3)

        self.groupBox_4 = QGroupBox(self.groupBox)
        self.groupBox_4.setObjectName(u"groupBox_4")
        self.gridLayout_3 = QGridLayout(self.groupBox_4)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.w_pb_obj_file = QPushButton(self.groupBox_4)
        self.w_pb_obj_file.setObjectName(u"w_pb_obj_file")
        sizePolicy1.setHeightForWidth(self.w_pb_obj_file.sizePolicy().hasHeightForWidth())
        self.w_pb_obj_file.setSizePolicy(sizePolicy1)
        self.w_pb_obj_file.setMaximumSize(QSize(25, 16777215))

        self.gridLayout_3.addWidget(self.w_pb_obj_file, 0, 2, 1, 1)

        self.label_2 = QLabel(self.groupBox_4)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout_3.addWidget(self.label_2, 0, 0, 1, 1)

        self.w_le_obj_file = QLineEdit(self.groupBox_4)
        self.w_le_obj_file.setObjectName(u"w_le_obj_file")
        self.w_le_obj_file.setMinimumSize(QSize(100, 0))

        self.gridLayout_3.addWidget(self.w_le_obj_file, 0, 1, 1, 1)

        self.label_4 = QLabel(self.groupBox_4)
        self.label_4.setObjectName(u"label_4")

        self.gridLayout_3.addWidget(self.label_4, 1, 0, 1, 1)

        self.w_obj_color_frame = QFrame(self.groupBox_4)
        self.w_obj_color_frame.setObjectName(u"w_obj_color_frame")
        sizePolicy2.setHeightForWidth(self.w_obj_color_frame.sizePolicy().hasHeightForWidth())
        self.w_obj_color_frame.setSizePolicy(sizePolicy2)
        self.w_obj_color_frame.setMinimumSize(QSize(0, 0))
        self.w_obj_color_frame.setMaximumSize(QSize(25, 25))
        self.w_obj_color_frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.w_obj_color_frame.setFrameShadow(QFrame.Shadow.Raised)

        self.gridLayout_3.addWidget(self.w_obj_color_frame, 1, 2, 1, 1)

        self.w_cb_obj_color = QComboBox(self.groupBox_4)
        self.w_cb_obj_color.setObjectName(u"w_cb_obj_color")
        self.w_cb_obj_color.setMinimumSize(QSize(100, 0))

        self.gridLayout_3.addWidget(self.w_cb_obj_color, 1, 1, 1, 1)


        self.verticalLayout.addWidget(self.groupBox_4)

        self.groupBox_5 = QGroupBox(self.groupBox)
        self.groupBox_5.setObjectName(u"groupBox_5")
        self.gridLayout = QGridLayout(self.groupBox_5)
        self.gridLayout.setObjectName(u"gridLayout")
        self.w_cb_background_color = QComboBox(self.groupBox_5)
        self.w_cb_background_color.setObjectName(u"w_cb_background_color")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.w_cb_background_color.sizePolicy().hasHeightForWidth())
        self.w_cb_background_color.setSizePolicy(sizePolicy3)
        self.w_cb_background_color.setMinimumSize(QSize(100, 0))
        self.w_cb_background_color.setLayoutDirection(Qt.LayoutDirection.LeftToRight)

        self.gridLayout.addWidget(self.w_cb_background_color, 0, 1, 1, 1)

        self.w_background_color_frame = QFrame(self.groupBox_5)
        self.w_background_color_frame.setObjectName(u"w_background_color_frame")
        sizePolicy2.setHeightForWidth(self.w_background_color_frame.sizePolicy().hasHeightForWidth())
        self.w_background_color_frame.setSizePolicy(sizePolicy2)
        self.w_background_color_frame.setMinimumSize(QSize(0, 0))
        self.w_background_color_frame.setMaximumSize(QSize(25, 25))
        self.w_background_color_frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.w_background_color_frame.setFrameShadow(QFrame.Shadow.Raised)

        self.gridLayout.addWidget(self.w_background_color_frame, 0, 2, 1, 1)

        self.label_5 = QLabel(self.groupBox_5)
        self.label_5.setObjectName(u"label_5")

        self.gridLayout.addWidget(self.label_5, 0, 0, 1, 1)


        self.verticalLayout.addWidget(self.groupBox_5)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.w_pb_save_image = QPushButton(self.groupBox)
        self.w_pb_save_image.setObjectName(u"w_pb_save_image")

        self.verticalLayout.addWidget(self.w_pb_save_image)


        self.horizontalLayout.addWidget(self.groupBox)

        self.groupBox_2 = QGroupBox(self.centralwidget)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.verticalLayout_2 = QVBoxLayout(self.groupBox_2)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.vtk_widget = QVTKRenderWindowInteractor(self.groupBox_2)
        self.vtk_widget.setObjectName(u"vtk_widget")
        sizePolicy.setHeightForWidth(self.vtk_widget.sizePolicy().hasHeightForWidth())
        self.vtk_widget.setSizePolicy(sizePolicy)
        self.vtk_widget.setMinimumSize(QSize(400, 400))
        self.vtk_widget.setMaximumSize(QSize(16777215, 16777215))

        self.verticalLayout_2.addWidget(self.vtk_widget)

        self.widget_2 = QWidget(self.groupBox_2)
        self.widget_2.setObjectName(u"widget_2")
        self.horizontalLayout_2 = QHBoxLayout(self.widget_2)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.w_rb_plusX = QRadioButton(self.widget_2)
        self.w_rb_plusX.setObjectName(u"w_rb_plusX")

        self.horizontalLayout_2.addWidget(self.w_rb_plusX)

        self.w_rb_minusX = QRadioButton(self.widget_2)
        self.w_rb_minusX.setObjectName(u"w_rb_minusX")

        self.horizontalLayout_2.addWidget(self.w_rb_minusX)

        self.w_rb_plusY = QRadioButton(self.widget_2)
        self.w_rb_plusY.setObjectName(u"w_rb_plusY")

        self.horizontalLayout_2.addWidget(self.w_rb_plusY)

        self.w_rb_minusY = QRadioButton(self.widget_2)
        self.w_rb_minusY.setObjectName(u"w_rb_minusY")

        self.horizontalLayout_2.addWidget(self.w_rb_minusY)

        self.w_rb_plusZ = QRadioButton(self.widget_2)
        self.w_rb_plusZ.setObjectName(u"w_rb_plusZ")

        self.horizontalLayout_2.addWidget(self.w_rb_plusZ)

        self.w_rb_minusZ = QRadioButton(self.widget_2)
        self.w_rb_minusZ.setObjectName(u"w_rb_minusZ")

        self.horizontalLayout_2.addWidget(self.w_rb_minusZ)

        self.horizontalSpacer = QSpacerItem(330, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer)


        self.verticalLayout_2.addWidget(self.widget_2)


        self.horizontalLayout.addWidget(self.groupBox_2)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1086, 33))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.groupBox.setTitle(QCoreApplication.translate("MainWindow", u"View Settings and FIle Information", None))
        self.groupBox_3.setTitle(QCoreApplication.translate("MainWindow", u"DICOM Files", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"Plan", None))
        self.w_pb_dicom_plan_file.setText(QCoreApplication.translate("MainWindow", u"...", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Structure Set", None))
        self.w_pb_dicom_struct_file.setText(QCoreApplication.translate("MainWindow", u"...", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Select Color", None))
        self.groupBox_4.setTitle(QCoreApplication.translate("MainWindow", u"OBJ File", None))
        self.w_pb_obj_file.setText(QCoreApplication.translate("MainWindow", u"...", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"FIle Parth", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"Select Color", None))
        self.groupBox_5.setTitle(QCoreApplication.translate("MainWindow", u"Render Settings", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"Background Color", None))
        self.w_pb_save_image.setText(QCoreApplication.translate("MainWindow", u"Save Render Window Image", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("MainWindow", u"Render Window", None))
        self.w_rb_plusX.setText(QCoreApplication.translate("MainWindow", u"+X", None))
        self.w_rb_minusX.setText(QCoreApplication.translate("MainWindow", u"-X", None))
        self.w_rb_plusY.setText(QCoreApplication.translate("MainWindow", u"+Y", None))
        self.w_rb_minusY.setText(QCoreApplication.translate("MainWindow", u"-Y", None))
        self.w_rb_plusZ.setText(QCoreApplication.translate("MainWindow", u"+Z", None))
        self.w_rb_minusZ.setText(QCoreApplication.translate("MainWindow", u"-Z", None))
    # retranslateUi

