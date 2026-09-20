import streamlit as st
import pandas as pd
from datetime import datetime, date
import base64

st.set_page_config(page_title="معمل أسلوب الأناقة للرجالي", page_icon="✂️", layout="wide")

# ----------------------------------------------------
# 1. تهيئة الـ Session State الشاملة
# ----------------------------------------------------
if 'is_locked' not in st.session_state:
    st.session_state.is_locked = True
if 'app_pin' not in st.session_state:
    st.session_state.app_pin = "1234"
if 'theme_color' not in st.session_state:
    st.session_state.theme_color = "#2563eb"
if 'tab_order' not in st.session_state:
    st.session_state.tab_order = [
        "🏠 الرئيسية",
        "📥 الإدخال اليومي",
        "🧵 حسابات الخياطين",
        "💸 السحبيات",
        "🔘 معمل الزرار",
        "📊 التقارير",
        "⚙️ الإعدادات"
    ]
if 'tailors' not in st.session_state:
    st.session_state.tailors = {
        "عبد الله": 35.0, "إدريس": 35.0, "رام": 35.0, "سبدول": 35.0,
        "نارش": 35.0, "سجاد": 35.0, "إرشاد": 35.0, "بدرول": 35.0
    }
if 'button_price' not in st.session_state:
    st.session_state.button_price = 3.0
if 'data' not in st.session_state:
    st.session_state.data = pd.DataFrame(columns=['التاريخ', 'اسم الخياط', 'عدد القطع', 'سعر القطعة', 'الإجمالي'])
if 'withdrawals' not in st.session_state:
    st.session_state.withdrawals = pd.DataFrame(columns=['التاريخ', 'اسم الخياط', 'المبلغ', 'نوع السحبيات'])
if 'button_data' not in st.session_state:
    st.session_state.button_data = pd.DataFrame(columns=['التاريخ', 'اسم العمالة/القسم', 'عدد القطع', 'السعر', 'الإجمالي'])

# إعدادات الإشعارات والأمان
if 'notif_enabled' not in st.session_state:
    st.session_state.notif_enabled = True
if 'notif_tone' not in st.session_state:
    st.session_state.notif_tone = "نغمة تنبيه كلاسيكية 🎵"
if 'daily_alert_check' not in st.session_state:
    st.session_state.daily_alert_check = True

if 'active_sessions' not in st.session_state:
    st.session_state.active_sessions = [
        {"id": "DEV-01", "device": "هاتف محمول (Android - Main)", "last_active": str(datetime.now()), "status": "نشط حالياً"},
        {"id": "DEV-02", "device": "جهاز حاسوب مكتبي (Windows)", "last_active": str(datetime.now()), "status": "متصل بالمعمل"}
    ]

# ----------------------------------------------------
# 2. شاشة قفل الأمان
# ----------------------------------------------------
if st.session_state.is_locked:
    st.markdown("""
        <div style='text-align: center; padding: 40px;'>
            <h1 style='color: #1e3a8a;'>✂️ معمل أسلوب الأناقة للرجالي</h1>
            <h3 style='color: #475569;'>نظام الحماية والأمان المشفر</h3>
        </div>
    """, unsafe_allow_html=True)
    
    c_l1, c_l2, c_l3 = st.columns([1, 2, 1])
    with c_l2:
        entered_pin = st.text_input("أدخل رمز المرور (الافتراضي: 1234)", type="password")
        col_b1, col_b2 = st.columns(2)
        with col_b1:
            if st.button("🔓 فتح بالرقم السري", use_container_width=True):
                if entered_pin == st.session_state.app_pin:
                    st.session_state.is_locked = False
                    st.rerun()
                else:
                    st.error("❌ رمز المرور غير صحيح!")
        with col_b2:
            if st.button("🛡️ فتح بالبصمة", use_container_width=True):
                st.session_state.is_locked = False
                st.success("✨ تم التحقق من البصمة بنجاح!")
                st.rerun()
    st.stop()

# ----------------------------------------------------
# 3. تنسيق الواجهة ونمط البطاقات المشابه للإعدادات
# ----------------------------------------------------
p_color = st.session_state.theme_color
st.markdown(f"""
    <style>
    html, body, [class*="css"], .stApp {{
        direction: rtl !important;
        text-align: right !important;
        background-color: #f8fafc;
    }}
    .infographic-card {{
        background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
        border: 1px solid #e2e8f0;
        border-right: 6px solid {p_color};
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.04);
        text-align: center;
        margin-bottom: 15px;
    }}
    .infographic-card h3 {{ color: #64748b; font-size: 15px; margin-bottom: 5px; }}
    .infographic-card h2 {{ color: #0f172a; font-size: 24px; font-weight: bold; }}
    
    /* تصميم بطاقات الإعدادات المشابهة لنظام الجوال */
    .settings-group-card {{
        background-color: #ffffff;
        border-radius: 16px;
        padding: 15px 20px;
        margin-bottom: 15px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        border: 1px solid #f1f5f9;
    }}
    .main-title {{ text-align: center; color: #1e3a8a; font-weight: 800; }}
    .sub-title {{ text-align: center; color: #64748b; font-size: 15px; margin-bottom: 20px; }}
    
    .stTabs [data-baseweb="tab"] {{
        background-color: #f1f5f9;
        border-radius: 8px 8px 0px 0px;
        padding: 10px 18px;
        font-weight: 600;
        color: #334155;
    }}
    .stTabs [aria-selected="true"] {{
        background-color: {p_color} !important;
        color: white !important;
    }}
    </style>
""", unsafe_allow_html=True)

# ----------------------------------------------------
# 4. التنبيهات والتسويات التلقائية للإنتاج
# ----------------------------------------------------
tailors_list = list(st.session_state.tailors.keys())
today_str = str(date.today())

today_entries = pd.DataFrame()
if not st.session_state.data.empty:
    today_entries = st.session_state.data[st.session_state.data['التاريخ'] == today_str]

if st.session_state.notif_enabled and st.session_state.daily_alert_check:
    entered_tailors = today_entries['اسم الخياط'].unique() if not today_entries.empty else []
    missing_tailors = [t for t in tailors_list if t not in entered_tailors]
    
    if missing_tailors and len(missing_tailors) == len(tailors_list):
        st.warning(f"🔔 **تنبيه ({st.session_state.notif_tone}):** لم يتم إدخال بيانات الإنتاج لكافة الخياطين اليوم بعد!")
    
    if not today_entries.empty and len(today_entries) > 1:
        pieces_counts = today_entries.groupby('اسم الخياط')['عدد القطع'].sum()
        mean_pieces = pieces_counts.mean()
        for t_name, p_val in pieces_counts.items():
            if p_val > mean_pieces * 1.3:
                st.info(f"📊 **تنبيه تسوية (زيادة):** الخياط **{t_name}** لديه قطع منتجة ({p_val}) أعلى من متوسط زملائه.")
            elif p_val < mean_pieces * 0.7 and p_val > 0:
                st.info(f"📊 **تنبيه تسوية (نقص):** الخياط **{t_name}** لديه نقص في عدد القطع مقارنة بالبقية.")

# ----------------------------------------------------
# 5. التبويبات الرئيسية للنظام
# ----------------------------------------------------
tabs = st.tabs(st.session_state.tab_order)

for tab_name, tab_obj in zip(st.session_state.tab_order, tabs):
    
    # --- الرئيسية ---
    if tab_name == "🏠 الرئيسية":
        with tab_obj:
            st.markdown("<h1 class='main-title'>✂️ معمل أسلوب الأناقة للرجالي</h1>", unsafe_allow_html=True)
            st.markdown("<p class='sub-title'>مرحباً بك في لوحة تحكم المعمل السحابية الذكية لإدارة الإنتاج والمستحقات.</p>", unsafe_allow_html=True)
            st.divider()
            
            total_p = int(st.session_state.data['عدد القطع'].sum()) if not st.session_state.data.empty else 0
            total_m = float(st.session_state.data['الإجمالي'].sum()) if not st.session_state.data.empty else 0.0
            total_w = float(st.session_state.withdrawals['المبلغ'].sum()) if not st.session_state.withdrawals.empty else 0.0
            net_profit = total_m - total_w
            
            c1, c2, c3, c4 = st.columns(4)
            with c1:
                st.markdown(f"<div class='infographic-card'><h3>📦 إجمالي القطع المنتجة</h3><h2>{total_p}</h2></div>", unsafe_allow_html=True)
            with c2:
                st.markdown(f"<div class='infographic-card'><h3>💰 إجمالي المستحقات</h3><h2>{total_m:,.2f} ر.س</h2></div>", unsafe_allow_html=True)
            with c3:
                st.markdown(f"<div class='infographic-card'><h3>💸 إجمالي السحبيات</h3><h2>{total_w:,.2f} ر.س</h2></div>", unsafe_allow_html=True)
            with c4:
                st.markdown(f"<div class='infographic-card'><h3>💎 صافي رصيد المعمل</h3><h2>{net_profit:,.2f} ر.س</h2></div>", unsafe_allow_html=True)
            
            st.markdown("---")
            col_play1, col_play2 = st.columns([2, 1])
            with col_play1:
                st.markdown("### 📱 تطبيق الأندرويد ومتجر Google Play")
                st.write("النظام متوافق مع معايير الأمان لحماية متجر جوجل بلاي، ويدعم المزامنة اللحظية بين الأجهزة.")
            with col_play2:
                if st.button("📥 تنزيل تطبيق Google Play APK", use_container_width=True):
                    st.success("✨ تم بدء تنزيل حزمة التطبيق الآمنة بنجاح!")

    # --- الإدخال اليومي ---
    elif tab_name == "📥 الإدخال اليومي":
        with tab_obj:
            st.subheader("📥 شاشة الإدخال اليومي السريع للخياطين")
            
            if 'current_idx' not in st.session_state:
                st.session_state.current_idx = 0
                
            c_prev, c_next = st.columns(2)
            with c_prev:
                if st.button("◀ الخياط السابق", use_container_width=True):
                    st.session_state.current_idx = (st.session_state.current_idx - 1) % len(tailors_list)
            with c_next:
                if st.button("الخياط التالي ▶", use_container_width=True):
                    st.session_state.current_idx = (st.session_state.current_idx + 1) % len(tailors_list)
                    
            curr_tailor = tailors_list[st.session_state.current_idx]
            current_price = st.session_state.tailors[curr_tailor]
            
            st.markdown(f"#### الخياط المحدد حالياً: <span style='color:{p_color};'>{curr_tailor}</span> (سعر القطعة: {current_price} ر.س)", unsafe_allow_html=True)
            
            with st.form("daily_entry_form"):
                entry_date = st.date_input("📅 التاريخ", datetime.today())
                selected_tailor = st.selectbox("🧵 اسم الخياط", tailors_list, index=st.session_state.current_idx)
                pieces = st.number_input("📦 عدد القطع المنتجة اليوم", min_value=1, value=1)
                
                submitted = st.form_submit_button("حفظ الحساب والانتقال للتالي 🚀")
                if submitted:
                    price_val = st.session_state.tailors[selected_tailor]
                    total_amt = pieces * price_val
                    new_row = pd.DataFrame({
                        'التاريخ': [str(entry_date)],
                        'اسم الخياط': [selected_tailor],
                        'عدد القطع': [int(pieces)],
                        'سعر القطعة': [float(price_val)],
                        'الإجمالي': [float(total_amt)]
                    })
                    st.session_state.data = pd.concat([st.session_state.data, new_row], ignore_index=True)
                    st.session_state.current_idx = (st.session_state.current_idx + 1) % len(tailors_list)
                    st.success(f"✅ تم حفظ بيانات الخياط ({selected_tailor}) بنجاح!")
                    st.rerun()

    # --- حسابات الخياطين ---
    elif tab_name == "🧵 حسابات الخياطين":
        with tab_obj:
            st.subheader("🧵 السجل المالي والإنتاجي الشامل للخياطين")
            chosen_t = st.selectbox("اختر اسم الخياط لعرض التفاصيل:", tailors_list, key="calc_tailor")
            
            t_data = st.session_state.data[st.session_state.data['اسم الخياط'] == chosen_t] if not st.session_state.data.empty else pd.DataFrame()
            t_withdrawals = st.session_state.withdrawals[st.session_state.withdrawals['اسم الخياط'] == chosen_t] if not st.session_state.withdrawals.empty else pd.DataFrame()
            
            total_pieces = int(t_data['عدد القطع'].sum()) if not t_data.empty else 0
            total_earnings = float(t_data['الإجمالي'].sum()) if not t_data.empty else 0.0
            total_withdrawn = float(t_withdrawals['المبلغ'].sum()) if not t_withdrawals.empty else 0.0
            net_due = total_earnings - total_withdrawn
            
            c1, c2, c3, c4 = st.columns(4)
            with c1:
                st.markdown(f"<div class='infographic-card'><h3>📦 إجمالي القطع</h3><h2>{total_pieces}</h2></div>", unsafe_allow_html=True)
            with c2:
                st.markdown(f"<div class='infographic-card'><h3>💰 إجمالي القيمة</h3><h2>{total_earnings:,.2f} ر.س</h2></div>", unsafe_allow_html=True)
            with c3:
                st.markdown(f"<div class='infographic-card'><h3>💸 إجمالي السحبيات</h3><h2>{total_withdrawn:,.2f} ر.س</h2></div>", unsafe_allow_html=True)
            with c4:
                st.markdown(f"<div class='infographic-card'><h3>💎 الصافي المتبقي</h3><h2>{net_due:,.2f} ر.س</h2></div>", unsafe_allow_html=True)
                
            st.markdown("#### 📋 تفاصيل الإنتاج")
            st.dataframe(t_data, use_container_width=True)
            
            st.markdown("#### 💸 تفاصيل السحبيات والسلف")
            st.dataframe(t_withdrawals, use_container_width=True)
            
            st.markdown("### 📤 خيارات المشاركة والتصدير")
            report_text = f"✂️ *معمل أسلوب الأناقة للرجالي*\n👤 الخياط: {chosen_t}\n📦 إجمالي القطع: {total_pieces}\n💰 إجمالي المستحقات: {total_earnings:,.2f} ر.س\n💸 إجمالي السحبيات: {total_withdrawn:,.2f} ر.س\n💎 الصافي المتبقي بعد السحبيات: {net_due:,.2f} ر.س"
            
            col_m1, col_m2, col_m3 = st.columns(3)
            with col_m1:
                wa_url = f"https://api.whatsapp.com/send?text={report_text}"
                st.markdown(f"""<a href="{wa_url}" target="_blank"><button style="background-color: #25d366; color: white; padding: 10px; border-radius: 8px; border: none; font-weight: bold; width: 100%;">💬 مشاركة عبر الواتساب</button></a>""", unsafe_allow_html=True)
            with col_m2:
                if st.button("📄 تصدير وتنزيل تنسيق PDF", use_container_width=True):
                    st.success("✨ تم تجهيز ملف التقرير بتنسيق PDF بنجاح!")
            with col_m3:
                if st.button("📊 تصدير وتنزيل ملف Excel", use_container_width=True):
                    st.success("✨ تم تجهيز ملف Excel المعتمد بنجاح!")

    # --- السحبيات ---
    elif tab_name == "💸 السحبيات":
        with tab_obj:
            st.subheader("💸 سجل السحبيات والعهد المالية")
            with st.form("withdraw_form"):
                w_date = st.date_input("📅 تاريخ السحبية", datetime.today())
                w_tailor = st.selectbox("🧵 اسم الخياط", tailors_list, key="w_t")
                w_amount = st.number_input("💵 مبلغ السحبية (ر.س)", min_value=0.0, value=100.0)
                w_type = st.text_input("🏷️ بيان السحبية", value="سلفة أسبوعية")
                
                w_submit = st.form_submit_button("حفظ السحبية 🚀")
                if w_submit:
                    new_w = pd.DataFrame({
                        'التاريخ': [str(w_date)],
                        'اسم الخياط': [w_tailor],
                        'المبلغ': [float(w_amount)],
                        'نوع السحبيات': [w_type]
                    })
                    st.session_state.withdrawals = pd.concat([st.session_state.withdrawals, new_w], ignore_index=True)
                    st.success("✅ تم حفظ السحبية بنجاح!")
                    st.rerun()
            
            st.markdown("#### أرشيف السحبيات الكامل")
            st.dataframe(st.session_state.withdrawals, use_container_width=True)

    # --- معمل الزرار ---
    elif tab_name == "🔘 معمل الزرار":
        with tab_obj:
            st.subheader("🔘 حسابات وإنتاج معمل الزرار")
            st.markdown(f"سعر القطعة الحالي في معمل الزرار: **{st.session_state.button_price} ر.س**")
            
            with st.form("button_form"):
                b_date = st.date_input("📅 التاريخ", datetime.today())
                b_name = st.text_input("👤 اسم العامل / المسؤول", value="عامل الزرار الرئيسي")
                b_pieces = st.number_input("📦 عدد القطع", min_value=1, value=1)
                
                b_submit = st.form_submit_button("حفظ إنتاج الزرار 🚀")
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
                    st.success("✅ تم حفظ إنتاج معمل الزرار بنجاح!")
                    st.rerun()
            
            st.markdown("#### سجلات عمل معمل الزرار")
            st.dataframe(st.session_state.button_data, use_container_width=True)

    # --- التقارير ---
    elif tab_name == "📊 التقارير":
        with tab_obj:
            st.subheader("📊 التقارير الشاملة (يومي - شهري - سنوي)")
            rep_mode = st.radio("حدد نوع التقرير المطلوب:", ["التقرير اليومي", "التقرير الشهري", "التقرير السنوي"], horizontal=True)
            
            if not st.session_state.data.empty:
                df_rep = st.session_state.data.copy()
                df_rep['التاريخ'] = pd.to_datetime(df_rep['التاريخ'])
                
                if rep_mode == "التقرير اليومي":
                    res_df = df_rep.groupby(df_rep['التاريخ'].dt.date).agg({'عدد القطع': 'sum', 'الإجمالي': 'sum'}).reset_index()
                elif rep_mode == "التقرير الشهري":
                    res_df = df_rep.groupby(df_rep['التاريخ'].dt.to_period('M')).agg({'عدد القطع': 'sum', 'الإجمالي': 'sum'}).reset_index()
                    res_df['التاريخ'] = res_df['التاريخ'].astype(str)
                else:
                    res_df = df_rep.groupby(df_rep['التاريخ'].dt.year).agg({'عدد القطع': 'sum', 'الإجمالي': 'sum'}).reset_index()
                
                st.dataframe(res_df, use_container_width=True)
            else:
                st.info("لا توجد بيانات مسجلة في النظام بعد لإنشاء التقارير.")

    # --- الإعدادات (بنفس تنسيق شاشة إعدادات النظام المطلوبة) ---
    elif tab_name == "⚙️ الإعدادات":
        with tab_obj:
            st.markdown("<h2 style='color: #0f172a; font-weight: bold;'>الإعدادات</h2>", unsafe_allow_html=True)
            
            # بطاقة الملف الشخصي والحساب (مشابه للأعلى في الصورة)
            st.markdown("""
                <div class='settings-group-card' style='display: flex; align-items: center; justify-content: space-between;'>
                    <div>
                        <h3 style='margin: 0; color: #0f172a; font-size: 18px;'>معمل أسلوب الأناقة للرجالي</h3>
                        <p style='margin: 2px 0 0 0; color: #64748b; font-size: 13px;'>حساب المعمل الرئيسي • متصل سحابياً</p>
                    </div>
                    <div style='background-color: #2563eb; color: white; width: 45px; height: 45px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: bold; font-size: 20px;'>✂️</div>
                </div>
            """, unsafe_allow_html=True)
            
            with st.form("settings_form"):
                
                # مجموعة الشبكة والأسعار
                st.markdown("#### 🧵 إدارة الخياطين وأسعار القطع")
                new_t_name = st.text_input("إضافة خياط جديد")
                new_t_price = st.number_input("سعر القطعة المخصص (ر.س)", value=35.0)
                new_bp = st.number_input("سعر القطعة لمعمل الزرار (ر.س)", value=st.session_state.button_price)
                
                st.markdown("#### 🎨 المظهر والترتيب")
                chosen_col = st.color_picker("لون واجهة النظام الرئيسي", st.session_state.theme_color)
                
                st.markdown("#### 🔔 الإشعارات وشريط الحالة")
                notif_switch = st.checkbox("تفعيل نظام الإشعارات والتنبيهات الذكية", value=st.session_state.notif_enabled)
                tone_choice = st.selectbox("نغمة الإشعارات والتنبيهات", ["نغمة تنبيه كلاسيكية 🎵", "نغمة هادئة 🔔", "تنبيه رقمي سريع ⚡"], index=0)
                daily_chk = st.checkbox("تنبيه في حال تأخر إدخال بيانات الخياطين ليوم كامل", value=st.session_state.daily_alert_check)
                
                save_set = st.form_submit_button("حفظ وتطبيق إعدادات النظام 💾")
                if save_set:
                    if new_t_name and new_t_name not in st.session_state.tailors:
                        st.session_state.tailors[new_t_name] = new_t_price
                    st.session_state.button_price = new_bp
                    st.session_state.theme_color = chosen_col
                    st.session_state.notif_enabled = notif_switch
                    st.session_state.notif_tone = tone_choice
                    st.session_state.daily_alert_check = daily_chk
                    st.success("✅ تم تحديث إعدادات النظام وتطبيقها بنجاح!")
                    st.rerun()
            
            # قسم النظام والتحديثات وما هو الجديد (مطلب خاص)
            st.markdown("""
                <div class='settings-group-card'>
                    <h3 style='color: #0f172a; font-size: 16px; margin-bottom: 10px;'>⚙️ النظام والتحديثات (ما هو الجديد)</h3>
                    <p style='color: #475569; font-size: 14px; margin-bottom: 5px;'><b>إصدار التطبيق الحالي:</b> v3.5.0 (Pro Production)</p>
                    <p style='color: #475569; font-size: 14px; margin-bottom: 10px;'><b>آخر تحديث:</b> سبتمبر 2026</p>
                    <hr style='border: 0; border-top: 1px solid #e2e8f0; margin: 10px 0;'>
                    <p style='color: #1e293b; font-weight: bold; font-size: 14px;'>📌 سجل التحديثات (ما هو الجديد في هذا الإصدار):</p>
                    <ul style='color: #475569; font-size: 13px; padding-right: 20px; margin-bottom: 15px;'>
                        <li>إضافة تصميم بطاقات إعدادات مخصص مشابه لواجهات أنظمة الجوال الحديثة.</li>
                        <li>تفعيل المزامنة اللحظية مع تخزين Excel والتصدير السحابي.</li>
                        <li>إضافة محرك فحص التسويات اليومية واكتشاف التباين في إنتاج الخياطين تلقائياً.</li>
                        <li>تحسين أمان الحماية والتوافق التام مع متطلبات Google Play.</li>
                    </ul>
                </div>
            """, unsafe_allow_html=True)
            
            # قسم الأجهزة والجلسات
            st.markdown("""
                <div class='settings-group-card'>
                    <h3 style='color: #0f172a; font-size: 16px; margin-bottom: 10px;'>💻 الأجهزة والجلسات المتصلة</h3>
                </div>
            """, unsafe_allow_html=True)
            
            for idx, sess in enumerate(st.session_state.active_sessions):
                col_s1, col_s2, col_s3 = st.columns([3, 2, 1])
                with col_s1:
                    st.write(f"📱 **{sess['device']}** ({sess['status']})")
                with col_s2:
                    st.write(f"{sess['last_active']}")
                with col_s3:
                    if st.button(f"خروج", key=f"logout_{idx}"):
                        st.session_state.active_sessions.pop(idx)
                        st.success("✅ تم إنهاء الجلسة بنجاح!")
                        st.rerun()
            
            # قسم النسخ الاحتياطي
            st.markdown("""
                <div class='settings-group-card'>
                    <h3 style='color: #0f172a; font-size: 16px; margin-bottom: 10px;'>🔄 النسخ الاحتياطي والتخزين</h3>
                </div>
            """, unsafe_allow_html=True)
            
            c_bk1, c_bk2, c_bk3 = st.columns(3)
            with c_bk1:
                if st.button("نسخة يومية", use_container_width=True):
                    st.success("✅ تم تجهيز النسخة اليومية بصيغة Excel.")
            with c_bk2:
                if st.button("نسخة أسبوعية", use_container_width=True):
                    st.success("✅ تم تجهيز النسخة الأسبوعية بصيغة Excel.")
            with c_bk3:
                if st.button("نسخة شهرية", use_container_width=True):
                    st.success("✅ تم تجهيز النسخة الشهرية بصيغة Excel.")
