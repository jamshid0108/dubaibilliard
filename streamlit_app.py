import streamlit as st
import datetime

ADMIN_USER = "admin"
ADMIN_PASS = "dubaibilliard5300"

# Narxlar (so'mda)
RATE_REGULAR = 50000  # Oddiy klient (50 000 so'm/soat)
RATE_DISCOUNT = 40000 # Doimiy klient (40 000 so'm/soat)

st.set_page_config(page_title="Dubai Billiard Club", page_icon="🎱", layout="wide")

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# Stollar holati va vaqtini saqlash
if "tables" not in st.session_state:
    st.session_state.tables = {
        1: {"start_time": None, "active": False, "rate": RATE_REGULAR, "is_vip": False},
        2: {"start_time": None, "active": False, "rate": RATE_REGULAR, "is_vip": False},
        3: {"start_time": None, "active": False, "rate": RATE_REGULAR, "is_vip": False},
        4: {"start_time": None, "active": False, "rate": RATE_REGULAR, "is_vip": False},
    }

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
        st.title("📊 Obshiy zal — 4 ta stol nazorati")
        
        cols = st.columns(2)
        
        for i in range(1, 5):
            col = cols[(i - 1) % 2]
            table = st.session_state.tables[i]
            
            with col:
                st.subheader(f"{'🔴' if table['active'] else '🟢'} {i}-Stol")
                
                if table['active']:
                    now = datetime.datetime.now()
                    elapsed = now - table['start_time']
                    minutes = int(elapsed.total_seconds() // 60)
                    cost = int((elapsed.total_seconds() / 3600) * table['rate'])
                    
                    rate_type_str = "⭐ Doimiy klient (40 ming)" if table['is_vip'] else "Standard (50 ming)"
                    
                    st.error(f"Holati: Band ({minutes} daqiqa)")
                    st.write(f"**Tarif:** {rate_type_str}")
                    st.write(f"Boshlangan vaqt:.strftime('%H:%M')}")
                    st.write(f"**Joriy summa:** {cost:,} so'm")
                    
                    if st.button(f"To'xtatish va hisoblash", key=f"stop_{i}"):
                        table['active'] = False
                        table['start_time'] = None
                        st.success(f"{i}-Stol to'xtatildi! Jami summa: {cost:,} so'm")
                        st.rerun()
                else:
                    st.success("Holati: Bo'sh")
                    
                    btn_col1, btn_col2 = st.columns(2)
                    with btn_col1:
                        if st.button(f"Boshlash (50 ming)", key=f"start_reg_{i}"):
                            table['active'] = True
                            table['start_time'] = datetime.datetime.now()
                            table['rate'] = RATE_REGULAR
                            table['is_vip'] = False
                            st.rerun()
                    with btn_col2:
                        if st.button(f"⭐ Skidka (40 ming)", key=f"start_disc_{i}"):
                            table['active'] = True
                            table['start_time'] = datetime.datetime.now()
                            table['rate'] = RATE_DISCOUNT
                            table['is_vip'] = True
                            st.rerun()
                            
                st.write("---")

    elif page == "Bar va Saqlash":
        st.title("🥤 Bar va saqlash xonasi")
        st.write("Bar mahsulotlari boshqaruvi")

    elif page == "Kassa va Hisobot":
        st.title("💰 Kunlik kassa va daromadlar")
        st.metric(label="Bugungi tushum", value="0 UZS")
