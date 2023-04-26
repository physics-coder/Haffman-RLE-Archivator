from RLE import RLE
import threading
import time
import tkinter as tk
from tkinter import *
from tkinter import filedialog as fd
from tkinter import messagebox

import magic

from Huffman import Huffman

root = tk.Tk()
root.title("Ultarc file archivator")
f_name = tk.StringVar(root)

# Function for checking the file extension of archived files


def check_file_extension(file_bytes):
    file_type = magic.from_buffer(file_bytes)
    if 'JPEG' in file_type:
        return '.jpg'
    elif 'PNG' in file_type:
        return '.png'
    elif 'text' in file_type:
        return '.txt'
    elif 'Audio file' in file_type:
        return '.mp3'
    else:
        return None

# Function for archiving files using the Huffman algorithm


def huff_load():
    global huff_data
    global data
    global huffer
    huff_data = huffer.archive(data)
    return

# Function for archiving files using the RLE algorithm


def rle_load():
    global rle
    global rle_data
    global data
    rle_data = rle.archive(data)
    return

# Function for unarchiving files


def unarchiver():
    global error
    global data
    global file_name
    global name
    global finished
    signature = data[:7]
    unarchived = b''
    if signature == b'ACEARCH':
        unarchived = huffer.unarchive(name)
    elif signature == b'ACEARCR':
        unarchived = rle.unarchive(name)
    elif signature == b'ACEARCF':
        with open(name, "rb") as f:
            f.read(7)
            unarchived = f.read()
    else:
        messagebox.showerror(
            "Corrupted archive file",
            "The archive file has been corrupted. Please select a valid file.")
        finished = True
        error = True
        return
    extension = check_file_extension(unarchived)
    if extension:
        with open(f"{file_name}{extension}", "wb") as f:
            f.write(unarchived)
        finished = True
    else:
        messagebox.showwarning(
            'Extension absense',
            'The file archived is of an unknown extension, so it will be saved without one.')
        with open(file_name, "wb") as f:
            f.write(unarchived)
        finished = True
    return

# Function for file selection and start button creation


def file_selector():
    global name
    name = fd.askopenfilename()
    start_button.pack_forget()
    start_button.pack()

# Main function in which the input file is archived and unarchived using
# RLE and Huffman. When archiving the best algorithm is chosen.


def callback():
    global error
    global compress_rate
    global rle
    global data
    global finished
    global huffer
    global finished
    global file_name
    global name
    global archivation
    error = False
    finished = False
    text.pack()
    threading.Thread(target=load_bar).start()
    with open(name, 'rb') as data:
        data = data.read()
        huffer = Huffman()
        rle = RLE()
        if name[-6::] == "ultarc":
            archivation = False
            if f_name.get() != 'Optionally enter the output file name here' and f_name.get():
                file_name = f_name.get()
            else:
                if '.' in name:
                    file_name = f"{name.split('.')[0]}_unarchivated"
                else:
                    file_name = f"{name}_unarchivated"
            t2 = threading.Thread(target=unarchiver)
            if not t2.is_alive():
                t2.start()
        else:
            archivation = True
            if f_name.get() != 'Optionally enter the output file name here' and f_name.get():
                file_name = f_name.get()
            else:
                if '.' in name:
                    file_name = f"{name.split('.')[0]}_archivated"
                else:
                    file_name = f"{name}_archivated"
            huffman_thread = threading.Thread(target=huff_load)
            rle_thread = threading.Thread(target=rle_load)
            if not huffman_thread.is_alive():
                huffman_thread.start()
            if not rle_thread.is_alive():
                rle_thread.start()
            huffman_thread.join()
            rle_thread.join()

            with open(f"{file_name}.ultarc", "wb") as f:
                f.write(b'ACEARC')
                if len(huff_data) < len(data) or len(rle_data) < len(data):
                    if len(huff_data) < len(rle_data):
                        compress_rate = int(
                            (len(data) - len(huff_data)) / len(data) * 100)
                        f.write(b'H')
                        f.write(huff_data)
                    else:
                        compress_rate = int(
                            (len(data) - len(rle_data)) / len(data) * 100)
                        f.write(b'R')
                        f.write(rle_data)

                else:
                    compress_rate = 0
                    f.write(b'F')
                    f.write(data)
            finished = True

# Function for animated file entry box


def on_entry_click(event):
    if textBox.get() == 'Optionally enter the output file name here':
        textBox.delete(0, 'end')
        textBox.config(font=('Arial', 16))


text_label = tk.Label(root, text='Welcome to the "Ultarc" archivator! Click the button below to select a file.', font=('Arial', 24),
                      padx=10, pady=20, anchor='center')
text_label.pack()
frame = Frame()
textBox = Entry(
    frame,
    width=14,
    font=(
        'Arial',
        16,
        'italic'),
    justify=CENTER,
    textvariable=f_name)
textBox.insert(0, "Optionally enter the output file name here")
textBox.bind('<FocusIn>', on_entry_click)
textBox.pack(side=LEFT, padx=20, expand=True, fill=BOTH)
b = tk.Button(frame, text='Click to Open File',
              command=file_selector, height=1)
b.pack(side=RIGHT, padx=20, expand=True, fill=BOTH)

frame.pack(expand=True, fill=X, pady=10)
start_button = tk.Button(root, text='Start magic!',
                         command=callback, height=1, fg="purple")

text = Label(
    root,
    text="Loading",
    font=(
        'Arial',
        20,
        'bold'),
    fg="yellow",
    pady=20)
list = [
    "       ",
    ".      ",
    "..     ",
    "...    ",
    "....   ",
    ".....  ",
    "...... ",
    "......."]


# Function to create loading animation, while archivation or unarchivation
# is happening
def load_bar():
    global compress_rate
    global archivation
    k = 0
    while not finished:
        k += 1
        text.config(text="Magic in proccess" + list[k % 8], fg="yellow")
        text.update()
        time.sleep(0.1)
    if not error:
        text.config(text="Magic has happened!", fg="green")
        time.sleep(0.01)
        if archivation:
            if compress_rate > 0:
                messagebox.showinfo(
                    'Archivation results',
                    f'The file has been successfully compressed by {compress_rate} percent!')
            else:
                messagebox.showwarning(
                    'Archivation results',
                    "The archivator wasn't able to reduce the file size, the archivated size remains the same.")
    else:
        text.config(text="Error", fg="red")
    b.focus()
    return


tk.mainloop()
