import streamlit as st
from annotated_text import annotated_text

st.title('History:date:')


tab1, tab2 = st.tabs(["Create", "List"])

with tab1:
    st.subheader("Title")
  

with tab2:
    st.header("List of Issues")
  