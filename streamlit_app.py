import streamlit as st
import time

# Sahifa sozlamalari
st.set_page_config(page_title="Dubai Billiard Club", page_icon="🎱", layout="centered")

# 1. LOGIN SESSIYASINI SAQLASH
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# Stollar vaqtini va holatini saqlash xotirasi
if "tables" not in st.session_state:
    st.session_state.tables = {
        1: {"active": False, "start_time": None, "price_per_hour": 30000},
        2: {"active": False, "start_time": None, "price_per_hour": 30000},
        3: {"active": False, "start_time": None, "price_per_hour": 30000},
        4: {"active": False, "start_time": None, "price_per_hour": 30000},
    }

# 2. LOGIN OYNASI
if not st.session_state.logged_in:
    st.title("🎱 Dubai Billiard Club")
    st.subheader("Boshqaruv paneliga kirish")
    
    username = st.text_input("Login")
    password = st.text_input("Parol", type="password")
    
    if st.button("Kirish", type="primary"):
        if username == "admin" and password == "dubaibilliard5300":
            st.session_state.logged_in = True
            st.rerun()
        else:
            st.error("Login yoki parol xato!")

# 3. ASOSIY BOSHQARUV PANELI
else:
    st.title("🎱 Dubai Billiard Club — Boshqaruv Paneli")
    st.write("---")

    # Har bir stol uchun interfeys
    for table_id, data in st.session_state.tables.items():
        st.write(f"### {table_id}-Stol")
        
        if not data["active"]:
            st.info("Stol bo'sh")
            if st.button(f"▶️ {table_id}-Stolni boshlash", key=f"start_{table_id}"):
                data["active"] = True
                data["start_time"] = time.time()  # Server vaqtini belgilash
                st.rerun()
        else:
            # O'tgan vaqtni real vaqt bilan hisoblash (fondagi vaqt)
            elapsed_seconds = int(time.time() - data["start_time"])
            minutes = elapsed_seconds // 60
            hours = minutes // 60
            rem_minutes = minutes % 60
            
            # Summani hisoblash
            current_sum = int((elapsed_seconds / 3600) * data["price_per_hour"])
            
            st.success(f"⏱ Vaqt: {hours} soat {rem_minutes} daqiqa | 💰 Summa: {current_sum:,} so'm")
            
            if st.button(f"⏹ {table_id}-Stolni to'xtatish (Hisob-kitob)", key=f"stop_{table_id}"):
                data["active"] = False
                data["start_time"] = None
                st.warning(f"Yakuniy summa: {current_sum:,} so'm")
                st.rerun()
        
        st.write("---")

    if st.button("Tizimdan chiqish"):
        st.session_state.logged_in = False
        st.rerun()
