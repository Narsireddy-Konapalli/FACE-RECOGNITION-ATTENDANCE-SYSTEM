import streamlit as st
import numpy as np
import cv2
import sqlite3
from datetime import datetime
import pytz
import pandas as pd
import os
import face_recognition

# Function to mark attendance
def mark_attendance(subject):
    # Getting all USNS
    try:
        with open('usns.txt', 'r') as file:
            usn_list = file.readlines()
            if len(usn_list) > 0:
                xx = usn_list[0]
                str_list = str(xx)
                split_list = str_list.split(',')
                USNS = split_list[:-1]
            else:
                USNS = []
    except Exception as e:
        print('Error in marking attendance -->', e)

    # Getting all NAMES
    try:
        with open('NAMES.txt', 'r') as file:
            name_list = file.readlines()
            if len(name_list) > 0:
                xx = name_list[0]
                str_list = str(xx)
                split_list = str_list.split(',')
                NAMES = split_list[:-1]
            else:
                NAMES = []
    except Exception as e:
        print('Error in marking attendance -->', e)

    # Getting all face ENCODINGS
    try:
        path = 'face_encodings.npy'
        if os.path.getsize(path) > 0:
            ENCODINGS = np.load(path)
            try:
                len(ENCODINGS[0])
            except Exception as e:
                print(e)
                ENCODINGS = [np.load(path)]
        else:
            ENCODINGS = []
    except Exception as e:
        print('Error in marking attendance -->', e)

    face_classifier = cv2.CascadeClassifier('haarcascade_frontalface_default (1).xml')
    video_capture = cv2.VideoCapture(0)
    n = 1
    present = []
    attend_list = []

    while True:
        xx = 0
        _, frame = video_capture.read()
        face = face_classifier.detectMultiScale(frame, 1.3, 5)
        if len(face) == 0:
            cv2.putText(frame, 'Face Not Found', (10, 30), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 2)
        else:
            if len(USNS) == 0:
                cv2.putText(frame, 'Not Registered', (10, 30), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 2)
                for (x, y, w, h) in face:
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            else:
                for (x, y, w, h) in face:
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    if n % 15 == 0:
                        xx = 1
                        try:
                            img_enc = face_recognition.face_encodings(frame)[0]
                            try:
                                results = face_recognition.compare_faces(ENCODINGS, img_enc)
                            except Exception as e:
                                print("error in sub of encodings:",e)
                            distance = face_recognition.face_distance(ENCODINGS, img_enc)
                            mi = min(distance)
                            ind = list(distance).index(mi)
                            usn = USNS[ind]
                            if mi > 0.55:
                                cv2.putText(frame, 'Face Not Matched', (10, 30), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 2)
                            else:
                                if usn in present:
                                    cv2.putText(frame, NAMES[ind] + ' Marked', (10, 30), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 102, 255), 2)
                                else:
                                    cv2.putText(frame, NAMES[ind], (10, 30), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 2)
                                    present.append(usn)

                                    current_time = datetime.now()

                                    # Extract the date and time separately
                                    date = current_time.date()
                                    time = current_time.strftime("%H:%M:%S") 

                                    attend_list.append((USNS[ind], NAMES[ind], subject, date, time))
                                    try:
                                        conn = sqlite3.connect('Attendance.db')
                                        cursor = conn.cursor()
                                        cursor.execute("INSERT INTO present_list VALUES(:USNS, :NAMES, :SUBJECT, :DATE, :TIME)",
                                                           {
                                                               'USNS': USNS[ind],
                                                               'NAMES': NAMES[ind],
                                                               'SUBJECT': subject,
                                                               'DATE': date,
                                                               'TIME': time
                                                           })
                                        conn.commit()
                                        conn.close()
                                    except Exception as e:
                                        print("Error in connecting to database",e)
                                    
                        except Exception as e:
                            print("Error in face encodings main",e)
                n += 1
        cv2.putText(frame, 'q-->Exit', (450, 30), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 2)        
        cv2.imshow('video', frame)
        if xx == 1:
            cv2.waitKey(500)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    video_capture.release()
    cv2.destroyAllWindows()


# Streamlit UI
st.title("Mark Attendance")

# Create a list of subjects and their corresponding values
subjects = [
    ("Business Intelligence", "21CDT71"),
    ("Intelligent Database Management System", "21CDT72"),
    ("Computer Vision", "21CDT734"),
    ("Text Analytics & Natural Language Processing", "21CDT741"),
    ("Open Elective", "21CDT75X"),
    ("Project Work", "21CDP76"),
]

# Create a dropdown menu for subject selection with a placeholder
subject_names = ["Select a subject"] + [subject[0] for subject in subjects]  # Add placeholder
selected_subject = st.selectbox("Choose a subject:", subject_names)

# Input text for USN
usn = st.text_input("Enter your USN:")

# Button to submit the USN and subject
if st.button("Submit"):
    with open('usns.txt', 'r') as file:
        usn_list = file.readlines()
        if len(usn_list) > 0:
            xx = usn_list[0]
            str_list = str(xx)
            split_list = str_list.split(',')
            USNS = split_list[:-1]
        else:
            USNS = []
    if selected_subject == "Select a subject":
        st.warning("Please select a subject ")

    elif usn == "":
        st.warning("Please Enter Your  USN")

    elif usn not in USNS:
        st.warning(f"USN {usn} Not Registred")
    else:
        # Get the corresponding value based on the selected subject
        selected_value = next((value for name, value in subjects if name == selected_subject), None)
        
        # Call the function to mark attendance
        mark_attendance(selected_value)
    