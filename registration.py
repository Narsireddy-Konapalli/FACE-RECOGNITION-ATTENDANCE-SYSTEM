import streamlit as st
import cv2
import os
import face_recognition
import numpy as np

# Set up page title
st.title("Face Registration")

# Function to handle face registration and image capturing
def registration_image_capturing(reg_name, reg_usn):
    try:
        # Check if the USN is already registered
        USNS = []
        with open('usns.txt', 'r') as file:
            usn_list = file.readlines()
            if len(usn_list) > 0:
                split_list = str(usn_list[0]).split(',')
                USNS = split_list[:-1]
    except Exception as e:
        st.warning(f'Error reading usns.txt: {e}')
        USNS = []

    if reg_name == '' or reg_usn == '':
        st.warning("Name and USN must be entered")
        return
    elif reg_usn in USNS:
        st.warning(f'USN: {reg_usn} is already registered')
        return

    # Load face classifier
    face_classifier = cv2.CascadeClassifier('haarcascade_frontalface_default (1).xml')
    video_capture = cv2.VideoCapture(0)

    face_detected = False
    face_detected_frames = 0
    required_frames = 20  # Approximately 2 seconds of face detection

    while True:
        ret, frame = video_capture.read()
        faces = face_classifier.detectMultiScale(frame, 1.3, 5)

        if len(faces) == 0:
            face_detected = False
            face_detected_frames = 0
            cv2.putText(frame, 'Face Not Found', (10, 30), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 2)
        else:
            face_detected = True
            face_detected_frames += 1
            cv2.putText(frame, f'Hold Still...{face_detected_frames}/{required_frames}', (10, 30),
                        cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 2)

            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

            if face_detected_frames >= required_frames:
                video_capture.release()
                cv2.destroyAllWindows()

                img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                nimg = cv2.resize(img, (500, 500))

                try:
                    enc_img = face_recognition.face_encodings(nimg)[0]
                    path = 'face_encodings.npy'

                    if os.path.exists(path) and os.path.getsize(path) > 0:
                        existing_encodings = np.load(path)
                        np.save(path, np.vstack([existing_encodings, enc_img]))
                    else:
                        np.save(path, enc_img)

                    # Update USN and Name
                    with open('usns.txt', 'a') as file:
                        file.write(reg_usn + ',')
                    with open('names.txt', 'a') as file:
                        file.write(reg_name + ',')

                    st.success(f"Registration successful for {reg_name} (USN: {reg_usn})")
                except Exception as e:
                    st.error(f"Failed to capture or save face: {e}")
                break

        cv2.putText(frame, 'Press q to Exit', (450, 30), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 2)

        cv2.imshow('video', frame)

        # Exit on 'q' key press
        if cv2.waitKey(1) & 0xFF == ord('q'):
            video_capture.release()
            cv2.destroyAllWindows()
            st.warning("Registration Stopped")
            break

    # Cleanup
    video_capture.release()
    cv2.destroyAllWindows()

# Streamlit input form
name = st.text_input("Enter your name:")
usn = st.text_input("Enter your USN:")

# Submit button logic
if st.button("Submit"):
    if name=='':
        st.warning("Please enter your name")
    elif usn=='':
        st.warning("Please enter your USN")
    #if name and usn:
    else:
        # Capture the face if inputs are valid
        registration_image_capturing(name, usn)
    