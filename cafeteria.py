from tkinter import *
import mysql.connector as c
from datetime import datetime
import cv2
from pyzbar.pyzbar import decode
from tkinter import messagebox
from gui import *
import warnings
from PIL import Image, ImageTk


warnings.filterwarnings('ignore')
conn = c.connect(
        host="localhost",
        user="root",
        password="WagonR#4022",
        database="rfs"
    )
cursor = conn.cursor()

def logout():
    exit()

def scan_student_id():
    cap = cv2.VideoCapture(0)
    secure_id = None
    while True:
        ret, frame = cap.read()
        cv2.imshow('Frame', frame)
        decoded_objects = decode(frame)
        for obj in decoded_objects:
            secure_id = obj.data.decode()

            break
        keyboard = cv2.waitKey(1)
        if secure_id or keyboard == 27:
            break

    cap.release()
    cv2.destroyAllWindows()
    return secure_id

def process_transaction(cursor, cart, secure_id,connection):
    cursor.execute("SELECT * FROM student_bonk WHERE secureid = %s", (secure_id,))
    student_data = cursor.fetchone()
    if student_data:
        Label(paypage, text=student_data[1],font=('Times New Roman', 14, 'bold'),bg='#ffde59',width=13,bd=0).place(x=595,y=395)
        new_balance = student_data[2] - tcost
        if new_balance < 0:
            Label(paypage, text='Insufficient Balance')
            return
        cursor.execute("UPDATE student_bonk SET balance = {} WHERE secureid = '{}'".format(new_balance, secure_id))
        connection.commit()
        cursor.execute("Select * from cafe_money")
        rs = cursor.fetchone()
        cafebal = rs[1]
        total = cafebal + tcost
        cursor.execute("Update cafe_money set balance = " + str(total))
        connection.commit()
        Label(paypage, text='Balance: ₹'+str(new_balance),font=('Times New Roman', 14, 'bold'),bg='#ffde59',width=13,bd=0).place(x=595,y=427)
        cursor.execute("SELECT MAX(transid) FROM trans")
        max_transid = cursor.fetchone()[0]
        new_transid = max_transid + 1 if max_transid else 1

        now = datetime.now()
        for item in cart:
            cursor.execute('select cost from menu where item="{}"'.format(item))
            (cost, )=cursor.fetchone()
            cursor.execute("INSERT INTO trans (transid, item, amount, id, timeofpur) VALUES (%s, %s, %s, %s, %s)",(new_transid, item, cost, student_data[0], now))
            connection.commit()
        else:
            messagebox.showinfo("Success", "Payment of Rs. " + str(tcost) + " Completed")
            paypage.destroy()
            cafepage()
            return


    else:
        Label(paypage, text='Invalid ID').pack()

def main():
    try:
        secure_id = scan_student_id()
        process_transaction(cursor, cart, secure_id, conn)
    finally:
        cursor.close()
        conn.close()

def add_to_cart(item, cost):
    cart[item] = cart.get(item, 0) + 1
    update_cart_display()

def update_cart_display():
    global tcost
    cart_text = ""
    total_cost = 0
    for item, quantity in cart.items():
        cart_text += f"{item} x {quantity}\n"
        total_cost += menu[item] * quantity
    cart_label.config(text=cart_text)
    total_label.config(text=f"Total: ₹{total_cost:.2f}")
    tcost=total_cost
    return cart

def proceed_to_payment():
    global paypage
    selpage.destroy()
    paypage = Tk()
    paypage.resizable(0,0)
    paypage.geometry('1366x768')
    bgImage = ImageTk.PhotoImage(file='PaymentPage.png')
    bgLabel = Label(paypage, image=bgImage, borderwidth=0, highlightthickness=0)
    bgLabel.place(x=0, y=0)
    Label(paypage, text=f"Total Cost: ₹{tcost}", font=('Times New Roman', 20, 'bold'),bg='#ffde59',width=13).place(x=575,y=255)
    Button(paypage, text='Pay',font=('Times New Roman', 20, 'bold'),bg='#f4f4f4',width=13, command=main,bd=0).place(x=575, y=537)
    paypage.mainloop()

cursor.execute("SELECT item, cost FROM menu")
rows = cursor.fetchall()

menu = {item: cost for item, cost in rows}

cart = {}

selpage = Tk()
selpage.title("Menu")
selpage.geometry('1366x768')
selpage.title('Menu Page')
selpage.resizable(0,0)
bgImage = ImageTk.PhotoImage(file='MenuPage_Final (1).png')
bgLabel = Label(selpage, image=bgImage, borderwidth=0, highlightthickness=0)
bgLabel.place(x=0,y=0)
#bgLabel.grid(row=0, column=0, columnspan=100, rowspan=400)  # Adjust as needed

bg_image = PhotoImage(file='Button.png')

# Resize the image to the desired dimensions (adjust width and height as needed)
#bg_image = bg_image.subsample(12,12)  # You can adjust the subsample factor

button_width = 200  # Adjust this value based on your design preference
columns = 3  # Adjust the number of columns as needed

# Create a frame to contain the buttons
button_frame = Frame(selpage)
button_frame.pack(side='top', pady=10)

# Function to create buttons and pack them in the frame
def create_button(item, cost):
    button = Button(
        button_frame,
        text=f"{item} - ₹{cost}",
        image=bg_image,
        compound='center',
        command=lambda item=item, cost=cost: add_to_cart(item, cost),
        bd=0,
        highlightthickness=0,
        width=100,
        height=10# Set highlightthickness to 0 for no background
    )
    button.pack(side='left', padx=5, pady=5)

# Create buttons in 4 columns and 3 rows
for item, cost in menu.items():
    create_button(item, cost)

    # Check if the number of buttons in the current row exceeds the specified columns
    if button_frame.grid_size()[0] == columns:
        # Create a new row by inserting an empty label
        Label(button_frame).pack(side='left')

# Other elements
cart_label = Label(selpage, text="Cart:", font=('Times New Roman', 20, 'bold'), bg='#f4f4f4')
cart_label.place(x=1110,y=100)

total_label = Label(selpage, text="Total: ₹0.00", font=('Times New Roman', 20, 'bold'), bg='#f4f4f4')
total_label.place(x=1090,y=600)

payment_button = Button(selpage, text="Proceed to Payment", font=('Times New Roman', 15, 'bold'), width=16, command=proceed_to_payment, bd=0, highlightthickness=0)
payment_button.pack(side='left', padx=5, pady=5)

logout_button = Button(selpage, text='Logout', font=('Times New Roman', 15, 'bold'), width=16, command=logout, bd=0, highlightthickness=0)
logout_button.pack(side='left', padx=5, pady=5)

selpage.mainloop()
