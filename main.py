import tkinter as tk
from tkinter import filedialog as fd
from Huffman import Huffman
def callback():
    name = fd.askopenfilename()
    with open(name, 'r') as data:
        huffer = Huffman()
        if name[-3::] == "txt":
            huffer.text_archive(data, "output")
        elif name[-6::] == "ultarc":
            huffer.text_unarchive("output", "unarchived")
        exit(0)


tk.Button(text='Click to Open File',
          command=callback).pack(fill=tk.X)

tk.mainloop()