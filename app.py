import streamlit as st
import sqlite3

# ---------- Database Setup ----------
conn = sqlite3.connect('students.db')
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        roll TEXT NOT NULL,
        dept TEXT NOT NULL,
        year TEXT NOT NULL
    )
''')
conn.commit()

# ---------- Streamlit UI ----------
st.title("🎓 Student Registration System")

menu = ["Register", "View Students"]
choice = st.sidebar.selectbox("Menu", menu)

if choice == "Register":
    st.subheader("Register New Student")
    name = st.text_input("Name")
    roll = st.text_input("Roll Number")
    dept = st.text_input("Department")
    year = st.text_input("Year")
    if st.button("Register"):
        if name and roll and dept and year:
            cursor.execute("INSERT INTO students (name, roll, dept, year) VALUES (?, ?, ?, ?)",
                           (name, roll, dept, year))
            conn.commit()
            st.success(f"✅ {name} registered successfully!")
        else:
            st.warning("Please fill all fields.")

elif choice == "View Students":
    st.subheader("📋 Registered Students")
    cursor.execute("SELECT * FROM students")
    data = cursor.fetchall()
    if data:
        st.table(data)
    else:
        st.info("No students registered yet.")

conn.close()
