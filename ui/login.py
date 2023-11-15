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

# Function to handle login
def login():
    user_id = entry_user_id.get()
    password = entry_password.get()
    # Check if the user ID and password match a record in the database
    try:
        cursor.execute("SELECT * FROM user_details WHERE user_id = %s AND passsword = %s", (user_id, password))
        if cursor.fetchone() is not None:
            label_result.config(text="Login successful!")
            import shared_data
            shared_data.user_id=user_id
            window.destroy()
            import main_window
            main_window.window.deiconify()
    except:
        messagebox.showinfo("Error" , "Invalid user ID or password!")

# Function to switch to the registration page
def go_to_register():
    window.withdraw()
    import register
    register.window.deiconify()

    # Create and position the widgets for registration
    # ...


# Create the main window
window = tk.Tk()
window.title("Login")
window.geometry("800x600")
window.configure(bg='#2F3136')

# Set the style for ttk widgets
style = ttk.Style(window)
style.theme_use('clam')
style.configure('TButton', background='#43B581', foreground='white')
style.configure('TLabel', background='#2F3136', foreground='white')
style.configure('TEntry', fieldbackground='#FFFFFF')

# Create and position the widgets for login
login_label = ttk.Label(window, text="Login", font=("Arial", 30))
login_label.place(relx=0.5, rely=0.1, anchor='center')

label_user_id = ttk.Label(window, text="User ID:", font=("Arial", 16))
label_user_id.place(relx=0.3, rely=0.3, anchor='e')
entry_user_id = ttk.Entry(window, font=("Arial", 16))
entry_user_id.place(relx=0.5, rely=0.3, anchor='w')

label_password = ttk.Label(window,  text="Password", font=("Arial", 16))
label_password.place(relx=0.3, rely=0.4, anchor='e')
entry_password = ttk.Entry(window, show="*", font=("Arial", 16))
entry_password.place(relx=0.5, rely=0.4, anchor='w')

button_login = ttk.Button(window, text="Login", command=login)
button_login.place(relx=0.7, rely=0.5, anchor='center')

label_result = ttk.Label(window, text="")
label_result.place(relx=0.5, rely=0.6, anchor='center')

button_register = ttk.Button(window, text="Register", command=go_to_register)
button_register.place(relx=0.6, rely=0.5, anchor='center')

window.mainloop()

# Close the database connection
cursor.close()
conn.close()