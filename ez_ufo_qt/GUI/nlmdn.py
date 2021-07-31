import logging
import os

from PyQt5.QtWidgets import QGridLayout, QLabel, QRadioButton, QGroupBox, QLineEdit, QCheckBox, QPushButton, QHBoxLayout
from PyQt5.QtCore import Qt

import ez_ufo_qt.GUI.params as parameters

class NLMDNGroup(QGroupBox):
    """
    Non-linear means de-noising settings
    """
    def __init__(self):
        super().__init__()

        self.setTitle("Non-local Means De-noising")
        self.setStyleSheet('QGroupBox {color: royalblue;}')

        self.input_dir_button = QPushButton("Select input directory")
        self.input_dir_button.setStyleSheet("background-color:lightgrey; font: 12pt;")
        self.input_dir_button.clicked.connect(self.set_indir_button)

        self.select_img_button = QPushButton("Select one image")
        self.select_img_button.setStyleSheet("background-color:lightgrey; font: 12pt;")
        self.select_img_button.clicked.connect(self.select_image)

        self.input_dir_entry = QLineEdit()
        self.input_dir_entry.textChanged.connect(self.set_indir_entry)

        self.output_dir_button = QPushButton("Select output directory or filename pattern")
        self.output_dir_button.setStyleSheet("background-color:lightgrey; font: 12pt;")
        self.output_dir_button.clicked.connect(self.set_outdir_button)

        self.save_biftiff_checkbox = QCheckBox("Save in bigtiff container")
        self.save_biftiff_checkbox.clicked.connect(self.set_save_bigtiff)

        self.output_dir_entry = QLineEdit()
        self.output_dir_entry.textChanged.connect(self.set_outdir_entry)

        self.similarity_radius_label = QLabel("Radius for similarity search")
        self.similarity_radius_entry = QLineEdit()
        self.similarity_radius_entry.textChanged.connect(self.set_rad_sim_entry)

        self.patch_radius_label = QLabel("Radius of patches")
        self.patch_radius_entry = QLineEdit()
        self.patch_radius_entry.textChanged.connect(self.set_rad_patch_entry)

        self.smoothing_label = QLabel("Smoothing control parameter")
        self.smoothing_entry = QLineEdit()
        self.smoothing_entry.textChanged.connect(self.set_smoothing_entry)

        self.noise_std_label = QLabel("Noise standard deviation")
        self.noise_std_entry = QLineEdit()
        self.noise_std_entry.textChanged.connect(self.set_noise_entry)

        self.window_label = QLabel("Window (optional)")
        self.window_entry = QLineEdit()
        self.window_entry.textChanged.connect(self.set_window_entry)

        self.fast_checkbox = QCheckBox("Fast")
        self.fast_checkbox.clicked.connect(self.set_fast_checkbox)

        self.sigma_checkbox = QCheckBox("Estimate sigma")
        self.sigma_checkbox.clicked.connect(self.set_sigma_checkbox)

        self.help_button = QPushButton("Help")
        self.help_button.setStyleSheet("background-color:lightgrey; font: 13pt; font-weight: bold;")
        self.help_button.clicked.connect(self.help_button_pressed)

        self.delete_button = QPushButton("Delete reco dir")
        self.delete_button.setStyleSheet("background-color:lightgrey; font: 13pt; font-weight: bold;")
        self.delete_button.clicked.connect(self.delete_button_pressed)

        self.dry_button = QPushButton("Dry run")
        self.dry_button.setStyleSheet("background-color:lightgrey; font: 13pt; font-weight: bold;")
        self.dry_button.clicked.connect(self.dry_button_pressed)

        self.apply_button = QPushButton("Apply filter")
        self.apply_button.setStyleSheet("background-color:lightgrey;color:royalblue; font: 13pt; font-weight: bold;")
        self.apply_button.clicked.connect(self.apply_button_pressed)

        self.set_layout()

    def set_layout(self):
        layout = QGridLayout()

        layout.addWidget(self.input_dir_button, 0, 0)
        layout.addWidget(self.select_img_button, 0, 1)
        layout.addWidget(self.input_dir_entry, 1, 0, 1, 2)
        layout.addWidget(self.output_dir_button, 2, 0)
        layout.addWidget(self.save_biftiff_checkbox, 2, 1, Qt.AlignCenter)
        layout.addWidget(self.output_dir_entry, 3, 0, 1, 2)
        layout.addWidget(self.similarity_radius_label, 4, 0)
        layout.addWidget(self.similarity_radius_entry, 4, 1)
        layout.addWidget(self.patch_radius_label, 5, 0)
        layout.addWidget(self.patch_radius_entry, 5, 1)
        layout.addWidget(self.smoothing_label, 6, 0)
        layout.addWidget(self.smoothing_entry, 6, 1)
        layout.addWidget(self.noise_std_label, 7, 0)
        layout.addWidget(self.noise_std_entry, 7, 1)
        layout.addWidget(self.window_label, 8, 0)
        layout.addWidget(self.window_entry, 8, 1)
        layout.addWidget(self.fast_checkbox, 9, 0, Qt.AlignCenter)
        layout.addWidget(self.sigma_checkbox, 9, 1, Qt.AlignCenter)

        hbox = QHBoxLayout()
        hbox.addWidget(self.help_button)
        hbox.addWidget(self.delete_button)
        hbox.addWidget(self.dry_button)
        hbox.addWidget(self.apply_button)

        layout.addItem(hbox, 10, 0, 1, 2)

        self.setLayout(layout)

    def init_values(self):
        self.input_dir_entry.setText(os.getcwd())
        self.output_dir_entry.setText(os.getcwd() + '-nlmfilt')
        self.similarity_radius_entry.setText("10")
        self.patch_radius_entry.setText("3")
        self.smoothing_entry.setText("0.0")
        self.noise_std_entry.setText("0.0")
        self.window_entry.setText("0.0")
        self.fast_checkbox.setChecked(True)
        self.sigma_checkbox.setChecked(False)

    def set_values_from_params(self):
        pass

    def set_indir_button(self):
        logging.debug("Select input directory pressed")

    def set_indir_entry(self):
        logging.debug("Indir entry: " + str(self.input_dir_entry.text()))

    def select_image(self):
        logging.debug("Select one image button pressed")

    def set_outdir_button(self):
        logging.debug("Select output directory pressed")

    def set_save_bigtiff(self):
        logging.debug("Save bigtiff checkbox: " + str(self.save_biftiff_checkbox.isChecked()))

    def set_outdir_entry(self):
        logging.debug("Outdir entry: " + str(self.output_dir_entry.text()))

    def set_rad_sim_entry(self):
        logging.debug("Radius for similarity: " + str(self.similarity_radius_entry.text()))

    def set_rad_patch_entry(self):
        logging.debug("Radius of patches: " + str(self.patch_radius_entry.text()))

    def set_smoothing_entry(self):
        logging.debug("Smoothing control: " + str(self.smoothing_entry.text()))

    def set_noise_entry(self):
        logging.debug("Noise std: " + str(self.noise_std_entry.text()))

    def set_window_entry(self):
        logging.debug("Window: " + str(self.window_entry.text()))

    def set_fast_checkbox(self):
        logging.debug("Fast: " + str(self.fast_checkbox.isChecked()))

    def set_sigma_checkbox(self):
        logging.debug("Estimate sigma: " + str(self.sigma_checkbox.isChecked()))

    def quit_button_pressed(self):
        logging.debug("Quit Button Pressed")

    def help_button_pressed(self):
        logging.debug("Help Button Pressed")

    def delete_button_pressed(self):
        logging.debug("Delete Reco Button Pressed")

    def dry_button_pressed(self):
        logging.debug("Dry Run Button Pressed")

    def apply_button_pressed(self):
        logging.debug("Apply Filter Button Pressed")

