# IMPORTING OF REQUIRED MODULES
import random
import time

from customtkinter import *
from tkinter import filedialog
from PIL import ImageGrab

def save_frame_as_image():
    """This function saves the palette generated in the color frame as a png"""

    # DEACTIVATING THE BUTTON TO PREVENT MULTIPLE CLICKS
    save_btn.configure(state="disabled")
    file_path = filedialog.asksaveasfilename()

    if file_path:
        # UPDATES FRAME TO GET THE CURRENT POSITION AND SIZE
        root.update()

        # GETTING THE CURRENT POSITION AND SIZE
        x = root.winfo_rootx() + c_frame.winfo_x()
        y = root.winfo_rooty() + c_frame.winfo_y()
        w =  c_frame.winfo_width()
        h = c_frame.winfo_height()

        # CAPTURE IMAGE FROM THE SCREEN
        img = ImageGrab.grab(bbox=(x, y, x + w, y + h))
        img.save(f"{file_path}.png")

    # RE-ACTIVATING THE BUTTON AFTER THE IMAGE HAS BEEN SAVED
    save_btn.configure(state="active")

def change_color():
    """This function to be used in an after method to recursely change the colours in the frame"""
    # The initial version of this code used this function to generate all the possible colors from the
    # color generator and capture an image of them saving them with their hexadecimal color code
    try:
        active_clr = next(color_generator)
        c_frame.configure(fg_color=active_clr)
        # save_frame_as_image(filename= f"{active_clr}.png")
    except Exception:
        ...

def generate_palette():
    """This function generates a random color palette of n_colors in the color frame when called"""

    # DELETING ALL ITEMS FROM THE COLOR FRAME WHEN A NEW PALETTE IS TO BE GENERATED
    for child in list(c_frame.children.values()):
        child.destroy()

    # CREATING RANDOM N_COLORS COLOR CARDS TO BE PACKED IN THE COLOR FRAME
    for j in range(int(n_colors.get())):
        color = random.choice(total_clrs)
        color_card = CTkFrame(c_frame, fg_color=color)
        color_card.pack(side=LEFT, fill= BOTH, expand=1, padx=5, pady=10)
        label = CTkLabel(color_card, text=color, fg_color="grey17", corner_radius=10, font=font)
        label.pack(side=BOTTOM, fill= X, padx=10, pady=10)

def configure_label(event):
    """This function updates the color label when the slider is moved"""

    # UPDATING THE COLOR LABEL
    if int(n_colors.get()) == 1:
        c_label.configure(text=f"The Number of Colors in the palette to be generated is {int(n_colors.get())}")
    else:
        c_label.configure(text=f"The Number of Colors in the palette to be generated are {int(n_colors.get())}")


# SETTING UP DEFAULT COLOR THEME
set_default_color_theme("green")

# DEFINING CONSTANTS
R, G, B = [], [], []

# GENERATING THE RANDOM COLORS
for i in range(256):
    if not (i+1) % 16 or i==0:
        R.append(f"{i:02X}")
        G.append(f"{i:02X}")
        B.append(f"{i:02X}")

total_clrs = []
for r in R:
    for g in G:
        for b in B:
            total_clrs.append("#"+r+g+b)



color_generator = (c for c in total_clrs)

# SETTING UP THE GUI
root = CTk()

root.iconbitmap("logo/s0urcec0de.ico")
root.geometry("600x400")
root.title("COLOR DISPLAYER")
root.minsize(400, 250)

font = ("Bahnschrift", 18)
padding = {"padx": 10,
           "pady": 10}

n_colors = CTkSlider(root, from_=1, to=4, number_of_steps=3, command=configure_label)
n_colors.set(1)

c_label = CTkLabel(root, text=f"The Number of Colors in the palette to be generated is {int(n_colors.get())}",
                   font=font, anchor="w", fg_color=('#2CC985', '#2FA572'), corner_radius=5)

btn_frame = CTkFrame(root)
save_btn = CTkButton(btn_frame, text="SAVE", command=save_frame_as_image, font=font)
palette_btn = CTkButton(btn_frame, text="GENERATE", command=generate_palette, font=font)

c_frame = CTkFrame(root)
c_label.pack(side=TOP, fill=X, **padding)
n_colors.pack(side=TOP, fill=X, **padding)
btn_frame.pack(side=TOP, fill=BOTH, **padding)

palette_btn.pack(side=LEFT, fill=X, expand=1, **padding)
save_btn.pack(side=LEFT, fill=X, expand=1, **padding)

c_frame.pack(side=TOP, fill=BOTH, expand=1, **padding)

generate_palette()
root.mainloop()
