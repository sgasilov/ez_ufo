import logging
from PyQt5.QtWidgets import QGridLayout, QLabel, QRadioButton, QGroupBox, QLineEdit, QCheckBox

import ez_ufo_qt.GUI.params as parameters

class AdvancedGroup(QGroupBox):
    """
    Advanced Tofu Reco settings
    """

    def __init__(self):
        super().__init__()

        self.setTitle("Advanced TOFU Reconstruction Settings")
        self.setStyleSheet('QGroupBox {color: green;}')

        #LAMINO
        self.rotation_range_label = QLabel("Rotation range")
        self.rotation_range_entry = QLineEdit()

        self.lamino_angle_label = QLabel("Lamino angle")
        self.lamino_angle_entry = QLineEdit()

        self.sample_rotation_beam_label = QLabel("Sample rotation around the beam axis")
        self.sample_rotation_beam_entry = QLineEdit()

        self.sample_rotation_vert_label = QLabel("Sample rotation around the vertical axis")
        self.sample_rotation_vert_entry = QLineEdit()

        #AUXILIARY FFC
        self.dark_scale_label = QLabel("Dark scale                              ")
        self.dark_scale_entry = QLineEdit()

        self.flat_scale_label = QLabel("Flat scale                              ")
        self.flat_scale_entry = QLineEdit()

        self.set_layout()

    def set_layout(self):
        layout = QGridLayout()

        lamino_group = QGroupBox("Laminography Settings")
        lamino_group.setCheckable(True)
        lamino_group.setChecked(False)
        lamino_layout = QGridLayout()
        lamino_layout.addWidget(self.rotation_range_label, 0, 0)
        lamino_layout.addWidget(self.rotation_range_entry, 0, 1)
        lamino_layout.addWidget(self.lamino_angle_label, 1, 0)
        lamino_layout.addWidget(self.lamino_angle_entry, 1, 1)
        lamino_layout.addWidget(self.sample_rotation_beam_label, 2, 0)
        lamino_layout.addWidget(self.sample_rotation_beam_entry, 2, 1)
        lamino_layout.addWidget(self.sample_rotation_vert_label, 3, 0)
        lamino_layout.addWidget(self.sample_rotation_vert_entry, 3, 1)
        lamino_group.setLayout(lamino_layout)

        aux_group = QGroupBox("Auxiliary FFC Settings")
        aux_group.setCheckable(True)
        aux_group.setChecked(False)
        aux_layout = QGridLayout()
        aux_layout.addWidget(self.dark_scale_label, 0, 0)
        aux_layout.addWidget(self.dark_scale_entry, 0, 1)
        aux_layout.addWidget(self.flat_scale_label, 1, 0)
        aux_layout.addWidget(self.flat_scale_entry, 1, 1)
        aux_group.setLayout(aux_layout)

        layout.addWidget(lamino_group)
        layout.addWidget(aux_group)

        self.setLayout(layout)

    def init_values(self):
        self.rotation_range_entry.setText("180")
        self.lamino_angle_entry.setText("0")
        self.sample_rotation_beam_entry.setText("")
        self.sample_rotation_vert_entry.setText("")

        self.dark_scale_entry.setText("")
        self.flat_scale_entry.setText("")

    def set_values_from_params(self):
        pass

