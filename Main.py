import streamlit as st
import pyrebase

# Firebase configuration
firebaseConfig = {
  'apiKey': "AIzaSyArRVNiOa-ZT1n87BFDqUf-OUKoTlzXgk0",
  'authDomain': "streamlit-frce.firebaseapp.com",
  'projectId': "streamlit-frce",
  'databaseURL':'https://streamlit-frce-default-rtdb.asia-southeast1.firebasedatabase.app/',
  'storageBucket':'streamlit-frce.appspot.com',
  'messagingSenderId': "154973952361",
  'appId': "1:154973952361:web:1581ec1d48293410b7c5f8",
  'measurementId': "G-3SQ2FK2LNP"
}

firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()

if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False

# Database and Storage
db = firebase.database()
storage = firebase.storage()

def login_page():
    st.title('CEIC FRCE Login')
    # Company logo
    st.image("company logo.png", width=200)
    # Authentication choice
    choice = st.selectbox('Login/Signup/', ['Login', 'Sign up'])
    # Obtain User Input for email and password
    email = st.text_input('Please enter your email address')
    password = st.text_input('Please enter your password', type='password')

    # Sign up Block
    if choice == 'Sign up':
        handle = st.text_input('Please input your app handle name', value='Default')
        submit = st.button('Create my account') 

        if submit:
            user = auth.create_user_with_email_and_password(email, password)
            st.success('Your account is created successfully!')
            st.balloons()
            # Sign in
            user = auth.sign_in_with_email_and_password(email, password)
            db.child(user['localId']).child("Handle").set(handle)
            db.child(user['localId']).child("ID").set(user['localId'])
            st.title('Welcome ' + handle)
            st.info('Login via login drop down selection')


    # Login Block
    if choice == 'Login':
        login = st.button('Login')
        submit1 = st.button('Reset Password')

        if login:
            user = auth.sign_in_with_email_and_password(email, password)
            st.session_state['authenticated'] = True
            st.session_state['current_page'] = 'Home'
            st.rerun()  # Refresh the page to show the home page

        if submit1:
            auth.send_password_reset_email(email)
            st.title('Check your email')
            st.info('Login via login drop down selection with your new password')

# Main Application
##if st.session_state['authenticated']:
##    home_page()

if st.session_state['authenticated']:
    st.sidebar.title("Navigation")
    page = st.sidebar.radio('Pages',('🏠Home', '📆History', '🔍Report Issue', '📴Log Out'))

    if page == '🏠Home':
        st.session_state['current_page'] = 'Home'
    elif page == '📆History':
        st.session_state['current_page'] = 'History'
    elif page == '🔍Report Issue':
        st.session_state['current_page'] = 'Report Issue'
    elif page == '📴Log Out':
        st.session_state['current_page'] = 'Log Out'
else:
    st.session_state['current_page']='Login'
    login_page()

def home_page():
    ##Home page code 
    st.image('CEIC img.png', width = 100)
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

def page1():
    st.title('History:date:')
    tab1, tab2 = st.tabs(["Create", "List"])
    with tab1:
        st.subheader("Title")
    with tab2:
        st.header("List of Issues")

def page2():
    st.title("Report Issue:warning:")
    title1 = st.text_input("Title", "Type here")
    create1 = st.text_input("Created by", "Type here")
    description1 = st.text_area("Description","Type here", height=300)

def page3():
    if st.button('Logout'):
        st.session_state['authenticated'] = False
        st.rerun()


# Conditional rendering based on session state
#if st.session_state['current_page'] == 'Login':
#    login_page()
#    st.write("asd")
if st.session_state['current_page'] == 'Home':
    home_page()
elif st.session_state['current_page'] == 'History':
    page1()
elif st.session_state['current_page'] == 'Report Issue':
    page2()
elif st.session_state['current_page'] == 'Log Out':
    page3()


