"""
Front-end GUI for SAR Manipulator.
"""

__author__ = 'Alex Alkire'
__version__ = '0.1'
__license__ = 'MIT'

from tkinter import filedialog

import cv2
import PIL.Image, PIL.ImageTk
from tkinter import *

from sar_crypto import decrypt_sar, struct_to_file
from symbol_art import SymbolArt


def foobar():
    print("fnc pressed")
    pass


class UI(Frame):
    def update_symbol_art(self, _image):
        _image = cv2.cvtColor(_image, cv2.COLOR_BGR2RGB)
        self.pil_image = _image
        self.tk_image = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(_image))

    def open_sar(self):
        filename = filedialog.askopenfilename(initialdir="/", title="Select file",
                                              filetypes=(("SAR files", "*.sar"), ("all files", "*.*")))
        print(filename)
        print("1")
        self.loaded_sar = decrypt_sar(filename)
        print("2")
        self.structured_sar = SymbolArt(self.loaded_sar)
        self.pil_image = self.structured_sar.get_as_image()
        self.update_symbol_art(self.pil_image)
        self.update()

    def save_sar(self):
        filename = filedialog.asksaveasfilename(initialdir="/", title="Save file",
                                          filetypes=(("SAR files", "*.sar"), ("all files", "*.*")))
        print(filename)
        with open(filename, "wb") as file:
            file.write(struct_to_file(self.structured_sar))

    def __init__(self, master=None):
        self.pil_image = None
        self.tk_image = None
        self.structured_sar = None
        self.loaded_sar = None
        super().__init__(master)
        master.geometry("512x512")
        master.resizable(False, False)
        master.title("SAR Manipulator")

        # Add Menus
        menu_bar = Menu(master)
        file_menu = Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Open .SAR", command=self.open_sar)
        file_menu.add_command(label="Open .PNG", command=foobar)
        file_menu.add_command(label="Save .SAR", command=self.save_sar)
        file_menu.add_command(label="SAVE .PNG", command=foobar)
        master.config(menu=menu_bar)

        # Set up Image to show in the window.
        image_canvas = Canvas(master, width=512, height=512)
        image_canvas.pack()
        self.image_label = Label(image_canvas)
        self.image_label.place(x=0, y=0)

    def update(self):
        self.image_label.configure(image=self.tk_image)
