import streamlit as st


st.title("Report Issue:warning:")


title1 = st.text_input("Title", "Type here")
create1 = st.text_input("Created by", "Type here")

description1 = st.text_area("Description","Type here", height=300)