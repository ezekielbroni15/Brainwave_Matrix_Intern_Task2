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


def add_product(prodid, product_name, category_name, price, stock_quantity, treeview):
    if prodid == '' or product_name == '' or category_name == '' or price == '' or stock_quantity == '':
        messagebox.showerror('Error', 'All fields are required')
    else:
        cursor, connection = connect_database()
        if not cursor or not connection:
            return
        try:
            cursor.execute('INSERT INTO product_data VALUES (%s, %s, %s, %s, %s)', (prodid, product_name, category_name, price, stock_quantity))
            connection.commit()
            messagebox.showinfo('Success', 'Product added successfully')
            fetch_data(treeview)  # Refresh the Treeview after adding
        except pymysql.MySQLError as e:
            messagebox.showerror('Database Error', f'Error: {e}')
        finally:
            connection.close()


def update_product(prodid, product_name, category_name, price, stock_quantity, treeview):
    if prodid == '' or product_name == '' or category_name == '' or price == '' or stock_quantity == '':
        messagebox.showerror('Error', 'All fields are required')
    else:
        cursor, connection = connect_database()
        if not cursor or not connection:
            return
        try:
            cursor.execute('UPDATE product_data SET product_name = %s, category_name = %s, price = %s, stock_quantity = %s WHERE prodid = %s',
                           (product_name, category_name, price, stock_quantity, prodid))
            connection.commit()
            if cursor.rowcount == 0:
                messagebox.showwarning('Warning', 'Product ID not found')
            else:
                messagebox.showinfo('Success', 'Product updated successfully')
                fetch_data(treeview)  # Refresh the Treeview after updating
        except pymysql.MySQLError as e:
            messagebox.showerror('Database Error', f'Error: {e}')
        finally:
            connection.close()


def delete_product(treeview):
    selected_item = treeview.selection()
    if not selected_item:
        messagebox.showwarning('Warning', 'Please select a product to delete')
        return

    prodid = treeview.item(selected_item)['values'][0]
    result = messagebox.askyesno('Confirm Delete', f'Are you sure you want to delete product with ID {prodid}?')
    if result:
        cursor, connection = connect_database()
        if not cursor or not connection:
            return
        try:
            cursor.execute('DELETE FROM product_data WHERE prodid = %s', (prodid,))
            connection.commit()
            if cursor.rowcount == 0:
                messagebox.showwarning('Warning', 'Product ID not found')
            else:
                messagebox.showinfo('Success', 'Product deleted successfully')
                fetch_data(treeview)  # Refresh the Treeview after deletion
        except pymysql.MySQLError as e:
            messagebox.showerror('Database Error', f'Error: {e}')
        finally:
            connection.close()


def fetch_data(treeview):
    cursor, connection = connect_database()
    if not cursor or not connection:
        return

    try:
        cursor.execute('SELECT * FROM product_data')
        rows = cursor.fetchall()
        for row in treeview.get_children():
            treeview.delete(row)
        for row in rows:
            treeview.insert('', 'end', values=row)
    except pymysql.MySQLError as e:
        messagebox.showerror('Database Error', f'Error: {e}')
    finally:
        connection.close()


def product_form(window):
    global back_image
    product_frame = Frame(window, width=1070, height=567, bg='white')
    product_frame.place(x=200, y=100)
    heading_label = Label(product_frame, text='Manage Product Details', font=('Times New Roman', 16, 'bold'),
                          bg='#0f4d7d', fg='white')
    heading_label.place(x=0, y=0, relwidth=1)
    back_image = PhotoImage(file='left-arrow.png')

    top_frame = Frame(product_frame, bg='white')
    top_frame.place(x=0, y=40, relwidth=1, height=235)

    back_button = Button(top_frame, image=back_image, bd=0, cursor='hand2', bg='white',
                         command=lambda: product_frame.place_forget())
    back_button.place(x=10, y=0)

    search_frame = Frame(top_frame, bg='white')
    search_frame.pack()
    search_combobox = ttk.Combobox(search_frame, values=('Id', 'Product Name', 'Category'), font=('Times New Roman', 12),
                                   state='readonly', justify='center')
    search_combobox.set('Search By')
    search_combobox.grid(row=0, column=0, padx=20)
    search_entry = Entry(search_frame, font=('Times New Roman', 12), bg='lightyellow')
    search_entry.grid(row=0, column=1)
    search_button = Button(search_frame, text='Search', font=('Times New Roman', 12), width=10, cursor='hand2',
                           fg='white', bg='#0f4d7d')
    search_button.grid(row=0, column=2, padx=20)
    show_button = Button(search_frame, text='Show All', font=('Times New Roman', 12), width=10, cursor='hand2',
                         fg='white', bg='#0f4d7d', command=lambda: fetch_data(product_treeview))
    show_button.grid(row=0, column=3)

    horizontal_scrollbar = Scrollbar(top_frame, orient=HORIZONTAL)
    vertical_scrollbar = Scrollbar(top_frame, orient=VERTICAL)
    product_treeview = ttk.Treeview(top_frame, columns=('prodid', 'product_name', 'category_name', 'price', 'stock_quantity'), show='headings',
                                    yscrollcommand=vertical_scrollbar.set, xscrollcommand=horizontal_scrollbar.set)
    horizontal_scrollbar.pack(side=BOTTOM, fill=X)
    vertical_scrollbar.pack(side=RIGHT, fill=Y, pady=(10, 0))
    horizontal_scrollbar.config(command=product_treeview.xview)
    vertical_scrollbar.config(command=product_treeview.yview)
    product_treeview.pack(pady=(10, 0))

    product_treeview.heading('prodid', text='Product ID')
    product_treeview.heading('product_name', text='Product Name')
    product_treeview.heading('category_name', text='Category')
    product_treeview.heading('price', text='Price')
    product_treeview.heading('stock_quantity', text='Stock Quantity')

    product_treeview.column('prodid', width=100)
    product_treeview.column('product_name', width=200)
    product_treeview.column('category_name', width=150)
    product_treeview.column('price', width=100)
    product_treeview.column('stock_quantity', width=150)

    detail_frame = Frame(product_frame, bg='white')
    detail_frame.place(x=20, y=280)

    prodid_label = Label(detail_frame, text='Product ID', font=('Times New Roman', 12), bg='white')
    prodid_label.grid(row=0, column=0, padx=20, pady=10, sticky='w')
    prodid_entry = Entry(detail_frame, font=('Times New Roman', 12), bg='lightyellow')
    prodid_entry.grid(row=0, column=1, padx=20, pady=10)

    product_name_label = Label(detail_frame, text='Product Name', font=('Times New Roman', 12), bg='white')
    product_name_label.grid(row=0, column=2, padx=20, pady=10, sticky='w')
    product_name_entry = Entry(detail_frame, font=('Times New Roman', 12), bg='lightyellow')
    product_name_entry.grid(row=0, column=3, padx=20, pady=10)

    category_label = Label(detail_frame, text='Category', font=('Times New Roman', 12), bg='white')
    category_label.grid(row=1, column=0, padx=20, pady=10, sticky='w')
    category_combobox = ttk.Combobox(detail_frame, values=('Select Category'), font=('Times New Roman', 12), width=18,
                                    state='readonly')
    category_combobox.set('Select Category')
    category_combobox.grid(row=1, column=1)

    price_label = Label(detail_frame, text='Price', font=('Times New Roman', 12), bg='white')
    price_label.grid(row=1, column=2, padx=20, pady=10, sticky='w')
    price_entry = Entry(detail_frame, font=('Times New Roman', 12), bg='lightyellow')
    price_entry.grid(row=1, column=3, padx=20, pady=10)

    stock_quantity_label = Label(detail_frame, text='Stock Quantity', font=('Times New Roman', 12), bg='white')
    stock_quantity_label.grid(row=2, column=0, padx=20, pady=10, sticky='w')
    stock_quantity_entry = Entry(detail_frame, font=('Times New Roman', 12), bg='lightyellow')
    stock_quantity_entry.grid(row=2, column=1, padx=20, pady=10)

    button_frame = Frame(product_frame, bg='white')
    button_frame.place(x=200, y=520)

    add_button = Button(button_frame, text='Add', font=('Times New Roman', 12), width=10, cursor='hand2',
                        fg='white', bg='#0f4d7d',
                        command=lambda: add_product(prodid_entry.get(), product_name_entry.get(), category_combobox.get(),
                                                     price_entry.get(), stock_quantity_entry.get(), product_treeview))
    add_button.grid(row=0, column=0, padx=20)

    update_button = Button(button_frame, text='Update', font=('Times New Roman', 12), width=10, cursor='hand2',
                           fg='white', bg='#0f4d7d',
                           command=lambda: update_product(prodid_entry.get(), product_name_entry.get(), category_combobox.get(),
                                                           price_entry.get(), stock_quantity_entry.get(), product_treeview))
    update_button.grid(row=0, column=1, padx=20)

    delete_button = Button(button_frame, text='Delete', font=('Times New Roman', 12), width=10, cursor='hand2',
                           fg='white', bg='#0f4d7d', command=lambda: delete_product(product_treeview))
    delete_button.grid(row=0, column=2, padx=20)

    clear_button = Button(button_frame, text='Clear', font=('Times New Roman', 12), width=10, cursor='hand2',
                          fg='white', bg='#0f4d7d',
                          command=lambda: (prodid_entry.delete(0, END), product_name_entry.delete(0, END),
                                           category_combobox.set('Select Category'), price_entry.delete(0, END),
                                           stock_quantity_entry.delete(0, END)))
    clear_button.grid(row=0, column=3, padx=20)

    fetch_data(product_treeview)  # Load data into Treeview initially
