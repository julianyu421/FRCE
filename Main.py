import streamlit as st
import pyrebase
import zipfile
import pandas as pd


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
    uploaded_file = st.file_uploader("Upload a Process Report zip file", type="zip")
    uploaded_file2 = st.file_uploader("Upload a Layout Report zip file", type="zip")
    # Initialize the session state variable if not already done
    if "show_macro_cap_flag" not in st.session_state:
        st.session_state.show_macro_cap_flag = False
    
    if "show_series_status" not in st.session_state:
        st.session_state.show_series_status = False
    
    if "show_new_series" not in st.session_state:
        st.session_state.show_new_series = False
    
    if "show_unit_edge" not in st.session_state:
        st.session_state.show_unit_edge = False
    
    if "show_series_name" not in st.session_state:
        st.session_state.show_series_name = False
    
    if "show_multiplier" not in st.session_state:
        st.session_state.show_multiplier = False
    
    if "show_series_remark" not in st.session_state:
        st.session_state.show_series_remark = False
    
    if "show_source_new" not in st.session_state:
        st.session_state.show_source_new = False
    
    if "show_source_delete" not in st.session_state:
        st.session_state.show_source_delete = False
    
    if "show_timepoint_summary_byseries" not in st.session_state:
        st.session_state.show_timepoint_summary_byseries = False
    
    if "show_timepoint_deleted" not in st.session_state:
        st.session_state.show_timepoint_deleted = False
    
    if "show_abnormal_timepoints" not in st.session_state:
        st.session_state.show_abnormal_timepoints = False    
    
    if "show_layoutseries_new" not in st.session_state:
        st.session_state.show_layoutseries_new = False  

    if "show_layoutseries_changed" not in st.session_state:
        st.session_state.show_layoutseries_changed = False              

    if uploaded_file is not None:
        # Read the uploaded zip file
        with zipfile.ZipFile(uploaded_file, 'r') as zip_ref:
            # Get a list of all archived file names from the zip
            file_list = zip_ref.namelist()
            
            # Display the list of files in the zip
            st.write("Files in the zip:")
            for file_name in file_list:
                st.write(file_name)
    
            ### Timepoints report
    
            timepoints_file = None
            for file_name in file_list:
                if "Timepoints" in file_name:
                    timepoints_file = file_name
                    break
    
            if timepoints_file:
                        with zip_ref.open(timepoints_file) as file:
                            # Use pandas to read the sheet of the Excel file
                            df_timepoint_summary_byseries = pd.read_excel(file, sheet_name=1)
                            df_timepoint_summary_byseries['Series_id'] = df_timepoint_summary_byseries['Series_id'].astype(str)
                            df_timepoint_deleted = pd.read_excel(file, sheet_name=2)
                            df_abnormal_timepoints = pd.read_excel(file, sheet_name=3)
    
                            timepoint_summary_byseries_count = df_timepoint_summary_byseries.shape[0]
                            timepoint_summary_byseries_sum = df_timepoint_summary_byseries.iloc[:, 5].sum()
                            timepoint_deleted_count = df_timepoint_deleted.shape[0]
                            abnormal_timepoints_count = df_abnormal_timepoints.shape[0]
            
            else:
                st.write("No file found with name containing 'Timepoints_Report'.")
    
            ##EDGE Source Tree Report
            edge_source_tree_file = None
            for file_name in file_list:
                if "EDGESourceTree" in file_name:
                    edge_source_tree_file = file_name
                    break
            ###EDGE Source Tree
            if edge_source_tree_file:
                        # Read the EDGESourceNew_Report Excel file
                        with zip_ref.open(edge_source_tree_file) as file:
                            # Use pandas to read the sheet of the Excel file
                            df_source_new = pd.read_excel(file, sheet_name=0)
                            df_source_delete = pd.read_excel(file, sheet_name=1)
    
                            source_new_row_count = df_source_new.shape[0]
                            source_delete_row_count = df_source_delete.shape[0]
            else:
                st.write("No file found with name containing 'EDGESourceTree_Report'.")
    
            # Find the file name containing "NewSeries_Report"
            new_series_file = None
            for file_name in file_list:
                if "NewSeries_Report" in file_name:
                    new_series_file = file_name
                    break
            
            if new_series_file:
                # Read the NewSeries_Report Excel file
                with zip_ref.open(new_series_file) as file:
                    df_new_series = pd.read_excel(file)
                    df_new_series['Series_Id'] = df_new_series['Series_Id'].astype(str) 
                    # Count the number of rows in the Excel file
                    new_series_row_count = df_new_series.shape[0]
                    
    
            else:
                st.write("No file found with name containing 'NewSeries_Report'.")
            
            # Find the file name containing "SeriesChange_Report"
            series_change_file = None
            for file_name in file_list:
                if "SeriesChange_Report" in file_name:
                    series_change_file = file_name
                    break
            
            if series_change_file:
                # Read the SeriesChange_Report Excel file
                with zip_ref.open(series_change_file) as file:
                    # Use pandas to read the sheet of the Excel file
                    df_macro_cap_flag = pd.read_excel(file, sheet_name=0)
                    df_series_status = pd.read_excel(file, sheet_name=1)
                    df_series_status['Series_Id'] = df_series_status['Series_Id'].astype(str)
                    df_unit_edge = pd.read_excel(file, sheet_name=2)
                    df_series_name = pd.read_excel(file, sheet_name=3)
                    df_series_name['Series_Id'] = df_series_name['Series_Id'].astype(str) 
                    df_multiplier = pd.read_excel(file, sheet_name=4)
                    df_series_remark = pd.read_excel(file, sheet_name=5)
    
                    # Count the number of rows in the sheet of the Excel file
                    macro_cap_flag_row_count = df_macro_cap_flag.shape[0]
                    series_status_row_count = df_series_status.shape[0]
                    unit_edge_row_count = df_unit_edge.shape[0]
                    series_name_row_count = df_series_name.shape[0]
                    multiplier_row_count = df_multiplier.shape[0]
                    series_remark_row_count = df_series_remark.shape[0]
    
    
    
            else:
                st.write("No file found with name containing 'SeriesChange_Report'.")
            
    if uploaded_file2 is not None:
        # Read the uploaded zip file
        with zipfile.ZipFile(uploaded_file2, 'r') as zip_ref2:
            # Get a list of all archived file names from the zip
            file_list2 = zip_ref2.namelist()
            
            # Display the list of files in the zip
            st.write("Files in the zip:")
            for file_name2 in file_list2:
                st.write(file_name2)

            #### Layout Report

            layouts_file = None
            for file_name2 in file_list2:
                if "Layout" in file_name2:
                    layouts_file = file_name2
                    break

            if layouts_file:
                    with zip_ref2.open(layouts_file) as file:
                        # Use pandas to read the sheet of the Excel file
                        df_layoutseries_new = pd.read_excel(file, sheet_name=0)
                        df_layoutseries_new['Series_Id'] = df_layoutseries_new['Series_Id'].astype(str)
                        df_layoutseries_changed = pd.read_excel(file, sheet_name=1)
                        df_layoutseries_changed['Series_Id'] = df_layoutseries_changed['Series_Id'].astype(str)
    
                        # Count the number of rows in the sheet of the Excel file
                        layoutseries_new_count = df_layoutseries_new.shape[0]
                        layoutseries_changed_count = df_layoutseries_changed.shape[0]
            
            else:
                st.write("No file found with name containing 'Timepoints_Report'.")
    
        data = {
            "Checking": ["Timepoint Summary by Series", "Timepoint Deleted", "Abnormal Timepoints", "Macro Cap Flag", "Series Status", "Unit EDGE CDM", "Series Name", "Multiplier", "Series Remark", "New Series", "Source New", "Source Delete","LayoutSeries_New","LayoutSeries_Changed"],
            "DPA Process Report": [timepoint_summary_byseries_sum,timepoint_deleted_count,abnormal_timepoints_count,macro_cap_flag_row_count,series_status_row_count,unit_edge_row_count,series_name_row_count,multiplier_row_count,series_remark_row_count,new_series_row_count, source_new_row_count,source_delete_row_count,layoutseries_new_count,layoutseries_changed_count],
            "CDMNext Layout": ["NA","NA","NA","NA","NA","NA","NA","NA","NA","NA","NA","NA","NA","NA"],
            "Status": ["NA","NA","NA","NA","NA","NA","NA","NA","NA","NA","NA","NA","NA","NA"]
        }
    
        df = pd.DataFrame(data)
        # Display the DataFrame
        st.write("Process Report Checking Table")
        st.dataframe(df)  # or use st.table(df) for a static table
    ######################################################  
        st.write(f"Series Detail - Timepoint Summary by Series from {timepoints_file}:")
        if st.button("Timepoint Summary by Series"):
            st.session_state.show_timepoint_summary_byseries = not st.session_state.show_timepoint_summary_byseries
     
        if st.session_state.show_timepoint_summary_byseries:
            st.dataframe(df_timepoint_summary_byseries)
    
        st.write(f"Series Detail - Timepoint Deleted from {timepoints_file}:")
        if st.button("Timepoint Deleted by Series"):
            st.session_state.show_timepoint_deleted = not st.session_state.show_timepoint_deleted
     
        if st.session_state.show_timepoint_deleted:
            st.dataframe(df_timepoint_deleted)
    
        st.write(f"Series Detail - Abnormal Timepoints from {timepoints_file}:")
        if st.button("Abnormal Timepoints by Series"):
            st.session_state.show_abnormal_timepoints = not st.session_state.show_abnormal_timepoints
     
        if st.session_state.show_abnormal_timepoints:
            st.dataframe(df_abnormal_timepoints)        
    
    
    
        # Display the dataframe (optional)
        st.write(f"Series Detail - Macro Cap Flag from {series_change_file}:")
        # Button to toggle the visibility of the DataFrame
        if st.button("Macro Cap Flag"):
            st.session_state.show_macro_cap_flag = not st.session_state.show_macro_cap_flag
    
        # Conditionally display the DataFrame based on the button's state
        if st.session_state.show_macro_cap_flag:
            st.dataframe(df_macro_cap_flag)
        ###### Unit
    
        st.write(f"Series Detail - Series Status from {series_change_file}:")
        # Button to toggle the visibility of the DataFrame
        if st.button("Series Status"):
            st.session_state.show_series_status = not st.session_state.show_series_status
    
        # Conditionally display the DataFrame based on the button's state
        if st.session_state.show_series_status:
            st.dataframe(df_series_status)
    
        st.write(f"Series Detail - Unit EDGE from {series_change_file}:")
        # Button to toggle the visibility of the DataFrame
        if st.button("Unit EDGE"):
            st.session_state.show_unit_edge = not st.session_state.show_unit_edge
     
        if st.session_state.show_unit_edge:
            st.dataframe(df_unit_edge)
    
        st.write(f"Series Detail - Series Name from {series_change_file}:")
        # Button to toggle the visibility of the DataFrame
        if st.button("Series Name"):
            st.session_state.show_series_name = not st.session_state.show_series_name
     
        if st.session_state.show_series_name:
            st.dataframe(df_series_name)
    
        st.write(f"Series Detail - Multiplier from {series_change_file}:")
        # Button to toggle the visibility of the DataFrame
        if st.button("Multiplier"):
            st.session_state.show_multiplier = not st.session_state.show_multiplier
     
        if st.session_state.show_multiplier:
            st.dataframe(df_multiplier)
    
        st.write(f"Series Detail - Series Remark from {series_change_file}:")
        # Button to toggle the visibility of the DataFrame
        if st.button("Series Remark"):
            st.session_state.show_series_remark = not st.session_state.show_series_remark
     
        if st.session_state.show_series_remark:
            st.dataframe(df_series_remark)
        
    ########## new series
    
        # Display the dataframe (optional)
        st.write(f"Series Detail - New Series from {new_series_file}:")
        if st.button("New Series"):
            st.session_state.show_new_series = not st.session_state.show_new_series
    
        # Conditionally display the DataFrame based on the button's state
        if st.session_state.show_new_series:
            st.dataframe(df_new_series)
    
    ####### EDGE SourceTree Report
        st.write(f"Series Detail - Source New from {edge_source_tree_file}:")
        if st.button("Source New"):
            st.session_state.show_source_new = not st.session_state.show_source_new
     
        if st.session_state.show_source_new:
            st.dataframe(df_source_new)
    
    
        st.write(f"Series Detail - Source Delete from {edge_source_tree_file}:")
        if st.button("Source Delete"):
            st.session_state.show_source_delete = not st.session_state.show_source_delete
     
        if st.session_state.show_source_delete:
            st.dataframe(df_source_delete)

    ######## Layout Report
        st.write(f"Series Detail - Source New from {layouts_file}:")
        if st.button("New Layout Series"):
            st.session_state.show_layoutseries_new = not st.session_state.show_layoutseries_new
     
        if st.session_state.show_layoutseries_new:
            st.dataframe(df_layoutseries_new)
    
    
        st.write(f"Series Detail - Series Status Changed from {layouts_file}:")
        if st.button("Layout Series Change"):
            st.session_state.show_layoutseries_changed = not st.session_state.show_layoutseries_changed
     
        if st.session_state.show_layoutseries_changed:
            st.dataframe(df_layoutseries_changed)


#    st.write("Feed Report Checking - Checking Result")
#    st.write("Feed Name: ", option1 +'-'+ option2)
#    st.write("Layout Report VS CDMNext Layout")

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


