# Face Recognition Attendance System

This project is a **Face Recognition Attendance System** built with Python. It uses Streamlit for a user-friendly web interface, captures images from a camera, registers faces, and maintains attendance records in a database. The system allows users to check attendance and is designed for easy deployment and use.

## Features

- **Face Registration**: Capture and register user faces using a camera.
- **Face Recognition**: Recognize and authenticate registered faces.
- **Attendance Tracking**: Record attendance of recognized users and store data in a database.
- **Attendance Check**: Users can view their attendance records.
- **Streamlit Interface**: Provides an interactive web interface for users.

## Technologies Used

- **Python**: Core programming language used.
- **OpenCV**: For capturing and processing images.
- **Face Recognition Library**: Used for detecting and recognizing faces.
- **Streamlit**: For building a web-based user interface.
- **SQLite**: For storing attendance records.

## Setup Instructions

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/Narsireddy-Konapalli/Face-Recognition-Attendance-System.git
   cd face-recognition-attendance-system
2. **Install Dependencies**: Ensure you have Python installed, then install the required libraries:

   ```bash
   pip install opencv-python face-recognition streamlit
   
3. **Run the Application:**

   After cloning the repository and installing all the necessary libraries, run the following command to start the Streamlit app:
   ``` bash
   streamlit run main.py
   
**Home Page**: Below is a screenshot of the Streamlit app homepage showcasing the face registration, mark attendance and check attendance features.
   ![Home](https://github.com/user-attachments/assets/da751a0c-22cd-4d24-9518-e7a4d37213f7)

### Registration Using Camera

After entering your name and USN, the camera will open and monitor your face for 60 frames. Once your face is detected continuously for 59 frames, the application will capture the image and display a confirmation message indicating successful registration.
> **Screenshot Example**: Below is a screenshot of the registration process showing the camera capturing the face.
> ![Registration](https://github.com/user-attachments/assets/2dce9359-3960-4099-91f7-9695814da461)

### Marking Attendance

To mark attendance, select the subject from the dropdown menu. Once the subject is selected, enter your USN in the provided field. After entering the information, click the "submit" button. The application will use your registered face to verify your identity and log your attendance accordingly.

 **Screenshot Example**: Below is a screenshot of the attendance marking page, showing the dropdown menu for subject selection and the USN entry field.
> ![Marking Attendance](https://github.com/user-attachments/assets/fb2aef99-3533-4613-aae7-d7d1e87b9662)

**Screenshot Example**: Below is a screenshot demonstrating the attendance marking process, where your name is displayed at the top after recognizing your face.
>![Marked Attendance](https://github.com/user-attachments/assets/18fd1105-6d86-4b69-bc5e-b44278dc2fc1)


### Checking Attendance

To check your attendance, enter your USN in the designated field and select the subject from the dropdown menu. After entering the information, click the "submit" button. The application will retrieve your attendance records for the selected subject and display the results accordingly.<br>

> **Screenshot Example**: Below is a screenshot showing the attendance checking process, displaying the results for the selected subject after entering the USN.<br>
> ![Attendance checked](https://github.com/user-attachments/assets/1364ef10-9afa-407e-b452-7c35f608ddbc)

## Conclusion

The Face Recognition Attendance System provides a modern and efficient way to manage attendance using advanced face recognition technology. This system streamlines the attendance process, making it easier for both students and educators to track attendance accurately and conveniently.



