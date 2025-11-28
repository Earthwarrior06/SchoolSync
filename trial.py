import mysql.connector
from pyzbar.pyzbar import decode
import cv2
import datetime
import time
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from PIL import Image, ImageTk


# Connect to the MySQL server
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="WagonR#4022",
    auth_plugin='mysql_native_password',
    database="rfs"

)

def logout():
    exit()

def showtable():
    new_today = 'Date_'
    today = datetime.date.today().isoformat()
    for i in today:
        if i == '-':
            new_today += '_'
        else:
            new_today += i

    t = Tk()
    t.title('Student Details')
    cur = db.cursor()
    cur.execute('select name, class, '+new_today+ ' from attendance where class="12A"')
    rs = cur.fetchall()
    tree = ttk.Treeview(t, columns=("Name", "Class", new_today), show='headings')
    tree.heading('Name', text='Name')
    tree.heading('Class', text='Class')
    tree.heading(new_today, text=new_today)
    for row in rs:
        tree.insert('', END, values=row)
    tree.pack()
    t.mainloop()

def add_current_date_column():
    new_today = 'Date_'
    today = datetime.date.today().isoformat()
    for i in today:
        if i == '-':
            new_today += '_'
        else:
            new_today += i
    today = new_today
    cursor = db.cursor()
    try:
        cursor.execute(f"ALTER TABLE attendance ADD COLUMN `{today}` CHAR(1)")
        db.commit()
    except mysql.connector.Error as err:
        messagebox.showinfo('Opened Today' ,'Attendance Session Started Today!!!')
    finally:
        cursor.close()
        att_button['state'] = 'disabled'
        mark_button.place(x=163,y=217)
        absent_button.place(x=163,y=309)

def mark_attendance(name):
    new_today='Date_'
    today = datetime.date.today().isoformat()
    for i in today:
        if i=='-':
            new_today+='_'
        else:
            new_today+=i
    today=new_today
    cursor = db.cursor()
    try:
        cursor.execute(f"UPDATE attendance SET `{today}` = 'P' WHERE secure_id = %s", (name,))
        db.commit()
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()



# Function to scan QR codes and mark attendance
def scan_qr_code():
    cap = cv2.VideoCapture(0)
    secure_id = None
    while True:
        ret, frame = cap.read()
        cv2.imshow('Frame', frame)
        decoded_objects = decode(frame)
        for obj in decoded_objects:
            secure_id = obj.data.decode()
            mark_attendance(secure_id)
            messagebox.showinfo('Attendance' ,'Scanned Successfully and Marked Present!')
            break
        keyboard = cv2.waitKey(1)
        if secure_id or keyboard == 27:
            break

    cap.release()
    cv2.destroyAllWindows()
    return secure_id

def mark_absent_records():
    new_today = 'Date_'
    today = datetime.date.today().isoformat()
    for i in today:
        if i == '-':
            new_today += '_'
        else:
            new_today += i
    today = new_today
    cursor = db.cursor()
    try:
        cursor.execute(f"UPDATE attendance SET `{today}` = 'A' WHERE `{today}` IS NULL")
        db.commit()
        messagebox.showinfo('Attendance', 'Remaining Records Marked Absent !')
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        showtable()
        cursor.close()


# Run the scheduled jobs
def attendpage():
    global att_button
    global mark_button
    global absent_button
    atp=Tk()
    atp.geometry('500x500')
    atp.title('Attendance')
    atp.resizable(0,0)
    bgImage = ImageTk.PhotoImage(file='AttendancePage_Final.png')
    bgLabel = Label(atp, image=bgImage, borderwidth=0, highlightthickness=0)
    bgLabel.place(x=0, y=0)


    att_button=Button(atp, text='Mark Today\'s Attendance',font=('Times New Roman', 11, 'bold'), bg='#f4f4f4', width=19, bd=0, command=add_current_date_column)
    att_button.place(x=163,y=135)
    mark_button=Button(atp, text='Student QR Scanner',font=('Times New Roman', 11, 'bold'), bg='#f4f4f4', width=19, bd=0, command=scan_qr_code)
    absent_button=Button(atp, text='Close Attendance Session', font=('Times New Roman', 11, 'bold'), bg='#f4f4f4', width=19, bd=0, command=mark_absent_records)
    logout_button=Button(atp, text="Logout",font=('Times New Roman', 11, 'bold'), bg='#fdea89', width=13, bd=0, command=logout)
    logout_button.place(x=190,y=393)
    atp.mainloop()

attendpage()
