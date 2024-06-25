"""
file: contains constants referenced in other parts of program, constant values and such
author: josh
last updated: 25/06/2024
"""

import datetime

sps_addr = 'GPIB0::6::INSTR' 
ars_addr = 'GPIB0::3::INSTR'

def log(tag, message):
    print(f'{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]} -- LOG -- {tag}: {message}')