import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="معمل أسلوب الأناقة", page_icon="✂️", layout="wide")

st.markdown("<h1 style='text-align: center; color: #1e293b;'>معمل أسلوب الأناقة - نظام الإدارة الشامل</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #64748b;'>لوحة التحكم السحابية المتقدمة لإنتاج الخياطين ومعمل الزرار</p>", unsafe_allow_html=True)
st.divider()

# تهيئة قاعدة البيانات في الـ Session State
if 'data' not in st.session_state:
    st.session_state.data = pd.DataFrame(columns=['التاريخ', 'اسم الخياط', 'عدد القطع', 'سعر القطعة', 'الإجمالي'])

if 'withdrawals' not in st.session_state:
    st.session_state.withdrawals = pd.DataFrame(columns=['التاريخ', 'اسم الخياط', 'المبلغ', 'نوع السحبية'])

tailors_list = ["عبد الله", "إدريس", "رام", "سبدول", "نارش", "سجاد", "إرشاد", "بدرول"]

# القائمة الجانبية لإدخال البيانات
st.sidebar.header("📝 لوحة الإدخال والتحكم")
menu_choice = st.sidebar.selectbox("اختر القسم", ["تسجيل إنتاج يومي", "تسجيل سحبية / سلفة"])

if menu_choice == "تسجيل إنتاج يومي":
    with st.sidebar.form("entry_form"):
        entry_date = st.date_input("التاريخ", datetime.today())
        tailor_name = st.selectbox("اختر اسم الخياط", tailors_list)
        pieces_count = st.number_input("عدد القطع", min_value=1, value=1)
        piece_price = st.number_input("سعر القطعة (ر.ي)", min_value=0.0, value=15.0)
        
        submit_button = st.form_submit_button(label="حفظ الإنتاج")

        if submit_button:
            total_amount = pieces_count * piece_price
            new_row = pd.DataFrame({
                'التاريخ': [str(entry_date)],
                'اسم الخياط': [tailor_name],
                'عدد القطع': [int(pieces_count)],
                'سعر القطعة': [float(piece_price)],
                'الإجمالي': [float(total_amount)]
            })
            st.session_state.data = pd.concat([st.session_state.data, new_row], ignore_index=True)
            st.sidebar.success("تم حفظ الإنتاج بنجاح!")

elif menu_choice == "تسجيل سحبية / سلفة":
    with st.sidebar.form("withdrawal_form"):
        w_date = st.date_input("تاريخ السحبية", datetime.today())
        w_tailor = st.selectbox("اسم الخياط", tailors_list, key="w_tailor")
        w_amount = st.number_input("مبلغ السحبية (ر.ي)", min_value=0.0, value=100.0)
        w_type = st.text_input("نوع السحبية (مثال: مصروف أسبوعي، سلفة)", value="مصروف أسبوعي")
        
        w_submit = st.form_submit_button(label="حفظ السحبية")

        if w_submit:
            new_w = pd.DataFrame({
                'التاريخ': [str(w_date)],
                'اسم الخياط': [w_tailor],
                'المبلغ': [float(w_amount)],
                'نوع السحبية': [w_type]
            })
            st.session_state.withdrawals = pd.concat([st.session_state.withdrawals, new_w], ignore_index=True)
            st.sidebar.success("تم تسجيل السحبية بنجاح!")

# التبويبات الرئيسية في الواجهة
tab1, tab2, tab3, tab4 = st.tabs(["📊 ملخص الخياطين", "🔘 حسابات معمل الزرار", "💸 السحبياّت والعهد", "📋 سجلات الإنتاج الكاملة"])

with tab1:
    st.subheader("📁 ملخص الإنتاج والمستحقات لكل خياط")
    
    # أزرار تنقل أفقية بالترتيب بين الخياطين
    st.markdown("**اختر الخياط لعرض تقريره الشهري:**")
    selected_tailor = st.radio("الخياطون", tailors_list, horizontal=True, label_visibility="collapsed")
    
    if not st.session_state.data.empty:
        tailor_df = st.session_state.data[st.session_state.data['اسم الخياط'] == selected_tailor]
        
        if not tailor_df.empty:
            # تجميع الشغل يومياً للخياط المختار
            daily_summary = tailor_df.groupby('التاريخ').agg({
                'عدد القطع': 'sum',
                'سعر القطعة': 'mean',
                'الإجمالي': 'sum'
            }).reset_index()
            
            st.markdown(f"### تقرير الخياط: <span style='color: #2563eb;'>{selected_tailor}</span>", unsafe_allow_html=True)
            st.dataframe(daily_summary, use_container_width=True)
            
            total_p = tailor_df['عدد القطع'].sum()
            total_m = tailor_df['الإجمالي'].sum()
            
            # حساب السحبياّت الخاصة بهذا الخياط
            tailor_w = 0.0
            if not st.session_state.withdrawals.empty:
                w_filtered = st.session_state.withdrawals[st.session_state.withdrawals['اسم الخياط'] == selected_tailor]
                tailor_w = w_filtered['المبلغ'].sum()
            
            net_balance = total_m - tailor_w
            
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("إجمالي القطع (الشهر)", int(total_p))
            col2.metric("إجمالي المستحقات", f"{total_m:,.2f} ر.ي")
            col3.metric("إجمالي السحبياّت", f"{tailor_w:,.2f} ر.ي")
            col4.metric("الصافي المستحق", f"{net_balance:,.2f} ر.ي")
        else:
            st.info(f"لا توجد سجلات مسجلة حتى الآن للخياط: {selected_tailor}")
    else:
        st.info("لا توجد بيانات إنتاج مسجلة في النظام بعد.")

with tab2:
    st.subheader("🔘 تقرير معمل الزرار الشامل")
    if not st.session_state.data.empty:
        # إجمالي شغل الخياطين كامل في اليوم الواحد
        daily_button_summary = st.session_state.data.groupby('التاريخ').agg({
            'عدد القطع': 'sum',
            'الإجمالي': 'sum'
        }).reset_index()
        daily_button_summary.columns = ['التاريخ', 'إجمالي القطع (اليومي)', 'إجمالي الرصيد (اليومي)']
        
        st.markdown("#### إجمالي شغل الخياطين اليومي")
        st.dataframe(daily_button_summary, use_container_width=True)
        
        total_all_pieces = st.session_state.data['عدد القطع'].sum()
        total_all_money = st.session_state.data['الإجمالي'].sum()
        avg_price = st.session_state.data['سعر القطعة'].mean()
        
        col_b1, col_b2, col_b3 = st.columns(3)
        col_b1.metric("إجمالي قطع الشهر (كامل الخياطين)", int(total_all_pieces))
        col_b2.metric("متوسط سعر القطعة", f"{avg_price:,.2f} ر.ي")
        col_b3.metric("إجمالي رصيد العمل الكامل", f"{total_all_money:,.2f} ر.ي")
    else:
        st.info("لا توجد بيانات متاحة لعرض تقرير المعمل حالياً.")

with tab3:
    st.subheader("💸 أرشيف السحبياّت والعهد المالية")
    if not st.session_state.withdrawals.empty:
        st.dataframe(st.session_state.withdrawals, use_container_width=True)
        total_w_all = st.session_state.withdrawals['المبلغ'].sum()
        st.metric("إجمالي السحبياّت لكافة الخياطين", f"{total_w_all:,.2f} ر.ي")
        
        if st.button("مسح كافة السحبياّت"):
            st.session_state.withdrawals = pd.DataFrame(columns=['التاريخ', 'اسم الخياط', 'المبلغ', 'نوع السحبية'])
            st.rerun()
    else:
        st.info("لم يتم تسجيل أي سحبياّت أو سلف حتى الآن.")

with tab4:
    st.subheader("📋 سجلات الإنتاج الخام الكاملة")
    if not st.session_state.data.empty:
        st.dataframe(st.session_state.data, use_container_width=True)
        if st.button("مسح كافة بيانات الإنتاج"):
            st.session_state.data = pd.DataFrame(columns=['التاريخ', 'اسم الخياط', 'عدد القطع', 'سعر القطعة', 'الإجمالي'])
            st.rerun()
    else:
        st.info("لا توجد سجلات مسجلة.")
