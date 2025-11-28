import tkinter
from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
from gui import hp

def homepage():
    def viewq():
        window1.destroy()
        hp()

    window1 = Tk()
    window1.geometry('1366x769')
    window1.resizable(0,0)
    window1.title("Home Page")
    window1.configure(bg="#D2C1FF")
    bgImage = ImageTk.PhotoImage(file='FinalHomepage.png')
    bgLabel = Label(window1, image=bgImage,borderwidth=0, highlightthickness=0)
    bgLabel.place(x=0, y=0)


    Next_Button = Button(window1, text='Next', font=('Book Antiqua', 22, 'bold'), fg='white', bg='black',
                activeforeground='white', activebackground='#1a2529', cursor='hand2', bd=0, width=10, command=viewq)
    Next_Button.place(x=590, y=500)

    window1.mainloop()
