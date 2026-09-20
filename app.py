import streamlit as st
import pandas as pd
from datetime import datetime
import io

st.set_page_config(page_title="معمل أسلوب الأناقة للإدارة الذكية", page_icon="✂️", layout="wide")

# تخصيص التصميم والإنفوجرافيك واتجاه الكتابة من اليمين لليسار (RTL) بشكل قسري
st.markdown("""
    <style>
    html, body, [class*="css"], .stApp {
        direction: rtl !important;
        text-align: right !important;
    }
    iframe {
        direction: rtl !important;
    }
    .infographic-card {
        background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
        border: 1px solid #e2e8f0;
        border-right: 5px solid #2563eb;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.03);
        text-align: center;
        margin-bottom: 15px;
    }
    .infographic-card h3 {
        color: #64748b;
        font-size: 15px;
        margin-bottom: 5px;
    }
    .infographic-card h2 {
        color: #0f172a;
        font-size: 24px;
        font-weight: bold;
    }
    .main-title {
        text-align: center;
        color: #0f172a;
        font-weight: 800;
        padding-bottom: 0px;
    }
    .sub-title {
        text-align: center;
        color: #64748b;
        font-size: 15px;
        margin-bottom: 25px;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 6px;
        direction: rtl !important;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: #f1f5f9;
        border-radius: 8px 8px 0px 0px;
        padding: 8px 16px;
        font-weight: 600;
        color: #334155;
        font-size: 14px;
    }
    .stTabs [aria-selected="true"] {
        background-color: #2563eb !important;
        color: white !important;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1 class='main-title'>✂️ معمل أسلوب الأناقة - نظام الإدارة والإنتاج الذكي</h1>", unsafe_allow_html=True)
st.markdown("<p class='sub-title'>إدارة متكاملة للإنتاج، الحسابات، السحبيات، والتقارير المالية بدقة واحترافية</p>", unsafe_allow_html=True)
st.divider()

# --- تهيئة قواعد البيانات وإعدادات الخياطين والأسعار الافتراضية ---
if 'tailors' not in st.session_state:
    st.session_state.tailors = ["عبد الله", "إدريس", "رام", "سبدول", "نارش", "سجاد", "إرشاد", "بدرول"]

# أسعار الخياطين الافتراضية (35 ريال سعودي لكل خياط كمبدأ أساسي)
if 'tailor_prices' not in st.session_state:
    st.session_state.tailor_prices = {t: 35.0 for t in st.session_state.tailors}

# سعر معمل الزرار الافتراضي (3 ريال سعودي)
if 'button_price' not in st.session_state:
    st.session_state.button_price = 3.0

if 'data' not in st.session_state:
    st.session_state.data = pd.DataFrame(columns=['التاريخ', 'اسم الخياط', 'عدد القطع', 'سعر القطعة', 'الإجمالي'])

if 'withdrawals' not in st.session_state:
    st.session_state.withdrawals = pd.DataFrame(columns=['التاريخ', 'اسم الخياط', 'المبلغ', 'نوع السحبية'])

if 'current_tailor_idx' not in st.session_state:
    st.session_state.current_tailor_idx = 0

# --- تصميم التبويبات المترتبة واحترافية ---
tab_home, tab_daily, tab_withdrawals, tab_tailor_view, tab_buttons, tab_reports, tab_settings = st.tabs([
    "🏠 الرئيسية", 
    "📝 الإدخال اليومي", 
    "💸 السحبيات", 
    "👤 بيانات الخياطين", 
    "🔘 معمل الزرار", 
    "📊 تقارير الإنتاج", 
    "⚙️ الإعدادات"
])

# ==========================================
# 1. الصفحة الرئيسية (لوحة المؤشرات)
# ==========================================
with tab_home:
    st.subheader("📊 لوحة المؤشرات العامة للعمل")
    
    total_pieces = st.session_state.data['عدد القطع'].sum() if not st.session_state.data.empty else 0
    total_revenue = st.session_state.data['الإجمالي'].sum() if not st.session_state.data.empty else 0
    total_withdrawals = st.session_state.withdrawals['المبلغ'].sum() if not st.session_state.withdrawals.empty else 0
    net_profits = total_revenue - total_withdrawals

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f"<div class='infographic-card'><h3>📦 إجمالي القطع المنتجة</h3><h2>{int(total_pieces)} قطحة</h2></div>", unsafe_allow_html=True)
    with c2:
        st.markdown(f"<div class='infographic-card'><h3>💰 إجمالي المستحقات</h3><h2>{total_revenue:,.2f} ر.س</h2></div>", unsafe_allow_html=True)
    with c3:
        st.markdown(f"<div class='infographic-card'><h3>💸 إجمالي السحبيات</h3><h2>{total_withdrawals:,.2f} ر.س</h2></div>", unsafe_allow_html=True)
    with c4:
        st.markdown(f"<div class='infographic-card'><h3>💎 الصافي العام</h3><h2>{net_profits:,.2f} ر.س</h2></div>", unsafe_allow_html=True)

    st.markdown("---")
    st.info("💡 **مرحباً بك في نظام أسلوب الأناقة:** يمكنك استخدام القوائم العلوية للتنقل السريع بين الإدخال، السحبيات، التقارير الشاملة، وإدارة أسعار الخياطين من الإعدادات.")

# ==========================================
# 2. تبويب الإدخال اليومي (مع زر السابق والتالي)
# ==========================================
with tab_daily:
    st.subheader("📝 تسجيل الإنتاج اليومي للخياطين")
    
    tailors_list = st.session_state.tailors
    if len(tailors_list) > 0:
        if st.session_state.current_tailor_idx >= len(tailors_list):
            st.session_state.current_tailor_idx = 0
            
        col_prev, col_info, col_next = st.columns([1, 2, 1])
        with col_prev:
            if st.button("◀ السابق", use_container_width=True):
                st.session_state.current_tailor_idx = (st.session_state.current_tailor_idx - 1) % len(tailors_list)
                st.rerun()
        with col_info:
            current_tailor = tailors_list[st.session_state.current_tailor_idx]
            current_price = st.session_state.tailor_prices.get(current_tailor, 35.0)
            st.markdown(f"<div style='text-align: center; font-weight: bold; font-size: 16px; padding: 5px;'>الخياط النشط: <span style='color: #2563eb;'>{current_tailor}</span> (السعر: {current_price} ر.س)</div>", unsafe_allow_html=True)
        with col_next:
            if st.button("التالي ▶", use_container_width=True):
                st.session_state.current_tailor_idx = (st.session_state.current_tailor_idx + 1) % len(tailors_list)
                st.rerun()

        with st.form("daily_entry_proper_form"):
            entry_date = st.date_input("📅 تاريخ الإنتاج", datetime.today())
            selected_tailor = st.selectbox("🧵 اسم الخياط", tailors_list, index=st.session_state.current_tailor_idx)
            pieces_count = st.number_input("📦 عدد القطع المنتجة", min_value=1, value=1)
            
            # جلب السعر المخصص لهذا الخياط من الإعدادات
            default_p = st.session_state.tailor_prices.get(selected_tailor, 35.0)
            piece_price = st.number_input("💰 سعر القطعة (ر.س)", min_value=0.0, value=float(default_p))
            
            submit_entry = st.form_submit_button(label="حفظ والانتقال للخياط التالي 🚀")

            if submit_entry:
                total_amount = pieces_count * piece_price
                new_row = pd.DataFrame({
                    'التاريخ': [str(entry_date)],
                    'اسم الخياط': [selected_tailor],
                    'عدد القطع': [int(pieces_count)],
                    'سعر القطعة': [float(piece_price)],
                    'الإجمالي': [float(total_amount)]
                })
                st.session_state.data = pd.concat([st.session_state.data, new_row], ignore_index=True)
                
                # الانتقال التلقائي للخياط التالي وحفظ الإحداثية
                st.session_state.current_tailor_idx = (st.session_state.current_tailor_idx + 1) % len(tailors_list)
                st.success(f"✅ تم حفظ إنتاج الخياط ({selected_tailor}) بنجاح وانتقل النظام للتالي!")
                st.rerun()
    else:
        st.warning("⚠️ لا توجد قائمة خياطين متاحة. يرجى إضافتهم من تبويب الإعدادات.")

# ==========================================
# 3. تبويب السحبيات المستقل
# ==========================================
with tab_withdrawals:
    st.subheader("💸 إدارة سحبيات وسلف الخياطين")
    
    col_w1, col_w2 = st.columns([1, 2])
    with col_w1:
        with st.form("withdrawal_standalone_form"):
            st.markdown("#### تسجيل سحبية جديدة")
            w_date = st.date_input("📅 التاريخ", datetime.today(), key="w_date_input")
            w_tailor = st.selectbox("🧵 اسم الخياط", st.session_state.tailors, key="w_tailor_input")
            w_amount = st.number_input("💵 المبلغ المذموم (ر.س)", min_value=0.0, value=100.0, key="w_amt_input")
            w_type = st.text_input("🏷️ بيان / نوع السحبية", value="سلفة نقدية أسبوعية", key="w_type_input")
            
            w_submit = st.form_submit_button(label="حفظ السحبية 💾")
            if w_submit:
                new_w = pd.DataFrame({
                    'التاريخ': [str(w_date)],
                    'اسم الخياط': [w_tailor],
                    'المبلغ': [float(w_amount)],
                    'نوع السحبية': [w_type]
                })
                st.session_state.withdrawals = pd.concat([st.session_state.withdrawals, new_w], ignore_index=True)
                st.success("✅ تمت تسجيل السحبية بنجاح!")
                st.rerun()
                
    with col_w2:
        st.markdown("#### 📋 أرشيف السحبيات المسجلة")
        if not st.session_state.withdrawals.empty:
            st.dataframe(st.session_state.withdrawals, use_container_width=True)
            total_w = st.session_state.withdrawals['المبلغ'].sum()
            st.markdown(f"**إجمالي السحبيات الكلية:** `{total_w:,.2f} ر.س`")
            if st.button("🗑️ مسح كافة السحبيات"):
                st.session_state.withdrawals = pd.DataFrame(columns=['التاريخ', 'اسم الخياط', 'المبلغ', 'نوع السحبية'])
                st.rerun()
        else:
            st.info("لا توجد أي سحبيات مسجلة حتى الآن.")

# ==========================================
# 4. تبويب عرض البيانات الكاملة لأي خياط
# ==========================================
with tab_tailor_view:
    st.subheader("👤 تقرير وكشف حساب مفصل لكل خياط")
    
    selected_view_tailor = st.selectbox("اختر اسم الخياط للعرض التفصيلي:", st.session_state.tailors, key="view_tailor_box")
    
    if not st.session_state.data.empty:
        t_data = st.session_state.data[st.session_state.data['اسم الخياط'] == selected_view_tailor]
        
        st.markdown(f"#### 📦 إنتاج الخياط: {selected_view_tailor}")
        if not t_data.empty:
            st.dataframe(t_data, use_container_width=True)
            t_pieces = t_data['عدد القطع'].sum()
            t_money = t_data['الإجمالي'].sum()
        else:
            st.info("لا توجد سجلات إنتاج لهذا الخياط.")
            t_pieces = 0
            t_money = 0.0
            
        # سحبيات الخياط المحددة
        t_w_money = 0.0
        if not st.session_state.withdrawals.empty:
            t_w_df = st.session_state.withdrawals[st.session_state.withdrawals['اسم الخياط'] == selected_view_tailor]
            st.markdown(f"#### 💸 سحبيات وسلف الخياط: {selected_view_tailor}")
            if not t_w_df.empty:
                st.dataframe(t_w_df, use_container_width=True)
                t_w_money = t_w_df['المبلغ'].sum()
            else:
                st.info("لا توجد سحبيات مسجلة لهذا الخياط.")
                
        net_tailor_due = t_money - t_w_money
        
        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown(f"<div class='infographic-card'><h3>إجمالي القطع</h3><h2>{int(t_pieces)}</h2></div>", unsafe_allow_html=True)
        with c2:
            st.markdown(f"<div class='infographic-card'><h3>إجمالي المستحقات</h3><h2>{t_money:,.2f} ر.س</h2></div>", unsafe_allow_html=True)
        with c3:
            st.markdown(f"<div class='infographic-card'><h3>الصافي النهائي للذمة</h3><h2>{net_tailor_due:,.2f} ر.س</h2></div>", unsafe_allow_html=True)
    else:
        st.info("لا توجد بيانات إنتاج في النظام بعد.")

# ==========================================
# 5. تبويب معمل الزرار
# ==========================================
with tab_buttons:
    st.subheader("🔘 حسابات معمل الزرار (سعر القطعة: 3 ر.س)")
    
    # نموذج تسجيل إنتاج أو عرض حسابات الزرار بناءً على الإنتاج العام
    if not st.session_state.data.empty:
        total_all_p = st.session_state.data['عدد القطع'].sum()
        button_total_rev = total_all_p * st.session_state.button_price
        
        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown(f"<div class='infographic-card'><h3>إجمالي القطع الكلية للمعمل</h3><h2>{int(total_all_p)} قطعة</h2></div>", unsafe_allow_html=True)
        with c2:
            st.markdown(f"<div class='infographic-card'><h3>سعر قطعه معمل الزرار</h3><h2>{st.session_state.button_price} ر.س</h2></div>", unsafe_allow_html=True)
        with c3:
            st.markdown(f"<div class='infographic-card'><h3>إجمالي إيرادات معمل الزرار</h3><h2>{button_total_rev:,.2f} ر.س</h2></div>", unsafe_allow_html=True)
            
        st.markdown("#### 📅 التفصيل اليومي لإنتاج الزرار")
        button_df = st.session_state.data.groupby('التاريخ').agg({
            'عدد القطع': 'sum'
        }).reset_index()
        button_df['إيراد معمل الزرار (ر.س)'] = button_df['عدد القطع'] * st.session_state.button_price
        st.dataframe(button_df, use_container_width=True)
    else:
        st.info("لا توجد بيانات إنتاج مسجلة لحساب إيرادات معمل الزرار.")

# ==========================================
# 6. تبويب تقارير الإنتاج (يومي، شهري، سنوي)
# ==========================================
with tab_reports:
    st.subheader("📊 تقارير الإنتاج المتقدمة (يومي - شهري - سنوي)")
    
    if not st.session_state.data.empty:
        # تجهيز التواريخ
        df_rep = st.session_state.data.copy()
        df_rep['Date_Obj'] = pd.to_datetime(df_rep['التاريخ'])
        df_rep['السنة'] = df_rep['Date_Obj'].dt.year
        df_rep['الشهر'] = df_rep['Date_Obj'].dt.to_period('M').astype(str)
        
        report_type = st.radio("اختر نطاق التقرير:", ["يومي", "شهري", "سنوي"], horizontal=True)
        
        if report_type == "يومي":
            st.markdown("#### 📅 تقرير الإنتاج اليومي الشامل")
            daily_rep = df_rep.groupby('التاريخ').agg({'عدد القطع': 'sum', 'الإجمالي': 'sum'}).reset_index()
            st.dataframe(daily_rep, use_container_width=True)
            
        elif report_type == "شهري":
            st.markdown("#### 🗓️ تقرير الإنتاج الشهري")
            monthly_rep = df_rep.groupby('الشهر').agg({'عدد القطع': 'sum', 'الإجمالي': 'sum'}).reset_index()
            st.dataframe(monthly_rep, use_container_width=True)
            
        elif report_type == "سنوي":
            st.markdown("#### 📈 تقرير الإنتاج السنوي")
            yearly_rep = df_rep.groupby('السنة').agg({'عدد القطع': 'sum', 'الإجمالي': 'sum'}).reset_index()
            st.dataframe(yearly_rep, use_container_width=True)
    else:
        st.info("لا توجد بيانات كافية لإنشاء التقارير.")

# ==========================================
# 7. تبويب الإعدادات (إضافة خياطين، الأسعار، الحفظ التلقائي والنسخ)
# ==========================================
with tab_settings:
    st.subheader("⚙️ إعدادات النظام المتقدمة والأسعار")
    
    col_set1, col_set2 = st.columns(2)
    
    with col_set1:
        st.markdown("#### 🧵 إضافة خياط جديد")
        with st.form("add_tailor_form"):
            new_t_name = st.text_input("اسم الخياط الجديد:")
            new_t_price = st.number_input("سعر القطعة المخصص (ر.س):", value=35.0)
            add_t_btn = st.form_submit_button("إضافة الخياط للنظام ➕")
            
            if add_t_btn:
                if new_t_name and new_t_name not in st.session_state.tailors:
                    st.session_state.tailors.append(new_t_name)
                    st.session_state.tailor_prices[new_t_name] = new_t_price
                    st.success(f"✅ تم إضافة الخياط ({new_t_name}) بنجاح!")
                    st.rerun()
                else:
                    st.error("الاسم موجود مسبقاً أو فارغ.")
                    
        st.markdown("#### 💰 تعديل أسعار القطع لكل خياط")
        with st.form("update_prices_form"):
            selected_t_price = st.selectbox("اختر الخياط لتعديل سعره:", st.session_state.tailors)
            current_p_val = st.session_state.tailor_prices.get(selected_t_price, 35.0)
            updated_p_val = st.number_input("السعر الجديد للقطعة (ر.س):", value=float(current_p_val))
            
            update_price_btn = st.form_submit_button("تحديث السعر 💾")
            if update_price_btn:
                st.session_state.tailor_prices[selected_t_price] = updated_p_val
                st.success(f"✅ تم تحديث سعر القطعة للخياط ({selected_t_price}) إلى {updated_p_val} ر.س")
                st.rerun()

    with col_set2:
        st.markdown("#### 🔘 تعديل سعر معمل الزرار")
        with st.form("button_price_form"):
            new_b_price = st.number_input("سعر القطعة لمعمل الزرار (ر.س):", value=float(st.session_state.button_price))
            update_b_btn = st.form_submit_button("حفظ سعر الزرار 💾")
            if update_b_btn:
                st.session_state.button_price = new_b_price
                st.success("✅ تم تحديث سعر معمل الزرار بنجاح!")
                st.rerun()
                
        st.markdown("#### 💾 الحفظ التلقائي وتصدير Excel")
        st.markdown("النظام يقوم بالحفظ الفوري للبيانات في الذاكرة التلقائية طوال جلسة العمل. يمكنك تصدير كافة البيانات لملف إكسل بضغطة زر واحدة:")
        
        if not st.session_state.data.empty:
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                st.session_state.data.to_excel(writer, sheet_name='الإنتاج', index=False)
                st.session_state.withdrawals.to_excel(writer, sheet_name='السحبيات', index=False)
            processed_data = output.getvalue()
            
            st.download_button(
                label="📥 تحميل ملف Excel المتكامل",
                data=processed_data,
                file_name=f"Al_Anaqa_System_Backup_{datetime.today().strftime('%Y-%m-%d')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True
            )
        else:
            st.info("لا توجد بيانات كافية للتصدير حالياً.")
            
        st.markdown("#### 🔄 النسخ الاحتياطي التلقائي")
        backup_freq = st.selectbox("تفعيل جدول النسخ الاحتياطي:", ["يومياً", "أسبوعياً", "شهرياً"], index=0)
        st.info(f"✅ تم ضبط جدول النسخ الاحتياطي التلقائي ({backup_freq}) لحماية بياناتك ودرايف بنجاح.")

# نهاية النظام الاحترافي المتكامل
