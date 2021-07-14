import sys
from PyQt5.QtWidgets import QGroupBox, QPushButton, QCheckBox, QLabel, QLineEdit, QGridLayout, QWidget, QApplication, QVBoxLayout, QHBoxLayout

class MultiStitch360Group(QGroupBox):

    def __init__(self):
        super().__init__()

        self.input_dir_button = QPushButton()
        self.input_dir_button.setStyleSheet("background-color:gainsboro")
        self.input_dir_button.setText("Select input directory with 000,001,...,00N subdirectories")
        self.input_dir_button.setStyleSheet("background-color:lightgrey; font: 12pt;")

        self.input_dir_entry = QLineEdit()

        self.temp_dir_button = QPushButton()
        self.temp_dir_button.setStyleSheet("background-color:gainsboro")
        self.temp_dir_button.setText("Select temporary directory - default value recommended")
        self.temp_dir_button.setStyleSheet("background-color:lightgrey; font: 12pt;")

        self.temp_dir_entry = QLineEdit()

        self.output_dir_button = QPushButton()
        self.output_dir_button.setStyleSheet("background-color:gainsboro")
        self.output_dir_button.setText("Directory to save stitched images")
        self.output_dir_button.setStyleSheet("background-color:lightgrey; font: 12pt;")

        self.output_dir_entry = QLineEdit()

        self.crop_checkbox = QCheckBox()
        self.crop_checkbox.setText("Crop all projections to match the width of smallest stitched projection")

        self.axis_bottom_label = QLabel()
        self.axis_bottom_label.setText("Axis of Rotation at bottom (z00):")

        self.axis_bottom_entry = QLineEdit()

        self.axis_top_label = QLabel()
        self.axis_top_label.setText("Axis of Rotation at top (ignored if not multi-slice):")

        self.axis_top_entry = QLineEdit()

        self.stitch_button = QPushButton()
        self.stitch_button.setStyleSheet("background-color:gainsboro")
        self.stitch_button.setText("Stitch")
        self.stitch_button.setStyleSheet("background-color:lightgrey; font: 12pt;")

        self.delete_button = QPushButton()
        self.delete_button.setStyleSheet("background-color:gainsboro")
        self.delete_button.setText("Delete")
        self.delete_button.setStyleSheet("background-color:lightgrey; font: 12pt;")

        self.help_button = QPushButton()
        self.help_button.setStyleSheet("background-color:gainsboro")
        self.help_button.setText("Help")
        self.help_button.setStyleSheet("background-color:lightgrey; font: 12pt;")

        self.quit_button = QPushButton()
        self.quit_button.setStyleSheet("background-color:gainsboro")
        self.quit_button.setText("Quit")
        self.quit_button.setStyleSheet("background-color:lightgrey; font: 12pt;")

        self.set_layout()


    def set_layout(self):
        layout = QGridLayout()

        vbox = QVBoxLayout()
        vbox.addWidget(self.input_dir_button)
        vbox.addWidget(self.input_dir_entry)
        vbox.addWidget(self.temp_dir_button)
        vbox.addWidget(self.temp_dir_entry)
        vbox.addWidget(self.output_dir_button)
        vbox.addWidget(self.output_dir_entry)
        layout.addItem(vbox, 0, 0)

        layout.addWidget(self.crop_checkbox, 1, 0)

        grid = QGridLayout()
        grid.addWidget(self.axis_bottom_label, 0, 0)
        grid.addWidget(self.axis_bottom_entry, 0, 1)
        grid.addWidget(self.axis_top_label, 1, 0)
        grid.addWidget(self.axis_top_entry, 1, 1)
        layout.addItem(grid)

        hbox = QHBoxLayout()
        hbox.addWidget(self.stitch_button)
        hbox.addWidget(self.delete_button)
        hbox.addWidget(self.help_button)
        hbox.addWidget(self.quit_button)
        layout.addItem(hbox, 4, 0)

        self.setLayout(layout)

        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MultiStitch360Group()
    sys.exit(app.exec_())