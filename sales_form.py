from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import pymysql


def connect_database():
    try:
        connection = pymysql.connect(host='localhost', user='root', passwd='WhiteChakra15$&', database='inventory_system')
        cursor = connection.cursor()
        return cursor, connection
    except pymysql.MySQLError as e:
        messagebox.showerror('Error', f'Database connectivity issue: {e}')
        return None, None


def add_sale(salesid, prodid, quantity, total_amount):
    if salesid == '' or prodid == '' or quantity == '' or total_amount == '':
        messagebox.showerror('Error', 'All fields are required')
    else:
        cursor, connection = connect_database()
        if not cursor or not connection:
            return
        try:
            cursor.execute('INSERT INTO sales_data VALUES (%s, %s, %s, %s)', (salesid, prodid, quantity, total_amount))
            connection.commit()
            messagebox.showinfo('Success', 'Sale added successfully')
            fetch_data()  # Refresh the Treeview after adding
        except pymysql.MySQLError as e:
            messagebox.showerror('Database Error', f'Error: {e}')
        finally:
            connection.close()


def update_sale(salesid, prodid, quantity, total_amount):
    if salesid == '' or prodid == '' or quantity == '' or total_amount == '':
        messagebox.showerror('Error', 'All fields are required')
    else:
        cursor, connection = connect_database()
        if not cursor or not connection:
            return
        try:
            cursor.execute('UPDATE sales_data SET prodid = %s, quantity = %s, total_amount = %s WHERE salesid = %s',
                           (prodid, quantity, total_amount, salesid))
            connection.commit()
            if cursor.rowcount == 0:
                messagebox.showwarning('Warning', 'Sales ID not found')
            else:
                messagebox.showinfo('Success', 'Sale updated successfully')
                fetch_data()  # Refresh the Treeview after updating
        except pymysql.MySQLError as e:
            messagebox.showerror('Database Error', f'Error: {e}')
        finally:
            connection.close()


def delete_sale():
    selected_item = sales_treeview.selection()
    if not selected_item:
        messagebox.showwarning('Warning', 'Please select a sale to delete')
        return

    salesid = sales_treeview.item(selected_item)['values'][0]
    result = messagebox.askyesno('Confirm Delete', f'Are you sure you want to delete sale with ID {salesid}?')
    if result:
        cursor, connection = connect_database()
        if not cursor or not connection:
            return
        try:
            cursor.execute('DELETE FROM sales_data WHERE salesid = %s', (salesid,))
            connection.commit()
            if cursor.rowcount == 0:
                messagebox.showwarning('Warning', 'Sales ID not found')
            else:
                messagebox.showinfo('Success', 'Sale deleted successfully')
                fetch_data()  # Refresh the Treeview after deletion
        except pymysql.MySQLError as e:
            messagebox.showerror('Database Error', f'Error: {e}')
        finally:
            connection.close()


def fetch_data():
    cursor, connection = connect_database()
    if not cursor or not connection:
        return

    try:
        cursor.execute('SELECT * FROM sales_data')
        rows = cursor.fetchall()
        for row in sales_treeview.get_children():
            sales_treeview.delete(row)
        for row in rows:
            sales_treeview.insert('', 'end', values=row)
    except pymysql.MySQLError as e:
        messagebox.showerror('Database Error', f'Error: {e}')
    finally:
        connection.close()


def sales_form(window):
    global sales_treeview, back_image
    sales_frame = Frame(window, width=1070, height=567, bg='white')
    sales_frame.place(x=200, y=100)
    heading_label = Label(sales_frame, text='Manage Sales Details', font=('Times New Roman', 16, 'bold'),
                          bg='#0f4d7d', fg='white')
    heading_label.place(x=0, y=0, relwidth=1)
    back_image = PhotoImage(file='left-arrow.png')

    top_frame = Frame(sales_frame, bg='white')
    top_frame.place(x=0, y=40, relwidth=1, height=235)

    back_button = Button(top_frame, image=back_image, bd=0, cursor='hand2', bg='white',
                         command=lambda: sales_frame.place_forget())
    back_button.place(x=10, y=0)

    search_frame = Frame(top_frame, bg='white')
    search_frame.pack()
    search_combobox = ttk.Combobox(search_frame, values=('Id', 'Product ID'), font=('Times New Roman', 12),
                                   state='readonly', justify='center')
    search_combobox.set('Search By')
    search_combobox.grid(row=0, column=0, padx=20)
    search_entry = Entry(search_frame, font=('Times New Roman', 12), bg='lightyellow')
    search_entry.grid(row=0, column=1)
    search_button = Button(search_frame, text='Search', font=('Times New Roman', 12), width=10, cursor='hand2',
                           fg='white', bg='#0f4d7d')
    search_button.grid(row=0, column=2, padx=20)
    show_button = Button(search_frame, text='Show All', font=('Times New Roman', 12), width=10, cursor='hand2',
                         fg='white', bg='#0f4d7d', command=fetch_data)
    show_button.grid(row=0, column=3)

    horizontal_scrollbar = Scrollbar(top_frame, orient=HORIZONTAL)
    vertical_scrollbar = Scrollbar(top_frame, orient=VERTICAL)
    sales_treeview = ttk.Treeview(top_frame, columns=('salesid', 'prodid', 'quantity', 'total_amount'), show='headings',
                                  yscrollcommand=vertical_scrollbar.set, xscrollcommand=horizontal_scrollbar.set)
    horizontal_scrollbar.pack(side=BOTTOM, fill=X)
    vertical_scrollbar.pack(side=RIGHT, fill=Y, pady=(10, 0))
    horizontal_scrollbar.config(command=sales_treeview.xview)
    vertical_scrollbar.config(command=sales_treeview.yview)
    sales_treeview.pack(pady=(10, 0))

    sales_treeview.heading('salesid', text='Sales ID')
    sales_treeview.heading('prodid', text='Product ID')
    sales_treeview.heading('quantity', text='Quantity')
    sales_treeview.heading('total_amount', text='Total Amount')

    sales_treeview.column('salesid', width=100)
    sales_treeview.column('prodid', width=100)
    sales_treeview.column('quantity', width=100)
    sales_treeview.column('total_amount', width=150)

    detail_frame = Frame(sales_frame, bg='white')
    detail_frame.place(x=20, y=280)

    salesid_label = Label(detail_frame, text='Sales ID', font=('Times New Roman', 12), bg='white')
    salesid_label.grid(row=0, column=0, padx=20, pady=10, sticky='w')
    salesid_entry = Entry(detail_frame, font=('Times New Roman', 12), bg='lightyellow')
    salesid_entry.grid(row=0, column=1, padx=20, pady=10)

    prodid_label = Label(detail_frame, text='Product ID', font=('Times New Roman', 12), bg='white')
    prodid_label.grid(row=0, column=2, padx=20, pady=10, sticky='w')
    prodid_entry = Entry(detail_frame, font=('Times New Roman', 12), bg='lightyellow')
    prodid_entry.grid(row=0, column=3, padx=20, pady=10)

    quantity_label = Label(detail_frame, text='Quantity', font=('Times New Roman', 12), bg='white')
    quantity_label.grid(row=1, column=0, padx=20, pady=10, sticky='w')
    quantity_entry = Entry(detail_frame, font=('Times New Roman', 12), bg='lightyellow')
    quantity_entry.grid(row=1, column=1, padx=20, pady=10)

    total_amount_label = Label(detail_frame, text='Total Amount', font=('Times New Roman', 12), bg='white')
    total_amount_label.grid(row=1, column=2, padx=20, pady=10, sticky='w')
    total_amount_entry = Entry(detail_frame, font=('Times New Roman', 12), bg='lightyellow')
    total_amount_entry.grid(row=1, column=3, padx=20, pady=10)

    button_frame = Frame(sales_frame, bg='white')
    button_frame.place(x=200, y=520)

    add_button = Button(button_frame, text='Add', font=('Times New Roman', 12), width=10, cursor='hand2',
                        fg='white', bg='#0f4d7d',
                        command=lambda: add_sale(salesid_entry.get(), prodid_entry.get(), quantity_entry.get(),
                                                 total_amount_entry.get()))
    add_button.grid(row=0, column=0, padx=20)

    update_button = Button(button_frame, text='Update', font=('Times New Roman', 12), width=10, cursor='hand2',
                           fg='white', bg='#0f4d7d',
                           command=lambda: update_sale(salesid_entry.get(), prodid_entry.get(), quantity_entry.get(),
                                                       total_amount_entry.get()))
    update_button.grid(row=0, column=1, padx=20)

    delete_button = Button(button_frame, text='Delete', font=('Times New Roman', 12), width=10, cursor='hand2',
                           fg='white', bg='#0f4d7d', command=delete_sale)
    delete_button.grid(row=0, column=2, padx=20)

    clear_button = Button(button_frame, text='Clear', font=('Times New Roman', 12), width=10, cursor='hand2',
                          fg='white', bg='#0f4d7d',
                          command=lambda: (salesid_entry.delete(0, END), prodid_entry.delete(0, END),
                                           quantity_entry.delete(0, END), total_amount_entry.delete(0, END)))
    clear_button.grid(row=0, column=3, padx=20)

    fetch_data()  # Load data into Treeview initially
