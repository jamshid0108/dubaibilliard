import streamlit as st
import datetime

RATE_REGULAR = 50000 
RATE_DISCOUNT = 40000

st.set_page_config(page_title="Dubai Billiard Club", page_icon="🎱", layout="wide")

def get_local_time():
    return datetime.datetime.utcnow() + datetime.timedelta(hours=5)

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "tables" not in st.session_state:
    st.session_state.tables = {
        1: {"start_time": None, "active": False, "rate": RATE_REGULAR, "is_vip": False},
        2: {"start_time": None, "active": False, "rate": RATE_REGULAR, "is_vip": False},
        3: {"start_time": None, "active": False, "rate": RATE_REGULAR, "is_vip": False},
        4: {"start_time": None, "active": False, "rate": RATE_REGULAR, "is_vip": False},
    }

# Kunlik kassa tarixi va umumiy tushum
if "daily_total" not in st.session_state:
    st.session_state.daily_total = 0

if "history" not in st.session_state:
    st.session_state.history = []

if "last_receipt" not in st.session_state:
    st.session_state.last_receipt = None

# --- LOGIN ---
if not st.session_state.logged_in:
    st.title("🎱 Dubai Billiard Club")
    st.subheader("Boshqaruv paneliga kirish")
    
    u = st.text_input("Login").strip()
    p = st.text_input("Parol", type="password").strip()
    
    if st.button("Kirish", type="primary"):
        if u.lower() == "admin" and p == "dubaibilliard5300":
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

    # 1-BO'LIM: STOLLAR NAZORATI
    if page == "Stollar nazorati (Obshiy zal)":
        st.title("📊 Obshiy zal — 4 ta stol nazorati")
        
        if st.session_state.last_receipt:
            rec = st.session_state.last_receipt
            st.success("🧾 **OXIRGI TO'LOV CHEKI:** " + str(rec['table']) + "-Stol | Jami vaqt: " + str(rec['minutes']) + " daqiqa | **TO'LANADIGAN SUMMA: " + str(rec['cost']) + " so'm**")
            if st.button("Yopish"):
                st.session_state.last_receipt = None
                st.rerun()
            st.write("---")

        cols = st.columns(2)
        
        for i in range(1, 5):
            col = cols[(i - 1) % 2]
            table = st.session_state.tables[i]
            
            with col:
                status_icon = "🔴" if table['active'] else "🟢"
                st.subheader(status_icon + " " + str(i) + "-Stol")
                
                if table['active']:
                    now = get_local_time()
                    elapsed = now - table['start_time']
                    minutes = int(elapsed.total_seconds() // 60)
                    cost = int((elapsed.total_seconds() / 3600) * table['rate'])
                    
                    rate_type_str = "⭐ Doimiy klient (40 ming)" if table['is_vip'] else "Standard (50 ming)"
                    
                    st.error("Holati: Band (" + str(minutes) + " daqiqa)")
                    st.write("**Tarif:** " + rate_type_str)
                    st.write("**Boshlangan vaqt:** " + table['start_time'].strftime('%H:%M'))
                    st.write("**Joriy summa:** " + str(cost) + " so'm")
                    
                    if st.button("To'xtatish va hisoblash", key="stop_" + str(i)):
                        end_time_str = get_local_time().strftime('%H:%M')
                        
                        # Kassaga qo'shish
                        st.session_state.daily_total += cost
                        st.session_state.history.append({
                            "stol": i,
                            "vaqt": table['start_time'].strftime('%H:%M') + " - " + end_time_str,
                            "daqiqa": minutes,
                            "summa": cost
                        })
                        
                        st.session_state.last_receipt = {
                            "table": i,
                            "minutes": minutes,
                            "cost": cost
                        }
                        
                        table['active'] = False
                        table['start_time'] = None
                        st.rerun()
                else:
                    st.success("Holati: Bo'sh")
                    
                    btn_col1, btn_col2 = st.columns(2)
                    with btn_col1:
                        if st.button("Boshlash (50 ming)", key="start_reg_" + str(i)):
                            table['active'] = True
                            table['start_time'] = get_local_time()
                            table['rate'] = RATE_REGULAR
                            table['is_vip'] = False
                            st.session_state.last_receipt = None
                            st.rerun()
                    with btn_col2:
                        if st.button("⭐ Skidka (40 ming)", key="start_disc_" + str(i)):
                            table['active'] = True
                            table['start_time'] = get_local_time()
                            table['rate'] = RATE_DISCOUNT
                            table['is_vip'] = True
                            st.session_state.last_receipt = None
                            st.rerun()
                            
                st.write("---")

    elif page == "Bar va Saqlash":
        st.title("🥤 Bar va saqlash xonasi")

    # 3-BO'LIM: KASSA VA HISOBOT
    elif page == "Kassa va Hisobot":
        st.title("💰 Kunlik kassa va hisobotlar")
        
        st.metric(label="Bugungi jami tushum", value=f"{st.session_state.daily_total:,} so'm")
        st.write("---")
        st.subheader("📋 Bugungi o'yinlar tarixi")
        
        if st.session_state.history:
            for item in reversed(st.session_state.history):
                st.write(f"🎱 **{item['stol']}-Stol** | Vaqti: {item['vaqt']} ({item['daqiqa']} daq) | **To'lov: {item['summa']:,} so'm**")
        else:
            st.info("Bugun hali to'xtatilgan o'yinlar yo'q.")
