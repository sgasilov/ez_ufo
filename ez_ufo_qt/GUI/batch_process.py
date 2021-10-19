from PyQt5.QtWidgets import QGroupBox, QLabel, QGridLayout, QPushButton, QFileDialog, QLineEdit
import logging

class BatchProcessGroup(QGroupBox):
    def __init__(self):
        super().__init__()

        self.parameters = {}

        self.input_dir_button = QPushButton("Select input directory")
        self.input_dir_button.clicked.connect(self.input_dir_button_pressed)

        self.input_dir_entry = QLineEdit()
        self.input_dir_entry.textChanged.connect(self.set_input_entry)

        self.batch_proc_button = QPushButton("Begin Batch Process")
        self.batch_proc_button.clicked.connect(self.batch_proc_button_pressed)

        self.set_layout()

    def set_layout(self):
        layout = QGridLayout()

        layout.addWidget(self.input_dir_button, 0, 0)
        layout.addWidget(self.input_dir_entry, 0, 1)

        layout.addWidget(self.batch_proc_button, 1, 0, 1, 2)
        self.setLayout(layout)

        self.show()

    def input_dir_button_pressed(self):
        logging.debug("Input Button Pressed")
        dir_explore = QFileDialog(self)
        input_dir = dir_explore.getExistingDirectory()
        self.input_entry.setText(input_dir)
        self.parameters['input_dir'] = input_dir

    def set_input_entry(self):
        logging.debug("Input Entry: " + str(self.input_entry.text()))
        self.parameters['input_dir'] = str(self.input_entry.text())

    def batch_proc_button_pressed(self):
        logging.debug("Batch Process Button Pressed")
