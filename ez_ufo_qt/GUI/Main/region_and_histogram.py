import logging
from PyQt5.QtWidgets import QGridLayout, QRadioButton, QLabel, QGroupBox, QLineEdit, QCheckBox
from PyQt5.QtCore import Qt

import ez_ufo_qt.GUI.params as parameters


class BinningGroup(QGroupBox):
    """
    Binning settings
    """

    def __init__(self):
        super().__init__()

        self.setTitle("Region of Interest and Histogram Settings")
        self.setStyleSheet('QGroupBox {color: red;}')

        self.select_rows_checkbox = QCheckBox("Select rows which will be reconstructed")
        self.select_rows_checkbox.stateChanged.connect(self.set_select_rows)

        self.first_row_label = QLabel("First row in projections:")
        self.first_row_label.setToolTip("Counting from the top")
        self.first_row_entry = QLineEdit()
        self.first_row_entry.textChanged.connect(self.set_first_row)

        self.num_rows_label = QLabel("Number of rows (ROI height):")
        self.num_rows_entry = QLineEdit()
        self.num_rows_entry.textChanged.connect(self.set_num_rows)

        self.nth_row_label = QLabel("Reconstruct every Nth row:")
        self.nth_row_entry = QLineEdit()
        self.nth_row_entry.textChanged.connect(self.set_reco_nth_rows)

        self.clip_histo_checkbox = QCheckBox("Clip histogram and save slices in")
        self.clip_histo_checkbox.stateChanged.connect(self.set_clip_histo)

        self.eight_bit_rButton = QRadioButton("8-bit")
        self.eight_bit_rButton.setChecked(True)
        self.eight_bit_rButton.clicked.connect(self.set_bitdepth)

        self.sixteen_bit_rButton = QRadioButton("16-bit")
        self.sixteen_bit_rButton.clicked.connect(self.set_bitdepth)

        self.min_val_label = QLabel("Min value in 32-bit histogram:")
        self.min_val_entry = QLineEdit()
        self.min_val_entry.textChanged.connect(self.set_min_val)

        self.max_val_label = QLabel("Max value in 32-bit histogram:")
        self.max_val_entry = QLineEdit()
        self.max_val_entry.textChanged.connect(self.set_max_val)

        self.crop_slices_checkbox = QCheckBox("Crop slices in the reconstruction plane")
        self.crop_slices_checkbox.stateChanged.connect(self.set_crop_slices)

        self.x_val_label = QLabel("x:")
        self.x_val_label.setToolTip("First column (counting from left)")
        self.x_val_entry = QLineEdit()
        self.x_val_entry.textChanged.connect(self.set_x)

        self.width_val_label = QLabel("width:")
        self.width_val_entry = QLineEdit()
        self.width_val_entry.textChanged.connect(self.set_width)

        self.y_val_label = QLabel("y:")
        self.y_val_label.setToolTip("First row (counting from top)")
        self.y_val_entry = QLineEdit()
        self.y_val_entry.textChanged.connect(self.set_y)

        self.height_val_label = QLabel("height:")
        self.height_val_entry = QLineEdit()
        self.height_val_entry.textChanged.connect(self.set_height)

        self.rotate_vol_label = QLabel("Rotate volume clockwise by [deg]:")
        self.rotate_vol_entry = QLineEdit()
        self.rotate_vol_entry.textChanged.connect(self.set_rotate_volume)

        self.crop_z_axis_checkbox = QCheckBox("Crop output images in z-axis")
        self.crop_z_axis_checkbox.stateChanged.connect(self.crop_z_axis_checkbox_clicked)

        self.crop_z_axis_start_label = QLabel("Number of images to crop at start:")
        self.crop_z_axis_start_entry = QLineEdit()
        self.crop_z_axis_start_entry.textChanged.connect(self.set_crop_z_axis_start)

        self.crop_z_axis_end_label = QLabel("Number of images to crop at end:")
        self.crop_z_axis_end_entry = QLineEdit()
        self.crop_z_axis_end_entry.textChanged.connect(self.set_crop_z_axis_end)

        self.set_layout()

    def set_layout(self):
        """
        Sets the layout of buttons, labels, etc. for binning group
        """
        layout = QGridLayout()

        layout.addWidget(self.select_rows_checkbox, 0, 0)
        layout.addWidget(self.first_row_label, 1, 0)
        layout.addWidget(self.first_row_entry, 1, 1, 1, 1)
        layout.addWidget(self.num_rows_label, 1, 2)
        layout.addWidget(self.num_rows_entry, 1, 3, 1, 1)
        layout.addWidget(self.nth_row_label, 2, 0)
        layout.addWidget(self.nth_row_entry, 2, 1, 1, 1)
        layout.addWidget(self.clip_histo_checkbox, 4, 0)
        layout.addWidget(self.eight_bit_rButton, 4, 1)
        layout.addWidget(self.sixteen_bit_rButton, 4, 2)
        layout.addWidget(self.min_val_label, 5, 0)
        layout.addWidget(self.min_val_entry, 5, 1)
        layout.addWidget(self.max_val_label, 5, 2)
        layout.addWidget(self.max_val_entry, 5, 3)
        layout.addWidget(self.crop_slices_checkbox, 7, 0)
        layout.addWidget(self.x_val_label, 8, 0, Qt.AlignRight)
        layout.addWidget(self.x_val_entry, 8, 1)
        layout.addWidget(self.width_val_label, 8, 2, Qt.AlignRight)
        layout.addWidget(self.width_val_entry, 8, 3)
        layout.addWidget(self.y_val_label, 9, 0, Qt.AlignRight)
        layout.addWidget(self.y_val_entry, 9, 1)
        layout.addWidget(self.height_val_label, 9, 2, Qt.AlignRight)
        layout.addWidget(self.height_val_entry, 9, 3)
        layout.addWidget(self.rotate_vol_label, 10, 0)
        layout.addWidget(self.rotate_vol_entry, 10, 1, 1, 3)
        layout.addWidget(self.crop_z_axis_checkbox, 11, 0, 1, 1)
        layout.addWidget(self.crop_z_axis_start_label, 12, 0, 1, 1)
        layout.addWidget(self.crop_z_axis_start_entry, 12, 1, 1, 1)
        layout.addWidget(self.crop_z_axis_end_label, 12, 2, 1, 1)
        layout.addWidget(self.crop_z_axis_end_entry, 12, 3, 1, 1)

        self.setLayout(layout)

    def init_values(self):
        self.select_rows_checkbox.setChecked(False)
        parameters.params['main_region_select_rows'] = False
        self.first_row_entry.setText("100")
        self.num_rows_entry.setText("200")
        self.nth_row_entry.setText("20")
        self.clip_histo_checkbox.setChecked(False)
        parameters.params['main_region_clip_histogram'] = False
        self.eight_bit_rButton.setChecked(True)
        parameters.params['main_region_bit_depth'] = str(8)
        self.min_val_entry.setText("0.0")
        self.max_val_entry.setText("0.0")
        self.crop_slices_checkbox.setChecked(False)
        parameters.params['main_region_crop_slices'] = False
        self.x_val_entry.setText("0")
        self.width_val_entry.setText("0")
        self.y_val_entry.setText("0")
        self.height_val_entry.setText("0")
        self.rotate_vol_entry.setText("0.0")
        parameters.params['main_region_crop_z_axis'] = False
        self.crop_z_axis_checkbox.setChecked(parameters.params['main_region_crop_z_axis'])
        parameters.params['main_region_crop_z_axis_start'] = "0"
        self.crop_z_axis_start_entry.setText(parameters.params['main_region_crop_z_axis_start'])
        parameters.params['main_region_crop_z_axis_end'] = "0"
        self.crop_z_axis_end_entry.setText(parameters.params['main_region_crop_z_axis_end'])

    def set_values_from_params(self):
        self.select_rows_checkbox.setChecked(parameters.params['main_region_select_rows'])
        self.first_row_entry.setText(str(parameters.params['main_region_first_row']))
        self.num_rows_entry.setText(str(parameters.params['main_region_number_rows']))
        self.nth_row_entry.setText(str(parameters.params['main_region_nth_row']))
        self.clip_histo_checkbox.setChecked(parameters.params['main_region_clip_histogram'])
        if int(parameters.params['main_region_bit_depth']) == 8:
            self.eight_bit_rButton.setChecked(True)
            self.sixteen_bit_rButton.setChecked(False)
        elif int(parameters.params['main_region_bit_depth']) == 16:
            self.eight_bit_rButton.setChecked(False)
            self.sixteen_bit_rButton.setChecked(True)
        self.min_val_entry.setText(str(parameters.params['main_region_histogram_min']))
        self.max_val_entry.setText(str(parameters.params['main_region_histogram_max']))
        self.crop_slices_checkbox.setChecked(parameters.params['main_region_crop_slices'])
        self.x_val_entry.setText(str(parameters.params['main_region_crop_x']))
        self.width_val_entry.setText(str(parameters.params['main_region_crop_width']))
        self.y_val_entry.setText(str(parameters.params['main_region_crop_y']))
        self.height_val_entry.setText(str(parameters.params['main_region_crop_height']))
        self.rotate_vol_entry.setText(str(parameters.params['main_region_rotate_volume_clock']))
        self.crop_z_axis_checkbox.setChecked(parameters.params['main_region_crop_z_axis'])
        self.crop_z_axis_start_entry.setText(str(parameters.params['main_region_crop_z_axis_start']))
        self.crop_z_axis_end_entry.setText(str(parameters.params['main_region_crop_z_axis_end']))

    def set_select_rows(self):
        logging.debug("Select rows: " + str(self.select_rows_checkbox.isChecked()))
        parameters.params['main_region_select_rows'] = bool(self.select_rows_checkbox.isChecked())

    def set_first_row(self):
        logging.debug(self.first_row_entry.text())
        parameters.params['main_region_first_row'] = str(self.first_row_entry.text())

    def set_num_rows(self):
        logging.debug(self.num_rows_entry.text())
        parameters.params['main_region_number_rows'] = str(self.num_rows_entry.text())

    def set_reco_nth_rows(self):
        logging.debug(self.nth_row_entry.text())
        parameters.params['main_region_nth_row'] = str(self.nth_row_entry.text())

    def set_clip_histo(self):
        logging.debug("Clip histo: " + str(self.clip_histo_checkbox.isChecked()))
        parameters.params['main_region_clip_histogram'] = bool(self.clip_histo_checkbox.isChecked())

    def set_bitdepth(self):
        if self.eight_bit_rButton.isChecked():
            logging.debug("8 bit")
            parameters.params['main_region_bit_depth'] = str(8)
        elif self.sixteen_bit_rButton.isChecked():
            logging.debug("16 bit")
            parameters.params['main_region_bit_depth'] = str(16)

    def set_min_val(self):
        logging.debug(self.min_val_entry.text())
        parameters.params['main_region_histogram_min'] = str(self.min_val_entry.text())

    def set_max_val(self):
        logging.debug(self.max_val_entry.text())
        parameters.params['main_region_histogram_max'] = str(self.max_val_entry.text())

    def set_crop_slices(self):
        logging.debug("Crop slices: " + str(self.crop_slices_checkbox.isChecked()))
        parameters.params['main_region_crop_slices'] = bool(self.crop_slices_checkbox.isChecked())

    def set_x(self):
        logging.debug(self.x_val_entry.text())
        parameters.params['main_region_crop_x'] = str(self.x_val_entry.text())

    def set_width(self):
        logging.debug(self.width_val_entry.text())
        parameters.params['main_region_crop_width'] = str(self.width_val_entry.text())

    def set_y(self):
        logging.debug(self.y_val_entry.text())
        parameters.params['main_region_crop_y'] = str(self.y_val_entry.text())

    def set_height(self):
        logging.debug(self.height_val_entry.text())
        parameters.params['main_region_crop_height'] = str(self.height_val_entry.text())

    def set_rotate_volume(self):
        logging.debug(self.rotate_vol_entry.text())
        parameters.params['main_region_rotate_volume_clock'] = str(self.rotate_vol_entry.text())

    def crop_z_axis_checkbox_clicked(self):
        logging.debug("Crop Z Axis: " + str(self.crop_z_axis_checkbox.isChecked()))
        parameters.params['main_region_crop_z_axis'] = bool(self.crop_z_axis_checkbox.isChecked())

    def set_crop_z_axis_start(self):
        logging.debug("Crop Z Axis Start: " + str(self.crop_z_axis_start_entry.text()))
        parameters.params['main_region_crop_z_axis_start'] = str(self.crop_z_axis_start_entry.text())

    def set_crop_z_axis_end(self):
        logging.debug("Crop Z Axis End: " + str(self.crop_z_axis_end_entry.text()))
        parameters.params['main_region_crop_z_axis_end'] = str(self.crop_z_axis_start_entry.text())
