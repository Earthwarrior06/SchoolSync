from tkinter import *
import tkinter
import qrcode
import os
import random
from tkinter import messagebox
from tkinter import ttk
from tkinter import Tk, Button, Canvas, PhotoImage,Toplevel, Label,Entry, END
from PIL import Image, ImageTk
import mysql.connector as c
def qrpage():
    try:
        qrpagex = Toplevel()
        qrpagex.geometry('1366x768')
        qrpagex.title("QR Generator Page")
        bgImage = ImageTk.PhotoImage(file='GenerateQR_Final.png')
        bgLabel = Label(qrpagex, image=bgImage, borderwidth=0, highlightthickness=0)
        bgLabel.place(x=0, y=0)

        def createqr(event):
            rfs_id = rfsid_entry.get()
            name = name_entry.get()
            amt = amt_entry.get()
            clas = class_entry.get()
            conn = c.connect(host='localhost', user='root', passwd='WagonR#4022', database='rfs')
            cur = conn.cursor()
            char_seq = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
            k = random.sample(char_seq, len(rfs_id))
            seq = ''
            for i in k:
                seq += i

            def merge(s1, s2):
                result = ""
                i = 0
                while (i < len(s1)) or (i < len(s2)):
                    if i < len(s1):
                        result += s1[i]
                    if i < len(s2):
                        result += s2[i]
                    i += 1
                return result

            def store():
                query = "insert into attendance (secure_id, name, class) values('{}', '{}', '{}')".format(rfs_key, name, clas)
                print(query)
                cur.execute(query)
                conn.commit()

            rfs_key = merge(merge(rfs_id, seq), seq)
            l1re = 'RFS Secure Key: ' + str(rfs_key)
            qr = qrcode.QRCode(version=1, box_size=10, border=4)
            qr.add_data(rfs_key)
            qr.make(fit=True)
            img = qr.make_image(fill_color='black', back_color='white')
            os.chdir(r'C:\Users\Smruti Kulkarni\Downloads\QR_Codes')
            img.save(rfs_id + '.png')
            query = "insert into student_bonk values({}, '{}', {}, '{}', '{}')".format(rfs_id, name, amt, rfs_key, clas)
            cur.execute(query)
            conn.commit()
            messagebox.showinfo('QR Generation Successful',
                                l1re + '\nYou may find QR saved in the QR_Codes folder in Downloads')
            store()


        Label(qrpagex, text='Student ID:', font=('Times New Roman', 20, 'bold'), bg='#f4f4f4', bd=0,width=13).place(x=400, y=200)
        rfsid_entry = Entry(qrpagex,font=('Times New Roman', 20), bg='#f4f4f4', bd=0,width=13)
        rfsid_entry.place(x=650,y=200)

        Label(qrpagex, text='Name:', font=('Times New Roman', 20, 'bold'), bg='#f4f4f4', bd=0,width=13).place(x=400, y=325)
        name_entry = Entry(qrpagex,font=('Times New Roman', 20), bg='#f4f4f4', bd=0,width=13)
        name_entry.place(x=650,y=325)

        #Change to place it in New GUI bg image
        Label(qrpagex, text='Class:',font=('Times New Roman', 20, 'bold'), bg='#f4f4f4', bd=0,width=13).place(x=400,y=447)
        class_entry = Entry(qrpagex,font=('Times New Roman', 20), bg='#f4f4f4', bd=0,width=13)
        class_entry.place(x=650,y=447)

        Label(qrpagex, text='Amount:', font=('Times New Roman', 20, 'bold'), bg='#f4f4f4', bd=0,width=13).place(x=400, y=565)
        amt_entry = Entry(qrpagex,font=('Times New Roman', 20), bg='#f4f4f4', bd=0,width=13)
        amt_entry.place(x=650,y=575)

        b1 = Button(qrpagex, text='Generate', font=('Times New Roman', 20, 'bold'), bg='#f4f4f4', bd=0, width=13)
        b1.bind('<Button-1>', createqr)
        b1.place(x=630,y=660)
        qrpagex.bind('<Return>', createqr)
        qrpagex.mainloop()

    finally:
        qrpagex.destroy()

def update_menu():
    def save_changes():
        try:
            conn = c.connect(host='localhost', user='root', passwd='WagonR#4022', database='rfs')
            cur = conn.cursor()
            for child in tree.get_children():
                serial_no, item, cost = tree.item(child)["values"]
                update_query = "UPDATE menu SET Item = %s, Cost = %s WHERE `sr` = %s"
                cur.execute(update_query, (item, cost, serial_no))
            conn.commit()
            messagebox.showinfo("Success", "Menu updated successfully")
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            if conn.is_connected():
                conn.close()

    def edit_item(event):
        selected = tree.focus()
        temp_values = tree.item(selected, 'values')
        entry_serial_no.delete(0, END)
        entry_item.delete(0, END)
        entry_cost.delete(0, END)
        entry_serial_no.insert(0, temp_values[0])
        entry_item.insert(0, temp_values[1])
        entry_cost.insert(0, temp_values[2])
        save_button["state"] = "disabled"

    def add_to_database():
        try:
            conn = c.connect(host='localhost', user='root', passwd='WagonR#4022', database='rfs')
            cur = conn.cursor()
            new_sr_no = entry_serial_no.get()
            new_item = entry_item.get()
            new_cost = entry_cost.get()
            query = "Insert into menu values(%s, %s, %s)"
            tup = (int(new_sr_no), new_item, int(new_cost))
            cur.execute(query, tup)
            conn.commit()
            entry_serial_no.delete(0, END)
            entry_item.delete(0, END)
            entry_cost.delete(0, END)

            messagebox.showinfo("Success", "New item added successfully")

        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            if conn.is_connected():
                conn.close()
            update_window.destroy()

    def delete_from_database(key):
        try:
            conn = c.connect(host='localhost', user='root', passwd='WagonR#4022', database='rfs')
            cur = conn.cursor()
            delete_query = "DELETE FROM menu WHERE sr = %s"
            cur.execute(delete_query, (key,))
            conn.commit()
            messagebox.showinfo("Success", "Record deleted successfully")
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            if conn.is_connected():
                conn.close()

    def delete_item():
        selected = tree.selection()
        if selected:
            primary_key = tree.item(selected[0], 'values')[0]
            tree.delete(selected[0])
            delete_from_database(primary_key)
        else:
            messagebox.showwarning("Warning", "No item selected for deletion")


    def save_item():
        selected = tree.focus()
        if selected:
            tree.item(selected, values=(tree.item(selected, 'values')[0], entry_item.get(), entry_cost.get()))
            save_button["state"] = "normal"
        else:
            messagebox.showwarning("Warning", "No item selected for editing")

    update_window = Tk()
    update_window.title("Update Menu")

    tree = ttk.Treeview(update_window, columns=("Serial No.", "Item", "Cost"), show='headings')
    tree.heading('Serial No.', text='Serial No.')
    tree.heading('Item', text='Item')
    tree.heading('Cost', text='Cost')
    tree.bind('<Double-1>', edit_item)
    tree.pack()

    conn = c.connect(host='localhost', user='root', passwd='WagonR#4022', database='rfs')
    cur = conn.cursor()
    cur.execute('SELECT * FROM menu')
    for row in cur:
        tree.insert('', END, values=row)
    conn.close()

    Label(update_window, text='Serial No.:').pack()
    entry_serial_no = Entry(update_window)
    entry_serial_no.pack()
    Label(update_window, text='Item:').pack()
    entry_item = Entry(update_window)
    entry_item.pack()
    Label(update_window, text='Cost:').pack()
    entry_cost = Entry(update_window)
    entry_cost.pack()

    add_button = Button(update_window, text="Add New Item", command=add_to_database)
    add_button.pack()

    delete_button = Button(update_window, text="Delete Selected Item", command=delete_item)
    delete_button.pack()

    save_item_button = Button(update_window, text="Save Item", command=save_item)
    save_item_button.pack()

    save_button = Button(update_window, text="Save Changes to Database", command=save_changes)
    save_button.pack()
    save_button["state"] = "disabled"

    update_window.mainloop()

def showtable1():
    t = Toplevel()
    t.title('Login Credentials')
    try:
        conn = c.connect(host='localhost', user='root', passwd='WagonR#4022', database='rfs')
        cur = conn.cursor()
        cur.execute('select * from login_creds')
        rs = cur.fetchall()
        tree = ttk.Treeview(t, columns=("Username", "Password"), show='headings')
        tree.heading('Username', text='Username')
        tree.heading('Password', text='Password')
        for row in rs:
            tree.insert('', END, values=row)
        tree.pack()
        t.mainloop()
    except Exception as e:
        messagebox.showerror("Error", str(e))
    finally:
        if conn.is_connected():
            conn.close()

def showtable2():
    t = Toplevel()
    t.title('Menu')
    try:
        conn = c.connect(host='localhost', user='root', passwd='WagonR#4022', database='rfs')
        cur = conn.cursor()
        cur.execute('select * from menu')
        rs = cur.fetchall()
        tree = ttk.Treeview(t, columns=("Serial No.", "Item", "Cost"), show='headings')
        tree.heading('Serial No.', text='Serial No.')
        tree.heading('Item', text='Item')
        tree.heading('Cost', text='Cost')
        for row in rs:
            tree.insert('', END, values=row)
        tree.pack()
        t.mainloop()
    except Exception as e:
        messagebox.showerror("Error", str(e))
    finally:
        if conn.is_connected():
            conn.close()

def showtable3():
    t = Toplevel()
    t.title('Student Details')
    try:
        conn = c.connect(host='localhost', user='root', passwd='WagonR#4022', database='rfs')
        cur = conn.cursor()
        cur.execute('select * from student_bonk')
        rs = cur.fetchall()
        tree = ttk.Treeview(t, columns=("RFS ID", "Name", "Balance", "Secure RFS Key","Class"), show='headings')
        tree.heading('RFS ID', text='RFS ID')
        tree.heading('Name', text='Name')
        tree.heading('Balance', text='Balance')
        tree.heading('Secure RFS Key', text='Secure RFS Key')
        tree.heading('Class',text='Class')
        for row in rs:
            tree.insert('', END, values=row)
        tree.pack()
        t.mainloop()
    except Exception as e:
        messagebox.showerror("Error", str(e))
    finally:
        if conn.is_connected():
            conn.close()

def showtable4():
    #print("Showing table 4")
    t = Toplevel()
    t.title('Transactions')
    try:
        conn = c.connect(host='localhost', user='root', passwd='WagonR#4022', database='rfs')
        cur = conn.cursor()
        cur.execute('select * from trans')
        rs = cur.fetchall()
        tree = ttk.Treeview(t, columns=("Transaction ID", "Item", "Amount", "RFS ID", "Time of Purchase"), show='headings')
        tree.heading('Transaction ID', text='Transaction ID')
        tree.heading('Item', text='Item')
        tree.heading('Amount', text='Amount')
        tree.heading('RFS ID', text='RFS ID')
        tree.heading('Time of Purchase', text='Time of Purchase')
        for row in rs:
            tree.insert('', END, values=row)
        tree.pack()
        t.mainloop()
    except Exception as e:
        messagebox.showerror("Error", str(e))
    finally:
        if conn.is_connected():
            conn.close()

def accesspage1():
    ap = Toplevel()
    ap.geometry('1366x768')
    ap.resizable(0, 0)
    ap.title("Update Table Page")
    bgImage = ImageTk.PhotoImage(file='Access_Tables_Page (1).png')
    bgLabel = Label(ap, image=bgImage, borderwidth=0, highlightthickness=0)
    bgLabel.place(x=0, y=0)
    Button(ap, text='Login Credentials', font=('Times New Roman', 20, 'bold'), bg='#f4f4f4', bd=0, command=showtable1, width=16).place(x=370, y=390)
    Button(ap, text='Menu', font=('Times New Roman', 20, 'bold'), bg='#f4f4f4', bd=0,
           command=showtable2, width=16).place(x=720, y=390)
    Button(ap, text='Student Details', font=('Times New Roman', 20, 'bold'), bg='#f4f4f4', bd=0,
           command=showtable3, width=16).place(x=370, y=535)
    Button(ap, text='Transaction Details', font=('Times New Roman', 20, 'bold'), bg='#f4f4f4', bd=0,
           command=showtable4, width=16).place(x=720, y=535)
    ap.mainloop()

def dcpage():
    ap = Toplevel()
    ap.geometry('1366x768')
    ap.title("Update Table Page")
    bgImage = ImageTk.PhotoImage(file='UpdateTablePage_Final.png')
    bgLabel = Label(ap, image=bgImage, borderwidth=0, highlightthickness=0)
    bgLabel.place(x=0, y=0)
    Button(ap, text='Login Credentials', font=('Times New Roman', 20, 'bold'), bg='#f4f4f4', bd=0, command=showtable1, width=16).place(x=370, y=390)
    Button(ap, text='Menu', font=('Times New Roman', 20, 'bold'), bg='#f4f4f4', bd=0, command=update_menu, width=16).place(x=720, y=390)
    Button(ap, text='Student Details', font=('Times New Roman', 20, 'bold'), bg='#f4f4f4', bd=0, command=showtable3, width=16).place(x=370, y=535)
    Button(ap, text='Transaction Details', font=('Times New Roman', 20, 'bold'), bg='#f4f4f4', bd=0, command=showtable4, width=16).place(x=720, y=535)
    ap.mainloop()

def adminpage():
    adp = Tk()
    adp.configure(bg='#eee3ee')
    adp.geometry('1366x768')
    adp.title('Admin')
    bgImage = ImageTk.PhotoImage(file='AdminPage.png')
    bgLabel = Label(adp, image=bgImage, borderwidth=0, highlightthickness=0)
    bgLabel.place(x=0, y=0)
    Button(adp, text='Generate QR', font=('Times New Roman', 20, 'bold'), bg='#f4f4f4', bd=0, command=qrpage, width=16).place(x=540, y=250)
    Button(adp, text='Access Tables', font=('Times New Roman', 20, 'bold'), bg='#f4f4f4', bd=0, command=accesspage1, width=16).place(x=540, y=390)
    Button(adp, text='Change Data', font=('Times New Roman', 20, 'bold'), bg='#f4f4f4', bd=0, command=dcpage, width=16).place(x=540, y=530)
    adp.mainloop()

def cafepage():
    import cafeteria

def attendpage():
    pass

def hp():
    def validate_login(event):
        username = username_entry.get()
        password = password_entry.get()

        cur = conn.cursor()
        cur.execute('SELECT * FROM login_creds WHERE username=%s AND pwd=%s', (username, password))
        result = cur.fetchone()

        if result is not None:
            if username == 'admin':
                hp.destroy()
                adminpage()

            elif username == 'cafe':
                hp.destroy()
                cafepage()
            else:
                hp.destroy()
                accesspage1()

        else:
            messagebox.showerror('Error','Invalid username or password!')
            username_entry.delete(0, END)
            password_entry.delete(0, END)

    hp = Tk()
    hp.geometry('1366x768')
    hp.resizable(0, 0)
    hp.title("Login Page")
    hp.configure(bg="#D2C1FF")
    bgImage = ImageTk.PhotoImage(file='UserLoginPage.png')
    bgLabel = Label(hp, image=bgImage, borderwidth=0, highlightthickness=0)
    bgLabel.place(x=0, y=0)
    conn = c.connect(
        host="localhost",
        user="root",
        password="WagonR#4022",
        database="rfs"
    )

    Label(hp, text='Enter Username',font=('Times New Roman', 23, 'bold'), bg='#f4f4f4', bd=0,width=13).place(x=369, y=287)
    username_entry = Entry(hp,font=('Times New Roman', 20), bg='white')
    username_entry.place(x=635,y=285)

    Label(hp, text='Enter Password',font=('Times New Roman', 23, 'bold'), bg='#f4f4f4', bd=0,width=13).place(x=369, y=433)
    password_entry = Entry(hp, show='*',font=('Times New Roman', 20), bg='white')
    password_entry.place(x=635,y=430)

    b1 = Button(hp, text='Login',font=('Times New Roman', 20, 'bold'), bg='#f4f4f4', bd=0,width=13)
    b1.bind('<Button-1>', validate_login)
    b1.place(x=570,y=587)
    hp.bind('<Return>', validate_login)
    hp.mainloop()
    conn.close()
