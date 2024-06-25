"""
file: main file containing the UI and instantiating the instrument
author: josh
last updated: 25/06/2024
"""

import sys
import sps
import tags
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QRadioButton, QHBoxLayout, QMessageBox
from PyQt5.QtGui import QDoubleValidator

class PowerSupplyControl(QWidget):
    def __init__(self):
        super().__init__()

        self.sps = sps.SPS(tags.sps_addr)
        self.sps.initialize()
        
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Power Supply Control')
        self.resize(300, 200)

        # Voltage input
        self.voltage_label = QLabel('Set Voltage (V):')
        self.voltage_input = QLineEdit(self)

        # Set up the validator for voltage input (for example, range from 0 to 1000 volts)
        self.voltage_validator = QDoubleValidator(0.0, 270, 2)  # min=0.0, max=1000.0, 2 decimal places
        self.voltage_input.setValidator(self.voltage_validator)

        # AC/DC selection
        self.ac_radio = QRadioButton('AC', self)
        self.dc_radio = QRadioButton('DC', self)
        self.dc_radio.setChecked(True)  # Default to DC

        # AC frequency input (only enabled when AC is selected)
        self.frequency_label = QLabel('Set AC Frequency (Hz):')
        self.frequency_input = QLineEdit(self)
        self.frequency_label.setEnabled(False)
        self.frequency_input.setEnabled(False)

        # Connect AC/DC radio buttons to toggle frequency input
        self.ac_radio.toggled.connect(self.toggle_frequency_input)

        # Submit button
        self.submit_button = QPushButton('Set Instrument', self)
        self.submit_button.clicked.connect(self.submit)

        # Stop amp button
        self.stop_button = QPushButton('Stop Amplifier', self)
        self.stop_button.clicked.connect(self.stop_amp)

        # Layout
        vbox = QVBoxLayout()

        vbox.addWidget(self.voltage_label)
        vbox.addWidget(self.voltage_input)

        hbox = QHBoxLayout()
        hbox.addWidget(self.dc_radio)
        hbox.addWidget(self.ac_radio)
        vbox.addLayout(hbox)

        vbox.addWidget(self.frequency_label)
        vbox.addWidget(self.frequency_input)

        vbox.addWidget(self.submit_button)
        vbox.addWidget(self.stop_button)

        self.setLayout(vbox)

    # UI helper function for AC/DC input change
    def toggle_frequency_input(self):
        if self.ac_radio.isChecked():
            self.frequency_label.setEnabled(True)
            self.frequency_input.setEnabled(True)
        else:
            self.frequency_label.setEnabled(False)
            self.frequency_input.setEnabled(False)

    def submit(self):
        voltage = self.voltage_input.text()
        if not voltage or float(voltage) > 270:
            self.show_error_message('Please enter a valid voltage.')
            return

        if self.dc_radio.isChecked():
            self.sps.set_voltage_dc(voltage)
            
        else:
            frequency = self.frequency_input.text()
            if not frequency:
                frequency = 50

            self.sps.set_voltage_ac(voltage, frequency)

    def stop_amp(self):
        self.sps.set_amp_off()

    def show_error_message(self, message):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setText(message)
        msg.setWindowTitle("Input Error")
        msg.exec_()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = PowerSupplyControl()
    ex.show()
    sys.exit(app.exec_())
