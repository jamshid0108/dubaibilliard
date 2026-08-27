import streamlit as st

ADMIN_USER = "admin"
ADMIN_PASS = "dubaibilliard5300"

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.title("🎱 Dubai Billiard Club")
    st.subheader("Boshqaruv paneliga kirish")
    
    username = st.text_input("Login")
    password = st.text_input("Parol", type="password")
    
    if st.button("Kirish"):
        if username == ADMIN_USER and password == ADMIN_PASS:
            st.session_state.logged_in = True
            st.rerun()
        else:
            st.error("Login yoki parol noto'g'ri!")
else:
    st.success("Tizimga muvaffaqiyatli kirdingiz!")
