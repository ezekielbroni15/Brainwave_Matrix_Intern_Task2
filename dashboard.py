from tkinter import *
from tkinter import messagebox
import tkinter.font as tkFont

# Import your forms
from employees import employee_form
from supplier_form import supplier_form
from category_form import category_form
from product_form import product_form
from sales_form import sales_form

# Function to authenticate user credentials
def authenticate(username, password):
    correct_username = 'admin'
    correct_password = 'admin123'
    return username == correct_username and password == correct_password

# Function to show the dashboard
def show_dashboard():
    login_window.destroy()  # Close the login window
    create_dashboard()  # Call the dashboard creation function

# Function to handle login
def login():
    username = username_entry.get()
    password = password_entry.get()
    if authenticate(username, password):
        show_dashboard()
    else:
        messagebox.showerror('Error', 'Invalid username or password')

# Function to create and show the login window
def create_login_window():
    global login_window, username_entry, password_entry

    login_window = Tk()
    login_window.title('Login')
    login_window.geometry('400x250')
    login_window.resizable(True, True)
    login_window.config(bg='#f0f0f0')

    title_font = tkFont.Font(family='Times New Roman', size=20, weight='bold')
    entry_font = tkFont.Font(family='Times New Roman', size=14)
    button_font = tkFont.Font(family='Times New Roman', size=12, weight='bold')

    # Title label
    title_label = Label(login_window, text='Login', font=title_font, bg='#f0f0f0')
    title_label.pack(pady=20)

    # Username
    username_label = Label(login_window, text='Username', font=entry_font, bg='#f0f0f0')
    username_label.pack(pady=(10, 0))
    username_entry = Entry(login_window, font=entry_font, width=30)  # Set width here
    username_entry.pack(pady=5, padx=20)

    # Password
    password_label = Label(login_window, text='Password', font=entry_font, bg='#f0f0f0')
    password_label.pack(pady=(10, 0))
    password_entry = Entry(login_window, font=entry_font, show='*', width=30)  # Set width here
    password_entry.pack(pady=5, padx=20)

    # Login Button
    login_button = Button(login_window, text='Login', font=button_font, command=login, bg='#009688', fg='white')
    login_button.pack(pady=20)

    login_window.mainloop()


# Function to create and show the dashboard
def create_dashboard():
    global window

    window = Tk()
    window.title('Dashboard')
    window.geometry('1270x668+0+0')
    window.resizable(True, True)
    window.config(background='white')

    bg_image = PhotoImage(file='inventory.png')
    title_label = Label(window, image=bg_image, compound=LEFT, text='  Inventory Management System (IMS)',
                        font=('Times New Roman', 40, 'bold'), bg='#010c48', fg='white', anchor='w', padx=20)
    title_label.place(x=0, y=0, relwidth=1)

    logoutButton = Button(window, text='Logout', font=('Times New Roman', 20, 'bold'), fg='#010c48')
    logoutButton.place(x=1100, y=10)

    subtitleLabel = Label(window, text='Welcome Admin\t\t Date: 08-07-2024\t\t Time: 12:36:17 pm',
                          font=('Times New Roman', 15), bg='#4d636d', fg='white')
    subtitleLabel.place(x=0, y=70, relwidth=1)

    leftFrame = Frame(window)
    leftFrame.place(x=0, y=102, width=200, height=555)

    logoImage = PhotoImage(file='logo.png')
    imageLabel = Label(leftFrame, image=logoImage)
    imageLabel.pack()

    menuLabel = Label(leftFrame, text='Menu', font=('Times New Roman', 20), bg='#009688')
    menuLabel.pack(fill='x')

    employee_icon = PhotoImage(file='employee.png')
    employee_button = Button(leftFrame, image=employee_icon, compound=LEFT, text=' Employee',
                             font=('Times New Roman', 20, 'bold'), anchor='w', padx=10,
                             command=lambda: employee_form(window))
    employee_button.pack(fill='x')

    supplier_icon = PhotoImage(file='supply.png')
    supplier_button = Button(leftFrame, image=supplier_icon, compound=LEFT, text=' Suppliers',
                             font=('Times New Roman', 20, 'bold'), anchor='w', padx=10,
                             command=lambda: supplier_form(window))
    supplier_button.pack(fill='x')

    category_icon = PhotoImage(file='category.png')
    category_button = Button(leftFrame, image=category_icon, compound=LEFT, text=' Categories',
                             font=('Times New Roman', 20, 'bold'), anchor='w', padx=10,
                             command=lambda: category_form(window))
    category_button.pack(fill='x')

    products_icon = PhotoImage(file='product.png')
    products_button = Button(leftFrame, image=products_icon, compound=LEFT, text=' Products',
                             font=('Times New Roman', 20, 'bold'), anchor='w', padx=10,
                             command=lambda: product_form(window))
    products_button.pack(fill='x')

    sales_icon = PhotoImage(file='sales.png')
    sales_button = Button(leftFrame, image=sales_icon, compound=LEFT, text=' Sales',
                          font=('Times New Roman', 20, 'bold'),
                          anchor='w', padx=10, command=lambda: sales_form(window))
    sales_button.pack(fill='x')

    exit_icon = PhotoImage(file='exit.png')
    exit_button = Button(leftFrame, image=exit_icon, compound=LEFT, text=' Exit', font=('Times New Roman', 20, 'bold'),
                         anchor='w', padx=10)
    exit_button.pack(fill='x')

    emp_frame = Frame(window, bg='#2C3E50', bd=3, relief=RIDGE)
    emp_frame.place(x=400, y=125, height=170, width=280)
    total_emp_icon = PhotoImage(file='total_emp.png')
    total_emp_icon_label = Label(emp_frame, image=total_emp_icon, bg='#2C3E50')
    total_emp_icon_label.pack(pady=10)

    total_emp_label = Label(emp_frame, text='Total Employees', bg='#2C3E50', fg='white',
                            font=('Times New Roman', 15, 'bold'))
    total_emp_label.pack()

    total_emp_count_label = Label(emp_frame, text='0', bg='#2C3E50', fg='white', font=('Times New Roman', 30, 'bold'))
    total_emp_count_label.pack()

    sup_frame = Frame(window, bg='#BE44AD', bd=3, relief=RIDGE)
    sup_frame.place(x=800, y=125, height=170, width=280)
    total_sub_icon = PhotoImage(file='total_supplier.png')
    total_sub_icon_label = Label(sup_frame, image=total_sub_icon, bg='#BE44AD')
    total_sub_icon_label.pack(pady=10)

    total_sub_label = Label(sup_frame, text='Total Supplier', bg='#BE44AD', fg='white',
                            font=('Times New Roman', 15, 'bold'))
    total_sub_label.pack()

    total_sub_count_label = Label(sup_frame, text='0', bg='#BE44AD', fg='white', font=('Times New Roman', 30, 'bold'))
    total_sub_count_label.pack()

    cat_frame = Frame(window, bg='#27AE60', bd=3, relief=RIDGE)
    cat_frame.place(x=400, y=310, height=170, width=280)
    total_cat_icon = PhotoImage(file='total_cate.png')
    total_cat_icon_label = Label(cat_frame, image=total_cat_icon, bg='#27AE60')
    total_cat_icon_label.pack(pady=10)

    total_cat_label = Label(cat_frame, text='Total Categories', bg='#27AE60', fg='white',
                            font=('Times New Roman', 15, 'bold'))
    total_cat_label.pack()

    total_cat_count_label = Label(cat_frame, text='0', bg='#27AE60', fg='white', font=('Times New Roman', 30, 'bold'))
    total_cat_count_label.pack()

    prod_frame = Frame(window, bg='#2C3E50', bd=3, relief=RIDGE)
    prod_frame.place(x=800, y=310, height=170, width=280)
    total_prod_icon = PhotoImage(file='total_products.png')
    total_prod_icon_label = Label(prod_frame, image=total_prod_icon, bg='#2C3E50')
    total_prod_icon_label.pack(pady=10)

    total_prod_label = Label(prod_frame, text='Total Products', bg='#2C3E50', fg='white',
                             font=('Times New Roman', 15, 'bold'))
    total_prod_label.pack()

    total_prod_count_label = Label(prod_frame, text='0', bg='#2C3E50', fg='white', font=('Times New Roman', 30, 'bold'))
    total_prod_count_label.pack()

    sales_frame = Frame(window, bg='#E74C3C', bd=3, relief=RIDGE)
    sales_frame.place(x=600, y=495, height=170, width=280)
    total_sales_icon = PhotoImage(file='total_sales.png')
    total_sales_icon_label = Label(sales_frame, image=total_sales_icon, bg='#E74C3C')
    total_sales_icon_label.pack(pady=10)

    total_sales_label = Label(sales_frame, text='Total Sales', bg='#E74C3C', fg='white',
                              font=('Times New Roman', 15, 'bold'))
    total_sales_label.pack()

    total_sales_count_label = Label(sales_frame, text='0', bg='#E74C3C', fg='white',
                                    font=('Times New Roman', 30, 'bold'))
    total_sales_count_label.pack()

    window.mainloop()

# Run the login window first
create_login_window()
