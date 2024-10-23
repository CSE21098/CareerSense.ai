import streamlit as st
import sqlite3
import bcrypt
import re

# Database connection
user_conn = sqlite3.connect('users.db', check_same_thread=False)
user_cursor = user_conn.cursor()

# Create users table if it doesn't exist
user_cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT UNIQUE,
        password TEXT
    )
''')
user_conn.commit()

# Initialize session state
if 'is_logged' not in st.session_state: 
    st.session_state['is_logged'] = False

def get_user_emails():
    user_cursor.execute('SELECT email FROM users')
    email_list = [row[0] for row in user_cursor.fetchall()]
    return email_list

def login():
    with st.form(key='login', clear_on_submit=True):
        st.subheader(':green[Login]')
        email = st.text_input(':blue[Email]', placeholder='Enter Your Email')
        password1 = st.text_input(':blue[Password]', placeholder='Enter Your Password', type='password')
        btn_login = st.form_submit_button('Login')
        
        if btn_login:
            email_lst = get_user_emails()
            if email in email_lst:
                user_cursor.execute('SELECT password FROM users WHERE email=?', (email,))
                saved_pass = user_cursor.fetchone()[0].encode()  # Ensure it is in bytes
                if bcrypt.checkpw(password1.encode(), saved_pass):
                    st.success("Logged In")
                    st.session_state['is_logged'] = True
                    st.session_state['user'] = email
                else:
                    st.warning("Wrong Password")                
            else:
                st.warning('Email is not correct')

def sign_up():
    with st.form(key='signup', clear_on_submit=True):
        st.subheader(':green[Sign Up]')
        email = st.text_input(':blue[Email]', placeholder='Enter Your Email')
        password1 = st.text_input(':blue[Password]', placeholder='Enter Your Password', type='password')
        password2 = st.text_input(':blue[Confirm Password]', placeholder='Confirm Your Password', type='password')
        btn_sign_up = st.form_submit_button('Sign Up')
        
        if btn_sign_up:
            if email:
                if validate_email(email):
                    if email not in get_user_emails():
                        if len(password1) >= 6:
                            if password1 == password2:
                                hashed_password = bcrypt.hashpw(password1.encode(), bcrypt.gensalt())
                                user_cursor.execute('INSERT INTO users (email, password) VALUES (?, ?)', (email, hashed_password))
                                user_conn.commit()
                                st.success('Account created successfully! Now you can log in with your registered email.')
                            else:
                                st.warning('Passwords do not match')
                        else:
                            st.warning('Password is too short')
                    else:
                        st.warning('Email already exists!')
                else:
                    st.warning('Invalid Email')

def validate_email(email):
    pattern = "^[a-zA-Z0-9-_]+@[a-zA-Z0-9]+\.[a-z]{1,3}$"
    return re.match(pattern, email) is not None

def logout():
    st.session_state['is_logged'] = False
    st.session_state['user'] = None
    st.success("Logged out successfully!")

def main():
    st.write("<h1><center>Account</center></h1>", unsafe_allow_html=True)
    
    if st.session_state['is_logged']:
        st.write(f"Logged in as: {st.session_state['user']}")
        if st.button("Logout"):
            logout()
    else:
        tab1, tab2 = st.tabs(["Login", "SignUp"])
        
        with tab1:
            login()
        with tab2:
            sign_up()

if __name__ == "__main__":
    main()
