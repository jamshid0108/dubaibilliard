import streamlit as st
import datetime
import json
import os
import urllib.request
import urllib.parse

RATE_REGULAR = 50000 
RATE_DISCOUNT = 40000
DATA_FILE = "billiard_history.json"

# Telegram Bot sozlamalari
TELEGRAM_BOT_TOKEN = "8853432484:AAHbAuheVuePQ56kvhed17iG4WZBLPFMm6A"
TELEGRAM_CHAT_ID = "1125780094"

st.set_page_config(page_title="Dubai Billiard Club", page_icon="🎱", layout="wide")

# Shriftlarni kattalashtirish uchun CSS uslubi
st.markdown("""
    <style>
    .stRadio label {
        font-size: 20px !important;
        font-weight: bold !important;
    }
    .stButton button {
        font-size: 18px !important;
        border-radius: 8px !important;
    }
    p, span {
        font-size: 18px !important;
    }
    </style>
""", unsafe_allow_html=True)

def get_local_time():
    return datetime.datetime.utcnow() + datetime.timedelta(hours=5)

def send_telegram_message(message):
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        data = urllib.parse.urlencode({"chat_id": TELEGRAM_CHAT_ID, "text": message, "parse_mode": "Markdown"}).encode("utf-8")
        req = urllib.request.Request(url, data=data)
        urllib.request.urlopen(req, timeout=5)
    except Exception as e:
        print("Telegram xatolik:", e)

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

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "tables" not in st.session_state:
    st.session_state.tables = {
        1: {"start_time": None, "active": False, "rate": RATE_REGULAR, "is_vip": False},
        2: {"start_time": None, "active": False, "rate": RATE_REGULAR, "is_vip": False},
        3: {"start_time": None, "active": False, "rate": RATE_REGULAR, "is_vip": False},
        4: {"start_time": None, "active": False, "rate": RATE_REGULAR, "is_vip": False},
    }

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
    
    for _ in range(10):
        st.sidebar.write("")
        
    if st.sidebar.button("🚪 Tizimdan chiqish", type="secondary"):
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
                        end_time = get_local_time()
                        start_str = table['start_time'].strftime('%H:%M')
                        end_str = end_time.strftime('%H:%M')
                        
                        history = load_history()
                        history.append({
                            "sana": end_time.strftime("%Y-%m-%d"),
                            "stol": i,
                            "vaqt": start_str + " - " + end_str,
                            "daqiqa": minutes,
                            "summa": cost
                        })
                        save_history(history)
                        
                        # Telegramga chek yuborish
                        tg_msg = f"🧾 *Dubai Billiard Chek*\n\n🎱 *Stol:* {i}-Stol\n⏱ *Vaqt:* {start_str} - {end_str} ({minutes} daq)\n💰 *Toʻlov:* {cost:,} soʻm"
                        send_telegram_message(tg_msg)
                        
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
