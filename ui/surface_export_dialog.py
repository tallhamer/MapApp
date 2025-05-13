# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'surface_export_dialog.ui'
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
    QDoubleSpinBox, QGridLayout, QGroupBox, QHBoxLayout,
    QLabel, QSizePolicy, QSpacerItem, QTabWidget,
    QVBoxLayout, QWidget)

from vtkmodules.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor

class Ui_SurfaceExportDialog(object):
    def setupUi(self, SurfaceExportDialog):
        if not SurfaceExportDialog.objectName():
            SurfaceExportDialog.setObjectName(u"SurfaceExportDialog")
        SurfaceExportDialog.resize(946, 643)
        self.verticalLayout_2 = QVBoxLayout(SurfaceExportDialog)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.widget = QWidget(SurfaceExportDialog)
        self.widget.setObjectName(u"widget")
        self.horizontalLayout = QHBoxLayout(self.widget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.groupBox = QGroupBox(self.widget)
        self.groupBox.setObjectName(u"groupBox")
        self.verticalLayout_4 = QVBoxLayout(self.groupBox)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.widget_2 = QWidget(self.groupBox)
        self.widget_2.setObjectName(u"widget_2")
        self.gridLayout_2 = QGridLayout(self.widget_2)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.label = QLabel(self.widget_2)
        self.label.setObjectName(u"label")

        self.gridLayout_2.addWidget(self.label, 0, 0, 1, 1)

        self.w_dsb_voxel_size = QDoubleSpinBox(self.widget_2)
        self.w_dsb_voxel_size.setObjectName(u"w_dsb_voxel_size")

        self.gridLayout_2.addWidget(self.w_dsb_voxel_size, 0, 1, 1, 1)

        self.label_2 = QLabel(self.widget_2)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout_2.addWidget(self.label_2, 0, 2, 1, 1)


        self.verticalLayout_4.addWidget(self.widget_2)

        self.groupBox_2 = QGroupBox(self.groupBox)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.gridLayout = QGridLayout(self.groupBox_2)
        self.gridLayout.setObjectName(u"gridLayout")
        self.label_3 = QLabel(self.groupBox_2)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setMinimumSize(QSize(50, 0))
        self.label_3.setMaximumSize(QSize(20, 16777215))

        self.gridLayout.addWidget(self.label_3, 0, 0, 1, 1)

        self.label_4 = QLabel(self.groupBox_2)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setMinimumSize(QSize(100, 0))

        self.gridLayout.addWidget(self.label_4, 0, 1, 1, 1)

        self.label_5 = QLabel(self.groupBox_2)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setMinimumSize(QSize(100, 0))

        self.gridLayout.addWidget(self.label_5, 0, 2, 1, 1)

        self.label_6 = QLabel(self.groupBox_2)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setMinimumSize(QSize(50, 0))

        self.gridLayout.addWidget(self.label_6, 1, 0, 1, 1)

        self.w_dsb_x_bounds_min = QDoubleSpinBox(self.groupBox_2)
        self.w_dsb_x_bounds_min.setObjectName(u"w_dsb_x_bounds_min")
        self.w_dsb_x_bounds_min.setMinimum(-10000.000000000000000)
        self.w_dsb_x_bounds_min.setMaximum(10000.000000000000000)
        self.w_dsb_x_bounds_min.setSingleStep(50.000000000000000)

        self.gridLayout.addWidget(self.w_dsb_x_bounds_min, 1, 1, 1, 1)

        self.w_dsb_x_bounds_max = QDoubleSpinBox(self.groupBox_2)
        self.w_dsb_x_bounds_max.setObjectName(u"w_dsb_x_bounds_max")
        self.w_dsb_x_bounds_max.setMinimum(-10000.000000000000000)
        self.w_dsb_x_bounds_max.setMaximum(10000.000000000000000)
        self.w_dsb_x_bounds_max.setSingleStep(50.000000000000000)

        self.gridLayout.addWidget(self.w_dsb_x_bounds_max, 1, 2, 1, 1)

        self.label_7 = QLabel(self.groupBox_2)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setMinimumSize(QSize(50, 0))

        self.gridLayout.addWidget(self.label_7, 2, 0, 1, 1)

        self.w_dsb_y_bounds_min = QDoubleSpinBox(self.groupBox_2)
        self.w_dsb_y_bounds_min.setObjectName(u"w_dsb_y_bounds_min")
        self.w_dsb_y_bounds_min.setMinimum(-10000.000000000000000)
        self.w_dsb_y_bounds_min.setMaximum(10000.000000000000000)
        self.w_dsb_y_bounds_min.setSingleStep(50.000000000000000)

        self.gridLayout.addWidget(self.w_dsb_y_bounds_min, 2, 1, 1, 1)

        self.w_dsb_y_bounds_max = QDoubleSpinBox(self.groupBox_2)
        self.w_dsb_y_bounds_max.setObjectName(u"w_dsb_y_bounds_max")
        self.w_dsb_y_bounds_max.setMinimum(-10000.000000000000000)
        self.w_dsb_y_bounds_max.setMaximum(10000.000000000000000)
        self.w_dsb_y_bounds_max.setSingleStep(50.000000000000000)

        self.gridLayout.addWidget(self.w_dsb_y_bounds_max, 2, 2, 1, 1)

        self.label_8 = QLabel(self.groupBox_2)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setMinimumSize(QSize(50, 0))

        self.gridLayout.addWidget(self.label_8, 3, 0, 1, 1)

        self.w_dsb_z_bounds_min = QDoubleSpinBox(self.groupBox_2)
        self.w_dsb_z_bounds_min.setObjectName(u"w_dsb_z_bounds_min")
        self.w_dsb_z_bounds_min.setMinimum(-10000.000000000000000)
        self.w_dsb_z_bounds_min.setMaximum(10000.000000000000000)
        self.w_dsb_z_bounds_min.setSingleStep(50.000000000000000)

        self.gridLayout.addWidget(self.w_dsb_z_bounds_min, 3, 1, 1, 1)

        self.w_dsb_z_bounds_max = QDoubleSpinBox(self.groupBox_2)
        self.w_dsb_z_bounds_max.setObjectName(u"w_dsb_z_bounds_max")
        self.w_dsb_z_bounds_max.setMinimum(-10000.000000000000000)
        self.w_dsb_z_bounds_max.setMaximum(10000.000000000000000)
        self.w_dsb_z_bounds_max.setSingleStep(50.000000000000000)

        self.gridLayout.addWidget(self.w_dsb_z_bounds_max, 3, 2, 1, 1)


        self.verticalLayout_4.addWidget(self.groupBox_2)

        self.verticalSpacer = QSpacerItem(20, 346, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_4.addItem(self.verticalSpacer)


        self.horizontalLayout.addWidget(self.groupBox)

        self.w_tw_visualizations = QTabWidget(self.widget)
        self.w_tw_visualizations.setObjectName(u"w_tw_visualizations")
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        self.verticalLayout = QVBoxLayout(self.tab)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.vtk_polydata_render_widget = QVTKRenderWindowInteractor(self.tab)
        self.vtk_polydata_render_widget.setObjectName(u"vtk_polydata_render_widget")

        self.verticalLayout.addWidget(self.vtk_polydata_render_widget)

        self.w_tw_visualizations.addTab(self.tab, "")
        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        self.verticalLayout_3 = QVBoxLayout(self.tab_2)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.vtk_ct_render_widget = QVTKRenderWindowInteractor(self.tab_2)
        self.vtk_ct_render_widget.setObjectName(u"vtk_ct_render_widget")

        self.verticalLayout_3.addWidget(self.vtk_ct_render_widget)

        self.w_tw_visualizations.addTab(self.tab_2, "")

        self.horizontalLayout.addWidget(self.w_tw_visualizations)


        self.verticalLayout_2.addWidget(self.widget)

        self.buttonBox = QDialogButtonBox(SurfaceExportDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.StandardButton.Cancel|QDialogButtonBox.StandardButton.Ok)

        self.verticalLayout_2.addWidget(self.buttonBox)


        self.retranslateUi(SurfaceExportDialog)
        self.buttonBox.accepted.connect(SurfaceExportDialog.accept)
        self.buttonBox.rejected.connect(SurfaceExportDialog.reject)

        self.w_tw_visualizations.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(SurfaceExportDialog)
    # setupUi

    def retranslateUi(self, SurfaceExportDialog):
        SurfaceExportDialog.setWindowTitle(QCoreApplication.translate("SurfaceExportDialog", u"Export Surface Data to DICOM", None))
        self.groupBox.setTitle(QCoreApplication.translate("SurfaceExportDialog", u"Export Settings", None))
        self.label.setText(QCoreApplication.translate("SurfaceExportDialog", u"Voxel Size", None))
        self.label_2.setText(QCoreApplication.translate("SurfaceExportDialog", u"mm", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("SurfaceExportDialog", u"Bounds", None))
        self.label_3.setText(QCoreApplication.translate("SurfaceExportDialog", u"Axis", None))
        self.label_4.setText(QCoreApplication.translate("SurfaceExportDialog", u"Min", None))
        self.label_5.setText(QCoreApplication.translate("SurfaceExportDialog", u"Max", None))
        self.label_6.setText(QCoreApplication.translate("SurfaceExportDialog", u"X", None))
        self.label_7.setText(QCoreApplication.translate("SurfaceExportDialog", u"Y", None))
        self.label_8.setText(QCoreApplication.translate("SurfaceExportDialog", u"Z", None))
        self.w_tw_visualizations.setTabText(self.w_tw_visualizations.indexOf(self.tab), QCoreApplication.translate("SurfaceExportDialog", u"Surface Data", None))
        self.w_tw_visualizations.setTabText(self.w_tw_visualizations.indexOf(self.tab_2), QCoreApplication.translate("SurfaceExportDialog", u"CT Data", None))
    # retranslateUi

