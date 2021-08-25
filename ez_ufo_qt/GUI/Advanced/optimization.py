import logging
from PyQt5.QtWidgets import QGridLayout, QLabel, QRadioButton, QGroupBox, QLineEdit, QCheckBox

import ez_ufo_qt.GUI.params as parameters

class OptimizationGroup(QGroupBox):
    """
    Optimization settings
    """

    def __init__(self):
        super().__init__()

        self.setTitle("Optimization Settings")
        self.setStyleSheet('QGroupBox {color: orange;}')

        self.slice_memory_label = QLabel("Slice memory coefficient")
        self.slice_memory_entry = QLineEdit()

        self.num_GPU_label = QLabel("Number of GPUs")
        self.num_GPU_entry = QLineEdit()

        self.slices_per_device_label = QLabel("Slices per device")
        self.slices_per_device_entry = QLineEdit()

        self.set_layout()

    def set_layout(self):
        layout = QGridLayout()

        gpu_group = QGroupBox('GPU optimization')
        gpu_group.setCheckable(True)
        gpu_group.setChecked(False)
        gpu_layout = QGridLayout()
        gpu_layout.addWidget(self.slice_memory_label, 0, 0)
        gpu_layout.addWidget(self.slice_memory_entry, 0, 1)
        gpu_layout.addWidget(self.num_GPU_label, 1, 0)
        gpu_layout.addWidget(self.num_GPU_entry, 1, 1)
        gpu_layout.addWidget(self.slices_per_device_label, 2, 0)
        gpu_layout.addWidget(self.slices_per_device_entry, 2, 1)
        gpu_group.setLayout(gpu_layout)

        layout.addWidget(gpu_group)

        self.setLayout(layout)

    def init_values(self):
        self.slice_memory_entry.setText("0.5")
        parameters.params['e_adv_slice_mem_coeff'] = "0.5"
        self.num_GPU_entry.setText("")
        parameters.params['e_adv_num_gpu'] = ""
        self.slices_per_device_entry.setText("")
        parameters.params['e_adv_slices_per_device'] = ""

    def set_values_from_params(self):
        self.slice_memory_entry.setText(str(parameters.params['e_adv_slice_mem_coeff']))
        self.num_GPU_entry.setText(str(parameters.params['e_adv_num_gpu']))
        self.slices_per_device_entry.setText(str(parameters.params['e_adv_slices_per_device']))