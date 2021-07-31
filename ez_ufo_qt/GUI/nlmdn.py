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

        self.select_img_button = QPushButton("Select one image")
        self.select_img_button.setStyleSheet("background-color:lightgrey; font: 12pt;")

        self.input_dir_entry = QLineEdit()

        self.output_dir_button = QPushButton("Select output directory or filename pattern")
        self.output_dir_button.setStyleSheet("background-color:lightgrey; font: 12pt;")

        self.save_biftiff_checkbox = QCheckBox("Save in bigtiff container")

        self.output_dir_entry = QLineEdit()

        self.similarity_radius_label = QLabel("Radius for similarity search")
        self.similarity_radius_entry = QLineEdit()

        self.patch_radius_label = QLabel("Radius of patches")
        self.patch_radius_entry = QLineEdit()

        self.smoothing_label = QLabel("Smoothing control parameter")
        self.smoothing_entry = QLineEdit()

        self.noise_std_label = QLabel("Noise standard deviation")
        self.noise_std_entry = QLineEdit()

        self.window_label = QLabel("Window (optional)")
        self.window_entry = QLineEdit()

        self.fast_checkbox = QCheckBox("Fast")

        self.sigma_checkbox = QCheckBox("Estimate sigma")

        self.help_button = QPushButton("Help")
        self.help_button.setStyleSheet("background-color:lightgrey; font: 13pt; font-weight: bold;")

        self.delete_button = QPushButton("Delete reco dir")
        self.delete_button.setStyleSheet("background-color:lightgrey; font: 13pt; font-weight: bold;")

        self.dry_button = QPushButton("Dry run")
        self.dry_button.setStyleSheet("background-color:lightgrey; font: 13pt; font-weight: bold;")

        self.apply_button = QPushButton("Apply filter")
        self.apply_button.setStyleSheet("background-color:lightgrey;color:royalblue; font: 13pt; font-weight: bold;")

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