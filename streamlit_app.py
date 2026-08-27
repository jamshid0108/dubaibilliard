import streamlit as st
import datetime
import json
import os

RATE_REGULAR = 50000 
RATE_DISCOUNT = 40000
DATA_FILE = "billiard_history.json"
STATE_FILE = "tables_state.json"

st.set_page_config(page_title="Dubai Billiard Club", page_icon="🎱", layout="wide")

# --- CSS: DIZAYN VA TUGMALARNI YONMA-YON QILISH ---
st.markdown("""
    <style>
    /* 1. Asosiy orqa fon */
    .stApp {
        background-image: linear-gradient(rgba(0, 0, 0, 0.35), rgba(0, 0, 0, 0.35)), 
                          url("https://images.unsplash.com/photo-1511193311914-0346f16efe90?q=80&w=1920");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }
    
    /* 2. Yon panel (Sidebar) biroz shaffof qora */
    [data-testid="stSidebar"] {
        background-color: rgba(18, 18, 18, 0.82) !important;
        border-right: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    /* Matnlarni tiniq ko'rsatish */
    h1, h2, h3, h4, p, span, label {
        color: #ffffff !important;
    }
    
    /* Sidebar sarlavhasi ("Dubai Billiard") */
    [data-testid="stSidebar"] h1 {
        font-size: 30px !important;
        font-weight: 800 !important;
        letter-spacing: 0.5px;
    }
    
    /* Sidebar menyu yozuvlari */
    [data-testid="stSidebar"] p, [data-testid="stSidebar"] label {
        font-size: 20px !important;
        font-weight: bold !important;
    }
    
    /* 3. "Tizimdan chiqish" tugmasi kichik va chap pastki burchakda */
    [data-testid="stSidebar"] .stButton button {
        font-size: 13px !important;
        padding: 5px 10px !important;
        border-radius: 6px !important;
    }
    
    /* Asosiy tugmalar */
    .stButton button { font-size: 18px !important; border-radius: 8px !important; }
    
    /* 4. OXIRGI TO'LOV CHEKI - ANIQ VA YORQIN YASHIL FON */
    div.stSuccess {
        background-color: #0d5c2e !important;
        border: 2px solid #00ff66 !important;
        opacity: 1 !important;
        border-radius: 10px;
        padding: 15px;
    }
    div.stSuccess * {
        color: #ffffff !important;
        font-size: 17px !important;
    }
    
    /* Stol kartochkalari foni */
    [data-testid="stVerticalBlock"] > div {
        background-color: rgba(40, 40, 40, 0.5) !important;
        border-radius: 12px;
        padding: 10px;
    }
    </style>
""", unsafe_allow_html=True)

def get_local_time():
    return datetime.datetime.utcnow() + datetime.timedelta(hours=5)

def load_history():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return []
    return []

def save_history(history_data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(history_data, f, ensure_ascii=False, indent=2)

def load_tables_state():
    default_tables = {
        "1": {"start_time": None, "active": False, "rate": RATE_REGULAR, "is_vip": False, "last_stopped_time": None},
        "2": {"start_time": None, "active": False, "rate": RATE_REGULAR, "is_vip": False, "last_stopped_time": None},
        "3": {"start_time": None, "active": False, "rate": RATE_REGULAR, "is_vip": False, "last_stopped_time": None},
        "4": {"start_time": None, "active": False, "rate": RATE_REGULAR, "is_vip": False, "last_stopped_time": None},
    }
    if os.path.exists(STATE_FILE):
        try:
            with open(STATE_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                for k, v in data.items():
                    if v.get("start_time"):
                        v["start_time"] = datetime.datetime.fromisoformat(v["start_time"])
                    if v.get("last_stopped_time"):
                        v["last_stopped_time"] = datetime.datetime.fromisoformat(v["last_stopped_time"])
                return data
        except:
            return default_tables
    return default_tables

def save_tables_state(tables_data):
    serializable_tables = {}
    for k, v in tables_data.items():
        serializable_tables[str(k)] = {
            "active": v["active"],
            "start_time": v["start_time"].isoformat() if v["start_time"] else None,
            "rate": v["rate"],
            "is_vip": v["is_vip"],
            "last_stopped_time": v["last_stopped_time"].isoformat() if v["last_stopped_time"] else None
        }
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(serializable_tables, f, ensure_ascii=False, indent=2)

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "tables" not in st.session_state:
    st.session_state.tables = load_tables_state()

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
    
    # Chiqish tugmasini pastki chap burchakka tushirish uchun bo'sh joy
    st.sidebar.markdown("<div style='height: 38vh;'></div>", unsafe_allow_html=True)
    
    if st.sidebar.button("🚪 Tizimdan chiqish", type="secondary", use_container_width=True):
        st.session_state.logged_in = False
        st.rerun()

    # 1-BO'LIM: STOLLAR NAZORATI
    if page == "Stollar nazorati (Obshiy zal)":
        st.title("📊 Obshiy zal — 4 ta stol nazorati")
        
        if st.session_state.last_receipt:
            rec = st.session_state.last_receipt
            t_num = rec['table']
            st.success("🧾 **OXIRGI TO'LOV CHEKI:** " + str(t_num) + "-Stol | Jami vaqt: " + str(rec['minutes']) + " daqiqa | **TO'LANADIGAN SUMMA: " + str(rec['cost']) + " so'm**")
            
            # Tugmalarni yonma-yon qilish uchun kichik ustunlar va o'nga surish uchun bo'sh ustun
            _, col_btn1, col_btn2 = st.columns([3, 1, 1.2])
            with col_btn1:
                if st.button("Yopish", use_container_width=True):
                    st.session_state.last_receipt = None
                    st.rerun()
            with col_btn2:
                if st.button("▶️ Davom ettirish", use_container_width=True):
                    table = st.session_state.tables[str(t_num)]
                    if table['last_stopped_time']:
                        now = get_local_time()
                        paused_duration = now - table['last_stopped_time']
                        table['start_time'] = table['start_time'] + paused_duration
                    
                    table['active'] = True
                    table['last_stopped_time'] = None
                    save_tables_state(st.session_state.tables)
                    st.session_state.last_receipt = None
                    st.rerun()
            st.write("---")

        cols = st.columns(2)
        
        for i in range(1, 5):
            col = cols[(i - 1) % 2]
            table = st.session_state.tables[str(i)]
            
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
                        end_time = get_local_time()
                        
                        history = load_history()
                        history.append({
                            "sana": end_time.strftime("%Y-%m-%d"),
                            "stol": i,
                            "vaqt": table['start_time'].strftime('%H:%M') + " - " + end_time.strftime('%H:%M'),
                            "daqiqa": minutes,
                            "summa": cost
                        })
                        save_history(history)
                        
                        st.session_state.last_receipt = {
                            "table": i,
                            "minutes": minutes,
                            "cost": cost
                        }
                        
                        table['active'] = False
                        table['last_stopped_time'] = end_time
                        save_tables_state(st.session_state.tables)
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
                            table['last_stopped_time'] = None
                            st.session_state.last_receipt = None
                            save_tables_state(st.session_state.tables)
                            st.rerun()
                    with btn_col2:
                        if st.button("⭐ Skidka (40 ming)", key="start_disc_" + str(i)):
                            table['active'] = True
                            table['start_time'] = get_local_time()
                            table['rate'] = RATE_DISCOUNT
                            table['is_vip'] = True
                            table['last_stopped_time'] = None
                            st.session_state.last_receipt = None
                            save_tables_state(st.session_state.tables)
                            st.rerun()
                            
                st.write("---")

    elif page == "Bar va Saqlash":
        st.title("🥤 Bar va saqlash xonasi")

    elif page == "Kassa va Hisobot":
        st.title("💰 Kassa va kunlik hisobotlar")
        
        history = load_history()
        
        if history:
            available_dates = sorted(list(set(item['sana'] for item in history)), reverse=True)
            selected_date = st.selectbox("📅 Sanani tanlang:", available_dates)
            
            day_records = [item for item in history if item['sana'] == selected_date]
            day_total = sum(item['summa'] for item in day_records)
            
            st.metric(label=f"💰 {selected_date} kunidagi jami tushum", value=f"{day_total:,} so'm")
            st.write("---")
            st.subheader(f"📋 {selected_date} sanasidagi o'yinlar ro'yxati:")
            
            for item in reversed(day_records):
                st.write(f"🎱 **{item['stol']}-Stol** | Vaqti: {item['vaqt']} ({item['daqiqa']} daq) | **To'lov: {item['summa']:,} so'm**")
        else:
            st.info("Hali hech qanday to'xtatilgan o'yinlar tarixi saqlanmagan.")
