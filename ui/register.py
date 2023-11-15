import tkinter as tk
from tkinter import ttk
import psycopg2
from tkinter import messagebox
# Connect to the PostgreSQL database
db_params = {
    "host": "localhost",
    "port": "5432",
    "database": "driver",
    "user": "postgres",
    "password": "qwe"
}
# Establish a connection to PostgreSQL
conn = psycopg2.connect(**db_params)
cursor = conn.cursor()

# Function to handle registration
def register():
    user_id = entry_user_id_reg.get()
    password = entry_password_reg.get()
    first_name = entry_first_name_reg.get()
    message = ""
    try:
        user_id = int(user_id)
        password = int(password)
    except:
        message = "user_id or password should be an integer"
    
    if len(str(password)) < 4 :
        message = "Password should be atleast 5 characters"
    if(first_name == "" or password == "" or user_id==""):
        message = "Enter all details"
    if(message != ""):
        messagebox.showinfo("Error" , message)
    # Check if user_id already exists in the database
    cursor.execute("SELECT user_id FROM user_details WHERE user_id = %s", (user_id, ))
    if cursor.fetchone() is not None:
        label_result_reg.config(text="User ID already exists!")
    else:
        # Insert the new user details into the database
        cursor.execute("INSERT INTO user_details (user_id, passsword, firstName) VALUES (%s, %s, %s)",
                       (str(user_id), str(password), first_name))
        conn.commit()
        label_result_reg.config(text="Registration successful!")

# Function to switch to the login page
def go_to_login():
    register_window.destroy()
    import login
    login.window.deiconify()

register_window = tk.Tk()
register_window.title("Register")
register_window.geometry("800x600")
register_window.configure(bg='#2F3136')

# Create and position the widgets for registration
style = ttk.Style(register_window)
style.theme_use('clam')
style.configure('TButton', background='#43B581', foreground='white')
style.configure('TLabel', background='#2F3136', foreground='white')
style.configure('TEntry', fieldbackground='#FFFFFF')
label_user_id_reg = tk.Label(register_window, text="User ID:", bg='#2F3136', fg='white', font=("Helvetica", 14))
label_user_id_reg.pack(pady=5)
entry_user_id_reg = tk.Entry(register_window, font=("Helvetica", 14))
entry_user_id_reg.pack(pady=5)

label_password_reg = tk.Label(register_window, text="Password:", bg='#2F3136', fg='white', font=("Helvetica", 14))
label_password_reg.pack(pady=5)
entry_password_reg = tk.Entry(register_window, show="*", font=("Helvetica", 14))
entry_password_reg.pack(pady=5)

label_first_name_reg = tk.Label(register_window, text="First Name:", bg='#2F3136', fg='white', font=("Helvetica", 14))
label_first_name_reg.pack(pady=5)
entry_first_name_reg = tk.Entry(register_window, font=("Helvetica", 14))
entry_first_name_reg.pack(pady=5)

button_register_reg = ttk.Button(register_window, text="Register", command=register)
button_register_reg.place(relx=0.4 , rely=0.4)

label_result_reg = tk.Label(register_window, text="", bg='#2F3136', fg='#50C878', font=("Helvetica", 14))


button_login_reg = ttk.Button(register_window, text="Login", command=go_to_login)

button_login_reg.place(relx=0.5 , rely=0.4)

register_window.mainloop()

# Close the database
