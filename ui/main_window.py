# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_window.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QDoubleSpinBox,
    QFrame, QGridLayout, QGroupBox, QHBoxLayout,
    QHeaderView, QLabel, QLineEdit, QMainWindow,
    QMenuBar, QPushButton, QRadioButton, QSizePolicy,
    QSlider, QSpacerItem, QStatusBar, QTabWidget,
    QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget)

from vtkmodules.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1268, 956)
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
        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setMinimumSize(QSize(400, 600))
        self.tabWidget.setMaximumSize(QSize(600, 16777215))
        self.tabWidget.setTabPosition(QTabWidget.TabPosition.North)
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        self.verticalLayout = QVBoxLayout(self.tab)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.groupBox_6 = QGroupBox(self.tab)
        self.groupBox_6.setObjectName(u"groupBox_6")
        self.gridLayout_4 = QGridLayout(self.groupBox_6)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.w_l_patient_last_name = QLabel(self.groupBox_6)
        self.w_l_patient_last_name.setObjectName(u"w_l_patient_last_name")

        self.gridLayout_4.addWidget(self.w_l_patient_last_name, 2, 2, 1, 1)

        self.label_15 = QLabel(self.groupBox_6)
        self.label_15.setObjectName(u"label_15")

        self.gridLayout_4.addWidget(self.label_15, 6, 0, 1, 3)

        self.label_12 = QLabel(self.groupBox_6)
        self.label_12.setObjectName(u"label_12")

        self.gridLayout_4.addWidget(self.label_12, 3, 0, 1, 1)

        self.w_ch_use_dicomrt = QCheckBox(self.groupBox_6)
        self.w_ch_use_dicomrt.setObjectName(u"w_ch_use_dicomrt")

        self.gridLayout_4.addWidget(self.w_ch_use_dicomrt, 8, 0, 1, 3)

        self.w_cb_plan_id = QComboBox(self.groupBox_6)
        self.w_cb_plan_id.setObjectName(u"w_cb_plan_id")

        self.gridLayout_4.addWidget(self.w_cb_plan_id, 3, 2, 1, 1)

        self.label_13 = QLabel(self.groupBox_6)
        self.label_13.setObjectName(u"label_13")

        self.gridLayout_4.addWidget(self.label_13, 2, 0, 1, 1)

        self.w_tw_beams = QTableWidget(self.groupBox_6)
        self.w_tw_beams.setObjectName(u"w_tw_beams")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.w_tw_beams.sizePolicy().hasHeightForWidth())
        self.w_tw_beams.setSizePolicy(sizePolicy1)

        self.gridLayout_4.addWidget(self.w_tw_beams, 7, 0, 1, 3)

        self.w_l_patient_first_name = QLabel(self.groupBox_6)
        self.w_l_patient_first_name.setObjectName(u"w_l_patient_first_name")

        self.gridLayout_4.addWidget(self.w_l_patient_first_name, 1, 2, 1, 1)

        self.label_11 = QLabel(self.groupBox_6)
        self.label_11.setObjectName(u"label_11")

        self.gridLayout_4.addWidget(self.label_11, 1, 0, 1, 1)

        self.label_17 = QLabel(self.groupBox_6)
        self.label_17.setObjectName(u"label_17")

        self.gridLayout_4.addWidget(self.label_17, 4, 0, 1, 1)

        self.w_gb_dicomrt_files = QGroupBox(self.groupBox_6)
        self.w_gb_dicomrt_files.setObjectName(u"w_gb_dicomrt_files")
        self.w_gb_dicomrt_files.setMinimumSize(QSize(0, 0))
        self.w_gb_dicomrt_files.setCheckable(False)
        self.gridLayout_2 = QGridLayout(self.w_gb_dicomrt_files)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.w_le_dcm_struct_file = QLineEdit(self.w_gb_dicomrt_files)
        self.w_le_dcm_struct_file.setObjectName(u"w_le_dcm_struct_file")
        self.w_le_dcm_struct_file.setEnabled(True)
        self.w_le_dcm_struct_file.setMinimumSize(QSize(100, 0))
        self.w_le_dcm_struct_file.setDragEnabled(False)
        self.w_le_dcm_struct_file.setReadOnly(True)

        self.gridLayout_2.addWidget(self.w_le_dcm_struct_file, 1, 1, 1, 1)

        self.w_pb_dcm_struct_file = QPushButton(self.w_gb_dicomrt_files)
        self.w_pb_dcm_struct_file.setObjectName(u"w_pb_dcm_struct_file")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.w_pb_dcm_struct_file.sizePolicy().hasHeightForWidth())
        self.w_pb_dcm_struct_file.setSizePolicy(sizePolicy2)
        self.w_pb_dcm_struct_file.setMaximumSize(QSize(25, 16777215))

        self.gridLayout_2.addWidget(self.w_pb_dcm_struct_file, 1, 2, 1, 1)

        self.w_pb_dcm_plan_file = QPushButton(self.w_gb_dicomrt_files)
        self.w_pb_dcm_plan_file.setObjectName(u"w_pb_dcm_plan_file")
        sizePolicy2.setHeightForWidth(self.w_pb_dcm_plan_file.sizePolicy().hasHeightForWidth())
        self.w_pb_dcm_plan_file.setSizePolicy(sizePolicy2)
        self.w_pb_dcm_plan_file.setMaximumSize(QSize(25, 16777215))

        self.gridLayout_2.addWidget(self.w_pb_dcm_plan_file, 0, 2, 1, 1)

        self.w_le_dcm_plan_file = QLineEdit(self.w_gb_dicomrt_files)
        self.w_le_dcm_plan_file.setObjectName(u"w_le_dcm_plan_file")
        self.w_le_dcm_plan_file.setEnabled(True)
        self.w_le_dcm_plan_file.setMinimumSize(QSize(100, 0))
        self.w_le_dcm_plan_file.setReadOnly(True)

        self.gridLayout_2.addWidget(self.w_le_dcm_plan_file, 0, 1, 1, 1)

        self.label = QLabel(self.w_gb_dicomrt_files)
        self.label.setObjectName(u"label")

        self.gridLayout_2.addWidget(self.label, 1, 0, 1, 1)

        self.label_6 = QLabel(self.w_gb_dicomrt_files)
        self.label_6.setObjectName(u"label_6")

        self.gridLayout_2.addWidget(self.label_6, 0, 0, 1, 1)


        self.gridLayout_4.addWidget(self.w_gb_dicomrt_files, 9, 0, 1, 3)

        self.w_cb_body_structure = QComboBox(self.groupBox_6)
        self.w_cb_body_structure.setObjectName(u"w_cb_body_structure")

        self.gridLayout_4.addWidget(self.w_cb_body_structure, 5, 2, 1, 1)

        self.label_9 = QLabel(self.groupBox_6)
        self.label_9.setObjectName(u"label_9")

        self.gridLayout_4.addWidget(self.label_9, 0, 0, 1, 1)

        self.w_le_patinet_id = QLineEdit(self.groupBox_6)
        self.w_le_patinet_id.setObjectName(u"w_le_patinet_id")

        self.gridLayout_4.addWidget(self.w_le_patinet_id, 0, 2, 1, 1)

        self.label_14 = QLabel(self.groupBox_6)
        self.label_14.setObjectName(u"label_14")

        self.gridLayout_4.addWidget(self.label_14, 5, 0, 1, 1)

        self.w_l_plan_isocenter = QLabel(self.groupBox_6)
        self.w_l_plan_isocenter.setObjectName(u"w_l_plan_isocenter")

        self.gridLayout_4.addWidget(self.w_l_plan_isocenter, 4, 1, 1, 2)


        self.verticalLayout.addWidget(self.groupBox_6)

        self.groupBox = QGroupBox(self.tab)
        self.groupBox.setObjectName(u"groupBox")
        self.gridLayout_6 = QGridLayout(self.groupBox)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.label_21 = QLabel(self.groupBox)
        self.label_21.setObjectName(u"label_21")

        self.gridLayout_6.addWidget(self.label_21, 2, 0, 1, 1)

        self.w_pb_get_map = QPushButton(self.groupBox)
        self.w_pb_get_map.setObjectName(u"w_pb_get_map")

        self.gridLayout_6.addWidget(self.w_pb_get_map, 7, 3, 1, 1)

        self.w_pb_api_ping = QPushButton(self.groupBox)
        self.w_pb_api_ping.setObjectName(u"w_pb_api_ping")

        self.gridLayout_6.addWidget(self.w_pb_api_ping, 0, 3, 1, 1)

        self.w_dsb_api_couch_buffer = QDoubleSpinBox(self.groupBox)
        self.w_dsb_api_couch_buffer.setObjectName(u"w_dsb_api_couch_buffer")
        self.w_dsb_api_couch_buffer.setDecimals(1)
        self.w_dsb_api_couch_buffer.setValue(2.000000000000000)

        self.gridLayout_6.addWidget(self.w_dsb_api_couch_buffer, 2, 1, 1, 2)

        self.w_ch_high_res = QCheckBox(self.groupBox)
        self.w_ch_high_res.setObjectName(u"w_ch_high_res")

        self.gridLayout_6.addWidget(self.w_ch_high_res, 4, 1, 1, 1)

        self.w_dsb_api_patient_buffer = QDoubleSpinBox(self.groupBox)
        self.w_dsb_api_patient_buffer.setObjectName(u"w_dsb_api_patient_buffer")
        self.w_dsb_api_patient_buffer.setDecimals(1)
        self.w_dsb_api_patient_buffer.setValue(2.000000000000000)

        self.gridLayout_6.addWidget(self.w_dsb_api_patient_buffer, 3, 1, 1, 2)

        self.w_cb_surface_for_map = QComboBox(self.groupBox)
        self.w_cb_surface_for_map.setObjectName(u"w_cb_surface_for_map")

        self.gridLayout_6.addWidget(self.w_cb_surface_for_map, 5, 1, 1, 2)

        self.label_22 = QLabel(self.groupBox)
        self.label_22.setObjectName(u"label_22")

        self.gridLayout_6.addWidget(self.label_22, 3, 0, 1, 1)

        self.label_20 = QLabel(self.groupBox)
        self.label_20.setObjectName(u"label_20")

        self.gridLayout_6.addWidget(self.label_20, 6, 0, 1, 1)

        self.label_23 = QLabel(self.groupBox)
        self.label_23.setObjectName(u"label_23")

        self.gridLayout_6.addWidget(self.label_23, 2, 3, 1, 1)

        self.label_18 = QLabel(self.groupBox)
        self.label_18.setObjectName(u"label_18")

        self.gridLayout_6.addWidget(self.label_18, 0, 0, 1, 1)

        self.label_24 = QLabel(self.groupBox)
        self.label_24.setObjectName(u"label_24")

        self.gridLayout_6.addWidget(self.label_24, 3, 3, 1, 1)

        self.w_l_api_status = QLabel(self.groupBox)
        self.w_l_api_status.setObjectName(u"w_l_api_status")

        self.gridLayout_6.addWidget(self.w_l_api_status, 0, 1, 1, 2)

        self.label_19 = QLabel(self.groupBox)
        self.label_19.setObjectName(u"label_19")

        self.gridLayout_6.addWidget(self.label_19, 5, 0, 1, 1)

        self.w_cb_treatment_room = QComboBox(self.groupBox)
        self.w_cb_treatment_room.setObjectName(u"w_cb_treatment_room")

        self.gridLayout_6.addWidget(self.w_cb_treatment_room, 6, 1, 1, 2)


        self.verticalLayout.addWidget(self.groupBox)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer_2)

        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        self.verticalLayout_3 = QVBoxLayout(self.tab_2)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.groupBox_7 = QGroupBox(self.tab_2)
        self.groupBox_7.setObjectName(u"groupBox_7")
        self.gridLayout_7 = QGridLayout(self.groupBox_7)
        self.gridLayout_7.setObjectName(u"gridLayout_7")
        self.w_fr_dcm_color = QFrame(self.groupBox_7)
        self.w_fr_dcm_color.setObjectName(u"w_fr_dcm_color")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.w_fr_dcm_color.sizePolicy().hasHeightForWidth())
        self.w_fr_dcm_color.setSizePolicy(sizePolicy3)
        self.w_fr_dcm_color.setMinimumSize(QSize(25, 25))
        self.w_fr_dcm_color.setMaximumSize(QSize(25, 25))
        self.w_fr_dcm_color.setFrameShape(QFrame.Shape.StyledPanel)
        self.w_fr_dcm_color.setFrameShadow(QFrame.Shadow.Raised)

        self.gridLayout_7.addWidget(self.w_fr_dcm_color, 0, 3, 1, 1)

        self.label_8 = QLabel(self.groupBox_7)
        self.label_8.setObjectName(u"label_8")

        self.gridLayout_7.addWidget(self.label_8, 2, 0, 1, 1)

        self.label_3 = QLabel(self.groupBox_7)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout_7.addWidget(self.label_3, 0, 0, 1, 1)

        self.w_hs_dcm_transparency = QSlider(self.groupBox_7)
        self.w_hs_dcm_transparency.setObjectName(u"w_hs_dcm_transparency")
        self.w_hs_dcm_transparency.setMaximum(100)
        self.w_hs_dcm_transparency.setValue(100)
        self.w_hs_dcm_transparency.setOrientation(Qt.Orientation.Horizontal)

        self.gridLayout_7.addWidget(self.w_hs_dcm_transparency, 2, 2, 1, 1)

        self.w_l_dcm_transparency = QLabel(self.groupBox_7)
        self.w_l_dcm_transparency.setObjectName(u"w_l_dcm_transparency")

        self.gridLayout_7.addWidget(self.w_l_dcm_transparency, 2, 3, 1, 1)

        self.w_pb_dcm_color = QPushButton(self.groupBox_7)
        self.w_pb_dcm_color.setObjectName(u"w_pb_dcm_color")

        self.gridLayout_7.addWidget(self.w_pb_dcm_color, 0, 1, 1, 2)


        self.verticalLayout_3.addWidget(self.groupBox_7)

        self.groupBox_8 = QGroupBox(self.tab_2)
        self.groupBox_8.setObjectName(u"groupBox_8")
        self.gridLayout_5 = QGridLayout(self.groupBox_8)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.w_pb_obj_color = QPushButton(self.groupBox_8)
        self.w_pb_obj_color.setObjectName(u"w_pb_obj_color")

        self.gridLayout_5.addWidget(self.w_pb_obj_color, 1, 1, 1, 1)

        self.w_hs_obj_transparency = QSlider(self.groupBox_8)
        self.w_hs_obj_transparency.setObjectName(u"w_hs_obj_transparency")
        self.w_hs_obj_transparency.setMaximum(100)
        self.w_hs_obj_transparency.setValue(100)
        self.w_hs_obj_transparency.setOrientation(Qt.Orientation.Horizontal)

        self.gridLayout_5.addWidget(self.w_hs_obj_transparency, 2, 1, 1, 1)

        self.w_fr_obj_color = QFrame(self.groupBox_8)
        self.w_fr_obj_color.setObjectName(u"w_fr_obj_color")
        sizePolicy3.setHeightForWidth(self.w_fr_obj_color.sizePolicy().hasHeightForWidth())
        self.w_fr_obj_color.setSizePolicy(sizePolicy3)
        self.w_fr_obj_color.setMinimumSize(QSize(25, 25))
        self.w_fr_obj_color.setMaximumSize(QSize(25, 25))
        self.w_fr_obj_color.setFrameShape(QFrame.Shape.StyledPanel)
        self.w_fr_obj_color.setFrameShadow(QFrame.Shadow.Raised)

        self.gridLayout_5.addWidget(self.w_fr_obj_color, 1, 2, 1, 1)

        self.label_4 = QLabel(self.groupBox_8)
        self.label_4.setObjectName(u"label_4")

        self.gridLayout_5.addWidget(self.label_4, 1, 0, 1, 1)

        self.label_10 = QLabel(self.groupBox_8)
        self.label_10.setObjectName(u"label_10")

        self.gridLayout_5.addWidget(self.label_10, 2, 0, 1, 1)

        self.w_l_obj_transparency = QLabel(self.groupBox_8)
        self.w_l_obj_transparency.setObjectName(u"w_l_obj_transparency")

        self.gridLayout_5.addWidget(self.w_l_obj_transparency, 2, 2, 1, 1)

        self.w_ch_use_obj = QCheckBox(self.groupBox_8)
        self.w_ch_use_obj.setObjectName(u"w_ch_use_obj")

        self.gridLayout_5.addWidget(self.w_ch_use_obj, 3, 0, 1, 1)

        self.w_gb_obj_file = QGroupBox(self.groupBox_8)
        self.w_gb_obj_file.setObjectName(u"w_gb_obj_file")
        self.gridLayout_3 = QGridLayout(self.w_gb_obj_file)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.w_pb_obj_file = QPushButton(self.w_gb_obj_file)
        self.w_pb_obj_file.setObjectName(u"w_pb_obj_file")
        sizePolicy2.setHeightForWidth(self.w_pb_obj_file.sizePolicy().hasHeightForWidth())
        self.w_pb_obj_file.setSizePolicy(sizePolicy2)
        self.w_pb_obj_file.setMaximumSize(QSize(25, 16777215))

        self.gridLayout_3.addWidget(self.w_pb_obj_file, 0, 2, 1, 1)

        self.w_le_obj_file = QLineEdit(self.w_gb_obj_file)
        self.w_le_obj_file.setObjectName(u"w_le_obj_file")
        self.w_le_obj_file.setMinimumSize(QSize(100, 0))

        self.gridLayout_3.addWidget(self.w_le_obj_file, 0, 1, 1, 1)

        self.label_2 = QLabel(self.w_gb_obj_file)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout_3.addWidget(self.label_2, 0, 0, 1, 1)

        self.widget = QWidget(self.w_gb_obj_file)
        self.widget.setObjectName(u"widget")
        self.horizontalLayout_3 = QHBoxLayout(self.widget)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.w_rb_hfs = QRadioButton(self.widget)
        self.w_rb_hfs.setObjectName(u"w_rb_hfs")

        self.horizontalLayout_3.addWidget(self.w_rb_hfs)

        self.w_rb_hfp = QRadioButton(self.widget)
        self.w_rb_hfp.setObjectName(u"w_rb_hfp")

        self.horizontalLayout_3.addWidget(self.w_rb_hfp)

        self.w_rb_ffs = QRadioButton(self.widget)
        self.w_rb_ffs.setObjectName(u"w_rb_ffs")

        self.horizontalLayout_3.addWidget(self.w_rb_ffs)

        self.w_rb_ffp = QRadioButton(self.widget)
        self.w_rb_ffp.setObjectName(u"w_rb_ffp")

        self.horizontalLayout_3.addWidget(self.w_rb_ffp)


        self.gridLayout_3.addWidget(self.widget, 1, 1, 1, 1)

        self.label_7 = QLabel(self.w_gb_obj_file)
        self.label_7.setObjectName(u"label_7")

        self.gridLayout_3.addWidget(self.label_7, 1, 0, 1, 1)


        self.gridLayout_5.addWidget(self.w_gb_obj_file, 4, 0, 1, 3)


        self.verticalLayout_3.addWidget(self.groupBox_8)

        self.groupBox_9 = QGroupBox(self.tab_2)
        self.groupBox_9.setObjectName(u"groupBox_9")
        self.gridLayout = QGridLayout(self.groupBox_9)
        self.gridLayout.setObjectName(u"gridLayout")
        self.w_fr_background_color = QFrame(self.groupBox_9)
        self.w_fr_background_color.setObjectName(u"w_fr_background_color")
        sizePolicy3.setHeightForWidth(self.w_fr_background_color.sizePolicy().hasHeightForWidth())
        self.w_fr_background_color.setSizePolicy(sizePolicy3)
        self.w_fr_background_color.setMinimumSize(QSize(25, 25))
        self.w_fr_background_color.setMaximumSize(QSize(25, 25))
        self.w_fr_background_color.setFrameShape(QFrame.Shape.StyledPanel)
        self.w_fr_background_color.setFrameShadow(QFrame.Shadow.Raised)

        self.gridLayout.addWidget(self.w_fr_background_color, 0, 2, 1, 1)

        self.label_5 = QLabel(self.groupBox_9)
        self.label_5.setObjectName(u"label_5")

        self.gridLayout.addWidget(self.label_5, 0, 0, 1, 1)

        self.w_pb_background_color = QPushButton(self.groupBox_9)
        self.w_pb_background_color.setObjectName(u"w_pb_background_color")

        self.gridLayout.addWidget(self.w_pb_background_color, 0, 1, 1, 1)

        self.label_16 = QLabel(self.groupBox_9)
        self.label_16.setObjectName(u"label_16")

        self.gridLayout.addWidget(self.label_16, 1, 0, 1, 1)

        self.widget_2 = QWidget(self.groupBox_9)
        self.widget_2.setObjectName(u"widget_2")
        sizePolicy4 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.widget_2.sizePolicy().hasHeightForWidth())
        self.widget_2.setSizePolicy(sizePolicy4)
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


        self.gridLayout.addWidget(self.widget_2, 1, 1, 1, 1)


        self.verticalLayout_3.addWidget(self.groupBox_9)

        self.verticalSpacer = QSpacerItem(373, 226, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_3.addItem(self.verticalSpacer)

        self.w_pb_save_image = QPushButton(self.tab_2)
        self.w_pb_save_image.setObjectName(u"w_pb_save_image")

        self.verticalLayout_3.addWidget(self.w_pb_save_image)

        self.tabWidget.addTab(self.tab_2, "")

        self.horizontalLayout.addWidget(self.tabWidget)

        self.tabWidget_2 = QTabWidget(self.centralwidget)
        self.tabWidget_2.setObjectName(u"tabWidget_2")
        self.tab_3 = QWidget()
        self.tab_3.setObjectName(u"tab_3")
        self.verticalLayout_4 = QVBoxLayout(self.tab_3)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.groupBox_3 = QGroupBox(self.tab_3)
        self.groupBox_3.setObjectName(u"groupBox_3")

        self.verticalLayout_4.addWidget(self.groupBox_3)

        self.tabWidget_2.addTab(self.tab_3, "")
        self.tab_4 = QWidget()
        self.tab_4.setObjectName(u"tab_4")
        self.horizontalLayout_4 = QHBoxLayout(self.tab_4)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.groupBox_2 = QGroupBox(self.tab_4)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.verticalLayout_2 = QVBoxLayout(self.groupBox_2)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.vtk_widget = QVTKRenderWindowInteractor(self.groupBox_2)
        self.vtk_widget.setObjectName(u"vtk_widget")
        sizePolicy.setHeightForWidth(self.vtk_widget.sizePolicy().hasHeightForWidth())
        self.vtk_widget.setSizePolicy(sizePolicy)
        self.vtk_widget.setMinimumSize(QSize(800, 800))
        self.vtk_widget.setMaximumSize(QSize(16777215, 16777215))

        self.verticalLayout_2.addWidget(self.vtk_widget)


        self.horizontalLayout_4.addWidget(self.groupBox_2)

        self.tabWidget_2.addTab(self.tab_4, "")

        self.horizontalLayout.addWidget(self.tabWidget_2)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1268, 33))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        self.tabWidget.setCurrentIndex(0)
        self.tabWidget_2.setCurrentIndex(1)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.groupBox_6.setTitle(QCoreApplication.translate("MainWindow", u"Patient Information", None))
        self.w_l_patient_last_name.setText("")
        self.label_15.setText(QCoreApplication.translate("MainWindow", u"Beams", None))
        self.label_12.setText(QCoreApplication.translate("MainWindow", u"Plan ID:", None))
        self.w_ch_use_dicomrt.setText(QCoreApplication.translate("MainWindow", u"Use Dicom RT Files", None))
        self.label_13.setText(QCoreApplication.translate("MainWindow", u"Last Name:", None))
        self.w_l_patient_first_name.setText("")
        self.label_11.setText(QCoreApplication.translate("MainWindow", u"First Name:", None))
        self.label_17.setText(QCoreApplication.translate("MainWindow", u"Isocenter:", None))
        self.w_gb_dicomrt_files.setTitle(QCoreApplication.translate("MainWindow", u"DICOM Files", None))
        self.w_pb_dcm_struct_file.setText(QCoreApplication.translate("MainWindow", u"...", None))
        self.w_pb_dcm_plan_file.setText(QCoreApplication.translate("MainWindow", u"...", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Structure Set", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"Plan", None))
        self.label_9.setText(QCoreApplication.translate("MainWindow", u"Patient ID:", None))
        self.label_14.setText(QCoreApplication.translate("MainWindow", u"Body Structure:", None))
        self.w_l_plan_isocenter.setText("")
        self.groupBox.setTitle(QCoreApplication.translate("MainWindow", u"MapRT", None))
        self.label_21.setText(QCoreApplication.translate("MainWindow", u"Couch Buffer:", None))
        self.w_pb_get_map.setText(QCoreApplication.translate("MainWindow", u"Get Map", None))
        self.w_pb_api_ping.setText(QCoreApplication.translate("MainWindow", u"Ping API", None))
        self.w_ch_high_res.setText(QCoreApplication.translate("MainWindow", u"High Resolution Map", None))
        self.label_22.setText(QCoreApplication.translate("MainWindow", u"Patient Buffer:", None))
        self.label_20.setText(QCoreApplication.translate("MainWindow", u"Treatment Room", None))
        self.label_23.setText(QCoreApplication.translate("MainWindow", u"cm", None))
        self.label_18.setText(QCoreApplication.translate("MainWindow", u"API Status:", None))
        self.label_24.setText(QCoreApplication.translate("MainWindow", u"cm", None))
        self.w_l_api_status.setText("")
        self.label_19.setText(QCoreApplication.translate("MainWindow", u"Surface:", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QCoreApplication.translate("MainWindow", u"Patient Context", None))
        self.groupBox_7.setTitle(QCoreApplication.translate("MainWindow", u"DICOM", None))
        self.label_8.setText(QCoreApplication.translate("MainWindow", u"Transparency:", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Color:", None))
        self.w_l_dcm_transparency.setText(QCoreApplication.translate("MainWindow", u"100", None))
        self.w_pb_dcm_color.setText(QCoreApplication.translate("MainWindow", u"Select Color", None))
        self.groupBox_8.setTitle(QCoreApplication.translate("MainWindow", u"OBJ", None))
        self.w_pb_obj_color.setText(QCoreApplication.translate("MainWindow", u"Select Color", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"Color:", None))
        self.label_10.setText(QCoreApplication.translate("MainWindow", u"Transparency:", None))
        self.w_l_obj_transparency.setText(QCoreApplication.translate("MainWindow", u"100", None))
        self.w_ch_use_obj.setText(QCoreApplication.translate("MainWindow", u"Use .obj File", None))
        self.w_gb_obj_file.setTitle(QCoreApplication.translate("MainWindow", u"OBJ File", None))
        self.w_pb_obj_file.setText(QCoreApplication.translate("MainWindow", u"...", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"File Path       ", None))
        self.w_rb_hfs.setText(QCoreApplication.translate("MainWindow", u"HFS", None))
        self.w_rb_hfp.setText(QCoreApplication.translate("MainWindow", u"HFP", None))
        self.w_rb_ffs.setText(QCoreApplication.translate("MainWindow", u"FFS", None))
        self.w_rb_ffp.setText(QCoreApplication.translate("MainWindow", u"FFP", None))
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"Orientation:", None))
        self.groupBox_9.setTitle(QCoreApplication.translate("MainWindow", u"Scene", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"Color:", None))
        self.w_pb_background_color.setText(QCoreApplication.translate("MainWindow", u"Select Color", None))
        self.label_16.setText(QCoreApplication.translate("MainWindow", u"View From", None))
        self.w_rb_plusX.setText(QCoreApplication.translate("MainWindow", u"+X", None))
        self.w_rb_minusX.setText(QCoreApplication.translate("MainWindow", u"-X", None))
        self.w_rb_plusY.setText(QCoreApplication.translate("MainWindow", u"+Y", None))
        self.w_rb_minusY.setText(QCoreApplication.translate("MainWindow", u"-Y", None))
        self.w_rb_plusZ.setText(QCoreApplication.translate("MainWindow", u"+Z", None))
        self.w_rb_minusZ.setText(QCoreApplication.translate("MainWindow", u"-Z", None))
        self.w_pb_save_image.setText(QCoreApplication.translate("MainWindow", u"Save Render Window Image", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QCoreApplication.translate("MainWindow", u"3D View Settings", None))
        self.groupBox_3.setTitle(QCoreApplication.translate("MainWindow", u"MapRT Collision Map", None))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.tab_3), QCoreApplication.translate("MainWindow", u"Map View", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("MainWindow", u"Render Window", None))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.tab_4), QCoreApplication.translate("MainWindow", u"3D View", None))
    # retranslateUi

