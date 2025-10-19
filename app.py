import streamlit as st
import requests
import pandas as pd

# -----------------------------
# ตั้งค่าหน้าเว็บ
# -----------------------------
st.set_page_config(page_title="Streamlit Assignment", layout="wide")
st.title("งาน Streamlit ของ Attapon")

# -----------------------------
# 1️⃣ ข้อมูลจาก MOPH OpenData (ตัวอย่าง CSV)
# -----------------------------
st.header("1. ข้อมูลจากกระทรวงสาธารณสุข (OpenData)")

moph_csv_url = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/03-01-2023.csv"

try:
    df_moph = pd.read_csv(moph_csv_url)
    st.write("ตัวอย่างข้อมูล COVID-19 ล่าสุดจากไฟล์ CSV ที่เข้าถึงได้:")
    st.dataframe(df_moph.head(10))
except Exception as e:
    st.error(f"เกิดข้อผิดพลาดในการโหลดข้อมูล: {e}")

# -----------------------------
# 2️⃣ แสดงอัตราแลกเปลี่ยนเงินตรา (ฟรี ไม่ต้อง API Key)
# -----------------------------
st.header("2. อัตราแลกเปลี่ยนเงินตรา (ฟรี ไม่ต้อง API Key)")

exchange_api_url = "https://api.exchangerate.host/latest?base=USD"

try:
    response = requests.get(exchange_api_url)
    response.raise_for_status()
    data = response.json()

    # ตรวจสอบว่า API สำเร็จ
    if data.get("success", False):
        rates = data.get("rates", {})
        if rates:
            df_rates = pd.DataFrame(list(rates.items()), columns=["Currency", "Rate"])
            st.write("อัตราแลกเปลี่ยน USD กับสกุลเงินอื่น (ฟรี ไม่ต้อง API Key):")
            st.dataframe(df_rates)
            
            # Dropdown เลือกสกุลเงิน
            selected_currency = st.selectbox("เลือกสกุลเงินที่ต้องการ:", df_rates["Currency"])
            st.write(f"1 USD = {rates[selected_currency]:,.2f} {selected_currency}")
        else:
            st.warning("ไม่พบข้อมูลอัตราแลกเปลี่ยน")
    else:
        st.error("API ไม่สามารถให้ข้อมูลได้")

except Exception as e:
    st.error(f"เกิดข้อผิดพลาดในการเรียก API: {e}")
