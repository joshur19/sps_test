"""
file: derived instrument class for Spitzenberger Spies "power supply"
author: josh
last updated: 03/07/2024
"""

import instrument
import tags
from time import sleep

class SPS(instrument.BaseInstrument):

    def __init__(self, visa_address):
        super().__init__(visa_address)

    # initialize system for direct voltage supply
    def initialize(self):
        if self.connect():
            self.instrument.write('DCL')   # reset SyCore to default settings
            sleep(2)
            self.disconnect()

        try:
            ars = self.rm.open_resource(tags.ars_addr)
            sleep(1)
            ars.write('SET_IMPEDANCE=OFF')
            sleep(1)
            ars.write('H_I_RANGE=8')        # configuration for ARS direct mode without harmonics/flicker
            sleep(1)
            ars.close()
        except:
            tags.log('SPS', 'Error initializing ARS to direct mode.')

    # turn amp off
    def set_amp_off(self):
        if self.connect():
            self.instrument.write(f'OSC:AMP 1,0V')              # reset oscillator amplitude to 0V
            sleep(3)
            self.instrument.write('AMP:OUTPUT 0')               # turn amplifier output off
            sleep(2)

            self.disconnect()
            tags.log('SPS', 'Amplifier turned off.')

    # set voltage DC
    def set_voltage_dc(self, voltage):
        if self.connect():

            self.instrument.write('DCL')                        # reset instrument to default state
            sleep(4)

            range = self.determine_range(voltage)
            
            self.instrument.write(f'AMP:RANGE {range}')         # set appropriate amplifier range
            sleep(3)
            self.instrument.write('AMP:MODE:DC')                # set amplifier to DC mode
            sleep(1)
            self.instrument.write('OSC:PAGE:FUNC 1,"DC"')       # set oscillator to DC mode (phase 1)
            sleep(1)
            self.instrument.write(f'OSC:AMP 1,{voltage}V')      # set oscillator amplitude to voltage (phase 1)
            sleep(7)
            self.instrument.write('AMP:OUTPUT 1')               # turn on amplifier output
            sleep(1)
            
            self.disconnect()
            tags.log('SPS', f'DC voltage set to {voltage}V')

    # set voltage AC
    def set_voltage_ac(self, voltage, freq):
        if self.connect():

            self.instrument.write('DCL')                        # reset instrument to default state
            sleep(4)

            range = self.determine_range(voltage)

            self.instrument.write(f'AMP:RANGE {range}')         # set appropriate amplifier range
            sleep(3)    
            self.instrument.write('AMP:MODE:AC')                # set amplifier to DC mode
            sleep(1)
            self.instrument.write(f'OSC:FREQ {freq}')           # set oscillator frequency
            sleep(1)
            self.instrument.write(f'OSC:AMP 1,{voltage}V')      # set oscillator amplitude to voltage (phase 1)
            sleep(7)
            self.instrument.write('AMP:OUTPUT 1')               # turn on amplifier output
            sleep(1)

            self.disconnect()
            tags.log('SPS', f'AC voltage set to {voltage}V at {freq}Hz')

    # helper function for range selection
    def determine_range(self, voltage):
        if 0 < voltage <= 65:
            return 1
        elif voltage <= 135:
            return 2
        elif voltage <= 270:
            return 3
        else: 
            return 0