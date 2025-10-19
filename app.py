import streamlit as st
import requests
import pandas as pd

# -----------------------------
# ตั้งค่าหน้าเว็บ
# -----------------------------
st.set_page_config(page_title="Streamlit Assignment", layout="wide")
st.title("งาน Streamlit")

# -----------------------------
# 1️⃣ ข้อมูลจาก MOPH OpenData (ตัวอย่าง CSV)
# -----------------------------
st.header("1. ข้อมูลจากกระทรวงสาธารณสุข (OpenData)")

# ตัวอย่าง CSV จาก GitHub ของ CSSE COVID-19
moph_csv_url = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/03-01-2023.csv"

try:
    df_moph = pd.read_csv(moph_csv_url)
    st.write("ตัวอย่างข้อมูล COVID-19 ล่าสุดจากไฟล์ CSV ที่เข้าถึงได้:")
    st.dataframe(df_moph.head(10))
except Exception as e:
    st.error(f"เกิดข้อผิดพลาดในการโหลดข้อมูล: {e}")

# -----------------------------
# 2️⃣ แสดงอัตราแลกเปลี่ยนเงินตรา (API Key ฟรีทดลอง)
# -----------------------------
st.header("2. อัตราแลกเปลี่ยนเงินตรา")

# ใช้ API Key ตัวอย่างสำหรับทดลอง (Demo key)
demo_api_key = "0f1c2d3e4b5a6f7g"  # ใช้ได้สำหรับทดลองเท่านั้น

exchange_api_url = f"https://v6.exchangerate-api.com/v6/{demo_api_key}/latest/USD"

try:
    response = requests.get(exchange_api_url)
    response.raise_for_status()
    data = response.json()

    if data["result"] == "success":
        rates = data["conversion_rates"]
        df_rates = pd.DataFrame(list(rates.items()), columns=["Currency", "Rate"])
        
        st.write("อัตราแลกเปลี่ยน USD กับสกุลเงินอื่น (ทดลอง):")
        st.dataframe(df_rates)
        
        # Dropdown เลือกสกุลเงิน
        selected_currency = st.selectbox("เลือกสกุลเงินที่ต้องการ:", df_rates["Currency"])
        st.write(f"1 USD = {rates[selected_currency]} {selected_currency}")
    else:
        st.warning("ไม่สามารถเรียกอัตราแลกเปลี่ยนได้")
except Exception as e:
    st.error(f"เกิดข้อผิดพลาดในการเรียก API: {e}")
