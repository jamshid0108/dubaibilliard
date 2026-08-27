import streamlit as st

ADMIN_USER = "admin"
ADMIN_PASS = "dubaibilliard5300"

st.set_page_config(page_title="Dubai Billiard Club", page_icon="🎱", layout="wide")

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
    st.sidebar.title("🎱 Dubai Billiard")
    page = st.sidebar.radio("Bo'limni tanlang:", ["Stollar nazorati (Obshiy zal)", "Bar va Saqlash", "Kassa va Hisobot"])
    
    if st.sidebar.button("Tizimdan chiqish"):
        st.session_state.logged_in = False
        st.rerun()

    if page == "Stollar nazorati (Obshiy zal)":
        st.title("📊 Obshiy zal — 4 ta stol holati")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🟢 1-Stol")
            st.info("Holati: Bo'sh")
            st.button("Vaqtni boshlash", key="s1")
            st.write("---")
            
            st.subheader("🟢 3-Stol")
            st.info("Holati: Bo'sh")
            st.button("Vaqtni boshlash", key="s3")
            
        with col2:
            st.subheader("🟢 2-Stol")
            st.info("Holati: Bo'sh")
            st.button("Vaqtni boshlash", key="s2")
            st.write("---")
            
            st.subheader("🟢 4-Stol")
            st.info("Holati: Bo'sh")
            st.button("Vaqtni boshlash", key="s4")

    elif page == "Bar va Saqlash":
        st.title("🥤 Bar va saqlash xonasi")
        st.write("Ichimliklar va bar mahsulotlari hisobi")

    elif page == "Kassa va Hisobot":
        st.title("💰 Kunlik kassa va daromadlar")
        st.metric(label="Bugungi tushum", value="0 UZS")
