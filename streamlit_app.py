import streamlit as st
import datetime
import json
import os

RATE_REGULAR = 50000 
RATE_DISCOUNT = 40000
DATA_FILE = "billiard_history.json"
STATE_FILE = "tables_state.json"
BAR_FILE = "bar_stock.json"

st.set_page_config(page_title="Dubai Billiard Club", page_icon="🎱", layout="wide")

# --- CSS: DIZAYN (SIDEBAR OCHIQ HOLATDA) ---
st.markdown("""
<style>
/* Yuqoridagi va pastdagi ortiqcha Streamlit/GitHub tugmalarini yashirish */
#MainMenu {visibility: hidden;}
header {visibility: hidden;}
.stAppToolbar {display: none !important;}
[data-testid="stDecoration"] {display: none;}
footer {visibility: hidden;}
.viewerBadge_container__1QSob {display: none !important;}
#streamlit-statusBar {display: none !important;}

.stApp {
    background-image: linear-gradient(rgba(0, 0, 0, 0.35), rgba(0, 0, 0, 0.35)), 
                      url("https://images.unsplash.com/photo-1511193311914-0346f16efe90?q=80&w=1920");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}
[data-testid="stSidebar"] {
    background-color: rgba(18, 18, 18, 0.92) !important;
    border-right: 1px solid rgba(255, 255, 255, 0.1);
}
h1, h2, h3, h4, p, span, label {
    color: #ffffff !important;
}
[data-testid="stSidebar"] h1 {
    font-size: 30px !important;
    font-weight: 800 !important;
}
[data-testid="stSidebar"] p, [data-testid="stSidebar"] label {
    font-size: 20px !important;
    font-weight: bold !important;
}
[data-testid="stSidebar"] .stButton button {
    font-size: 13px !important;
    padding: 5px 10px !important;
    border-radius: 6px !important;
}
.stButton button { font-size: 17px !important; border-radius: 8px !important; }

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
        "1": {"start_time": None, "active": False, "rate": RATE_REGULAR, "is_vip": False, "last_stopped_time": None, "cart": []},
        "2": {"start_time": None, "active": False, "rate": RATE_REGULAR, "is_vip": False, "last_stopped_time": None, "cart": []},
        "3": {"start_time": None, "active": False, "rate": RATE_REGULAR, "is_vip": False, "last_stopped_time": None, "cart": []},
        "4": {"start_time": None, "active": False, "rate": RATE_REGULAR, "is_vip": False, "last_stopped_time": None, "cart": []},
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
                    if "cart" not in v:
                        v["cart"] = []
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
            "last_stopped_time": v["last_stopped_time"].isoformat() if v["last_stopped_time"] else None,
            "cart": v.get("cart", [])
        }
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(serializable_tables, f, ensure_ascii=False, indent=2)

def load_bar_stock():
    today_str = get_local_time().strftime("%Y-%m-%d")
    default_bar = {
        "Shisha cola": {
            "price": 5000, "unit": "dona", "sold": 0,
            "batches": [{"date": today_str, "qty": 48}]
        },
        "Shisha fanta": {
            "price": 5000, "unit": "dona", "sold": 0,
            "batches": [{"date": today_str, "qty": 24}]
        },
        "Coca cola 1.5l": {
            "price": 20000, "unit": "dona", "sold": 0,
            "batches": [{"date": today_str, "qty": 6}]
        },
        "Fanta 1.5l": {
            "price": 20000, "unit": "dona", "sold": 0,
            "batches": []
        },
        "Fanta 1l": {
            "price": 15000, "unit": "dona", "sold": 0,
            "batches": []
        },
        "Garella": {
            "price": 15000, "unit": "dona", "sold": 0,
            "batches": []
        },
        "Toshkent suv": {
            "price": 7000, "unit": "dona", "sold": 0,
            "batches": []
        },
        "Coca-Cola 1l": {
            "price": 15000, "unit": "dona", "sold": 0,
            "batches": []
        },
        "Parlament": {
            "price": 27000, "unit": "pachka", "sold": 0, "note": "dona 2000 som",
            "batches": [{"date": today_str, "qty": 2}]
        },
        "Winston caster": {
            "price": 27000, "unit": "pachka", "sold": 0, "note": "dona 2000 som",
            "batches": [{"date": today_str, "qty": 2}]
        }
    }
    if os.path.exists(BAR_FILE):
        try:
            with open(BAR_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                for k, v in data.items():
                    if "batches" not in v:
                        initial_val = v.get("initial", 0)
                        v["batches"] = [{"date": today_str, "qty": initial_val}]
                return data
        except:
            return default_bar
    return default_bar

def save_bar_stock(bar_data):
    with open(BAR_FILE, "w", encoding="utf-8") as f:
        json.dump(bar_data, f, ensure_ascii=False, indent=2)

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "tables" not in st.session_state:
    st.session_state.tables = load_tables_state()

if "last_receipt" not in st.session_state:
    st.session_state.last_receipt = None

if "bar_stock" not in st.session_state:
    st.session_state.bar_stock = load_bar_stock()

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
            
            bar_items_text = ""
            if rec['bar_items']:
                bar_items_text = " | Bar mahsulotlari: " + ", ".join([f"{item['name']} ({item['qty']} ta) - {item['total']:,} so'm" for item in rec['bar_items']])
            
            st.success(f"🧾 **OXIRGI TO'LOV CHEKI:** {t_num}-Stol | Vaqt: {rec['minutes']} daq ({rec['time_cost']:,} so'm){bar_items_text} | **JAMI: {rec['total_cost']:,} so'm**")
            
            now = get_local_time()
            time_since_start = (now - rec['start_time']).total_seconds() / 60
            can_cancel = time_since_start <= 6
            
            if can_cancel:
                col_btn1, col_btn2, col_btn3 = st.columns(3)
            else:
                col_btn1, col_btn2 = st.columns(2)
                col_btn3 = None
                
            with col_btn1:
                if st.button("Yopish", use_container_width=True):
                    history = load_history()
                    
                    bar_summary_str = "Yo'q"
                    if rec['bar_items']:
                        bar_summary_str = ", ".join([f"{i['name']} x{i['qty']}" for i in rec['bar_items']])

                    history.append({
                        "sana": get_local_time().strftime("%Y-%m-%d"),
                        "turi": "Stol va Bar",
                        "nomi": f"{t_num}-Stol yakuniy hisob",
                        "vaqt": rec['start_str'] + " - " + rec['end_str'],
                        "tafsilot": f"O'yin: {rec['minutes']} daq. Bar: {bar_summary_str}",
                        "summa": rec['total_cost']
                    })
                    save_history(history)
                    
                    table = st.session_state.tables[str(t_num)]
                    table['cart'] = []
                    save_tables_state(st.session_state.tables)
                    
                    st.session_state.last_receipt = None
                    st.rerun()
                    
            with col_btn2:
                if st.button("▶️ Davom ettirish", use_container_width=True):
                    table = st.session_state.tables[str(t_num)]
                    if table['last_stopped_time']:
                        paused_duration = now - table['last_stopped_time']
                        table['start_time'] = table['start_time'] + paused_duration
                    
                    table['active'] = True
                    table['last_stopped_time'] = None
                    save_tables_state(st.session_state.tables)
                    st.session_state.last_receipt = None
                    st.rerun()
                    
            if can_cancel and col_btn3:
                with col_btn3:
                    if st.button("❌ Rad qilish", use_container_width=True):
                        bar = load_bar_stock()
                        for b_item in rec['bar_items']:
                            if b_item['name'] in bar:
                                bar[b_item['name']]['sold'] -= b_item['qty']
                        save_bar_stock(bar)
                        st.session_state.bar_stock = bar
                        
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
                    time_cost = int((elapsed.total_seconds() / 3600) * table['rate'])
                    
                    bar_cart_total = sum(item['total'] for item in table.get('cart', []))
                    total_cost = time_cost + bar_cart_total
                    
                    rate_type_str = "⭐ Doimiy klient (40 ming)" if table['is_vip'] else "Standard (50 ming)"
                    
                    st.error("Holati: Band (" + str(minutes) + " daqiqa)")
                    st.write("**Tarif:** " + rate_type_str)
                    st.write("**Boshlangan vaqt:** " + table['start_time'].strftime('%H:%M'))
                    st.write(f"**O'yin summasi:** {time_cost:,} so'm")
                    
                    if table.get('cart'):
                        st.write("**Stoldagi mahsulotlar:**")
                        for cart_item in table['cart']:
                            st.write(f"- {cart_item['name']} ({cart_item['qty']} ta) = {cart_item['total']:,} so'm")
                        st.write(f"**Bar jami:** {bar_cart_total:,} so'm")
                    
                    st.markdown(f"### 💵 Jami to'lov: {total_cost:,} so'm")
                    
                    with st.expander("➕ Stolga bar mahsuloti qo'shish"):
                        bar = st.session_state.bar_stock
                        selected_prod = st.selectbox("Mahsulotni tanlang:", list(bar.keys()), key=f"sel_prod_{i}")
                        prod_qty = st.number_input("Soni:", min_value=1, value=1, key=f"prod_qty_{i}")
                        
                        if st.button("Stolga qo'shish", key=f"add_to_table_{i}"):
                            p_data = bar[selected_prod]
                            total_initial = sum(b['qty'] for b in p_data['batches'])
                            remaining = total_initial - p_data['sold']
                            
                            if prod_qty <= remaining:
                                p_data['sold'] += prod_qty
                                save_bar_stock(bar)
                                
                                item_total = prod_qty * p_data['price']
                                table['cart'].append({
                                    "name": selected_prod,
                                    "qty": prod_qty,
                                    "total": item_total
                                })
                                save_tables_state(st.session_state.tables)
                                st.success(f"{selected_prod} stolga qo'shildi!")
                                st.rerun()
                            else:
                                st.error(f"Omborda yetarli mahsulot yo'q! Qolgani: {remaining}")

                    if st.button("To'xtatish va hisoblash", key="stop_" + str(i)):
                        end_time = get_local_time()
                        
                        st.session_state.last_receipt = {
                            "table": i,
                            "minutes": minutes,
                            "time_cost": time_cost,
                            "bar_items": table.get('cart', []),
                            "total_cost": total_cost,
                            "start_str": table['start_time'].strftime('%H:%M'),
                            "end_str": end_time.strftime('%H:%M'),
                            "start_time": table['start_time']
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
                            table['cart'] = []
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
                            table['cart'] = []
                            st.session_state.last_receipt = None
                            save_tables_state(st.session_state.tables)
                            st.rerun()
                            
                st.write("---")

    # 2-BO'LIM: BAR VA SAQLASH
    elif page == "Bar va Saqlash":
        st.title("🥤 Bar va saqlash xonasi")
        st.write("Mahsulotlar savdosi, qolgan miqdori, narxlari va kelish partiyalari:")
        st.write("---")
        
        bar = st.session_state.bar_stock
        
        for item_name, data in bar.items():
            total_initial = sum(b['qty'] for b in data['batches'])
            remaining = total_initial - data['sold']
            
            st.subheader(f"📦 {item_name}")
            st.write(f"💰 Narxi: **{data['price']:,} so'm** ({data.get('note', data['unit'])})")
            st.write(f"✅ Qolgani: **{remaining} {data['unit']}** (Jami olib kelingan: {total_initial}, Sotilgan: {data['sold']})")
            
            with st.expander(f"📅 Kelish partiyalari tarixi ({item_name})"):
                if data['batches']:
                    for b in data['batches']:
                        st.write(f"- Kelgan sanasi: **{b['date']}** | Miqdori: **{b['qty']} {data['unit']}**")
                else:
                    st.write("Hali partiya qo'shilmagan (jami olib kelingan: 0)")
            
            col_s1, col_s2, col_s3 = st.columns([2, 1, 1])
            with col_s1:
                new_sold = st.number_input(f"Sotilgan sonini kiritish ({item_name})", min_value=0, max_value=max(total_initial, 0), value=data['sold'], key=f"sold_{item_name}")
            with col_s2:
                if st.button(f"Yangilash", key=f"btn_upd_{item_name}"):
                    diff = new_sold - data['sold']
                    if diff > 0:
                        sale_amount = diff * data['price']
                        now_str = get_local_time().strftime("%H:%M")
                        history = load_history()
                        history.append({
                            "sana": get_local_time().strftime("%Y-%m-%d"),
                            "turi": "Bar",
                            "nomi": f"Bar savdosi (alohida): {item_name}",
                            "vaqt": now_str,
                            "tafsilot": f"{diff} {data['unit']}",
                            "summa": sale_amount
                        })
                        save_history(history)
                    
                    data['sold'] = new_sold
                    save_bar_stock(bar)
                    st.success("Muvaffaqiyatli saqlandi va kassaga qo'shildi!")
                    st.rerun()
            with col_s3:
                add_qty = st.number_input(f"Qo'shish miqdori", min_value=1, value=1, key=f"add_qty_{item_name}")
                if st.button(f"➕ Yangi partiya qo'shish", key=f"btn_add_{item_name}"):
                    today_str = get_local_time().strftime("%Y-%m-%d")
                    data['batches'].append({"date": today_str, "qty": add_qty})
                    save_bar_stock(bar)
                    st.success(f"Yangi partiya ({add_qty} ta) qo'shildi!")
                    st.rerun()
            st.write("---")

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
            st.subheader(f"📋 {selected_date} sanasidagi barcha kirimlar tarixi:")
            
            for item in reversed(day_records):
                if item.get("turi") == "Bar":
                    st.write(f"🥤 **{item['nomi']}** | Soni: {item['tafsilot']} | Vaqti: {item['vaqt']} | **To'lov: {item['summa']:,} so'm**")
                else:
                    st.write(f"🎱 **{item['nomi']}** | Vaqti: {item['vaqt']} | Tafsilot: {item['tafsilot']} | **Jami to'lov: {item['summa']:,} so'm**")
        else:
            st.info("Hali hech qanday to'lovlar tarixi saqlanmagan.")
