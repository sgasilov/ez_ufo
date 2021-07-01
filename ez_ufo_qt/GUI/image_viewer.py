import sys
import os
import logging
import pyqtgraph as pg
import pyqtgraph.exporters
import numpy as np
import tifffile
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import ez_ufo_qt.GUI.image_read_write as image_read_write


class ImageViewerGroup(QGroupBox):

    def __init__(self):
        super().__init__()

        self.tiff_arr = np.empty([0, 0, 0])
        self.img_arr = np.empty([0, 0])
        self.bit_depth = 32

        self.open_file_button = QPushButton("Open Image File")
        self.open_file_button.clicked.connect(self.open_image_from_file)
        self.open_file_button.setStyleSheet("background-color: lightgrey; font: 11pt")

        self.open_stack_button = QPushButton("Open Image Stack")
        self.open_stack_button.clicked.connect(self.open_stack_from_directory)
        self.open_stack_button.setStyleSheet("background-color: lightgrey; font: 11pt")

        self.save_file_button = QPushButton("Save Image File")
        self.save_file_button.clicked.connect(self.save_image_to_file)
        self.save_file_button.setStyleSheet("background-color: lightgrey; font: 11pt")

        self.save_stack_button = QPushButton("Save Image Stack")
        self.save_stack_button.clicked.connect(self.save_stack_to_directory)
        self.save_stack_button.setStyleSheet("background-color: lightgrey; font: 11pt")

        self.open_big_tiff_button = QPushButton("Open BigTiff")
        self.open_big_tiff_button.clicked.connect(self.open_big_tiff)
        self.open_big_tiff_button.setStyleSheet("background-color: lightgrey; font: 11pt")

        self.save_big_tiff_button = QPushButton("Save BigTiff")
        self.save_big_tiff_button.clicked.connect(self.save_stack_to_big_tiff)
        self.save_big_tiff_button.setStyleSheet("background-color: lightgrey; font: 11pt")

        self.hist_min_label = QLabel("Histogram Min:")
        self.hist_min_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.hist_max_label = QLabel("Histogram Max:")
        self.hist_max_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        self.hist_min_input = QSpinBox()
        self.hist_min_input.setRange(0, 100000)
        self.hist_min_input.valueChanged.connect(self.min_spin_changed)
        self.hist_max_input = QSpinBox()
        self.hist_max_input.setRange(0, 100000)
        self.hist_max_input.valueChanged.connect(self.max_spin_changed)

        self.save_8bit_rButton = QRadioButton()
        self.save_8bit_rButton.setText("Save as 8-bit")
        self.save_8bit_rButton.clicked.connect(self.set_8bit)
        self.save_8bit_rButton.setChecked(False)

        self.save_16bit_rButton = QRadioButton()
        self.save_16bit_rButton.setText("Save as 16-bit")
        self.save_16bit_rButton.clicked.connect(self.set_16bit)
        self.save_16bit_rButton.setChecked(False)

        self.save_32bit_rButton = QRadioButton()
        self.save_32bit_rButton.setText("Save as 32-bit")
        self.save_32bit_rButton.clicked.connect(self.set_32bit)
        self.save_32bit_rButton.setChecked(True)

        #self.big_tiff_checkbox = QCheckBox()
        #self.big_tiff_checkbox.setText("Save as BigTiff")
        #self.big_tiff_checkbox.stateChanged.connect(self.big_tiff_checkbox_clicked)

        self.image_window = pg.ImageView()

        self.image_window.ui.histogram.gradient.hide()
        self.histo = self.image_window.getHistogramWidget()

        self.scroller = QScrollBar(Qt.Horizontal)
        self.scroller.orientation()
        self.scroller.setEnabled(False)
        self.scroller.valueChanged.connect(self.scroll_changed)

        vbox = QVBoxLayout()
        vbox.addWidget(self.save_8bit_rButton)
        vbox.addWidget(self.save_16bit_rButton)
        vbox.addWidget(self.save_32bit_rButton)

        gridbox = QGridLayout()
        gridbox.addWidget(self.hist_max_label, 0, 0)
        gridbox.addWidget(self.hist_max_input, 0, 1)
        gridbox.addWidget(self.hist_min_label, 1, 0)
        gridbox.addWidget(self.hist_min_input, 1, 1)

        layout = QGridLayout()
        layout.addWidget(self.open_file_button, 0, 0)
        layout.addWidget(self.save_file_button, 1, 0)
        layout.addWidget(self.open_stack_button, 0, 1)
        layout.addWidget(self.save_stack_button, 1, 1)
        layout.addWidget(self.open_big_tiff_button, 0, 2)
        layout.addWidget(self.save_big_tiff_button, 1, 2)
        layout.addItem(vbox, 0, 3, 2, 1)
        #layout.addWidget(self.big_tiff_checkbox, 1, 3)
        layout.addItem(gridbox, 0, 4, 2, 1)
        layout.addWidget(self.image_window, 2, 0, 1, 5)
        layout.addWidget(self.scroller, 4, 0, 1, 5)

        self.setLayout(layout)

        self.resize(640, 480)

        self.show()

    def scroll_changed(self):
        self.image_window.setImage(self.tiff_arr[self.scroller.value()].T)

    def open_image_from_file(self):
        logging.debug("Open image button pressed")
        options = QFileDialog.Options()
        filePath, _ = QFileDialog.getOpenFileName(self, 'QFileDialog.getOpenFileName()', "", "All Files (*)",
                                                  options=options)
        if filePath:
            logging.debug("Import image path: " + filePath)
            self.img_arr = image_read_write.read_image(filePath)
            self.image_window.setImage(self.img_arr.T)
            self.scroller.setEnabled(False)

    def save_image_to_file(self):
        logging.debug("Save image to file")
        options = QFileDialog.Options()
        filepath, _ = QFileDialog.getSaveFileName(self, "QFileDialog.getSaveFileName()", "", "Tiff Files (*.tif)", options=options)
        if filepath:
            logging.debug(filepath)
            bit_depth_string = self.check_bit_depth(self.bit_depth)
            #np_image_arr = fn.imageToArray(self.image_item.qimage)
            #np_image_arr = fn.qimage_to_ndarray(self.image_item.qimage) #Trying to figure out how to save with histogram
            image_read_write.write_image(self.img_arr, os.path.dirname(filepath), os.path.basename(filepath), bit_depth_string)

    def open_stack_from_directory(self):
        logging.debug("Open image stack button pressed")
        dir_explore = QFileDialog()
        dir = dir_explore.getExistingDirectory()
        if dir:
            try:
                tiff_list = (".tif", ".tiff")
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setWindowTitle("Loading Images...")
                msg.setText("Loading Images from Directory")
                msg.show()
                self.tiff_arr = image_read_write.read_all_images(dir, tiff_list)
                self.scroller.setRange(0, self.tiff_arr.shape[0] - 1)
                self.scroller.setEnabled(True)
                self.image_window.setImage(self.tiff_arr[0].T)
                msg.close()
                mid_index = self.tiff_arr.shape[0] / 2
                self.scroller.setValue(mid_index)
            except image_read_write.InvalidDataSetError:
                print("Invalid Data Set")

    def open_stack_from_path(self, dir_path: str):
        """
        Read images from directory path into RAM as 3D numpy array
        :param dir_path: Path to directory containing multiple .tiff image files
        """
        logging.debug("Open stack from path")
        try:
            tiff_list = (".tif", ".tiff")
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setWindowTitle("Loading Images...")
            msg.setText("Loading Images from Directory")
            msg.show()
            self.tiff_arr = image_read_write.read_all_images(dir_path, tiff_list)
            self.scroller.setRange(0, self.tiff_arr.shape[0] - 1)
            self.scroller.setEnabled(True)
            self.image_window.setImage(self.tiff_arr[0].T)
            msg.close()
            mid_index = self.tiff_arr.shape[0] / 2
            self.scroller.setValue(mid_index)
        except image_read_write.InvalidDataSetError:
            print("Invalid Data Set")

    def save_stack_to_directory(self):
        """
        Saves images stored in numpy array to individual files in directory specified by user dialog
        Saves these images as BigTiff if checkbox is set to True
        """
        logging.debug("Save stack to directory button pressed")
        logging.debug("Saving with bitdepth: " + str(self.bit_depth))
        dir_explore = QFileDialog()
        dir = dir_explore.getExistingDirectory()
        logging.debug("Writing to directory: " + dir)
        if dir:
            bit_depth_string = self.check_bit_depth(self.bit_depth)
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setWindowTitle("Saving Images...")
            msg.setText("Saving Images to Directory")
            msg.show()
            image_read_write.write_all_images(self.tiff_arr, dir, bit_depth_string)
            msg.close()

    def open_big_tiff(self):
        logging.debug("Open big tiff button pressed")
        options = QFileDialog.Options()
        filePath, _ = QFileDialog.getOpenFileName(self, 'QFileDialog.getOpenFileName()', "", "All Files (*)",
                                                  options=options)
        if filePath:
            logging.debug("Import image path: " + filePath)
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setWindowTitle("Loading Images...")
            msg.setText("Loading Images from BigTiff")
            msg.show()



    def save_stack_to_big_tiff(self):
        logging.debug("Save stack to bigtiff button pressed")
        logging.debug("Saving with bitdepth: " + str(self.bit_depth))
        dir_explore = QFileDialog()
        options = QFileDialog.Options()
        filepath, _ = QFileDialog.getSaveFileName(self, "QFileDialog.getSaveFileName()", "", "Tiff Files (*.tif)", options=options)
        #logging.debug("Writing to file path: " + save_file)
        if filepath:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setWindowTitle("Saving Images...")
            msg.setText("Saving Images to BigTiff")
            msg.show()
            print(filepath)
            tifffile.imwrite(filepath, self.tiff_arr, bigtiff=True, dtype=self.bit_depth)
            msg.close()

    def min_spin_changed(self):
        histo = self.image_window.getHistogramWidget()
        levels = self.histo.getLevels()
        min_level = self.hist_min_input.value()
        self.image_window.setLevels(min_level, levels[1])

    def max_spin_changed(self):
        histo = self.image_window.getHistogramWidget()
        levels = self.histo.getLevels()
        max_level = self.hist_max_input.value()
        self.image_window.setLevels(levels[0], max_level)

    def check_bit_depth(self, bit_depth: int) -> str:
        if bit_depth == 8:
            return "uint8"
        elif bit_depth == 16:
            return "uint16"
        elif bit_depth == 32:
            return "uint32"

    def set_8bit(self):
        logging.debug("Set 8-bit")
        self.bit_depth = 8

    def set_16bit(self):
        logging.debug("Set 16-bit")
        self.bit_depth = 16

    def set_32bit(self):
        logging.debug("Set 32-bit")
        self.bit_depth = 32

    def big_tiff_checkbox_clicked(self):
        logging.debug("BigTiff checkbox: " + str(self.big_tiff_checkbox.isChecked()))