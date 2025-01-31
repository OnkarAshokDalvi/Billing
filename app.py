import streamlit as st
import pandas as pd
from datetime import datetime
import os

# File path for Excel
EXCEL_FILE = 'billing_data.xlsx'

# Create Excel file if it doesn't exist
if not os.path.exists(EXCEL_FILE):
    df = pd.DataFrame(columns=['Date', 'Amount', 'Description'])
    df.to_excel(EXCEL_FILE, index=False)

# User credentials (in real app, use secure storage)
USERS = {
    'admin': 'password123'
}

def login():
    st.title('Login')
    
    username = st.text_input('Username')
    password = st.text_input('Password', type='password')
    
    if st.button('Login'):
        if username in USERS and USERS[username] == password:
            st.session_state.logged_in = True
            st.session_state.username = username
            st.rerun()
        else:
            st.error('Invalid credentials')

def billing_system():
    st.title('Billing System')
    
    # Sidebar with logout button
    with st.sidebar:
        st.write(f'Welcome, {st.session_state.username}!')
        if st.button('Logout'):
            st.session_state.logged_in = False
            st.rerun()
    
    # Input form
    with st.form('billing_form'):
        amount = st.number_input('Amount', min_value=0.0, step=0.01)
        description = st.text_input('Description')
        submitted = st.form_submit_button('Add Bill')
        
        if submitted:
            df = pd.read_excel(EXCEL_FILE)
            new_row = pd.DataFrame({
                'Date': [datetime.now().strftime('%Y-%m-%d %H:%M:%S')],
                'Amount': [amount],
                'Description': [description]
            })
            df = pd.concat([df, new_row], ignore_index=True)
            df.to_excel(EXCEL_FILE, index=False)
            st.success('Bill added successfully!')
    
    # Display data and summary
    st.subheader('Billing Summary')
    df = pd.read_excel(EXCEL_FILE)
    
    if not df.empty:
        st.dataframe(df)
        total = df['Amount'].sum()
        st.metric('Total Amount', f'${total:.2f}')
        
        # Download button
        if st.download_button(
            label='Download Excel',
            data=open(EXCEL_FILE, 'rb'),
            file_name='billing_data.xlsx',
            mime='application/vnd.ms-excel'
        ):
            st.success('File downloaded successfully!')
    else:
        st.info('No billing data available')

def main():
    # Initialize session state
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    
    # Session timeout (30 minutes)
    if 'last_activity' in st.session_state:
        if (datetime.now() - st.session_state.last_activity).seconds > 1800:  # 30 minutes
            st.session_state.logged_in = False
    
    st.session_state.last_activity = datetime.now()
    
    # Show login or main app based on session state
    if not st.session_state.logged_in:
        login()
    else:
        billing_system()

if __name__ == '__main__':
    main()