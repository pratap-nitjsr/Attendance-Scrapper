import numpy as np
import pandas as pd
import streamlit as st
from StudentPortal import StudentPortal

portal = StudentPortal()

st.title('Check Attendance')

username = st.text_input('Enter your username')

if st.button('Get Results'):
    with st.spinner('Fetching attendance...'):
        attendance = portal.get_attendance(username.upper())
        if attendance:
            df = pd.DataFrame(attendance[1:])
            df.columns = attendance[0]
            st.write(df.to_html(index=None), unsafe_allow_html=True)
        else:
            st.error('Failed')
