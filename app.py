import pandas as pd
import streamlit as st

# إعدادات الصفحة
st.set_page_config(
    page_title="نظام إدارة معمل أسلوب الأناقة", page_icon="✂️", layout="wide"
)

# عنوان النظام
st.title("✂️ النظام الشامل لإدارة معمل أسلوب الأناقة")
st.markdown("إدارة إنتاج الخياطين، معمل الزرار، والملخصات المالية (2026-2028)")

# محاولة قراءة ملف الإكسيل الموجود في المستودع
excel_file = "النظام الإدارة الشامل للمعمل أسلوب الأناقة_تنسيق_كامل.xlsx"

try:
  xls = pd.ExcelFile(excel_file)
  sheet_names = xls.sheet_names

  # الشريط الجانبي للتنقل بين الأقسام
  st.sidebar.header("قائمة التنقل")
  choice = st.sidebar.selectbox(
      "اختر القسم:", ["الرئيسية والملخص السنوي", "الجداول الشهرية للإنتاج"]
  )

  if choice == "الرئيسية والملخص السنوي":
    st.subheader("📊 الملخص السنوي الشامل")
    df_summary = pd.read_excel(excel_file, sheet_name="الملخص السنوي الشامل")
    st.dataframe(df_summary, use_container_width=True)

  elif choice == "الجداول الشهرية للإنتاج":
    st.subheader("📅 متابعة الإنتاج اليومي والشهرى")
    # استبعاد ورقة الملخص وعرض الأشهر فقط
    months_sheets = [s for s in sheet_names if s != "الملخص السنوي الشامل"]
    selected_month = st.sidebar.selectbox("اختر الشهر:", months_sheets)

    df_month = pd.read_excel(excel_file, sheet_name=selected_month)
    st.markdown(f"### تفاصيل جدول: {selected_month}")
    st.dataframe(df_month, use_container_width=True)

except Exception as e:
  st.error(
      f"عذراً، لم يتم العثور على ملف الإكسيل في المستودع أو حدث خطأ في القراءة:"
      f" {e}"
  )
  st.info(
      "يرجى التأكد من رفع ملف الإكسيل الأصلي إلى المستودع بنفس الاسم تماماً."
  )

