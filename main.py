import os
from tkinter import StringVar, TOP, BOTTOM, LEFT, RIGHT
from PIL import Image, ImageTk
# from tkinterdnd2 import TkinterDnD, DND_ALL
from tkinterdnd2 import DND_FILES, TkinterDnD
import customtkinter as ctk
from CTkMenuBar import *
from rembg import remove

class Tk(ctk.CTk, TkinterDnD.DnDWrapper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.TkdndVersion = TkinterDnD._require(self)

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")
root = Tk()
root.geometry("720x550")
root.title("Image resizer")
basedir = os.path.dirname(__file__)
root.iconbitmap(os.path.join(basedir, "resize.ico"))

extensions = ['.png', '.jpg', '.gif', '.bmp', '.ico', '.webp']

def is_valid_extension(name, extension):
    if name in extension:
        return True
    else:
        return False

def ChangeToDark():
    ctk.set_appearance_mode("dark")
    menu.configure(bg_color="#1C1C1C")

def ChangeToLight():
    ctk.set_appearance_mode("light")
    menu.configure(bg_color='#C3C3C3')

def get_path(event):
    labelStart.pack_forget()
    path = event.data
    path = path.replace('{', '').replace('}', '')
    file_name = os.path.basename(path)
    extension = os.path.splitext(file_name)[1]
    print(path)
    if is_valid_extension(extension, extensions):
        infoLabel.configure(text='')
        pathLabel.configure(text = path)
        # browse_button.configure(text = event.data)
        try:
            image = Image.open(path)
            # image = Image.open(event.data)
            image_tk = ctk.CTkImage(image, size=[300, 300])
            labelImage.configure(image=image_tk)
            width, height = image.size
            image_size = f'Image size: {width}px x {height}px'
            labelSize.configure(text=image_size)
            firstNum.set(value=width)
            secondNum.set(value=height)
        except Exception as e:
            infoLabel.configure(text="Could not load image")
            labelImage.configure(image=None)
            labelSize.configure(text='')
            pathLabel.configure(text='')

    else:
        infoLabel.configure(text="Extension of this file is not supported")

def browse_folder():
    file_path = ctk.filedialog.askopenfilename()
    print(file_path)
    if file_path:
        labelStart.pack_forget()
        pathLabel.configure(text=file_path)
        try:
            image = Image.open(file_path)
            image_tk = ctk.CTkImage(image, size=[300, 300])
            labelImage.configure(image=image_tk)
            width, height = image.size
            image_size = f'Image size: {width}px x {height}px'
            labelSize.configure(text=image_size)
            firstNum.set(value=width)
            secondNum.set(value=height)
        except Exception as e:
            infoLabel.configure(text="Could not load image")
            labelImage.configure(image=None)
            labelSize.configure(text='')

def download_file():
    # try:
    file_path = pathLabel.cget('text')
    folder_path = folderLabel.cget('text')
    if file_path != '':
        file_name = os.path.basename(file_path)
        name, extension = os.path.splitext(file_name)
        # print(os.path.splitext(file_name)[0])
        image = Image.open(file_path)
        if removeBackground.get() == 1:
            image = remove(image)
        try:
            width = firstNum.get()
            widthImage, heightImage = image.size
            if checkAspectRatio.get() == 1:
                ratio = widthImage/heightImage
                height = int(int(width)/ratio)
                secondNum.set(value=height)
            height = secondNum.get()
            new_image = image.resize((int(width), int(height)))
            if folder_path != '':
                new_image.save(f'{folder_path}/{name}-res{extension}')
            else:
                new_image.save(f'{name}-res{extension}')
            infoLabel.configure(text='Download completed')
        except:
            infoLabel.configure(text='Size must be an integer')
    else:
        infoLabel.configure(text='You have to insert an image')
    # except:
    #     infoLabel.configure(text='You have to insert an image')

def SetAspectRatio():
    file_path = pathLabel.cget('text')
    if file_path != '':
        # print(os.path.splitext(file_name)[0])
        image = Image.open(file_path)
        width, height = image.size
        ratio = int(width)/int(height)
        widthImage = firstNum.get()
        heightImage = int(int(widthImage)/ratio)
        secondNum.set(value=heightImage)
        # width = firstNum.get()
        # secondNum.set(value=width)

def changeFolderDownload():
    folder_path = ctk.filedialog.askdirectory()
    if folder_path:
        folderLabel.configure(text=folder_path)

def AboutAuthor():
    author_window = ctk.CTkToplevel()
    author_window.title("Author info")
    author_window.geometry("300x300")
    text = ctk.CTkLabel(author_window, text="Created by anteczek\nfor fun", font=fontlabelStart)
    text.pack(pady=100)

def AboutApp():
    app_window = ctk.CTkToplevel()
    app_window.title("App info")
    app_window.geometry("300x300")
    text = ctk.CTkLabel(app_window, text="Basic image resizer\nwritten in python", font=fontlabelStart)
    text.pack(pady=100)
    # print(removeBackground.get())
# nameVar = StringVar()

# entryWidget = ctk.CTkEntry(root)
# entryWidget.pack(side=TOP, padx=5, pady=5)

# pathLabel = ctk.CTkLabel(root, text="Drag and drop file in the entry box")
# pathLabel.pack(side=TOP)

# entryWidget.drop_target_register(DND_FILES)
# entryWidget.dnd_bind("<<Drop>>", get_path)
fontButton = ctk.CTkFont(family="Roboto", size=16, weight="bold")
fontlabelStart = ctk.CTkFont(family="Roboto", size=25, weight="bold")
fontaspectRatio = ctk.CTkFont(family="Roboto", size=15, weight="bold")

menu = CTkMenuBar(root, bg_color="#1C1C1C")
button_1 = menu.add_cascade("File")
button_2 = menu.add_cascade("Settings")
button_3 = menu.add_cascade("About")

dropdown1 = CustomDropdownMenu(widget=button_1)
dropdown1.add_option(option="Select location of saving", command= changeFolderDownload)
# dropdown1.add_option(option="Save", command=lambda: print("Open"))

# dropdown2 = CustomDropdownMenu(widget=button_2)
# dropdown2.add_option(option="Cut")
# dropdown2.add_option(option="Copy")
# dropdown2.add_option(option="Paste")

dropdown3 = CustomDropdownMenu(widget=button_2)
ThemeDropDown = dropdown3.add_submenu("Theme")
ThemeDropDown.add_option(option="Dark", command=ChangeToDark)
ThemeDropDown.add_option(option="Light", command=ChangeToLight)

dropdown4 = CustomDropdownMenu(widget=button_3)
dropdown4.add_option(option="About author", command=AboutAuthor)
dropdown4.add_option(option="About app", command=AboutApp)
# file_menu = CTkMenuBar(my_menu)

folderLabel = ctk.CTkLabel(root, text='')

labelImage = ctk.CTkLabel(root, text='', width=200, height=200)
labelImage.pack(side=TOP, padx=5, pady=2)

labelStart = ctk.CTkLabel(root, text='To resize an image browse a file using\na browse button or drop it somewhere in the app', font=fontlabelStart)
labelStart.pack(side=TOP)

frameButtons = ctk.CTkFrame(root, width=300, height=200, fg_color='transparent')
frameButtons.pack(side=BOTTOM, padx=5, pady=10)

browse_button = ctk.CTkButton(frameButtons, text='Browse a file', width=150, height=50, text_color='#18141D', font=fontButton, command=browse_folder)
browse_button.pack(side=LEFT, padx=2)

resize_button = ctk.CTkButton(frameButtons, text='Download resized', width=150, height=50, text_color='#18141D', font=fontButton, command=download_file)
resize_button.pack(padx=2)

frameEntry = ctk.CTkFrame(root, width=200, height=40, fg_color='transparent')
frameEntry.pack(side=BOTTOM, padx=136.5, anchor='e')

firstNum = ctk.StringVar()

removeBackground = ctk.CTkCheckBox(frameEntry, text='remove BG', height=40, font=fontaspectRatio)
removeBackground.pack(side=LEFT, padx=20)

firstEntry = ctk.CTkEntry(frameEntry, textvariable=firstNum, width=60)
firstEntry.pack(side=LEFT, padx=2)

secondNum = ctk.StringVar()

secondEntry = ctk.CTkEntry(frameEntry, textvariable=secondNum, width=60)
secondEntry.pack(side=LEFT, padx=2)

checkAspectRatio = ctk.CTkCheckBox(frameEntry, text='aspect ratio', height=40, font=fontaspectRatio, command=SetAspectRatio)
checkAspectRatio.pack(side=RIGHT, padx=20)

infoLabel = ctk.CTkLabel(root, text='', font=fontaspectRatio, text_color='red')
infoLabel.pack(side=BOTTOM, padx=5, pady=2)

pathLabel = ctk.CTkLabel(root, text='', font=fontaspectRatio)
pathLabel.pack(side=BOTTOM, padx=5)

labelSize = ctk.CTkLabel(root, text='', font=fontaspectRatio)
labelSize.pack(side=BOTTOM, padx=5, pady=2)

root.bind("<Return>", lambda event: download_file())

root.drop_target_register(DND_FILES)
root.dnd_bind("<<Drop>>", get_path)

root.mainloop()