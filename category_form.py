from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import pymysql


def connect_database():
    try:
        connection = pymysql.connect(host='localhost', user='root', passwd='WhiteChakra15$&',
                                     database='inventory_system')
        cursor = connection.cursor()
        return cursor, connection
    except pymysql.MySQLError as e:
        messagebox.showerror('Error', f'Database connectivity issue: {e}')
        return None, None


def add_category(catid, category_name, treeview):
    if catid == '' or category_name == '':
        messagebox.showerror('Error', 'All fields are required')
    else:
        cursor, connection = connect_database()
        if not cursor or not connection:
            return

        try:
            cursor.execute('INSERT INTO category_data (catid, category_name) VALUES (%s, %s)', (catid, category_name))
            connection.commit()
            messagebox.showinfo('Success', 'Category added successfully')
            fetch_data(treeview)  # Refresh the Treeview after adding
        except pymysql.MySQLError as e:
            messagebox.showerror('Database Error', f'Error: {e}')
        finally:
            connection.close()  # Ensure the connection is closed


def update_category(catid, category_name, treeview):
    if catid == '' or category_name == '':
        messagebox.showerror('Error', 'All fields are required')
    else:
        cursor, connection = connect_database()
        if not cursor or not connection:
            return

        try:
            cursor.execute('UPDATE category_data SET category_name = %s WHERE catid = %s', (category_name, catid))
            connection.commit()
            if cursor.rowcount == 0:
                messagebox.showwarning('Warning', 'Category ID not found')
            else:
                messagebox.showinfo('Success', 'Category updated successfully')
                fetch_data(treeview)  # Refresh the Treeview after updating
        except pymysql.MySQLError as e:
            messagebox.showerror('Database Error', f'Error: {e}')
        finally:
            connection.close()  # Ensure the connection is closed


def delete_category(treeview):
    selected_item = treeview.selection()
    if not selected_item:
        messagebox.showwarning('Warning', 'Please select a category to delete')
        return

    catid = treeview.item(selected_item)['values'][0]
    result = messagebox.askyesno('Confirm Delete', f'Are you sure you want to delete category with ID {catid}?')
    if result:
        cursor, connection = connect_database()
        if not cursor or not connection:
            return

        try:
            cursor.execute('DELETE FROM category_data WHERE catid = %s', (catid,))
            connection.commit()
            if cursor.rowcount == 0:
                messagebox.showwarning('Warning', 'Category ID not found')
            else:
                messagebox.showinfo('Success', 'Category deleted successfully')
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
        cursor.execute('SELECT * FROM category_data')
        rows = cursor.fetchall()
        for row in treeview.get_children():
            treeview.delete(row)
        for row in rows:
            treeview.insert('', 'end', values=row)
    except pymysql.MySQLError as e:
        messagebox.showerror('Database Error', f'Error: {e}')
    finally:
        connection.close()  # Ensure the connection is closed


def category_form(window):
    global back_image
    category_frame = Frame(window, width=1070, height=567, bg='white')
    category_frame.place(x=200, y=100)
    heading_label = Label(category_frame, text='Manage Category Details', font=('Times New Roman', 16, 'bold'),
                          bg='#0f4d7d', fg='white')
    heading_label.place(x=0, y=0, relwidth=1)
    back_image = PhotoImage(file='left-arrow.png')

    top_frame = Frame(category_frame, bg='white')
    top_frame.place(x=0, y=40, relwidth=1, height=235)

    back_button = Button(top_frame, image=back_image, bd=0, cursor='hand2', bg='white',
                         command=lambda: category_frame.place_forget())
    back_button.place(x=10, y=0)

    search_frame = Frame(top_frame, bg='white')
    search_frame.pack()
    search_combobox = ttk.Combobox(search_frame, values=('Id', 'Category Name'), font=('Times New Roman', 12),
                                   state='readonly', justify='center')
    search_combobox.set('Search By')
    search_combobox.grid(row=0, column=0, padx=20)
    search_entry = Entry(search_frame, font=('Times New Roman', 12), bg='lightyellow')
    search_entry.grid(row=0, column=1)
    search_button = Button(search_frame, text='Search', font=('Times New Roman', 12), width=10, cursor='hand2',
                           fg='white', bg='#0f4d7d')
    search_button.grid(row=0, column=2, padx=20)
    show_button = Button(search_frame, text='Show All', font=('Times New Roman', 12), width=10, cursor='hand2',
                         fg='white', bg='#0f4d7d', command=lambda: fetch_data(category_treeview))
    show_button.grid(row=0, column=3)

    horizontal_scrollbar = Scrollbar(top_frame, orient=HORIZONTAL)
    vertical_scrollbar = Scrollbar(top_frame, orient=VERTICAL)
    category_treeview = ttk.Treeview(top_frame, columns=('catid', 'category_name'), show='headings',
                                     yscrollcommand=vertical_scrollbar.set, xscrollcommand=horizontal_scrollbar.set)
    horizontal_scrollbar.pack(side=BOTTOM, fill=X)
    vertical_scrollbar.pack(side=RIGHT, fill=Y, pady=(10, 0))
    horizontal_scrollbar.config(command=category_treeview.xview)
    vertical_scrollbar.config(command=category_treeview.yview)
    category_treeview.pack(pady=(10, 0))

    category_treeview.heading('catid', text='Category ID')
    category_treeview.heading('category_name', text='Category Name')

    category_treeview.column('catid', width=100)
    category_treeview.column('category_name', width=300)

    detail_frame = Frame(category_frame, bg='white')
    detail_frame.place(x=20, y=280)

    catid_label = Label(detail_frame, text='Category ID', font=('Times New Roman', 12), bg='white')
    catid_label.grid(row=0, column=0, padx=20, pady=10, sticky='w')
    catid_entry = Entry(detail_frame, font=('Times New Roman', 12), bg='lightyellow')
    catid_entry.grid(row=0, column=1, padx=20, pady=10)

    category_name_label = Label(detail_frame, text='Category Name', font=('Times New Roman', 12), bg='white')
    category_name_label.grid(row=0, column=2, padx=20, pady=10, sticky='w')
    category_name_entry = Entry(detail_frame, font=('Times New Roman', 12), bg='lightyellow')
    category_name_entry.grid(row=0, column=3, padx=20, pady=10)

    button_frame = Frame(category_frame, bg='white')
    button_frame.place(x=200, y=520)

    add_button = Button(button_frame, text='Add', font=('Times New Roman', 12), width=10, cursor='hand2',
                        fg='white', bg='#0f4d7d',
                        command=lambda: add_category(catid_entry.get(), category_name_entry.get(), category_treeview))
    add_button.grid(row=0, column=0, padx=20)

    update_button = Button(button_frame, text='Update', font=('Times New Roman', 12), width=10, cursor='hand2',
                           fg='white', bg='#0f4d7d',
                           command=lambda: update_category(catid_entry.get(), category_name_entry.get(),
                                                           category_treeview))
    update_button.grid(row=0, column=1, padx=20)

    delete_button = Button(button_frame, text='Delete', font=('Times New Roman', 12), width=10, cursor='hand2',
                           fg='white', bg='#f44336', command=lambda: delete_category(category_treeview))
    delete_button.grid(row=0, column=2, padx=20)

    clear_button = Button(button_frame, text='Clear', font=('Times New Roman', 12), width=10, cursor='hand2',
                          fg='white', bg='#0f4d7d',
                          command=lambda: (catid_entry.delete(0, END), category_name_entry.delete(0, END)))
    clear_button.grid(row=0, column=3, padx=20)

    fetch_data(category_treeview)  # Load data into Treeview initially
