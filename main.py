import tkinter as tk
from tkinter import filedialog as fd
from Huffman import Huffman

import magic

def check_file_extension(file_bytes):
    file_type = magic.from_buffer(file_bytes)
    if 'PDF' in file_type:
        return '.pdf'
    elif 'JPEG' in file_type:
        return '.jpg'
    elif 'PNG' in file_type:
        return '.png'
    elif 'text' in file_type:
        return '.txt'
    elif 'MP3' in file_type:
        return '.mp3'
    else:
        return None

from RLE import RLE
def callback():
    name = fd.askopenfilename()
    with open(name, 'rb') as data:
        data = data.read()
        huffer = Huffman()
        rle = RLE()
        if name[-6::] == "ultarc":
            signature = data[:7]
            unarchived = b''
            if signature == b'ACEARCH':
                print("huff")
                unarchived = huffer.unarchive("output")
            elif signature == b'ACEARCR':
                unarchived = rle.unarchive("output")
            else:
                print("What da heeeel")
            extension = check_file_extension(unarchived)
            with open (f"unarchived{extension}", "wb") as f:
                f.write(unarchived)
        else:
            huff_data = huffer.archive(data)
            rle_data = rle.archive(data)
            with open("output.ultarc", "wb") as f:
                f.write(b'ACEARC')
                if len(huff_data) < len(rle_data):
                    f.write(b'H')
                    f.write(huff_data)
                else:
                    f.write(b'R')
                    f.write(rle_data)

        exit(0)


tk.Button(text='Click to Open File',
          command=callback).pack(fill=tk.X)

tk.mainloop()