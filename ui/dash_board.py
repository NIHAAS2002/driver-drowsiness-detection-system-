import tkinter as tk
from tkinter import Canvas, ttk

import matplotlib.pyplot as plt
import psycopg2
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import shared_data
# Import user_id from shared_data.py
user_id=shared_data.user_id
def retrieve_data():
    try:
        # Create a connection to the PostgreSQL database
        db_params = {
            "host": "localhost",
            "port": "5432",
            "database": "driver",
            "user": "postgres",
            "password": "qwe"
        }
        # Establish a connection to PostgreSQL
        conn = psycopg2.connect(**db_params)

        # Create a cursor object to execute SQL queries
        cursor = conn.cursor()

        # Retrieve data from PostgreSQL
        cursor.execute("SELECT detection_time FROM sleep WHERE user_id = %s", (user_id,))
        data = cursor.fetchall()
        cursor.execute("SELECT firstname from user_details where user_id = %s", (user_id ,))
        global  first_name
        first_name = cursor.fetchall()[0][0]
        print(first_name)
        # Close the cursor and connection
        cursor.close()
        conn.close()

        return data , first_name
    except (psycopg2.Error) as error:
        print("Error while retrieving data from PostgreSQL", error)

def plot_graph():
    # Retrieve data from PostgreSQL
    data , _ = retrieve_data()
    date = []
    sleeptime = []
    count = 0
    for dt in data:
        for ele in dt:
            dateval = str(ele).split(" ")[0]
            if dateval not in date:
                date.append(dateval)
                sleeptime.append(count)
            count += 1
    sleeptime.append(count)
    sleeptime = sleeptime[1:]
    fig ,(ax1 , ax2) = plt.subplots(1,2)
    # sizes = len(sleeptime)
    plt.title("drowsiness alterted")
    ax1.pie(sleeptime, labels=date)
    sleeptime_min = [time//6 for time in sleeptime]
    ax2.scatter(sleeptime_min , date)
    # ax2.xlabel("sleeptime (min)")
    # ax2.ylabel("date")
    ax1.axis('equal')
    # Create a FigureCanvasTkAgg instance and display it in the Tkinter window
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    canvas.get_tk_widget().pack()

# Create the main Tkinter window


root = tk.Tk()
root.title("Dashboard")
root.geometry("800x600")
root.configure(bg='#2F3136')
style = ttk.Style(root)
style.theme_use('clam')
style.configure('TButton', background='#43B581', foreground='white')
style.configure('TLabel', background='#2F3136', foreground='white')
style.configure('TEntry', fieldbackground='#FFFFFF')
# Create a button to plot the graph
_ , first_name = retrieve_data()
user_id_display = ttk.Label(root, text="User : " + str(first_name))
user_id_display.place(relx=0.1, rely=0.01, anchor='center')
button = ttk.Button(root, text="Plot Graph", command=plot_graph)
button.pack(pady=10)

# Start the Tkinter event loop
root.mainloop()
