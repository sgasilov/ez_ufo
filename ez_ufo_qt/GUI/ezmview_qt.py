import sys
from PyQt5.QtWidgets import QGroupBox, QPushButton, QLineEdit, QLabel, QCheckBox, QGridLayout, QHBoxLayout, QApplication

class EZMView(QGroupBox):

    def __init__(self):
        super().__init__()

        self.setTitle("EZMView")
        self.setStyleSheet('QGroupBox {color: green;}')

        self.input_dir_button = QPushButton()
        self.input_dir_button.setText("Select directory with a CT sequence")

        self.input_dir_entry = QLineEdit()

        self.num_projections_label = QLabel()
        self.num_projections_label.setText("Number of projections")

        self.num_projections_entry = QLineEdit()

        self.num_flats_label = QLabel()
        self.num_flats_label.setText("Number of flats")

        self.num_flats_entry = QLineEdit()

        self.num_darks_label = QLabel()
        self.num_darks_label.setText("Number of darks")

        self.num_darks_entry = QLineEdit()

        self.num_vert_steps_label = QLabel()
        self.num_vert_steps_label.setText("Number of vertical steps")

        self.num_vert_steps_entry = QLineEdit()

        self.no_trailing_flats_darks_checkbox = QCheckBox()
        self.no_trailing_flats_darks_checkbox.setText("No trailing flats/darks")

        self.filenames_without_padding_checkbox = QCheckBox()
        self.filenames_without_padding_checkbox.setText("File names without zero padding")

        self.convert_button = QPushButton()
        self.convert_button.setText("Convert")

        self.undo_button = QPushButton()
        self.undo_button.setText("Undo")

        self.help_button = QPushButton()
        self.help_button.setText("Help")

        self.quit_button = QPushButton()
        self.quit_button.setText("Quit")

        self.set_layout()

        #self.show()

    def set_layout(self):
        layout = QGridLayout()
        layout.addWidget(self.input_dir_button, 0, 0)
        layout.addWidget(self.input_dir_entry, 1, 0)

        grid = QGridLayout()
        grid.addWidget(self.num_projections_label, 0, 0)
        grid.addWidget(self.num_projections_entry, 0, 1)
        grid.addWidget(self.num_flats_label, 1, 0)
        grid.addWidget(self.num_flats_entry, 1, 1)
        grid.addWidget(self.num_darks_label, 2, 0)
        grid.addWidget(self.num_darks_entry, 2, 1)
        grid.addWidget(self.num_vert_steps_label, 3, 0)
        grid.addWidget(self.num_vert_steps_entry, 3, 1)
        grid.addWidget(self.no_trailing_flats_darks_checkbox, 4, 0)
        grid.addWidget(self.filenames_without_padding_checkbox, 4, 1)
        layout.addItem(grid, 2, 0)

        hbox = QHBoxLayout()
        hbox.addWidget(self.convert_button)
        hbox.addWidget(self.undo_button)
        hbox.addWidget(self.help_button)
        hbox.addWidget(self.quit_button)

        layout.addItem(hbox, 3, 0)

        self.setLayout(layout)

'''
if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = EZMView()
    sys.exit(app.exec_())
'''