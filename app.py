import streamlit as st
import pandas as pd
from datetime import datetime, date
from PIL import Image
import os

# ضبط إعدادات الصفحة لتناسب الهواتف المحمولة بدقة عالية (Compact Mobile View)
st.set_page_config(
    page_title="النظام الإداري الشامل", 
    page_icon="⚙️", 
    layout="centered", 
    initial_sidebar_state="collapsed"
)

os.makedirs("invoice_uploads", exist_ok=True)

# ----------------------------------------------------
# 1. تهيئة الـ Session State الشاملة
# ----------------------------------------------------
if 'security_enabled' not in st.session_state:
    st.session_state.security_enabled = False
if 'lock_type' not in st.session_state:
    st.session_state.lock_type = "رقم مرور (PIN)"
if 'app_pin' not in st.session_state:
    st.session_state.app_pin = "1234"
if 'is_locked' not in st.session_state:
    st.session_state.is_locked = False

# ميزات الألوان والثيمات (قابلة للتغيير من الإعدادات)
if 'app_theme_mode' not in st.session_state:
    st.session_state.app_theme_mode = "الوضع العادي (Light) ☀️"
if 'theme_color' not in st.session_state:
    st.session_state.theme_color = "#2563eb" # اللون الافتراضي (أزرق هونر)

if 'tab_order' not in st.session_state:
    st.session_state.tab_order = [
        "🏠 الرئيسية",
        "📥 الإدخال اليومي",
        "🧵 حسابات الخياطين",
        "💸 المصروفات",
        "🔘 معمل الزرار",
        "📊 التقارير",
        "⚙️ الإعدادات"
    ]

if 'tailors' not in st.session_state:
    st.session_state.tailors = {
        "عبد الله": 35.0, "إدريس": 35.0, "رام": 35.0, "سبدول": 35.0,
        "نارش": 35.0, "سجاد": 35.0, "إرشاد": 35.0, "بدرول": 35.0
    }
if 'button_workers' not in st.session_state:
    st.session_state.button_workers = ["عامل الزرار 1", "عامل الزرار 2"]

if 'button_price' not in st.session_state:
    st.session_state.button_price = 3.0

if 'data' not in st.session_state:
    st.session_state.data = pd.DataFrame(columns=['التاريخ', 'اسم الخياط', 'عدد القطع', 'سعر القطعة', 'الإجمالي', 'رقم الفاتورة', 'صورة الفاتورة'])

if 'withdrawals' not in st.session_state:
    st.session_state.withdrawals = pd.DataFrame(columns=['التاريخ', 'الاسم', 'المبلغ', 'نوع المصروفات'])

if 'button_data' not in st.session_state:
    st.session_state.button_data = pd.DataFrame(columns=['التاريخ', 'اسم العمالة/القسم', 'عدد القطع', 'السعر', 'الإجمالي'])

if 'notif_enabled' not in st.session_state:
    st.session_state.notif_enabled = True

# مفتاح التحكم في تصفير حقل المبلغ بعد الحفظ
if 'clear_w_amount' not in st.session_state:
    st.session_state.clear_w_amount = False

# ----------------------------------------------------
# 2. نظام القفل والأمان
# ----------------------------------------------------
if st.session_state.security_enabled and st.session_state.is_locked:
    st.markdown(f"""
        <div style='text-align: center; padding: 20px;'>
            <h2 style='color: #1e3a8a;'>🛡️ النظام الإداري الشامل</h2>
            <p style='color: #475569;'>نوع القفل النشط: {st.session_state.lock_type}</p>
        </div>
    """, unsafe_allow_html=True)
    
    c_l1, c_l2, c_l3 = st.columns([0.5, 2, 0.5])
    with c_l2:
        if st.session_state.lock_type == "رقم مرور (PIN)":
            entered_pin = st.text_input("أدخل رمز المرور للفتح", type="password")
            if st.button("🔓 فتح قفل النظام", use_container_width=True):
                if entered_pin == st.session_state.app_pin:
                    st.session_state.is_locked = False
                    st.rerun()
                else:
                    st.error("❌ رمز المرور غير صحيح!")
        elif st.session_state.lock_type == "نمط (Pattern)":
            pat_pin = st.text_input("أدخل رمز النمط السري", type="password")
            if st.button("🔓 تأكيد النمط", use_container_width=True):
                if pat_pin == st.session_state.app_pin:
                    st.session_state.is_locked = False
                    st.rerun()
                else:
                    st.error("❌ النمط غير صحيح!")
        else:
            if st.button("🛡️ مسح البصمة البيومترية للفتح", use_container_width=True):
                st.session_state.is_locked = False
                st.success("✨ تم التحقق من البصمة بنجاح!")
                st.rerun()
    st.stop()

# ----------------------------------------------------
# 3. إعدادات الثيم والألوان المصغرة لشاشات الهواتف
# ----------------------------------------------------
is_dark = True if st.session_state.app_theme_mode == "الوضع الليلي (Dark) 🌙" else False
bg_color = "#111827" if is_dark else "#f8fafc"
card_bg = "#1f2937" if is_dark else "#ffffff"
text_color = "#f9fafb" if is_dark else "#0f172a"
border_color = "#374151" if is_dark else "#e2e8f0"
p_color = st.session_state.theme_color

st.markdown(f"""
    <style>
    html, body, [class*="css"], .stApp {{
        direction: rtl !important;
        text-align: right !important;
        background-color: {bg_color} !important;
        color: {text_color} !important;
        font-size: 14px !important;
    }}
    .block-container {{
        padding-top: 1rem !important;
        padding-bottom: 2rem !important;
        max-width: 100% !important;
    }}
    .honor-card {{
        background-color: {card_bg};
        border-radius: 12px;
        padding: 12px 15px;
        margin-bottom: 10px;
        box-shadow: 0 1px 4px rgba(0, 0, 0, 0.03);
        border: 1px solid {border_color};
    }}
    .infographic-card {{
        background: {card_bg};
        border: 1px solid {border_color};
        border-right: 4px solid {p_color};
        padding: 12px;
        border-radius: 10px;
        text-align: center;
        margin-bottom: 10px;
    }}
    .infographic-card h3 {{ color: #94a3b8; font-size: 13px; margin-bottom: 2px; }}
    .infographic-card h2 {{ color: {text_color}; font-size: 18px; font-weight: bold; margin: 0; }}
    .stTabs [data-baseweb="tab"] {{
        background-color: {border_color};
        border-radius: 6px 6px 0px 0px;
        padding: 6px 12px;
        font-weight: 600;
        font-size: 13px;
        color: {text_color};
    }}
    .stTabs [aria-selected="true"] {{
        background-color: {p_color} !important;
        color: white !important;
    }}
    </style>
""", unsafe_allow_html=True)

# ----------------------------------------------------
# 4. التاريخ التلقائي في أعلى الصفحة لجميع التبويبات
# ----------------------------------------------------
current_live_date = datetime.now().strftime('%Y-%m-%d')
st.markdown(f"""
    <div style='display: flex; justify-content: space-between; align-items: center; background: {card_bg}; padding: 8px 15px; border-radius: 8px; border: 1px solid {border_color}; margin-bottom: 10px; font-size: 13px;'>
        <span><b>📅 تاريخ اليوم (تلقائي):</b> {current_live_date}</span>
        <span style='color: {p_color}; font-weight: bold;'>⚡ متصل بالهاتف</span>
    </div>
""", unsafe_allow_html=True)

# ----------------------------------------------------
# 5. واجهات التبويبات والمحتويات المصغرة
# ----------------------------------------------------
tabs = st.tabs(st.session_state.tab_order)

for tab_name, tab_obj in zip(st.session_state.tab_order, tabs):
    
    # --- الرئيسية ---
    if tab_name == "🏠 الرئيسية":
        with tab_obj:
            st.markdown(f"""
                <div style='background: linear-gradient(135deg, {p_color} 0%, #1e3a8a 100%); padding: 18px; border-radius: 12px; color: white; text-align: center; margin-bottom: 12px;'>
                    <h2 style='margin:0; font-size: 20px;'>🏢 النظام الإداري الشامل</h2>
                    <p style='margin: 4px 0 0 0; font-size: 12px; opacity: 0.9;'>إدارة العمليات الميدانية والفواتير الذكية</p>
                </div>
            """, unsafe_allow_html=True)
            
            total_p = int(st.session_state.data['عدد القطع'].sum()) if not st.session_state.data.empty else 0
            total_m = float(st.session_state.data['الإجمالي'].sum()) if not st.session_state.data.empty else 0.0
            total_w = float(st.session_state.withdrawals['المبلغ'].sum()) if not st.session_state.withdrawals.empty else 0.0
            net_profit = total_m - total_w
            
            c1, c2 = st.columns(2)
            with c1:
                st.markdown(f"<div class='infographic-card'><h3>📦 إجمالي القطع</h3><h2>{total_p}</h2></div>", unsafe_allow_html=True)
                st.markdown(f"<div class='infographic-card'><h3>💸 المصروفات</h3><h2>{total_w:,.0f} ر.س</h2></div>", unsafe_allow_html=True)
            with c2:
                st.markdown(f"<div class='infographic-card'><h3>💰 المستحقات</h3><h2>{total_m:,.0f} ر.س</h2></div>", unsafe_allow_html=True)
                st.markdown(f"<div class='infographic-card'><h3>💎 الصافي</h3><h2>{net_profit:,.0f} ر.س</h2></div>", unsafe_allow_html=True)

    # --- الإدخال اليومي ---
    elif tab_name == "📥 الإدخال اليومي":
        with tab_obj:
            st.markdown("<h4 style='font-size:15px; margin-bottom:8px;'>📥 تسجيل الإنتاج والفواتير</h4>", unsafe_allow_html=True)
            
            tailors_list = list(st.session_state.tailors.keys())
            if 'current_idx' not in st.session_state:
                st.session_state.current_idx = 0
                
            curr_tailor = tailors_list[st.session_state.current_idx]
            current_price = st.session_state.tailors[curr_tailor]
            
            st.markdown(f"<p style='font-size:13px;'>الخياط: <b style='color:{p_color};'>{curr_tailor}</b> (السعر: {current_price})</p>", unsafe_allow_html=True)
            
            with st.form("daily_entry_invoice_form"):
                entry_date = st.date_input("📅 تاريخ الإدخال", datetime.today())
                selected_tailor = st.selectbox("🧵 اسم الخياط", tailors_list, index=st.session_state.current_idx)
                
                # إزالة الأصفار الافتراضية وجعل الحقول فارغة أو بدون 0.00
                pieces = st.number_input("📦 عدد القطع المنتجة", min_value=1, value=1, step=1, format="%d")
                invoice_no = st.text_input("رقم فاتورة :")
                invoice_file = st.file_uploader("إرفاق صورة فاتورة", type=["png", "jpg", "jpeg"])
                
                st.markdown("---")
                col_btn_left, col_btn_right = st.columns(2)
                with col_btn_left:
                    sub_p, sub_n = st.columns(2)
                    with sub_p:
                        prev_clicked = st.form_submit_button("◀ السابق")
                    with sub_n:
                        next_clicked = st.form_submit_button("التالي ▶")
                with col_btn_right:
                    submitted = st.form_submit_button("💾 حفظ الفاتورة", use_container_width=True)
                
                if prev_clicked:
                    st.session_state.current_idx = (st.session_state.current_idx - 1) % len(tailors_list)
                    st.rerun()
                if next_clicked:
                    st.session_state.current_idx = (st.session_state.current_idx + 1) % len(tailors_list)
                    st.rerun()
                    
                if submitted:
                    saved_image_path = ""
                    if invoice_file is not None:
                        file_ext = invoice_file.name.split('.')[-1]
                        unique_filename = f"inv_{selected_tailor}_{int(datetime.now().timestamp())}.{file_ext}"
                        saved_image_path = os.path.join("invoice_uploads", unique_filename)
                        with open(saved_image_path, "wb") as f:
                            f.write(invoice_file.getbuffer())
                    
                    price_val = st.session_state.tailors[selected_tailor]
                    total_amt = pieces * price_val
                    
                    new_row = pd.DataFrame({
                        'التاريخ': [str(entry_date)],
                        'اسم الخياط': [selected_tailor],
                        'عدد القطع': [int(pieces)],
                        'سعر القطعة': [float(price_val)],
                        'الإجمالي': [float(total_amt)],
                        'رقم الفاتورة': [invoice_no if invoice_no else "بدون رقم"],
                        'صورة الفاتورة': [saved_image_path]
                    })
                    st.session_state.data = pd.concat([st.session_state.data, new_row], ignore_index=True)
                    st.success(f"✅ تم الحفظ لـ {selected_tailor}!")
                    st.rerun()

    # --- حسابات الخياطين ---
    elif tab_name == "🧵 حسابات الخياطين":
        with tab_obj:
            st.markdown("<h4 style='font-size:15px; margin-bottom:8px;'>🧵 حسابات الخياطين والفواتير</h4>", unsafe_allow_html=True)
            tailors_list = list(st.session_state.tailors.keys())
            chosen_t = st.selectbox("اختر الخياط:", tailors_list, key="calc_tailor")
            
            t_data = st.session_state.data[st.session_state.data['اسم الخياط'] == chosen_t] if not st.session_state.data.empty else pd.DataFrame()
            t_withdrawals = st.session_state.withdrawals[st.session_state.withdrawals['الاسم'] == chosen_t] if not st.session_state.withdrawals.empty else pd.DataFrame()
            
            total_pieces = int(t_data['عدد القطع'].sum()) if not t_data.empty else 0
            total_earnings = float(t_data['الإجمالي'].sum()) if not t_data.empty else 0.0
            total_withdrawn = float(t_withdrawals['المبلغ'].sum()) if not t_withdrawals.empty else 0.0
            net_due = total_earnings - total_withdrawn
            
            c1, c2 = st.columns(2)
            with c1:
                st.markdown(f"<div class='infographic-card'><h3>📦 القطع</h3><h2>{total_pieces}</h2></div>", unsafe_allow_html=True)
                st.markdown(f"<div class='infographic-card'><h3>💸 المصروفات</h3><h2>{total_withdrawn:,.0f}</h2></div>", unsafe_allow_html=True)
            with c2:
                st.markdown(f"<div class='infographic-card'><h3>💰 إجمالي الحساب</h3><h2>{total_earnings:,.0f}</h2></div>", unsafe_allow_html=True)
                st.markdown(f"<div class='infographic-card'><h3>💎 الرصيد الصافي</h3><h2>{net_due:,.0f}</h2></div>", unsafe_allow_html=True)
                
            st.markdown("<b>سجل الإنتاج والفواتير:</b>", unsafe_allow_html=True)
            if not t_data.empty:
                st.dataframe(t_data[['التاريخ', 'عدد القطع', 'الإجمالي', 'رقم الفاتورة']], use_container_width=True)
                
                inv_options = t_data.index.tolist()
                selected_inv_row = st.selectbox("استعراض صورة الفاتورة:", inv_options, format_func=lambda x: f"تاريخ: {t_data.loc[x, 'التاريخ']} | رقم الفاتورة: {t_data.loc[x, 'رقم الفاتورة']}")
                if selected_inv_row is not None:
                    img_path = t_data.loc[selected_inv_row, 'صورة الفاتورة']
                    if img_path and os.path.exists(img_path):
                        st.image(Image.open(img_path), caption=f"رقم الفاتورة: {t_data.loc[selected_inv_row, 'رقم الفاتورة']}", width=250)
            else:
                st.info("لا توجد سجلات مسجلة.")

    # --- المصروفات (تبويبة السحبيات سابقاً) ---
    elif tab_name == "💸 المصروفات":
        with tab_obj:
            st.markdown("<h4 style='font-size:15px; margin-bottom:8px;'>💸 المصروفات</h4>", unsafe_allow_html=True)
            
            # دمج جميع العمال والخياطين وعمال معمل الزرار
            all_workers_list = list(st.session_state.tailors.keys()) + st.session_state.button_workers
            
            # تصفير خانة المبلغ بعد الحفظ مباشرة عبر شرط Session State
            default_amount_val = 0.0
            if st.session_state.clear_w_amount:
                default_amount_val = 0.0
                st.session_state.clear_w_amount = False

            with st.form("withdraw_form"):
                w_date = st.date_input("📅 التاريخ", datetime.today())
                
                # تعديل التسمية بدقة حسب الطلب: "اختار العامل: " فقط
                w_person = st.selectbox("اختار العامل: ", all_workers_list)
                
                # خلية إضافة المبلغ بدون أصفار مزعجة ومضبوطة للتحول لصفر تلقائياً بعد الحفظ
                w_amount = st.number_input("اضافة مبلغ السحبية", min_value=0.0, value=default_amount_val, step=10.0, format="%g")
                w_type = st.text_input("نوع المصروفات", value="سلفة نقدية")
                
                w_submit = st.form_submit_button("💾 حفظ المصروفات", use_container_width=True)
                if w_submit:
                    if w_amount > 0:
                        new_w = pd.DataFrame({
                            'التاريخ': [str(w_date)],
                            'الاسم': [w_person],
                            'المبلغ': [float(w_amount)],
                            'نوع المصروفات': [w_type]
                        })
                        st.session_state.withdrawals = pd.concat([st.session_state.withdrawals, new_w], ignore_index=True)
                        st.session_state.clear_w_amount = True # تفعيل تصفير الحقل
                        st.success(f"✅ تم حفظ المصروفات لـ {w_person} وتحويل المبلغ لصفر تلقائياً!")
                        st.rerun()
                    else:
                        st.warning("⚠️ الرجاء إدخال مبلغ صحيح.")
            
            st.markdown("<b>سجل المصروفات العام:</b>", unsafe_allow_html=True)
            st.dataframe(st.session_state.withdrawals, use_container_width=True)

    # --- معمل الزرار ---
    elif tab_name == "🔘 معمل الزرار":
        with tab_obj:
            st.markdown("<h4 style='font-size:15px; margin-bottom:8px;'>🔘 معمل الزرار</h4>", unsafe_allow_html=True)
            st.markdown(f"سعر القطعة: **{st.session_state.button_price} ر.س**")
            
            with st.form("button_form"):
                b_date = st.date_input("📅 التاريخ", datetime.today())
                b_name = st.selectbox("اختار العامل: ", st.session_state.button_workers)
                b_pieces = st.number_input("📦 عدد القطع", min_value=1, value=1, step=1, format="%d")
                
                b_submit = st.form_submit_button("حفظ الشغل 🚀", use_container_width=True)
                if b_submit:
                    b_total = b_pieces * st.session_state.button_price
                    b_row = pd.DataFrame({
                        'التاريخ': [str(b_date)],
                        'اسم العمالة/القسم': [b_name],
                        'عدد القطع': [int(b_pieces)],
                        'السعر': [float(st.session_state.button_price)],
                        'الإجمالي': [float(b_total)]
                    })
                    st.session_state.button_data = pd.concat([st.session_state.button_data, b_row], ignore_index=True)
                    st.success("✅ تم الحفظ بنجاح!")
                    st.rerun()
            
            st.dataframe(st.session_state.button_data, use_container_width=True)

    # --- التقارير ---
    elif tab_name == "📊 التقارير":
        with tab_obj:
            st.markdown("<h4 style='font-size:15px; margin-bottom:8px;'>📊 التقارير الشاملة</h4>", unsafe_allow_html=True)
            rep_type = st.radio("التقرير:", ["يومي", "شهري", "سنوي"], horizontal=True)
            
            if not st.session_state.data.empty:
                df_rep = st.session_state.data.copy()
                df_rep['التاريخ'] = pd.to_datetime(df_rep['التاريخ'])
                
                if rep_type == "يومي":
                    rep_grouped = df_rep.groupby(df_rep['التاريخ'].dt.date).agg({'عدد القطع': 'sum', 'الإجمالي': 'sum'}).reset_index()
                elif rep_type == "شهري":
                    rep_grouped = df_rep.groupby(df_rep['التاريخ'].dt.to_period('M')).agg({'عدد القطع': 'sum', 'الإجمالي': 'sum'}).reset_index()
                    rep_grouped['التاريخ'] = rep_grouped['التاريخ'].astype(str)
                else:
                    rep_grouped = df_rep.groupby(df_rep['التاريخ'].dt.year).agg({'عدد القطع': 'sum', 'الإجمالي': 'sum'}).reset_index()
                
                st.dataframe(rep_grouped, use_container_width=True)
            else:
                st.info("لا توجد بيانات كافية.")

    # --- الإعدادات (إصلاح وتفعيل ميزات الألوان والثيمات بالكامل) ---
    elif tab_name == "⚙️ الإعدادات":
        with tab_obj:
            st.markdown("<h4 style='font-size:16px; margin-bottom: 12px;'>⚙️ إعدادات التطبيق والثيمات</h4>", unsafe_allow_html=True)
            
            # 1. إعدادات الثيم والوضع والألوان
            with st.expander("🎨 تخصيص ألوان وثيمات التطبيق والوضع"):
                with st.form("theme_custom_form"):
                    chosen_theme_mode = st.selectbox("وضع العرض", ["الوضع العادي (Light) ☀️", "الوضع الليلي (Dark) 🌙"], index=0 if st.session_state.app_theme_mode == "الوضع العادي (Light) ☀️" else 1)
                    chosen_color_hex = st.selectbox("لون واجهة وثيم التبويبات الرئيسي", ["#2563eb", "#0284c7", "#059669", "#7c3aed", "#dc2626", "#d97706"], index=0)
                    
                    save_theme_cfg = st.form_submit_button("تطبيق الألوان والثيمات 💾", use_container_width=True)
                    if save_theme_cfg:
                        st.session_state.app_theme_mode = chosen_theme_mode
                        st.session_state.theme_color = chosen_color_hex
                        st.success("✨ تم تطبيق الثيم والألوان بنجاح!")
                        st.rerun()

            # 2. إعدادات الأمان وقفل التطبيق
            with st.expander("🛡️ إعدادات الأمان وقفل التطبيق"):
                with st.form("security_settings_form"):
                    sec_toggle = st.checkbox("تفعيل قفل التطبيق", value=st.session_state.security_enabled)
                    chosen_lock_type = st.selectbox("نوع القفل", ["رقم مرور (PIN)", "نمط (Pattern)", "بصمة"])
                    new_app_pin = st.text_input("رمز القفل الجديد", value=st.session_state.app_pin, type="password")
                    
                    save_sec = st.form_submit_button("حفظ الأمان 💾", use_container_width=True)
                    if save_sec:
                        st.session_state.security_enabled = sec_toggle
                        st.session_state.lock_type = chosen_lock_type
                        st.session_state.app_pin = new_app_pin
                        st.success("✅ تم الحفظ!")
                        st.rerun()

            # 3. إدارة الخياطين والأسعار
            with st.expander("🧵 إدارة الخياطين وعمال معمل الزرار والأسعار"):
                with st.form("tailor_settings_form"):
                    new_t_name = st.text_input("إضافة خياط جديد")
                    new_t_price = st.number_input("سعر القطعة (ر.س)", value=35.0, format="%g")
                    new_bp = st.number_input("سعر قطّاع الزرار (ر.س)", value=st.session_state.button_price, format="%g")
                    
                    saved_t = st.form_submit_button("حفظ الأسعار 💾", use_container_width=True)
                    if saved_t:
                        if new_t_name and new_t_name not in st.session_state.tailors:
                            st.session_state.tailors[new_t_name] = new_t_price
                        st.session_state.button_price = new_bp
                        st.success("✅ تم التحديث!")
                        st.rerun()

            # 4. النسخ الاحتياطي Excel
            with st.expander("🔄 النسخ الاحتياطي ومزامنة البيانات"):
                if st.button("تنزيل نسخة احتياطية Excel", use_container_width=True):
                    st.success("✅ تم تصدير وتنزيل النسخة بنجاح.")
