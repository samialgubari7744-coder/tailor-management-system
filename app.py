import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="معمل أسلوب الأناقة", page_icon="✂️", layout="wide")

st.markdown("<h1 style='text-align: center; color: #1e293b;'>معمل أسلوب الأناقة - نظام الإدارة الشامل</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #64748b;'>لوحة التحكم السحابية لإدارة إنتاج الخياطين ومعمل الزرار</p>", unsafe_allow_html=True)
st.divider()

if 'data' not in st.session_state:
    st.session_state.data = pd.DataFrame(columns=['التاريخ', 'اسم الخياط', 'عدد القطع'])

st.sidebar.header("📝 تسجيل إنتاج يومي")
with st.sidebar.form("entry_form"):
    entry_date = st.date_input("التاريخ", datetime.today())
    tailor_name = st.selectbox("اختر اسم الخياط", [
        "عبد الله", "إدريس", "رام", "سبدول", 
        "نارش", "سجاد", "إرشاد", "بدرول"
    ])
    pieces_count = st.number_input("عدد القطع", min_value=1, value=1)
    
    submit_button = st.form_submit_button(label="حفظ السجل")

    if submit_button:
        new_row = pd.DataFrame({
            'التاريخ': [str(entry_date)],
            'اسم الخياط': [tailor_name],
            'عدد القطع': [int(pieces_count)]
        })
        st.session_state.data = pd.concat([st.session_state.data, new_row], ignore_index=True)
        st.sidebar.success("تم الحفظ بنجاح!")

if not st.session_state.data.empty:
    total_pieces = int(st.session_state.data['عدد القطع'].sum())
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="إجمالي القطع المسجلة", value=total_pieces)
    with col2:
        st.metric(label="حساب معمل الزرار التقديري", value=f"{total_pieces * 5} ر.ي")
    with col3:
        st.metric(label="مستحقات الخياطين الإجمالية", value=f"{total_pieces * 15} ر.ي")
    
    st.divider()
    st.subheader("📊 أرشيفات الإنتاج اليومي")
    st.dataframe(st.session_state.data, use_container_width=True)
    
    if st.button("مسح كافة البيانات"):
        st.session_state.data = pd.DataFrame(columns=['التاريخ', 'اسم الخياط', 'عدد القطع'])
        st.rerun()
else:
    st.info("لا توجد سجلات مسجلة حتى الآن. استخدم القائمة الجانبية لإضافة أول سجل إنتاج.")
