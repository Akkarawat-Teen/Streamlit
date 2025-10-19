import streamlit as st
import requests
import pandas as pd

# -----------------------------
# ตั้งค่าหน้าเว็บ
# -----------------------------
st.set_page_config(page_title="Streamlit Assignment", layout="wide")
st.title("งาน Streamlit ของ Attapon")

# -----------------------------
# 1️⃣ ข้อมูลจาก MOPH OpenData
# -----------------------------
st.header("1. ข้อมูลจากกระทรวงสาธารณสุข (OpenData)")

# ตัวอย่าง resource_id ของ MOPH (เปลี่ยนเป็น dataset ที่คุณต้องการ)
RESOURCE_ID = "9c76c1a2-f4c0-44a6-9d90-0a87935e484e"  # ตัวอย่าง: ข้อมูลผู้ป่วย COVID-19 รายวัน

moph_api_url = f"https://data.moph.go.th/api/datastore_search?resource_id={RESOURCE_ID}&limit=10"

try:
    response = requests.get(moph_api_url)
    response.raise_for_status()
    data = response.json()
    
    if "result" in data and "records" in data["result"]:
        df_moph = pd.DataFrame(data["result"]["records"])
        st.write("ตัวอย่างข้อมูล 10 รายการล่าสุด:")
        st.dataframe(df_moph)
    else:
        st.warning("ไม่พบข้อมูลใน API")
except Exception as e:
    st.error(f"เกิดข้อผิดพลาดในการเรียก API: {e}")

# -----------------------------
# 2️⃣ แสดงอัตราแลกเปลี่ยนเงินตรา (API Key required)
# -----------------------------
st.header("2. อัตราแลกเปลี่ยนเงินตรา")

# ใส่ API Key ของคุณ
api_key = st.text_input("กรุณาใส่ API Key ของ ExchangeRate-API:", type="password")

if api_key:
    exchange_api_url = f"https://v6.exchangerate-api.com/v6/{api_key}/latest/USD"

    try:
        response = requests.get(exchange_api_url)
        response.raise_for_status()
        data = response.json()

        if data["result"] == "success":
            rates = data["conversion_rates"]
            df_rates = pd.DataFrame(list(rates.items()), columns=["Currency", "Rate"])
            
            st.write("อัตราแลกเปลี่ยน USD กับสกุลเงินอื่น:")
            st.dataframe(df_rates)
            
            # Dropdown เลือกสกุลเงิน
            selected_currency = st.selectbox("เลือกสกุลเงินที่ต้องการ:", df_rates["Currency"])
            st.write(f"1 USD = {rates[selected_currency]} {selected_currency}")
        else:
            st.warning("ไม่สามารถเรียกอัตราแลกเปลี่ยนได้")
    except Exception as e:
        st.error(f"เกิดข้อผิดพลาดในการเรียก API: {e}")
else:
    st.info("กรุณาใส่ API Key เพื่อดูอัตราแลกเปลี่ยน")
