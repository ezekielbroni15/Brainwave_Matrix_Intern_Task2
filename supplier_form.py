from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkcalendar import DateEntry
import pymysql


def connect_database():
    try:
        connection = pymysql.connect(
            host='localhost',
            user='root',
            passwd='WhiteChakra15$&',
            database='inventory_system'
        )
        cursor = connection.cursor()
        return cursor, connection
    except pymysql.MySQLError as e:
        messagebox.showerror('Error', f'Database connectivity issue: {e}')
        return None, None


def add_supplier(supid, name, email, contact, address, doj, company_name, status, treeview):
    if supid == '' or name == '' or email == '' or contact == '' or address == '' or doj == '' or company_name == '' or status == '':
        messagebox.showerror('Error', 'All fields are required')
    else:
        cursor, connection = connect_database()
        if not cursor or not connection:
            return

        try:
            # Check if the SupID already exists
            cursor.execute('SELECT * FROM supplier_data WHERE supid = %s', (supid,))
            if cursor.fetchone():
                messagebox.showerror('Error', 'Supplier ID already exists.')
                return

            cursor.execute(
                'INSERT INTO supplier_data (supid, name, email, contact, address, doj, company_name, status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)',
                (
                    supid, name, email, contact, address, doj, company_name, status))
            connection.commit()
            messagebox.showinfo('Success', 'Supplier added successfully')
            fetch_data(treeview)  # Refresh the Treeview after adding
        except pymysql.MySQLError as e:
            messagebox.showerror('Database Error', f'Error: {e}')
        finally:
            connection.close()  # Ensure the connection is closed


def delete_supplier(treeview):
    selected_item = treeview.selection()
    if not selected_item:
        messagebox.showwarning('Warning', 'Please select a supplier to delete')
        return

    supid = treeview.item(selected_item)['values'][0]
    result = messagebox.askyesno('Confirm Delete', f'Are you sure you want to delete supplier with ID {supid}?')
    if result:
        cursor, connection = connect_database()
        if not cursor or not connection:
            return

        try:
            cursor.execute('DELETE FROM supplier_data WHERE supid = %s', (supid,))
            connection.commit()
            messagebox.showinfo('Success', 'Supplier deleted successfully')
            fetch_data(treeview)  # Refresh the Treeview after deletion
        except pymysql.MySQLError as e:
            messagebox.showerror('Database Error', f'Error: {e}')
        finally:
            connection.close()  # Ensure the connection is closed


def fetch_data(treeview):
    cursor, connection = connect_database()
    if not cursor or not connection:
        return

    try:
        cursor.execute('SELECT * FROM supplier_data')
        rows = cursor.fetchall()
        for row in treeview.get_children():
            treeview.delete(row)
        for row in rows:
            treeview.insert('', 'end', values=row)
    except pymysql.MySQLError as e:
        messagebox.showerror('Database Error', f'Error: {e}')
    finally:
        connection.close()  # Ensure the connection is closed


def supplier_form(window):
    supplier_frame = Frame(window, width=1070, height=567, bg='white')
    supplier_frame.place(x=200, y=100)
    heading_label = Label(supplier_frame, text='Manage Supplier Details', font=('Times New Roman', 16, 'bold'),
                          bg='#0f4d7d', fg='white')
    heading_label.place(x=0, y=0, relwidth=1)

    back_image = PhotoImage(file='left-arrow.png')
    back_button = Button(supplier_frame, image=back_image, bd=0, cursor='hand2', bg='white',
                         command=lambda: supplier_frame.place_forget())
    back_button.place(x=10, y=0)

    top_frame = Frame(supplier_frame, bg='white')
    top_frame.place(x=0, y=40, relwidth=1, height=235)

    search_frame = Frame(top_frame, bg='white')
    search_frame.pack()
    search_combobox = ttk.Combobox(search_frame, values=('Id', 'Name', 'Email'), font=('Times New Roman', 12),
                                   state='readonly', justify='center')
    search_combobox.set('Search By')
    search_combobox.grid(row=0, column=0, padx=20)
    search_entry = Entry(search_frame, font=('Times New Roman', 12), bg='lightyellow')
    search_entry.grid(row=0, column=1)
    search_button = Button(search_frame, text='Search', font=('Times New Roman', 12), width=10, cursor='hand2',
                           fg='white', bg='#0f4d7d')
    search_button.grid(row=0, column=2, padx=20)
    show_button = Button(search_frame, text='Show All', font=('Times New Roman', 12), width=10, cursor='hand2',
                         fg='white', bg='#0f4d7d', command=lambda: fetch_data(supplier_treeview))
    show_button.grid(row=0, column=3)

    horizontal_scrollbar = Scrollbar(top_frame, orient=HORIZONTAL)
    vertical_scrollbar = Scrollbar(top_frame, orient=VERTICAL)
    supplier_treeview = ttk.Treeview(top_frame, columns=(
        'supid', 'name', 'email', 'contact', 'address', 'doj', 'company_name', 'status'), show='headings',
                                     yscrollcommand=vertical_scrollbar.set, xscrollcommand=horizontal_scrollbar.set)
    horizontal_scrollbar.pack(side=BOTTOM, fill=X)
    vertical_scrollbar.pack(side=RIGHT, fill=Y, pady=(10, 0))
    horizontal_scrollbar.config(command=supplier_treeview.xview)
    vertical_scrollbar.config(command=supplier_treeview.yview)
    supplier_treeview.pack(pady=(10, 0))

    supplier_treeview.heading('supid', text='SupId')
    supplier_treeview.heading('name', text='Name')
    supplier_treeview.heading('email', text='Email')
    supplier_treeview.heading('contact', text='Contact')
    supplier_treeview.heading('address', text='Address')
    supplier_treeview.heading('doj', text='Date of Joining')
    supplier_treeview.heading('company_name', text='Company Name')
    supplier_treeview.heading('status', text='Status')

    supplier_treeview.column('supid', width=60)
    supplier_treeview.column('name', width=140)
    supplier_treeview.column('email', width=180)
    supplier_treeview.column('contact', width=100)
    supplier_treeview.column('address', width=150)
    supplier_treeview.column('doj', width=100)
    supplier_treeview.column('company_name', width=120)
    supplier_treeview.column('status', width=100)

    detail_frame = Frame(supplier_frame, bg='white')
    detail_frame.place(x=20, y=280)

    supid_label = Label(detail_frame, text='SupId', font=('Times New Roman', 12), bg='white')
    supid_label.grid(row=0, column=0, padx=20, pady=10, sticky='w')
    supid_entry = Entry(detail_frame, font=('Times New Roman', 12), bg='lightyellow')
    supid_entry.grid(row=0, column=1, padx=20, pady=10)

    name_label = Label(detail_frame, text='Name', font=('Times New Roman', 12), bg='white')
    name_label.grid(row=0, column=2, padx=20, pady=10, sticky='w')
    name_entry = Entry(detail_frame, font=('Times New Roman', 12), bg='lightyellow')
    name_entry.grid(row=0, column=3, padx=20, pady=10, sticky='w')

    email_label = Label(detail_frame, text='Email', font=('Times New Roman', 12), bg='white')
    email_label.grid(row=0, column=4, padx=20, pady=10, sticky='w')
    email_entry = Entry(detail_frame, font=('Times New Roman', 12), bg='lightyellow')
    email_entry.grid(row=0, column=5, padx=20, pady=10)

    contact_label = Label(detail_frame, text='Contact', font=('Times New Roman', 12), bg='white')
    contact_label.grid(row=1, column=0, padx=20, pady=10, sticky='w')
    contact_entry = Entry(detail_frame, font=('Times New Roman', 12), bg='lightyellow')
    contact_entry.grid(row=1, column=1, padx=20, pady=10)

    address_label = Label(detail_frame, text='Address', font=('Times New Roman', 12), bg='white')
    address_label.grid(row=1, column=2, padx=20, pady=10, sticky='w')
    address_text = Text(detail_frame, width=20, height=3, font=('Times New Roman', 12), bg='lightyellow')
    address_text.grid(row=1, column=3, rowspan=2)

    doj_label = Label(detail_frame, text='Date of Joining', font=('Times New Roman', 12), bg='white')
    doj_label.grid(row=1, column=4, padx=20, pady=10, sticky='w')
    doj_date_entry = DateEntry(detail_frame, width=18, font=('Times New Roman', 12), state='readonly',
                               date_pattern='dd/mm/yyyy')
    doj_date_entry.grid(row=1, column=5)

    company_name_label = Label(detail_frame, text='Company Name', font=('Times New Roman', 12), bg='white')
    company_name_label.grid(row=2, column=0, padx=20, pady=10, sticky='w')
    company_name_entry = Entry(detail_frame, font=('Times New Roman', 12), bg='lightyellow')
    company_name_entry.grid(row=2, column=1, padx=20, pady=10)

    status_label = Label(detail_frame, text='Status', font=('Times New Roman', 12), bg='white')
    status_label.grid(row=2, column=2, padx=20, pady=10, sticky='w')
    status_entry = Entry(detail_frame, font=('Times New Roman', 12), bg='lightyellow')
    status_entry.grid(row=2, column=3, padx=20, pady=10)

    save_button = Button(detail_frame, text='Save', font=('Times New Roman', 12), width=10, cursor='hand2',
                         fg='white', bg='#0f4d7d', command=lambda: add_supplier(
            supid_entry.get(),
            name_entry.get(),
            email_entry.get(),
            contact_entry.get(),
            address_text.get("1.0", 'end-1c'),
            doj_date_entry.get(),
            company_name_entry.get(),
            status_entry.get(),
            supplier_treeview  # Pass the Treeview widget to add_supplier
        ))
    save_button.grid(row=3, column=0, columnspan=6, pady=20)

    delete_button = Button(detail_frame, text='Delete', font=('Times New Roman', 12), width=10, cursor='hand2',
                           fg='white', bg='#f44336', command=lambda: delete_supplier(supplier_treeview))
    delete_button.grid(row=4, column=0, columnspan=6, pady=20)

    fetch_data(supplier_treeview)  # Load data into Treeview initially
