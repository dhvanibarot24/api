import requests
import streamlit as st

st.title("Teacher Dashboard")

teacher_id = st.number_input("Enter Teacher ID", min_value=1, step=1)
if st.button("View Schedule"):
  response = requests.get(f"http://127.0.0.1:8000/teacher/{teacher_id}")    
st.write(response.json())
