import streamlit as st
import requests
import pandas as pd

# ตั้งค่าหน้าเว็บ
st.set_page_config(page_title="Streamlit Assignment", layout="wide")
st.title("งาน Streamlit ของ Attapon")

# -----------------------------
# 1️⃣ ข้อมูลจาก MOPH OpenData
# -----------------------------
st.header("1. ข้อมูลจากกระทรวงสาธารณสุข (OpenData)")

# ตัวอย่าง API ของ MOPH (JSON)
moph_api_url = "https://data.moph.go.th/api/datastore_search?resource_id=YOUR_RESOURCE_ID&limit=10"

try:
    response = requests.get(moph_api_url)
    response.raise_for_status()
    data = response.json()
    
    # ตรวจสอบ structure ของข้อมูล
    if "result" in data and "records" in data["result"]:
        df_moph = pd.DataFrame(data["result"]["records"])
        st.write("ตัวอย่างข้อมูล 10 รายการล่าสุด:")
        st.dataframe(df_moph)
    else:
        st.warning("ไม่พบข้อมูลใน API")
except Exception as e:
    st.error(f"เกิดข้อผิดพลาดในการเรียก API: {e}")

# -----------------------------
# 2️⃣ แสดงอัตราแลกเปลี่ยนเงินตรา
# -----------------------------
st.header("2. อัตราแลกเปลี่ยนเงินตรา")

exchange_api_url = "https://open.er-api.com/v6/latest/USD"  # ตัวอย่าง USD เป็นฐาน

try:
    response = requests.get(exchange_api_url)
    response.raise_for_status()
    data = response.json()
    
    if data["result"] == "success":
        rates = data["rates"]
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
