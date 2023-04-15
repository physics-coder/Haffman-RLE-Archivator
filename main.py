import tkinter as tk
from tkinter import filedialog as fd
from Huffman import Huffman
from RLE import RLE
def callback():
    name = fd.askopenfilename()
    with open(name, 'r') as data:
        # huffer = Huffman()
        rle = RLE()
        if name[-3::] == "txt":
            rle.text_archive(data, "output")
            # huffer.text_archive(data, "output")
        elif name[-6::] == "ultarc":
            rle.text_unarchive("output", "unarchived")
            # huffer.text_unarchive("output", "unarchived")
        exit(0)


tk.Button(text='Click to Open File',
          command=callback).pack(fill=tk.X)

tk.mainloop()
