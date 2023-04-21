import tkinter as tk
from tkinter import filedialog as fd
from Huffman import Huffman
from RLE import RLE
def callback():
    name = fd.askopenfilename()
    with open(name, 'rb') as data:
        huffer = Huffman()
        # rle = RLE()
        if name[-3::] == "txt":
            huffer.archive(data, "output")
        elif name[-6::] == "ultarc":
            huffer.unarchive("output", "unarchived")
        exit(0)


tk.Button(text='Click to Open File',
          command=callback).pack(fill=tk.X)

tk.mainloop()