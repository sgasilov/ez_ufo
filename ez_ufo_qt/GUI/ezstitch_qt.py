import sys
from PyQt5.QtWidgets import QGroupBox, QPushButton, QCheckBox, QLabel, QLineEdit, QGridLayout, QWidget, QApplication, QVBoxLayout, QHBoxLayout, QRadioButton

class EZStitchGroup(QGroupBox):

    def __init__(self):
        super().__init__()

        self.setTitle("EZ Stitch")
        self.setStyleSheet('QGroupBox {color: purple;}')

        self.input_dir_button = QPushButton()
        self.input_dir_button.setText("Select input directory with a 000,001,...,00N subdirectories")
        self.input_dir_entry = QLineEdit()

        self.tmp_dir_button = QPushButton()
        self.tmp_dir_button.setText("Select temporary directory - default value recommended")
        self.tmp_dir_entry = QLineEdit()

        self.output_dir_button = QPushButton()
        self.output_dir_button.setText("Directory to save stitched images")
        self.output_dir_entry = QLineEdit()

        self.types_of_images_label = QLabel()
        self.types_of_images_label.setText("Type of images to stitch (e.g. sli, tomo, proj-pr, etc.)")
        self.types_of_images_entry = QLineEdit()

        self.orthogonal_checkbox = QCheckBox()
        self.orthogonal_checkbox.setText("Stitch orthogonal sections")

        self.start_stop_step_label = QLabel()
        self.start_stop_step_label.setText("Which images to be stitched: start,stop,step:")
        self.start_stop_step_entry = QLineEdit()

        self.sample_moved_down_checkbox = QCheckBox()
        self.sample_moved_down_checkbox.setText("Sample was moved downwards during scan")

        self.interpolate_regions_rButton = QRadioButton()
        self.interpolate_regions_rButton.setText("Interpolate overlapping regions and equalize intensity")

        self.num_overlaps_label = QLabel()
        self.num_overlaps_label.setText("Number of overlapping rows")
        self.num_overlaps_entry = QLineEdit()

        self.clip_histogram_checkbox = QCheckBox()
        self.clip_histogram_checkbox.setText("Clip histogram and convert slices to 8-bit before saving")

        self.min_value_label = QLabel()
        self.min_value_label.setText("Min value in 32-bit histogram")
        self.min_value_entry = QLineEdit()

        self.max_value_label = QLabel()
        self.max_value_label.setText("Max value in 32-bit histogram")
        self.max_value_entry = QLineEdit()

        self.concatenate_rButton = QRadioButton()
        self.concatenate_rButton.setText("Concatenate only")

        self.first_row_label = QLabel()
        self.first_row_label.setText("First row")
        self.first_row_entry = QLineEdit()

        self.last_row_label = QLabel()
        self.last_row_label.setText("Last row")
        self.last_row_entry = QLineEdit()

        self.half_acquisition_rButton = QRadioButton()
        self.half_acquisition_rButton.setText("Half acquisition mode")

        self.column_of_axis_label = QLabel()
        self.column_of_axis_label.setText("In which column the axis of rotation is")
        self.column_of_axis_entry = QLineEdit()

        self.stitch_button = QPushButton()
        self.stitch_button.setText("Stitch")
        self.stitch_button.setStyleSheet("background-color:lightgrey;color: royalblue; font: 14pt; font-weight: bold;")

        self.delete_button = QPushButton()
        self.delete_button.setText("Delete output dir")
        self.delete_button.setStyleSheet("background-color:lightgrey;color:black; font: 14pt; font-weight: bold;")

        self.help_button = QPushButton()
        self.help_button.setText("Help")
        self.help_button.setStyleSheet("background-color:lightgrey;color:black; font: 14pt; font-weight: bold;")

        self.quit_button = QPushButton()
        self.quit_button.setText("Quit")
        self.quit_button.setStyleSheet("background-color:lightgrey;color:black; font: 14pt; font-weight: bold;")

        self.set_layout()

        #self.show()

    def set_layout(self):
        layout = QGridLayout()

        vbox1 = QVBoxLayout()
        vbox1.addWidget(self.input_dir_button)
        vbox1.addWidget(self.input_dir_entry)
        vbox1.addWidget(self.tmp_dir_button)
        vbox1.addWidget(self.tmp_dir_entry)
        vbox1.addWidget(self.output_dir_button)
        vbox1.addWidget(self.output_dir_entry)
        layout.addItem(vbox1, 0, 0)

        grid = QGridLayout()
        grid.addWidget(self.types_of_images_label, 0, 0)
        grid.addWidget(self.types_of_images_entry, 0, 1)
        grid.addWidget(self.orthogonal_checkbox, 1, 0)
        grid.addWidget(self.start_stop_step_label, 2, 0)
        grid.addWidget(self.start_stop_step_entry, 2, 1)
        grid.addWidget(self.sample_moved_down_checkbox, 3, 0)
        grid.addWidget(self.interpolate_regions_rButton, 4, 0)
        grid.addWidget(self.num_overlaps_label, 5, 0)
        grid.addWidget(self.num_overlaps_entry, 5, 1)
        grid.addWidget(self.clip_histogram_checkbox, 6, 0)
        grid.addWidget(self.min_value_label, 7, 0)
        grid.addWidget(self.min_value_entry, 7, 1)
        layout.addItem(grid, 1, 0)

        grid2 = QGridLayout()
        grid2.addWidget(self.concatenate_rButton, 0, 0)
        grid2.addWidget(self.first_row_label, 1, 0)
        grid2.addWidget(self.first_row_entry, 1, 1)
        grid2.addWidget(self.last_row_label, 1, 2)
        grid2.addWidget(self.last_row_entry, 1, 3)
        layout.addItem(grid2, 2, 0)

        grid3 = QGridLayout()
        grid3.addWidget(self.half_acquisition_rButton, 0, 0)
        grid3.addWidget(self.column_of_axis_label, 1, 0)
        grid3.addWidget(self.column_of_axis_entry, 1, 1)
        layout.addItem(grid3, 3, 0)

        hbox = QHBoxLayout()
        hbox.addWidget(self.stitch_button)
        hbox.addWidget(self.delete_button)
        hbox.addWidget(self.help_button)
        hbox.addWidget(self.quit_button)
        layout.addItem(hbox, 4, 0)

        self.setLayout(layout)

'''
if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = EZStitchGroup()
    sys.exit(app.exec_())
'''
