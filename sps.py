"""
file: derived instrument class for Spitzenberger Spies "power supply"
author: josh
last updated: 25/06/2024
"""

import instrument
import tags
from time import sleep

class SPS(instrument.BaseInstrument):

    def __init__(self, visa_address):
        super().__init__(visa_address)

    # turn amp off
    def set_amp_off(self):
        if self.connect():
            self.instrument.write('AMP:OUTPUT 0')
            self.disconnect()
            tags.log('SPS', 'Amplifier turned off.')

    # set voltage DC
    def set_voltage_dc(self, voltage):
        if self.connect():
            self.instrument.write('AMP:RANGE 1')
            self.instrument.write('AMP:MODE:DC')
            self.instrument.write('OSC:FREQ 0')
            self.instrument.write(f'OSC:AMP 1,{voltage}V')
            self.instrument.write('AMP:OUTPUT 1')
            
            self.disconnect()
            tags.log('SPS', f'DC voltage set to {voltage}V')

    # set voltage AC
    def set_voltage_ac(self, voltage, freq):
        if self.connect():
            self.instrument.write('AMP:RANGE 3')
            self.instrument.write('AMP:MODE:AC')
            self.instrument.write(f'OSC:FREQ {freq}')
            self.instrument.write(f'OSC:AMP 1,{voltage}V')
            self.instrument.write('AMP:OUTPUT 1')

            self.disconnect()
            tags.log('SPS', f'AC voltage set to {voltage}V at {freq}Hz')