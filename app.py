import streamlit as st

# Sidebar title
st.sidebar.title("Attendance Management System")
# Create the navigation pages
registration = st.Page(
    page="registration.py",
    title="Registration",
    default=True,
)
attendance = st.Page(
    page="attendance.py",
    title="Mark Attendance",
)
check = st.Page(
    page="check.py",
    title="Check Attendance",
)
st.logo("menu.png")
# Create the navigation in the sidebar
pg = st.navigation(pages=[registration, attendance, check])
pg.run()
