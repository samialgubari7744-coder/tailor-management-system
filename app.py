import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="نظام إدارة معمل أسلوب الأناقة", page_icon="✂️", layout="wide"
)

st.title("✂️ نظام إدارة معمل أسلوب الأناقة")
st.markdown("مرحباً بك في لوحة تحكم المعمل السحابية")

# اسم ملف الإكسيل المفترض في المستودع
excel_file = "النظام الإدارة الشامل للمعمل أسلوب الأناقة_تنسيق_كامل.xlsx"

try:
  xls = pd.ExcelFile(excel_file)
  sheet_names = xls.sheet_names

  st.sidebar.header("قائمة التنقل")
  selected_sheet = st.sidebar.selectbox("اختر القسم أو الشهر:", sheet_names)

  st.subheader(f"عرض بيانات: {selected_sheet}")
  df = pd.read_excel(excel_file, sheet_name=selected_sheet)
  st.dataframe(df, use_container_width=True)

except Exception as e:
  st.error(f"حدث خطأ أثناء قراءة ملف الإكسيل: {e}")
  st.info(
      "تأكد من أن ملف الإكسيل مرفوع في المستودع وأن اسمه مطابق تماماً لما تم"
      " كتابته."
  )
