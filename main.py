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



raw_sar = None
with open('sar/stock2m.sar', "rb") as f:
    raw_sar = bytearray(f.read())
    print("raw:", raw_sar)
loaded_sar = decrypt_sar('sar/stock2m.sar')
structured_sar = SymbolArt(loaded_sar)
e_sar = struct_to_file(structured_sar)
print("raw:", raw_sar)
print("ree:", e_sar)
print("lens", len(raw_sar), len(loaded_sar)+4, len(e_sar))

i = 0
for (b1, b2) in zip(raw_sar, e_sar):
   # print("i: "+(str(i))+" b1: "+str(b1)+", b2: "+str(b2))
    if(b1 != b2):
        if i<12:
            print("MISMATCH: on byte [",i-4,"]",b1,b2)
        else:
            print("MISMATCH: on byte [",i-4, (i+12)%16, "]", b1, b2)
    i += 1

if structured_sar:
    img = structured_sar.get_as_image()
    root = Tk()
    app = UI(master=root)
    app.update_symbol_art(img)
    app.update()
    app.mainloop()
    root.destroy()
