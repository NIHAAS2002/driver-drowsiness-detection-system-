import tkinter as tk
from tkinter import *
from tkinter import ttk 
from PIL import Image, ImageTk
import cv2,mediapipe as mp,tensorflow as tf,numpy as np,psycopg2,shared_data
from ultralytics import YOLO
from pygame import mixer
from datetime import datetime
mixer.init()
face_detection=mp.solutions.face_detection.FaceDetection(0.75)
model_phone =YOLO("yolov8n.pt")
model = tf.keras.models.load_model("../final_model")
class_names=['awake' 'sleep']
user_id=shared_data.user_id
# Initialize video capture
cap = cv2.VideoCapture(0)
# PostgreSQL connection parameters
db_params = {
    "host": "localhost",
    "port": "5432",
    "database": "driver",
    "user": "postgres",
    "password": "qwe"
}
# Establish a connection to PostgreSQL
conn = psycopg2.connect(**db_params)


def start():
    def show_frame():
        success, image = cap.read()
        if success:
            image.flags.writeable = False
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            results = face_detection.process(image)
            resultphn = model_phone(image, classes=67)
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            for r in resultphn:
                if r.boxes:
                    #cv2.putText(image, 'phone', (100, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
                    insert_phndata(user_id)
                    mixer.music.load("phn.mp3")
                    mixer.music.play()
            if results.detections:
                for detection in results.detections:
                    bboxc = detection.location_data.relative_bounding_box
                    ih, iw, ic = image.shape
                    xmin = int(bboxc.xmin * iw)
                    ymin = int(bboxc.ymin * ih)
                    w, h = int(bboxc.width * iw), int(bboxc.height * ih)
                    x1, y1 = xmin, ymin
                    x2, y2 = x1 + w, y1 + h
                    cv2.rectangle(image, (x1, y1), (x2, y2), (250, 0, 250), 3)
                    try:
                        cropped_img = image[y1:y2, x1:x2]
                        resize = tf.image.resize(cropped_img, (224, 224))
                        predictions = model.predict(np.expand_dims(resize / 255, axis=0))
                        predicted_label = predictions[0].argmax()
                        if predicted_label == 1:
                            insert_sleepdata(user_id)
                            cv2.putText(image, 'sleep', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2,cv2.LINE_AA)
                            mixer.music.load("beep.mp3")
                            mixer.music.play()
                        else:
                            image = cv2.putText(image, 'awake', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2,cv2.LINE_AA)
                    except:
                        pass

            # Convert the frame to PIL format
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            image_pil = Image.fromarray(image)

            # Create Tkinter-compatible image
            img_tk = ImageTk.PhotoImage(image=image_pil)

            # Update the label with the new image
            label.config(image=img_tk)
            label.image = img_tk

        # Call this function again after 1ms
        if running:
            label.after(1, show_frame)

    # Set running flag to True
    global running
    running = True
    show_frame()


def stop():
    # Set running flag to False
    global running
    running = False

def dash():
    root.withdraw()
    import dash_board
    dash_board.window.deconify()




def insert_phndata(user_id):
    try:
        # Create a cursor object to execute SQL queries
        cursor = conn.cursor()
        # Get the current timestamp
        detection_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # Insert the user ID, detection time into the PostgreSQL table
        cursor.execute("INSERT INTO phone (user_id, detection_time) VALUES (%s, %s)", (user_id, detection_time))
        # Commit the transaction
        conn.commit()
        # Close the cursor
        cursor.close()
    except (psycopg2.Error) as error:
        print("Error while inserting data into PostgreSQL", error)

def insert_sleepdata(user_id):
    try:
        # Create a cursor object to execute SQL queries
        cursor = conn.cursor()
        # Get the current timestamp
        detection_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # Insert the user ID, detection time into the PostgreSQL table
        cursor.execute("INSERT INTO sleep (user_id, detection_time) VALUES (%s, %s)", (user_id, detection_time))
        # Commit the transaction
        conn.commit()
        # Close the cursor
        cursor.close()
    except (psycopg2.Error) as error:
        print("Error while inserting data into PostgreSQL", error)

# Create the main window

root = Tk()
root.title("Object Detection")
root.geometry("800x600")
root.configure(bg='#2F3136')
style = ttk.Style(root)
style.theme_use('clam')
style.configure('TButton', background='#43B581', foreground='white')
style.configure('TLabel', background='#2F3136', foreground='white')
style.configure('TEntry', fieldbackground='#FFFFFF')
# Create a frame for the video feed
feed_frame = ttk.Frame(root)
feed_frame.pack(side=RIGHT)

# Create a label for the video feed
label = ttk.Label(feed_frame)
label.pack()

# Create a frame for the sidebar
sidebar_frame = ttk.Frame(root)
sidebar_frame.pack(side=LEFT, padx=10, pady=10)

# Create start button
start_button = ttk.Button(sidebar_frame, text="Start", command=start)
start_button.pack(pady=10)

# Create stop button
stop_button = ttk.Button(sidebar_frame, text="Stop", command=stop)
stop_button.pack(pady=10)

dash_board = ttk.Button(sidebar_frame, text="Dash_Board", command=dash)
dash_board.pack(pady=10)
# Start the Tkinter event loop
root.mainloop()