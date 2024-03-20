import streamlit as st
from st_pages import Page, show_pages, add_page_title
show_pages(
    [
        Page("Home.py", "Home", "🏠"),
        Page("pages/1_History.py", "History", "📆"),
        Page("pages/2_Report issue.py","Report issue","🔍"),
        Page("pages/3_Log out.py","Log Out","📴"),
        Page("pages/4_test.py","test","💯")
    ]
)
st.title("Feed Report Checking:book:")

option1 = st.selectbox("Select a Source Name", ("IMF", "OECD", "JODI", "Statcounter", "FE", "ILO","sadsad"))

if option1 == "IMF":
    option2 = st.selectbox("Select a Feed Name", ("IFS", "FSI"))
elif option1 == "OECD":
    option2 = st.selectbox("Select a Feed Name", ("MUNW", "AHPI"))
elif option1 == "JODI":
    option2 = st.selectbox("Select a Feed Name", ("WDB",))
elif option1 == "Statcounter":
    option2 = st.selectbox("Select a Feed Name", ("IUT",))
elif option1 == "FE":
    option2 = st.selectbox("Select a Feed Name", ("FE",))
elif option1 == "ILO":
    option2 = st.selectbox("Select a Feed Name", ("LFS",))
else:
    option2 = st.write("No Feed")

st.write("You selected:", option1, option2)


st.write("Upload Supporting Files (*.zip)")
uploadzip = st.file_uploader("Upload Zip File", type=["zip"])
if(uploadzip is None):
      st.write("Error")


st.write("Feed Report Checking - Checking Result")
st.write("Feed Name: ", option1 +'-'+ option2)
st.write("Layout Report VS CDMNext Layout")
