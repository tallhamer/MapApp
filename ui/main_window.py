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
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QDoubleSpinBox,
    QFormLayout, QFrame, QGridLayout, QGroupBox,
    QHBoxLayout, QHeaderView, QLabel, QLineEdit,
    QMainWindow, QPushButton, QRadioButton, QSizePolicy,
    QSlider, QSpacerItem, QStatusBar, QTabWidget,
    QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget)

from vtkmodules.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1268, 956)
        MainWindow.setMinimumSize(QSize(0, 0))
        self.exit_action = QAction(MainWindow)
        self.exit_action.setObjectName(u"exit_action")
        self.settings_action = QAction(MainWindow)
        self.settings_action.setObjectName(u"settings_action")
        self.about_action = QAction(MainWindow)
        self.about_action.setObjectName(u"about_action")
        self.actionCollision_Map = QAction(MainWindow)
        self.actionCollision_Map.setObjectName(u"actionCollision_Map")
        self.actionView_From = QAction(MainWindow)
        self.actionView_From.setObjectName(u"actionView_From")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.horizontalLayout = QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.w_tw_patient_settings = QTabWidget(self.centralwidget)
        self.w_tw_patient_settings.setObjectName(u"w_tw_patient_settings")
        self.w_tw_patient_settings.setMinimumSize(QSize(400, 600))
        self.w_tw_patient_settings.setMaximumSize(QSize(600, 16777215))
        self.w_tw_patient_settings.setTabPosition(QTabWidget.TabPosition.North)
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        self.verticalLayout = QVBoxLayout(self.tab)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.groupBox_6 = QGroupBox(self.tab)
        self.groupBox_6.setObjectName(u"groupBox_6")
        self.gridLayout_4 = QGridLayout(self.groupBox_6)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
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
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.w_pb_dcm_struct_file.sizePolicy().hasHeightForWidth())
        self.w_pb_dcm_struct_file.setSizePolicy(sizePolicy1)
        self.w_pb_dcm_struct_file.setMaximumSize(QSize(25, 16777215))

        self.gridLayout_2.addWidget(self.w_pb_dcm_struct_file, 1, 2, 1, 1)

        self.w_pb_dcm_plan_file = QPushButton(self.w_gb_dicomrt_files)
        self.w_pb_dcm_plan_file.setObjectName(u"w_pb_dcm_plan_file")
        sizePolicy1.setHeightForWidth(self.w_pb_dcm_plan_file.sizePolicy().hasHeightForWidth())
        self.w_pb_dcm_plan_file.setSizePolicy(sizePolicy1)
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


        self.gridLayout_4.addWidget(self.w_gb_dicomrt_files, 10, 0, 1, 4)

        self.w_tw_beams = QTableWidget(self.groupBox_6)
        self.w_tw_beams.setObjectName(u"w_tw_beams")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.w_tw_beams.sizePolicy().hasHeightForWidth())
        self.w_tw_beams.setSizePolicy(sizePolicy2)

        self.gridLayout_4.addWidget(self.w_tw_beams, 8, 0, 1, 4)

        self.w_pb_esapi_search = QPushButton(self.groupBox_6)
        self.w_pb_esapi_search.setObjectName(u"w_pb_esapi_search")

        self.gridLayout_4.addWidget(self.w_pb_esapi_search, 0, 3, 1, 1)

        self.label_11 = QLabel(self.groupBox_6)
        self.label_11.setObjectName(u"label_11")

        self.gridLayout_4.addWidget(self.label_11, 1, 0, 1, 1)

        self.label_12 = QLabel(self.groupBox_6)
        self.label_12.setObjectName(u"label_12")

        self.gridLayout_4.addWidget(self.label_12, 4, 0, 1, 1)

        self.w_ch_use_dicomrt = QCheckBox(self.groupBox_6)
        self.w_ch_use_dicomrt.setObjectName(u"w_ch_use_dicomrt")

        self.gridLayout_4.addWidget(self.w_ch_use_dicomrt, 9, 0, 1, 4)

        self.label_17 = QLabel(self.groupBox_6)
        self.label_17.setObjectName(u"label_17")

        self.gridLayout_4.addWidget(self.label_17, 5, 0, 1, 1)

        self.label_14 = QLabel(self.groupBox_6)
        self.label_14.setObjectName(u"label_14")

        self.gridLayout_4.addWidget(self.label_14, 6, 0, 1, 1)

        self.label_15 = QLabel(self.groupBox_6)
        self.label_15.setObjectName(u"label_15")

        self.gridLayout_4.addWidget(self.label_15, 7, 0, 1, 4)

        self.label_13 = QLabel(self.groupBox_6)
        self.label_13.setObjectName(u"label_13")

        self.gridLayout_4.addWidget(self.label_13, 2, 0, 1, 1)

        self.label_9 = QLabel(self.groupBox_6)
        self.label_9.setObjectName(u"label_9")

        self.gridLayout_4.addWidget(self.label_9, 0, 0, 1, 1)

        self.label_26 = QLabel(self.groupBox_6)
        self.label_26.setObjectName(u"label_26")

        self.gridLayout_4.addWidget(self.label_26, 3, 0, 1, 1)

        self.w_cb_course_id = QComboBox(self.groupBox_6)
        self.w_cb_course_id.setObjectName(u"w_cb_course_id")

        self.gridLayout_4.addWidget(self.w_cb_course_id, 3, 1, 1, 2)

        self.w_cb_plan_id = QComboBox(self.groupBox_6)
        self.w_cb_plan_id.setObjectName(u"w_cb_plan_id")

        self.gridLayout_4.addWidget(self.w_cb_plan_id, 4, 1, 1, 2)

        self.w_cb_body_structure = QComboBox(self.groupBox_6)
        self.w_cb_body_structure.setObjectName(u"w_cb_body_structure")

        self.gridLayout_4.addWidget(self.w_cb_body_structure, 6, 1, 1, 2)

        self.w_le_patinet_id = QLineEdit(self.groupBox_6)
        self.w_le_patinet_id.setObjectName(u"w_le_patinet_id")

        self.gridLayout_4.addWidget(self.w_le_patinet_id, 0, 1, 1, 2)

        self.w_l_patient_first_name = QLabel(self.groupBox_6)
        self.w_l_patient_first_name.setObjectName(u"w_l_patient_first_name")

        self.gridLayout_4.addWidget(self.w_l_patient_first_name, 1, 1, 1, 2)

        self.w_l_patient_last_name = QLabel(self.groupBox_6)
        self.w_l_patient_last_name.setObjectName(u"w_l_patient_last_name")

        self.gridLayout_4.addWidget(self.w_l_patient_last_name, 2, 1, 1, 2)

        self.w_l_plan_isocenter = QLabel(self.groupBox_6)
        self.w_l_plan_isocenter.setObjectName(u"w_l_plan_isocenter")

        self.gridLayout_4.addWidget(self.w_l_plan_isocenter, 5, 1, 1, 3)


        self.verticalLayout.addWidget(self.groupBox_6)

        self.groupBox = QGroupBox(self.tab)
        self.groupBox.setObjectName(u"groupBox")
        self.gridLayout_6 = QGridLayout(self.groupBox)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.label_21 = QLabel(self.groupBox)
        self.label_21.setObjectName(u"label_21")

        self.gridLayout_6.addWidget(self.label_21, 2, 0, 1, 1)

        self.w_l_api_status = QLabel(self.groupBox)
        self.w_l_api_status.setObjectName(u"w_l_api_status")

        self.gridLayout_6.addWidget(self.w_l_api_status, 0, 1, 1, 2)

        self.w_cb_treatment_room = QComboBox(self.groupBox)
        self.w_cb_treatment_room.setObjectName(u"w_cb_treatment_room")

        self.gridLayout_6.addWidget(self.w_cb_treatment_room, 8, 1, 1, 2)

        self.label_28 = QLabel(self.groupBox)
        self.label_28.setObjectName(u"label_28")

        self.gridLayout_6.addWidget(self.label_28, 4, 1, 1, 1)

        self.w_pb_get_map = QPushButton(self.groupBox)
        self.w_pb_get_map.setObjectName(u"w_pb_get_map")
        self.w_pb_get_map.setEnabled(False)

        self.gridLayout_6.addWidget(self.w_pb_get_map, 9, 3, 1, 1)

        self.label_22 = QLabel(self.groupBox)
        self.label_22.setObjectName(u"label_22")

        self.gridLayout_6.addWidget(self.label_22, 3, 0, 1, 1)

        self.label_24 = QLabel(self.groupBox)
        self.label_24.setObjectName(u"label_24")

        self.gridLayout_6.addWidget(self.label_24, 3, 3, 1, 1)

        self.w_cb_surface_for_map = QComboBox(self.groupBox)
        self.w_cb_surface_for_map.setObjectName(u"w_cb_surface_for_map")

        self.gridLayout_6.addWidget(self.w_cb_surface_for_map, 7, 1, 1, 2)

        self.label_20 = QLabel(self.groupBox)
        self.label_20.setObjectName(u"label_20")

        self.gridLayout_6.addWidget(self.label_20, 8, 0, 1, 1)

        self.label_23 = QLabel(self.groupBox)
        self.label_23.setObjectName(u"label_23")

        self.gridLayout_6.addWidget(self.label_23, 2, 3, 1, 1)

        self.label_18 = QLabel(self.groupBox)
        self.label_18.setObjectName(u"label_18")

        self.gridLayout_6.addWidget(self.label_18, 0, 0, 1, 1)

        self.w_pb_fetch_api_data = QPushButton(self.groupBox)
        self.w_pb_fetch_api_data.setObjectName(u"w_pb_fetch_api_data")

        self.gridLayout_6.addWidget(self.w_pb_fetch_api_data, 0, 3, 1, 1)

        self.label_19 = QLabel(self.groupBox)
        self.label_19.setObjectName(u"label_19")

        self.gridLayout_6.addWidget(self.label_19, 7, 0, 1, 1)

        self.label_29 = QLabel(self.groupBox)
        self.label_29.setObjectName(u"label_29")

        self.gridLayout_6.addWidget(self.label_29, 5, 1, 1, 1)

        self.label_27 = QLabel(self.groupBox)
        self.label_27.setObjectName(u"label_27")

        self.gridLayout_6.addWidget(self.label_27, 4, 0, 1, 1)

        self.label_30 = QLabel(self.groupBox)
        self.label_30.setObjectName(u"label_30")

        self.gridLayout_6.addWidget(self.label_30, 6, 1, 1, 1)

        self.w_dsb_surface_shift_x = QDoubleSpinBox(self.groupBox)
        self.w_dsb_surface_shift_x.setObjectName(u"w_dsb_surface_shift_x")
        self.w_dsb_surface_shift_x.setMinimum(-100.000000000000000)
        self.w_dsb_surface_shift_x.setSingleStep(0.500000000000000)
        self.w_dsb_surface_shift_x.setValue(0.000000000000000)

        self.gridLayout_6.addWidget(self.w_dsb_surface_shift_x, 4, 2, 1, 1)

        self.w_dsb_surface_shift_y = QDoubleSpinBox(self.groupBox)
        self.w_dsb_surface_shift_y.setObjectName(u"w_dsb_surface_shift_y")
        self.w_dsb_surface_shift_y.setMinimum(-100.000000000000000)
        self.w_dsb_surface_shift_y.setMaximum(100.000000000000000)
        self.w_dsb_surface_shift_y.setSingleStep(0.500000000000000)

        self.gridLayout_6.addWidget(self.w_dsb_surface_shift_y, 5, 2, 1, 1)

        self.w_dsb_surface_shift_z = QDoubleSpinBox(self.groupBox)
        self.w_dsb_surface_shift_z.setObjectName(u"w_dsb_surface_shift_z")
        self.w_dsb_surface_shift_z.setMinimum(-100.000000000000000)
        self.w_dsb_surface_shift_z.setMaximum(100.000000000000000)
        self.w_dsb_surface_shift_z.setSingleStep(0.500000000000000)

        self.gridLayout_6.addWidget(self.w_dsb_surface_shift_z, 6, 2, 1, 1)

        self.w_pb_obj_file = QPushButton(self.groupBox)
        self.w_pb_obj_file.setObjectName(u"w_pb_obj_file")

        self.gridLayout_6.addWidget(self.w_pb_obj_file, 7, 3, 1, 1)

        self.label_2 = QLabel(self.groupBox)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout_6.addWidget(self.label_2, 4, 3, 1, 1)

        self.label_7 = QLabel(self.groupBox)
        self.label_7.setObjectName(u"label_7")

        self.gridLayout_6.addWidget(self.label_7, 5, 3, 1, 1)

        self.label_31 = QLabel(self.groupBox)
        self.label_31.setObjectName(u"label_31")

        self.gridLayout_6.addWidget(self.label_31, 6, 3, 1, 1)

        self.w_dsb_api_couch_buffer = QDoubleSpinBox(self.groupBox)
        self.w_dsb_api_couch_buffer.setObjectName(u"w_dsb_api_couch_buffer")
        self.w_dsb_api_couch_buffer.setDecimals(1)
        self.w_dsb_api_couch_buffer.setValue(2.000000000000000)

        self.gridLayout_6.addWidget(self.w_dsb_api_couch_buffer, 2, 1, 1, 2)

        self.w_dsb_api_patient_buffer = QDoubleSpinBox(self.groupBox)
        self.w_dsb_api_patient_buffer.setObjectName(u"w_dsb_api_patient_buffer")
        self.w_dsb_api_patient_buffer.setDecimals(1)
        self.w_dsb_api_patient_buffer.setValue(2.000000000000000)

        self.gridLayout_6.addWidget(self.w_dsb_api_patient_buffer, 3, 1, 1, 2)


        self.verticalLayout.addWidget(self.groupBox)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer_2)

        self.w_tw_patient_settings.addTab(self.tab, "")
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

        self.w_hs_dcm_opacity = QSlider(self.groupBox_7)
        self.w_hs_dcm_opacity.setObjectName(u"w_hs_dcm_opacity")
        self.w_hs_dcm_opacity.setMaximum(100)
        self.w_hs_dcm_opacity.setValue(100)
        self.w_hs_dcm_opacity.setOrientation(Qt.Orientation.Horizontal)

        self.gridLayout_7.addWidget(self.w_hs_dcm_opacity, 2, 2, 1, 1)

        self.w_l_dcm_opacity = QLabel(self.groupBox_7)
        self.w_l_dcm_opacity.setObjectName(u"w_l_dcm_opacity")

        self.gridLayout_7.addWidget(self.w_l_dcm_opacity, 2, 3, 1, 1)

        self.w_pb_dcm_color = QPushButton(self.groupBox_7)
        self.w_pb_dcm_color.setObjectName(u"w_pb_dcm_color")

        self.gridLayout_7.addWidget(self.w_pb_dcm_color, 0, 1, 1, 2)


        self.verticalLayout_3.addWidget(self.groupBox_7)

        self.groupBox_8 = QGroupBox(self.tab_2)
        self.groupBox_8.setObjectName(u"groupBox_8")
        self.gridLayout_3 = QGridLayout(self.groupBox_8)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.label_4 = QLabel(self.groupBox_8)
        self.label_4.setObjectName(u"label_4")

        self.gridLayout_3.addWidget(self.label_4, 0, 0, 1, 1)

        self.w_pb_obj_color = QPushButton(self.groupBox_8)
        self.w_pb_obj_color.setObjectName(u"w_pb_obj_color")

        self.gridLayout_3.addWidget(self.w_pb_obj_color, 0, 1, 1, 1)

        self.w_fr_obj_color = QFrame(self.groupBox_8)
        self.w_fr_obj_color.setObjectName(u"w_fr_obj_color")
        sizePolicy3.setHeightForWidth(self.w_fr_obj_color.sizePolicy().hasHeightForWidth())
        self.w_fr_obj_color.setSizePolicy(sizePolicy3)
        self.w_fr_obj_color.setMinimumSize(QSize(25, 25))
        self.w_fr_obj_color.setMaximumSize(QSize(25, 25))
        self.w_fr_obj_color.setFrameShape(QFrame.Shape.StyledPanel)
        self.w_fr_obj_color.setFrameShadow(QFrame.Shadow.Raised)

        self.gridLayout_3.addWidget(self.w_fr_obj_color, 0, 2, 1, 1)

        self.label_10 = QLabel(self.groupBox_8)
        self.label_10.setObjectName(u"label_10")
        self.label_10.setMaximumSize(QSize(16777215, 16777215))

        self.gridLayout_3.addWidget(self.label_10, 1, 0, 1, 1)

        self.w_hs_obj_opacity = QSlider(self.groupBox_8)
        self.w_hs_obj_opacity.setObjectName(u"w_hs_obj_opacity")
        self.w_hs_obj_opacity.setMaximum(100)
        self.w_hs_obj_opacity.setValue(100)
        self.w_hs_obj_opacity.setOrientation(Qt.Orientation.Horizontal)

        self.gridLayout_3.addWidget(self.w_hs_obj_opacity, 1, 1, 1, 1)

        self.w_l_obj_opacity = QLabel(self.groupBox_8)
        self.w_l_obj_opacity.setObjectName(u"w_l_obj_opacity")

        self.gridLayout_3.addWidget(self.w_l_obj_opacity, 1, 2, 1, 1)


        self.verticalLayout_3.addWidget(self.groupBox_8)

        self.groupBox_9 = QGroupBox(self.tab_2)
        self.groupBox_9.setObjectName(u"groupBox_9")
        self.gridLayout = QGridLayout(self.groupBox_9)
        self.gridLayout.setObjectName(u"gridLayout")
        self.label_33 = QLabel(self.groupBox_9)
        self.label_33.setObjectName(u"label_33")

        self.gridLayout.addWidget(self.label_33, 2, 0, 1, 1)

        self.w_pb_laser_color = QPushButton(self.groupBox_9)
        self.w_pb_laser_color.setObjectName(u"w_pb_laser_color")

        self.gridLayout.addWidget(self.w_pb_laser_color, 1, 1, 1, 1)

        self.w_l_laser_opacity = QLabel(self.groupBox_9)
        self.w_l_laser_opacity.setObjectName(u"w_l_laser_opacity")

        self.gridLayout.addWidget(self.w_l_laser_opacity, 2, 2, 1, 1)

        self.label_5 = QLabel(self.groupBox_9)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setMaximumSize(QSize(100, 16777215))

        self.gridLayout.addWidget(self.label_5, 0, 0, 1, 1)

        self.w_fr_laser_color = QFrame(self.groupBox_9)
        self.w_fr_laser_color.setObjectName(u"w_fr_laser_color")
        sizePolicy3.setHeightForWidth(self.w_fr_laser_color.sizePolicy().hasHeightForWidth())
        self.w_fr_laser_color.setSizePolicy(sizePolicy3)
        self.w_fr_laser_color.setMinimumSize(QSize(25, 25))
        self.w_fr_laser_color.setMaximumSize(QSize(25, 25))
        self.w_fr_laser_color.setFrameShape(QFrame.Shape.StyledPanel)
        self.w_fr_laser_color.setFrameShadow(QFrame.Shadow.Raised)

        self.gridLayout.addWidget(self.w_fr_laser_color, 1, 2, 1, 1)

        self.w_pb_background_color = QPushButton(self.groupBox_9)
        self.w_pb_background_color.setObjectName(u"w_pb_background_color")
        self.w_pb_background_color.setMaximumSize(QSize(16777215, 16777215))

        self.gridLayout.addWidget(self.w_pb_background_color, 0, 1, 1, 1)

        self.w_hs_laser_opacity = QSlider(self.groupBox_9)
        self.w_hs_laser_opacity.setObjectName(u"w_hs_laser_opacity")
        self.w_hs_laser_opacity.setMaximum(100)
        self.w_hs_laser_opacity.setValue(100)
        self.w_hs_laser_opacity.setOrientation(Qt.Orientation.Horizontal)

        self.gridLayout.addWidget(self.w_hs_laser_opacity, 2, 1, 1, 1)

        self.label_16 = QLabel(self.groupBox_9)
        self.label_16.setObjectName(u"label_16")

        self.gridLayout.addWidget(self.label_16, 3, 0, 1, 1)

        self.label_32 = QLabel(self.groupBox_9)
        self.label_32.setObjectName(u"label_32")

        self.gridLayout.addWidget(self.label_32, 1, 0, 1, 1)

        self.w_fr_background_color = QFrame(self.groupBox_9)
        self.w_fr_background_color.setObjectName(u"w_fr_background_color")
        sizePolicy3.setHeightForWidth(self.w_fr_background_color.sizePolicy().hasHeightForWidth())
        self.w_fr_background_color.setSizePolicy(sizePolicy3)
        self.w_fr_background_color.setMinimumSize(QSize(25, 25))
        self.w_fr_background_color.setMaximumSize(QSize(25, 25))
        self.w_fr_background_color.setFrameShape(QFrame.Shape.StyledPanel)
        self.w_fr_background_color.setFrameShadow(QFrame.Shadow.Raised)

        self.gridLayout.addWidget(self.w_fr_background_color, 0, 2, 1, 1)

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


        self.gridLayout.addWidget(self.widget_2, 4, 0, 1, 3)


        self.verticalLayout_3.addWidget(self.groupBox_9)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_3.addItem(self.verticalSpacer)

        self.w_pb_save_image = QPushButton(self.tab_2)
        self.w_pb_save_image.setObjectName(u"w_pb_save_image")

        self.verticalLayout_3.addWidget(self.w_pb_save_image)

        self.w_tw_patient_settings.addTab(self.tab_2, "")

        self.horizontalLayout.addWidget(self.w_tw_patient_settings)

        self.w_tw_visualizations = QTabWidget(self.centralwidget)
        self.w_tw_visualizations.setObjectName(u"w_tw_visualizations")
        self.tab_3 = QWidget()
        self.tab_3.setObjectName(u"tab_3")
        self.verticalLayout_4 = QVBoxLayout(self.tab_3)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.w_gb_collision_map = QGroupBox(self.tab_3)
        self.w_gb_collision_map.setObjectName(u"w_gb_collision_map")
        self.verticalLayout_5 = QVBoxLayout(self.w_gb_collision_map)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.w_w_collision_map = QWidget(self.w_gb_collision_map)
        self.w_w_collision_map.setObjectName(u"w_w_collision_map")

        self.verticalLayout_5.addWidget(self.w_w_collision_map)

        self.widget_4 = QWidget(self.w_gb_collision_map)
        self.widget_4.setObjectName(u"widget_4")
        sizePolicy5 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Minimum)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.widget_4.sizePolicy().hasHeightForWidth())
        self.widget_4.setSizePolicy(sizePolicy5)
        self.formLayout = QFormLayout(self.widget_4)
        self.formLayout.setObjectName(u"formLayout")
        self.label_25 = QLabel(self.widget_4)
        self.label_25.setObjectName(u"label_25")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.label_25)

        self.w_cb_current_map = QComboBox(self.widget_4)
        self.w_cb_current_map.setObjectName(u"w_cb_current_map")

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.w_cb_current_map)


        self.verticalLayout_5.addWidget(self.widget_4)


        self.verticalLayout_4.addWidget(self.w_gb_collision_map)

        self.w_tw_visualizations.addTab(self.tab_3, "")
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
        sizePolicy6 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        sizePolicy6.setHorizontalStretch(0)
        sizePolicy6.setVerticalStretch(0)
        sizePolicy6.setHeightForWidth(self.vtk_widget.sizePolicy().hasHeightForWidth())
        self.vtk_widget.setSizePolicy(sizePolicy6)
        self.vtk_widget.setMinimumSize(QSize(800, 800))
        self.vtk_widget.setMaximumSize(QSize(16777215, 16777215))

        self.verticalLayout_2.addWidget(self.vtk_widget)


        self.horizontalLayout_4.addWidget(self.groupBox_2)

        self.w_tw_visualizations.addTab(self.tab_4, "")

        self.horizontalLayout.addWidget(self.w_tw_visualizations)

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        self.w_tw_patient_settings.setCurrentIndex(0)
        self.w_tw_visualizations.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.exit_action.setText(QCoreApplication.translate("MainWindow", u"E&xit", None))
        self.settings_action.setText(QCoreApplication.translate("MainWindow", u"&Settings", None))
        self.about_action.setText(QCoreApplication.translate("MainWindow", u"&About", None))
        self.actionCollision_Map.setText(QCoreApplication.translate("MainWindow", u"Collision Map", None))
        self.actionView_From.setText(QCoreApplication.translate("MainWindow", u"View From", None))
        self.groupBox_6.setTitle(QCoreApplication.translate("MainWindow", u"Patient Information", None))
        self.w_gb_dicomrt_files.setTitle(QCoreApplication.translate("MainWindow", u"DICOM Files", None))
        self.w_pb_dcm_struct_file.setText(QCoreApplication.translate("MainWindow", u"...", None))
        self.w_pb_dcm_plan_file.setText(QCoreApplication.translate("MainWindow", u"...", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Structure Set", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"Plan", None))
        self.w_pb_esapi_search.setText(QCoreApplication.translate("MainWindow", u"Search", None))
        self.label_11.setText(QCoreApplication.translate("MainWindow", u"First Name:", None))
        self.label_12.setText(QCoreApplication.translate("MainWindow", u"Plan ID:", None))
        self.w_ch_use_dicomrt.setText(QCoreApplication.translate("MainWindow", u"Use Dicom RT Files", None))
        self.label_17.setText(QCoreApplication.translate("MainWindow", u"Isocenter:", None))
        self.label_14.setText(QCoreApplication.translate("MainWindow", u"Body Structure:", None))
        self.label_15.setText(QCoreApplication.translate("MainWindow", u"Beams", None))
        self.label_13.setText(QCoreApplication.translate("MainWindow", u"Last Name:", None))
        self.label_9.setText(QCoreApplication.translate("MainWindow", u"Patient ID:", None))
        self.label_26.setText(QCoreApplication.translate("MainWindow", u"Course ID:", None))
        self.w_l_patient_first_name.setText("")
        self.w_l_patient_last_name.setText("")
        self.w_l_plan_isocenter.setText("")
        self.groupBox.setTitle(QCoreApplication.translate("MainWindow", u"MapRT", None))
        self.label_21.setText(QCoreApplication.translate("MainWindow", u"Couch Buffer:", None))
        self.w_l_api_status.setText("")
        self.label_28.setText(QCoreApplication.translate("MainWindow", u"X", None))
        self.w_pb_get_map.setText(QCoreApplication.translate("MainWindow", u"Get Map", None))
        self.label_22.setText(QCoreApplication.translate("MainWindow", u"Patient Buffer:", None))
        self.label_24.setText(QCoreApplication.translate("MainWindow", u"cm", None))
        self.label_20.setText(QCoreApplication.translate("MainWindow", u"Treatment Room", None))
        self.label_23.setText(QCoreApplication.translate("MainWindow", u"cm", None))
        self.label_18.setText(QCoreApplication.translate("MainWindow", u"API Status:", None))
        self.w_pb_fetch_api_data.setText(QCoreApplication.translate("MainWindow", u"Fetch Data", None))
        self.label_19.setText(QCoreApplication.translate("MainWindow", u"Surface:", None))
        self.label_29.setText(QCoreApplication.translate("MainWindow", u"Y", None))
        self.label_27.setText(QCoreApplication.translate("MainWindow", u"Shift Surface", None))
        self.label_30.setText(QCoreApplication.translate("MainWindow", u"Z", None))
        self.w_pb_obj_file.setText(QCoreApplication.translate("MainWindow", u"From File", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"cm", None))
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"cm", None))
        self.label_31.setText(QCoreApplication.translate("MainWindow", u"cm", None))
        self.w_tw_patient_settings.setTabText(self.w_tw_patient_settings.indexOf(self.tab), QCoreApplication.translate("MainWindow", u"Patient Context", None))
        self.groupBox_7.setTitle(QCoreApplication.translate("MainWindow", u"DICOM", None))
        self.label_8.setText(QCoreApplication.translate("MainWindow", u"Surface Opacity:", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Surface Color:", None))
        self.w_l_dcm_opacity.setText(QCoreApplication.translate("MainWindow", u"100", None))
        self.w_pb_dcm_color.setText(QCoreApplication.translate("MainWindow", u"Select Color", None))
        self.groupBox_8.setTitle(QCoreApplication.translate("MainWindow", u"MapRT", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"Surface Color:", None))
        self.w_pb_obj_color.setText(QCoreApplication.translate("MainWindow", u"Select Color", None))
        self.label_10.setText(QCoreApplication.translate("MainWindow", u"Surface Opacity:", None))
        self.w_l_obj_opacity.setText(QCoreApplication.translate("MainWindow", u"100", None))
        self.groupBox_9.setTitle(QCoreApplication.translate("MainWindow", u"Scene", None))
        self.label_33.setText(QCoreApplication.translate("MainWindow", u"Laser Opacity", None))
        self.w_pb_laser_color.setText(QCoreApplication.translate("MainWindow", u"Select Color", None))
        self.w_l_laser_opacity.setText(QCoreApplication.translate("MainWindow", u"100", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"Background Color:", None))
        self.w_pb_background_color.setText(QCoreApplication.translate("MainWindow", u"Select Color", None))
        self.label_16.setText(QCoreApplication.translate("MainWindow", u"View From", None))
        self.label_32.setText(QCoreApplication.translate("MainWindow", u"Laser Color:", None))
        self.w_rb_plusX.setText(QCoreApplication.translate("MainWindow", u"+X", None))
        self.w_rb_minusX.setText(QCoreApplication.translate("MainWindow", u"-X", None))
        self.w_rb_plusY.setText(QCoreApplication.translate("MainWindow", u"+Y", None))
        self.w_rb_minusY.setText(QCoreApplication.translate("MainWindow", u"-Y", None))
        self.w_rb_plusZ.setText(QCoreApplication.translate("MainWindow", u"+Z", None))
        self.w_rb_minusZ.setText(QCoreApplication.translate("MainWindow", u"-Z", None))
        self.w_pb_save_image.setText(QCoreApplication.translate("MainWindow", u"Save Render Window Image", None))
        self.w_tw_patient_settings.setTabText(self.w_tw_patient_settings.indexOf(self.tab_2), QCoreApplication.translate("MainWindow", u"3D View Settings", None))
        self.w_gb_collision_map.setTitle(QCoreApplication.translate("MainWindow", u"MapRT Collision Map", None))
        self.label_25.setText(QCoreApplication.translate("MainWindow", u"Current Collision Map:", None))
        self.w_tw_visualizations.setTabText(self.w_tw_visualizations.indexOf(self.tab_3), QCoreApplication.translate("MainWindow", u"Map View", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("MainWindow", u"Render Window", None))
        self.w_tw_visualizations.setTabText(self.w_tw_visualizations.indexOf(self.tab_4), QCoreApplication.translate("MainWindow", u"3D View", None))
    # retranslateUi

