"""
SAR Manipulator is an application for translating between .sar files used in PSO2 (Symbol Arts) and standard
image file formats.
"""

__author__ = 'Alex Alkire'
__version__ = '0.1'
__license__ = 'MIT'

from sar_crypto import *
from symbol_art import *
from ui import *

loaded_sar = None
loaded_sar=decrypt_sar('sar/stock1.sar')
structured_sar = SymbolArt(loaded_sar)

if structured_sar:
    img = structured_sar.get_as_image()
    root = Tk()
    app = UI(master=root)
    app.update_symbol_art(img)
    app.update()
    app.mainloop()
    root.destroy()
