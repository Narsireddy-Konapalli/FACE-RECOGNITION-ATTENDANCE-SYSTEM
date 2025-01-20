import streamlit as st
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

# Function to fetch the number of classes attended
def fetching_no_of_classes(enquire_usn, subject):
    # Read USNs and names from files
    with open('usns.txt', 'r') as file:
        usn_list = [line.strip() for line in file.readlines()]
        usn_lst=usn_list[0].split(',')
        usn_list=usn_lst[:-1]
        
    with open('names.txt', 'r') as file:
        name_list = [line.strip() for line in file.readlines()]
        name_lst=name_list[0].split(',')
        name_list=name_lst[:-1]

    if enquire_usn == '':
        return None, "Please enter USN"
    elif str(enquire_usn) not in usn_list:
        return None, "USN Not Registered"
    else:
        usn_ind = usn_list.index(enquire_usn)
        conn = sqlite3.connect('Attendance.db')
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM present_list WHERE USNS=? AND SUBJECT=?", (enquire_usn, subject))
        count = cursor.fetchone()[0]

        cursor.execute("SELECT NAMES FROM present_list WHERE USNS=?", (enquire_usn,))
        name = cursor.fetchone()

        conn.commit()
        conn.close()

        return name, count

# Set up the page title
st.title("Check Attendance")

# Create a text input for USN
usn = st.text_input("Enter your USN:")

# Dropdown for subjects
subjects = [
    "Select a subject",
    "business intelligence (21CDT71)",
    "Intelligent Database Management System (21CDT72)",
    "computer vision (21CDT734)",
    "Text Analytics & Natural Language Processing (21CDT741)",
    "Open Elective (21CDT75X)",
    "Project Work (21CDP76)"
]
clicked = st.selectbox("Choose a subject", subjects)

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
    if usn=='':
        st.warning("Please Enter USN")
    elif clicked == "Select a subject":
        st.warning("Please select a subject ")
    elif usn not in USNS:
        st.warning(f"USN {usn} Not Registred")
    else:
        name, no_of_classes = fetching_no_of_classes(usn, clicked.split(' (')[1][:-1])  # Get subject code
        
        if name and isinstance(no_of_classes, int):  # Ensure no_of_classes is an integer
            # Display results
            st.success(f"Your USN: **{usn}**")
            st.success(f"Your Name: **{name[0]}**")
            st.success(f"Number of Classes Attended for {clicked} : **{no_of_classes}**")
            
        else:
            st.error(no_of_classes)  # Display error message
