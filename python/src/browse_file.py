# Python program to create 
# a file explorer in Tkinter

# import all components
# from the tkinter library
from tkinter import *

# import filedialog module
from tkinter import filedialog

# Function for opening the 
# file explorer window
def browseFiles():
    
    filename = filedialog.askopenfilename(initialdir = "/",title = "Select a File for making template",filetypes = (("all files","*.*"),("jpeg files","*.jpeg*"),("png files","*.png*"),("jpg files","*.jpg*")))
    return filename
	
	

def browse():

    # Create the root window
    window = Tk()
    window.withdraw()

   

    path = browseFiles()
    # window.mainloop()
    window.destroy()
    return path 


if __name__=='__main__':
    browse()
