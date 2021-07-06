import logging
from PyQt5.QtWidgets import QGridLayout, QLabel, QGroupBox, QLineEdit, QCheckBox

import ez_ufo_qt.GUI.params as parameters

class FFCGroup(QGroupBox):
    """
    Flat Field Correction Settings
    """
    def __init__(self):
        super().__init__()

        self.setTitle("Flat Field Correction")
        self.setStyleSheet('QGroupBox {color: indigo;}')

        self.enable_sinFFC_checkbox = QCheckBox()
        self.enable_sinFFC_checkbox.setText("Use Smart Intensity Normalization Flat Field Correction")
        self.enable_sinFFC_checkbox.stateChanged.connect(self.set_sinFFC)

        self.eigen_pco_repetitions_label = QLabel()
        self.eigen_pco_repetitions_label.setText("Eigen PCO Repetitions")
        self.eigen_pco_repetitions_entry = QLineEdit()
        self.eigen_pco_repetitions_entry.textChanged.connect(self.set_pcoReps)

        self.eigen_pco_downsample_label = QLabel()
        self.eigen_pco_downsample_label.setText("Eigen PCO Downsample")
        self.eigen_pco_downsample_entry = QLineEdit()
        self.eigen_pco_downsample_entry.textChanged.connect(self.set_pcoDowns)

        self.downsample_label = QLabel()
        self.downsample_label.setText("Downsample")
        self.downsample_entry = QLineEdit()
        self.downsample_entry.textChanged.connect(self.set_downsample)

        self.set_layout()

    def set_layout(self):
        layout = QGridLayout()

        layout.addWidget(self.enable_sinFFC_checkbox, 0, 0)
        layout.addWidget(self.eigen_pco_repetitions_label, 1, 0)
        layout.addWidget(self.eigen_pco_repetitions_entry, 1, 1)
        layout.addWidget(self.eigen_pco_downsample_label, 2, 0)
        layout.addWidget(self.eigen_pco_downsample_entry, 2, 1)
        layout.addWidget(self.downsample_label, 3, 0)
        layout.addWidget(self.downsample_entry, 3, 1)

        self.setLayout(layout)

    #TODO Set initial values
    def init_values(self):
        pass

    #TODO update values from parameters file
    def set_values_from_params(self):
        self.enable_sinFFC_checkbox.setChecked(parameters.params['e_sinFFC'])

    def set_sinFFC(self):
        logging.debug("sinFFC: " + str(self.enable_sinFFC_checkbox.isChecked()))
        parameters.params['e_sinFFC'] = bool(self.enable_sinFFC_checkbox.isChecked())

    #TODO Add values in parameters file
    def set_pcoReps(self):
        logging.debug("PCO Reps: ")

    def set_pcoDowns(self):
        logging.debug("PCO Downsample: ")

    def set_downsample(self):
        logging.debug("Downsample: ")