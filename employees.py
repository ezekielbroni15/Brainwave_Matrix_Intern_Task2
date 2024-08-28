from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkcalendar import DateEntry
import pymysql


def connect_database():
    try:
        connection = pymysql.connect(host='localhost', user='root', password='WhiteChakra15$&')
        cursor = connection.cursor()
    except:
        messagebox.showerror('Error', 'Database connectivity issue try again, please open mysql command line client')
        return None, None
    cursor.execute('CREATE DATABASE IF NOT EXISTS inventory_system')
    cursor.execute('USE inventory_system')
    cursor.execute('CREATE TABLE IF NOT EXISTS employee_data (empid INT PRIMARY KEY, name VARCHAR(100), '
                   'email VARCHAR(50), gender VARCHAR(50), dob VARCHAR(30), contact VARCHAR(30), employment_type VARCHAR(50), education VARCHAR(50), '
                   'work_shift VARCHAR(50), address VARCHAR(100), doj VARCHAR(30), salary VARCHAR(50), usertype VARCHAR(50), '
                   'password VARCHAR(50))')
    return cursor, connection


connect_database()


def add_employee(empid, name, email, gender, dob, contact, employment_type, education, work_shift, address, doj, salary,
                 usertype, password):
    if (
            empid == '' or name == '' or email == '' or gender == 'Select Gender' or contact == '' or employment_type == 'Select type' or
            education == 'Select Education' or work_shift == 'Select Shift' or address == '\n' or salary == '' or
            usertype == 'Select User Type' or password == ''):
        messagebox.showerror('Error', 'All field are required')
    else:
        cursor, connection = connect_database()
        if not cursor or not connection:
            return
        cursor.execute('INSERT INTO employee_data VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', (
        empid, name, email, gender, dob, contact, employment_type, education, work_shift, address, doj, salary,
        usertype, password))
        connection.commit()
        messagebox.showinfo('Success', 'Data is inserted successfully')


def employee_form(window):
    global back_image
    employee_frame = Frame(window, width=1070, height=567, bg='white')
    employee_frame.place(x=200, y=100)
    heading_label = Label(employee_frame, text='Manage Employee Details', font=('Times New Roman', 16, 'bold'),
                          bg='#0f4d7d', fg='white')
    heading_label.place(x=0, y=0, relwidth=1)
    back_image = PhotoImage(file='left-arrow.png')

    top_frame = Frame(employee_frame, bg='white')
    top_frame.place(x=0, y=40, relwidth=1, height=235)

    back_button = Button(top_frame, image=back_image, bd=0, cursor='hand2', bg='white',
                         command=lambda: employee_frame.place_forget())
    back_button.place(x=10, y=0)

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
                         fg='white', bg='#0f4d7d')
    show_button.grid(row=0, column=3)

    horizontal_scrollbar = Scrollbar(top_frame, orient=HORIZONTAL)
    vertical_scrollbar = Scrollbar(top_frame, orient=VERTICAL)
    employee_treeview = ttk.Treeview(top_frame, columns=(
        'empid', 'name', 'email', 'gender', 'dob', 'contact', 'employment_type', 'education', 'work_shift', 'address',
        'doj',
        'salary',
        'usertype'), show='headings', yscrollcommand=vertical_scrollbar.set, xscrollcommand=horizontal_scrollbar.set)
    horizontal_scrollbar.pack(side=BOTTOM, fill=X)
    vertical_scrollbar.pack(side=RIGHT, fill=Y, pady=(10, 0))
    horizontal_scrollbar.config(command=employee_treeview.xview)
    vertical_scrollbar.config(command=employee_treeview.yview)
    employee_treeview.pack(pady=(10, 0))

    employee_treeview.heading('empid', text='EmpId')
    employee_treeview.heading('name', text='Name')
    employee_treeview.heading('email', text='Email')
    employee_treeview.heading('gender', text='Gender')
    employee_treeview.heading('dob', text='Date of Birth')
    employee_treeview.heading('contact', text='Contact')
    employee_treeview.heading('employment_type', text='Employment Type')
    employee_treeview.heading('education', text='Education')
    employee_treeview.heading('work_shift', text='Work Shift')
    employee_treeview.heading('address', text='Address')
    employee_treeview.heading('doj', text='Date of Joining')
    employee_treeview.heading('salary', text='Salary')
    employee_treeview.heading('usertype', text='User Type')

    employee_treeview.column('empid', width=60)
    employee_treeview.column('name', width=140)
    employee_treeview.column('email', width=180)
    employee_treeview.column('gender', width=80)
    employee_treeview.column('contact', width=100)
    employee_treeview.column('dob', width=140)
    employee_treeview.column('employment_type', width=120)
    employee_treeview.column('education', width=120)
    employee_treeview.column('work_shift', width=100)
    employee_treeview.column('address', width=100)
    employee_treeview.column('doj', width=100)
    employee_treeview.column('salary', width=100)
    employee_treeview.column('usertype', width=120)

    detail_frame = Frame(employee_frame, bg='white')
    detail_frame.place(x=20, y=280)

    empid_label = Label(detail_frame, text='EmpId', font=('Times New Roman', 12), bg='white')
    empid_label.grid(row=0, column=0, padx=20, pady=10, sticky='w')
    empid_entry = Entry(detail_frame, font=('Times New Roman', 12), bg='lightyellow')
    empid_entry.grid(row=0, column=1, padx=20, pady=10)

    name_label = Label(detail_frame, text='Name', font=('Times New Roman', 12), bg='white')
    name_label.grid(row=0, column=2, padx=20, pady=10, sticky='w')
    name_entry = Entry(detail_frame, font=('Times New Roman', 12), bg='lightyellow')
    name_entry.grid(row=0, column=3, padx=20, pady=10, sticky='w')

    email_label = Label(detail_frame, text='Email', font=('Times New Roman', 12), bg='white')
    email_label.grid(row=0, column=4, padx=20, pady=10, sticky='w')
    email_entry = Entry(detail_frame, font=('Times New Roman', 12), bg='lightyellow')
    email_entry.grid(row=0, column=5, padx=20, pady=10)

    gender_label = Label(detail_frame, text='Gender', font=('Times New Roman', 12), bg='white')
    gender_label.grid(row=1, column=0, padx=20, pady=10, sticky='w')

    gender_combobox = ttk.Combobox(detail_frame, values=('Male', 'Female'), font=('Times New Roman', 12), width=18,
                                   state='readonly')
    gender_combobox.set('Select Gender')
    gender_combobox.grid(row=1, column=1)

    dob_label = Label(detail_frame, text='Date of Birth', font=('Times New Roman', 12), bg='white')
    dob_label.grid(row=1, column=2, padx=20, pady=10, sticky='w')

    dob_date_entry = DateEntry(detail_frame, width=18, font=('Times New Roman', 12), state='readonly',
                               date_pattern='dd/mm/yyyy')
    dob_date_entry.grid(row=1, column=3)

    contact_label = Label(detail_frame, text='Contact', font=('Times New Roman', 12), bg='white')
    contact_label.grid(row=1, column=4, padx=20, pady=10, sticky='w')
    contact_entry = Entry(detail_frame, font=('Times New Roman', 12), bg='lightyellow')
    contact_entry.grid(row=1, column=5, padx=20, pady=10)

    employment_type_label = Label(detail_frame, text='Employment Type', font=('Times New Roman', 12), bg='white')
    employment_type_label.grid(row=2, column=0, padx=20, pady=10, sticky='w')

    employment_type_combobox = ttk.Combobox(detail_frame,
                                            values=('Full Time', 'Part Time', 'Casual', 'Contract', 'Intern'),
                                            font=('Times New Roman', 12), width=18,
                                            state='readonly')
    employment_type_combobox.set('Select Type')
    employment_type_combobox.grid(row=2, column=1)

    education_label = Label(detail_frame, text='Education', font=('Times New Roman', 12), bg='white')
    education_label.grid(row=2, column=2, padx=20, pady=10, sticky='w')

    education_options = ["B.Tech", "B.con", "M.Tech", "M.con", "B.Bsc", "M.Sc", "BBA", "MBA", "LLB", "LLM", "B.Arch",
                         "M.Arch"]

    education_combobox = ttk.Combobox(detail_frame, values=education_options, font=('Times New Roman', 12), width=18,
                                      state='readonly')
    education_combobox.set('Select Education')
    education_combobox.grid(row=2, column=3)

    work_shift_label = Label(detail_frame, text='Work Shift', font=('Times New Roman', 12), bg='white')
    work_shift_label.grid(row=2, column=4, padx=20, pady=10, sticky='w')

    work_shift_combobox = ttk.Combobox(detail_frame, values=('Morning', 'Evening', 'Night'),
                                       font=('Times New Roman', 12), width=18,
                                       state='readonly')
    work_shift_combobox.set('Select Work Shift')
    work_shift_combobox.grid(row=2, column=5)

    address_label = Label(detail_frame, text='Address', font=('Times New Roman', 12), bg='white')
    address_label.grid(row=3, column=0, padx=20, pady=10, sticky='w')
    address_text = Text(detail_frame, width=20, height=3, font=('Times New Roman', 12), bg='lightyellow')
    address_text.grid(row=3, column=1, rowspan=2)

    doj_label = Label(detail_frame, text='Date of Joining', font=('Times New Roman', 12), bg='white')
    doj_label.grid(row=3, column=2, padx=20, pady=10, sticky='w')
    doj_date_entry = DateEntry(detail_frame, width=18, font=('Times New Roman', 12), state='readonly',
                               date_pattern='dd/mm/yyyy')
    doj_date_entry.grid(row=3, column=3)

    usertype_label = Label(detail_frame, text='User Type', font=('Times New Roman', 12), bg='white')
    usertype_label.grid(row=4, column=2, padx=20, pady=10, sticky='w')
    usertype_combobox = ttk.Combobox(detail_frame, values=('Admin', 'Employee'), font=('Times New Roman', 12), width=18,
                                     state='readonly')
    usertype_combobox.set('Select User Type')
    usertype_combobox.grid(row=4, column=3)

    salary_label = Label(detail_frame, text='Salary', font=('Times New Roman', 12), bg='white')
    salary_label.grid(row=3, column=4, padx=20, pady=10, sticky='w')
    salary_entry = Entry(detail_frame, font=('Times New Roman', 12), bg='lightyellow')
    salary_entry.grid(row=3, column=5, padx=20, pady=10)

    password_label = Label(detail_frame, text='Password', font=('Times New Roman', 12), bg='white')
    password_label.grid(row=4, column=4, padx=20, pady=10, sticky='w')
    password_entry = Entry(detail_frame, font=('Times New Roman', 12), bg='lightyellow')
    password_entry.grid(row=4, column=5, padx=20, pady=10)

    button_frame = Frame(employee_frame, bg='white')
    button_frame.place(x=200, y=520)

    add_button = Button(button_frame, text='Add', font=('Times New Roman', 12), width=10, cursor='hand2',
                        fg='white', bg='#0f4d7d',
                        command=lambda: add_employee(empid_entry.get(), name_entry.get(), email_entry.get(),
                                                     gender_combobox.get(),
                                                     dob_date_entry.get(), contact_entry.get(),
                                                     employment_type_combobox.get(),
                                                     education_combobox.get(), work_shift_combobox.get(),
                                                     address_text.get(1.0, END),
                                                     doj_date_entry.get(), salary_entry.get(), usertype_combobox.get(),
                                                     password_entry.get()))
    add_button.grid(row=0, column=0, padx=20)

    update_button = Button(button_frame, text='Update', font=('Times New Roman', 12), width=10, cursor='hand2',
                           fg='white', bg='#0f4d7d')
    update_button.grid(row=0, column=1, padx=20)

    delete_button = Button(button_frame, text='Delete', font=('Times New Roman', 12), width=10, cursor='hand2',
                           fg='white', bg='#0f4d7d')
    delete_button.grid(row=0, column=2, padx=20)

    clear_button = Button(button_frame, text='Clear', font=('Times New Roman', 12), width=10, cursor='hand2',
                          fg='white', bg='#0f4d7d')
    clear_button.grid(row=0, column=3, padx=20)
