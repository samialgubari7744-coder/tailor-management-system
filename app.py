import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="معمل أسلوب الأناقة", page_icon="✂️", layout="wide")

# تخصيص التصميم والإنفوجرافيك واتجاه الكتابة من اليمين لليسار (RTL)
st.markdown("""
    <style>
    /* تطبيق الاتجاه من اليمين إلى اليسار على كافة عناصر النظام */
    html, body, [class*="css"] {
        direction: rtl;
        text-align: right;
    }
    
    /* تخصيص القائمة الجانبية والنصوص فيها */
    .sidebar .sidebar-content {
        direction: rtl;
        text-align: right;
    }

    .infographic-card {
        background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
        border: 1px solid #e2e8f0;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        text-align: center;
        margin-bottom: 15px;
    }
    .infographic-card h3 {
        color: #334155;
        font-size: 16px;
        margin-bottom: 5px;
    }
    .infographic-card h2 {
        color: #0f172a;
        font-size: 26px;
        font-weight: bold;
    }
    .main-title {
        text-align: center;
        color: #1e293b;
        font-weight: 800;
        padding-bottom: 0px;
    }
    .sub-title {
        text-align: center;
        color: #64748b;
        font-size: 15px;
        margin-bottom: 25px;
    }
    
    /* محاذاة الجداول لتكون متوافقة مع اليمين */
    dataframe, table {
        text-align: right !important;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1 class='main-title'>✂️ معمل أسلوب الأناقة</h1>", unsafe_allow_html=True)
st.markdown("<p class='sub-title'>نظام الإدارة والإنتاج الذكي بتصميم الإنفوجرافيك المتقدم</p>", unsafe_allow_html=True)
st.divider()

# تهيئة قاعدة البيانات في الـ Session State
if 'data' not in st.session_state:
    st.session_state.data = pd.DataFrame(columns=['التاريخ', 'اسم الخياط', 'عدد القطع', 'سعر القطعة', 'الإجمالي'])

if 'withdrawals' not in st.session_state:
    st.session_state.withdrawals = pd.DataFrame(columns=['التاريخ', 'اسم الخياط', 'المبلغ', 'نوع السحبية'])

tailors_list = ["عبد الله", "إدريس", "رام", "سبدول", "نارش", "سجاد", "إرشاد", "بدرول"]

# القائمة الجانبية للإدخال
st.sidebar.header("📝 لوحة الإدخال والتحكم")
menu_choice = st.sidebar.selectbox("اختر القسم", ["تسجيل إنتاج يومي", "تسجيل سحبية / سلفة"])

if menu_choice == "تسجيل إنتاج يومي":
    with st.sidebar.form("entry_form"):
        entry_date = st.date_input("📅 التاريخ", datetime.today())
        tailor_name = st.selectbox("🧵 اسم الخياط", tailors_list)
        pieces_count = st.number_input("📦 عدد القطع", min_value=1, value=1)
        piece_price = st.number_input("💰 سعر القطعة (ر.ي)", min_value=0.0, value=15.0)
        
        submit_button = st.form_submit_button(label="حفظ الإنتاج 🚀")

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
            st.sidebar.success("✅ تم حفظ الإنتاج بنجاح!")

elif menu_choice == "تسجيل سحبية / سلفة":
    with st.sidebar.form("withdrawal_form"):
        w_date = st.date_input("📅 تاريخ السحبية", datetime.today())
        w_tailor = st.selectbox("🧵 اسم الخياط", tailors_list, key="w_tailor")
        w_amount = st.number_input("💵 مبلغ السحبية (ر.ي)", min_value=0.0, value=100.0)
        w_type = st.text_input("🏷️ نوع السحبية", value="مصروف أسبوعي")
        
        w_submit = st.form_submit_button(label="حفظ السحبية 🚀")

        if w_submit:
            new_w = pd.DataFrame({
                'التاريخ': [str(w_date)],
                'اسم الخياط': [w_tailor],
                'المبلغ': [float(w_amount)],
                'نوع السحبية': [w_type]
            })
            st.session_state.withdrawals = pd.concat([st.session_state.withdrawals, new_w], ignore_index=True)
            st.sidebar.success("✅ تم تسجيل السحبية بنجاح!")

# التبويبات الرئيسية
tab1, tab2, tab3, tab4 = st.tabs(["📊 ملخص الخياطين", "🔘 حسابات معمل الزرار", "💸 السحبياّت والعهد", "📋 سجلات الإنتاج الكاملة"])

with tab1:
    st.subheader("📁 ملخص الإنتاج الشهري لكل خياط")
    
    st.markdown("**اختر الخياط للتنقل السريع:**")
    selected_tailor = st.radio("الخياطون", tailors_list, horizontal=True, label_visibility="collapsed")
    
    if not st.session_state.data.empty:
        tailor_df = st.session_state.data[st.session_state.data['اسم الخياط'] == selected_tailor]
        
        if not tailor_df.empty:
            daily_summary = tailor_df.groupby('التاريخ').agg({
                'عدد القطع': 'sum',
                'سعر القطعة': 'mean',
                'الإجمالي': 'sum'
            }).reset_index()
            
            st.markdown(f"### 👤 تقرير الخياط: <span style='color: #2563eb;'>{selected_tailor}</span>", unsafe_allow_html=True)
            st.dataframe(daily_summary, use_container_width=True)
            
            total_p = tailor_df['عدد القطع'].sum()
            total_m = tailor_df['الإجمالي'].sum()
            
            tailor_w = 0.0
            if not st.session_state.withdrawals.empty:
                w_filtered = st.session_state.withdrawals[st.session_state.withdrawals['اسم الخياط'] == selected_tailor]
                tailor_w = w_filtered['المبلغ'].sum()
            
            net_balance = total_m - tailor_w
            
            # عرض المؤشرات بتصميم إنفوجرافيك جذاب
            c1, c2, c3, c4 = st.columns(4)
            with c1:
                st.markdown(f"<div class='infographic-card'><h3>📦 إجمالي قطع الشهر</h3><h2>{int(total_p)}</h2></div>", unsafe_allow_html=True)
            with c2:
                st.markdown(f"<div class='infographic-card'><h3>💰 إجمالي المستحقات</h3><h2>{total_m:,.2f}</h2></div>", unsafe_allow_html=True)
            with c3:
                st.markdown(f"<div class='infographic-card'><h3>💸 إجمالي السحبياّت</h3><h2>{tailor_w:,.2f}</h2></div>", unsafe_allow_html=True)
            with c4:
                st.markdown(f"<div class='infographic-card'><h3>💎 الصافي المستحق</h3><h2>{net_balance:,.2f}</h2></div>", unsafe_allow_html=True)
        else:
            st.info(f"لا توجد سجلات مسجلة حتى الآن للخياط: {selected_tailor}")
    else:
        st.info("لا توجد بيانات إنتاج مسجلة في النظام بعد.")

with tab2:
    st.subheader("🔘 تقرير معمل الزرار الشامل")
    if not st.session_state.data.empty:
        daily_button_summary = st.session_state.data.groupby('التاريخ').agg({
            'عدد القطع': 'sum',
            'الإجمالي': 'sum'
        }).reset_index()
        daily_button_summary.columns = ['التاريخ', 'إجمالي القطع (اليومي)', 'إجمالي الرصيد (اليومي)']
        
        st.markdown("#### 📅 إجمالي شغل الخياطين اليومي للمعمل")
        st.dataframe(daily_button_summary, use_container_width=True)
        
        total_all_pieces = st.session_state.data['عدد القطع'].sum()
        total_all_money = st.session_state.data['الإجمالي'].sum()
        avg_price = st.session_state.data['سعر القطعة'].mean()
        
        b1, b2, b3 = st.columns(3)
        with b1:
            st.markdown(f"<div class='infographic-card'><h3>🏢 إجمالي قطع الشهر (للكل)</h3><h2>{int(total_all_pieces)}</h2></div>", unsafe_allow_html=True)
        with b2:
            st.markdown(f"<div class='infographic-card'><h3>📈 متوسط سعر القطعة</h3><h2>{avg_price:,.2f} ر.ي</h2></div>", unsafe_allow_html=True)
        with b3:
            st.markdown(f"<div class='infographic-card'><h3>💎 إجمالي رصيد المعمل</h3><h2>{total_all_money:,.2f} ر.ي</h2></div>", unsafe_allow_html=True)
    else:
        st.info("لا توجد بيانات متاحة لعرض تقرير المعمل حالياً.")

with tab3:
    st.subheader("💸 أرشيف السحبياّت والعهد المالية")
    if not st.session_state.withdrawals.empty:
        st.dataframe(st.session_state.withdrawals, use_container_width=True)
        total_w_all = st.session_state.withdrawals['المبلغ'].sum()
        st.markdown(f"<div class='infographic-card' style='max-width: 400px; margin: auto;'><h3>إجمالي السحبياّت لكافة الخياطين</h3><h2>{total_w_all:,.2f} ر.ي</h2></div>", unsafe_allow_html=True)
        
        if st.button("🗑️ مسح كافة السحبياّت"):
            st.session_state.withdrawals = pd.DataFrame(columns=['التاريخ', 'اسم الخياط', 'المبلغ', 'نوع السحبية'])
            st.rerun()
    else:
        st.info("لم يتم تسجيل أي سحبياّت أو سلف حتى الآن.")

with tab4:
    st.subheader("📋 سجلات الإنتاج الخام الكاملة")
    if not st.session_state.data.empty:
        st.dataframe(st.session_state.data, use_container_width=True)
        if st.button("🗑️ مسح كافة بيانات الإنتاج"):
            st.session_state.data = pd.DataFrame(columns=['التاريخ', 'اسم الخياط', 'عدد القطع', 'سعر القطعة', 'الإجمالي'])
            st.rerun()
    else:
        st.info("لا توجد سجلات مسجلة.")
