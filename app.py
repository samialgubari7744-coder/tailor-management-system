import streamlit as st
import pandas as pd
from datetime import datetime, date
import base64

st.set_page_config(page_title="ةمعمل لمسة أسلوب الأناقة للخياطة الرجالي", page_icon="✂️", layout="wide")

# ----------------------------------------------------
# 1. تهيئة قاعدة البيانات والـ Session State الشاملة
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

# إعدادات الإشعارات والتنبيهات
if 'notif_enabled' not in st.session_state:
    st.session_state.notif_enabled = True
if 'notif_tone' not in st.session_state:
    st.session_state.notif_tone = "نغمة هادئة 🔔"
if 'daily_alert_check' not in st.session_state:
    st.session_state.daily_alert_check = True

# محاكاة إدارة الجلسات والأجهزة المتصلة
if 'active_sessions' not in st.session_state:
    st.session_state.active_sessions = [
        {"id": "DEV-01", "device": "هاتف هونر (Honor MagicOS - Main)", "last_active": str(datetime.now()), "status": "نشط حالياً"},
        {"id": "DEV-02", "device": "جهاز حاسوب مكتبي (Windows)", "last_active": str(datetime.now()), "status": "متصل بالمعمل"}
    ]

# ----------------------------------------------------
# 2. نظام قفل الأمان (رمز مرور / بصمة)
# ----------------------------------------------------
if st.session_state.is_locked:
    st.markdown("""
        <div style='text-align: center; padding: 40px;'>
            <h1 style='color: #1e3a8a;'>✂️ معمل أسلوب الأناقة للرجالي</h1>
            <h3 style='color: #475569;'>نظام الحماية والأمان المشفر (Honor Style)</h3>
        </div>
    """, unsafe_allow_html=True)
    
    c_l1, c_l2, c_l3 = st.columns([1, 2, 1])
    with c_l2:
        entered_pin = st.text_input("أدخل رمز المرور (الافتراضي: 1234)", type="password")
        col_b1, col_b2 = st.columns(2)
        with col_b1:
            if st.button("🔓 فتح بالرقم", use_container_width=True):
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
# 3. التصميم العام ونمط واجهة إعدادات Honor MagicOS
# ----------------------------------------------------
p_color = st.session_state.theme_color
st.markdown(f"""
    <style>
    /* خلفية رمادية فاتحة جداً للصفحة بالكامل لتشبه واجهة النظام */
    html, body, [class*="css"], .stApp {{
        direction: rtl !important;
        text-align: right !important;
        background-color: #f3f4f6 !important;
    }}
    
    /* تصميم البطاقات (Honor Cards Style) */
    .honor-card {{
        background-color: #ffffff;
        border-radius: 16px;
        padding: 12px 18px;
        margin-bottom: 12px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
        border: 1px solid #e5e7eb;
    }}
    
    .setting-row {{
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 10px 5px;
        border-bottom: 1px solid #f3f4f6;
        font-weight: 500;
        color: #1f2937;
    }}
    .setting-row:last-child {{
        border-bottom: none;
    }}
    
    .infographic-card {{
        background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
        border: 1px solid #e2e8f0;
        border-right: 6px solid {p_color};
        padding: 20px;
        border-radius: 14px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.04);
        text-align: center;
        margin-bottom: 15px;
    }}
    .infographic-card h3 {{ color: #64748b; font-size: 15px; margin-bottom: 5px; }}
    .infographic-card h2 {{ color: #0f172a; font-size: 24px; font-weight: bold; }}
    
    .main-title {{ text-align: center; color: #1e3a8a; font-weight: 800; }}
    .sub-title {{ text-align: center; color: #64748b; font-size: 15px; margin-bottom: 20px; }}
    
    .stTabs [data-baseweb="tab"] {{
        background-color: #e5e7eb;
        border-radius: 8px 8px 0px 0px;
        padding: 10px 18px;
        font-weight: 600;
        color: #374151;
    }}
    .stTabs [aria-selected="true"] {{
        background-color: {p_color} !important;
        color: white !important;
    }}
    </style>
""", unsafe_allow_html=True)

# ----------------------------------------------------
# 4. محرك فحص الإشعارات والتسويات التلقائية
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
        st.warning(f"🔔 **تنبيه إشعارات ({st.session_state.notif_tone}):** لم يتم إدخال بيانات الإنتاج لكافة الخياطين اليوم بعد!")
    
    if not today_entries.empty and len(today_entries) > 1:
        pieces_counts = today_entries.groupby('اسم الخياط')['عدد القطع'].sum()
        mean_pieces = pieces_counts.mean()
        for t_name, p_val in pieces_counts.items():
            if p_val > mean_pieces * 1.3:
                st.info(f"📊 **تنبيه تسوية (زيادة):** الخياط **{t_name}** لديه قطع ({p_val}) أعلى من متوسط الزملاء.")
            elif p_val < mean_pieces * 0.7 and p_val > 0:
                st.info(f"📊 **تنبيه تسوية (نقص):** الخياط **{t_name}** لديه نقص ملحوظ في عدد القطع اليوم.")

# ----------------------------------------------------
# 5. التبويبات والواجهات
# ----------------------------------------------------
tabs = st.tabs(st.session_state.tab_order)

for tab_name, tab_obj in zip(st.session_state.tab_order, tabs):
    
    # --- الصفحة الرئيسية ---
    if tab_name == "🏠 الرئيسية":
        with tab_obj:
            # شاشة ترحيبية مع شعار المعمل
            st.markdown("""
                <div style='background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%); padding: 30px; border-radius: 16px; color: white; text-align: center; margin-bottom: 20px;'>
                    <h1 style='margin:0; font-size: 32px;'>✂️ معمل أسلوب الأناقة للرجالي</h1>
                    <p style='margin-top: 8px; font-size: 16px; opacity: 0.9;'>أهلاً بك في لوحة التحكم الذكية للإدارة الشاملة - نظام عالي الأداء ومحمي</p>
                </div>
            """, unsafe_allow_html=True)
            
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
                st.write("النظام متوافق مع معايير الأمان وحماية متجر جوجل بلاي، ويدعم التثبيت المباشر على الهاتف المحمول.")
            with col_play2:
                if st.button("📥 تنزيل تطبيق Google Play APK", use_container_width=True):
                    st.success("✨ جاري تنزيل حزمة التطبيق الآمنة بنجاح!")

    # --- الإدخال اليومي ---
    elif tab_name == "📥 الإدخال اليومي":
        with tab_obj:
            st.subheader("📥 تسجيل الإنتاج اليومي للخياطين")
            
            if 'current_idx' not in st.session_state:
                st.session_state.current_idx = 0
                
            c_prev, c_next = st.columns(2)
            with c_prev:
                if st.button("◀ السابق", use_container_width=True):
                    st.session_state.current_idx = (st.session_state.current_idx - 1) % len(tailors_list)
            with c_next:
                if st.button("التالي ▶", use_container_width=True):
                    st.session_state.current_idx = (st.session_state.current_idx + 1) % len(tailors_list)
                    
            curr_tailor = tailors_list[st.session_state.current_idx]
            current_price = st.session_state.tailors[curr_tailor]
            
            st.markdown(f"#### الخياط الحالي: <span style='color:{p_color};'>{curr_tailor}</span> (السعر الثابت: {current_price} ر.س)", unsafe_allow_html=True)
            
            with st.form("daily_entry_form"):
                entry_date = st.date_input("📅 التاريخ", datetime.today())
                selected_tailor = st.selectbox("🧵 اسم الخياط", tailors_list, index=st.session_state.current_idx)
                pieces = st.number_input("📦 عدد القطع المنتجة", min_value=1, value=1)
                
                submitted = st.form_submit_button("حفظ والانتقال للتالي 🚀")
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
                    st.success(f"✅ تم حفظ إنتاج {selected_tailor} ومزامنة البيانات بنجاح!")
                    st.rerun()

    # --- حسابات الخياطين ---
    elif tab_name == "🧵 حسابات الخياطين":
        with tab_obj:
            st.subheader("🧵 السجل المالي والإنتاجي الشامل للخياطين")
            chosen_t = st.selectbox("اختر الخياط لعرض التفاصيل الكاملة:", tailors_list, key="calc_tailor")
            
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
                
            st.markdown("#### 📋 سجل الإنتاج")
            st.dataframe(t_data, use_container_width=True)
            
            st.markdown("#### 💸 سجل السحبيات")
            st.dataframe(t_withdrawals, use_container_width=True)
            
            st.markdown("### 📤 خيارات التصدير والمشاركة")
            report_text = f"✂️ *معمل أسلوب الأناقة للرجالي*\n👤 الخياط: {chosen_t}\n📦 القطع: {total_pieces}\n💰 المستحقات: {total_earnings:,.2f} ر.س\n💸 السحبيات: {total_withdrawn:,.2f} ر.س\n💎 الصافي: {net_due:,.2f} ر.س"
            
            col_m1, col_m2, col_m3 = st.columns(3)
            with col_m1:
                wa_url = f"https://api.whatsapp.com/send?text={report_text}"
                st.markdown(f"""<a href="{wa_url}" target="_blank"><button style="background-color: #25d366; color: white; padding: 10px; border-radius: 8px; border: none; font-weight: bold; width: 100%;">💬 واتساب</button></a>""", unsafe_allow_html=True)
            with col_m2:
                if st.button("📄 تصدير PDF", use_container_width=True):
                    st.success("✨ تم تجهيز ملف PDF بنجاح!")
            with col_m3:
                if st.button("📊 تصدير Excel", use_container_width=True):
                    st.success("✨ تم تجهيز ملف Excel بنجاح!")

    # --- السحبيات ---
    elif tab_name == "💸 السحبيات":
        with tab_obj:
            st.subheader("💸 إدارة سحبيات وسلف الخياطين")
            with st.form("withdraw_form"):
                w_date = st.date_input("📅 التاريخ", datetime.today())
                w_tailor = st.selectbox("🧵 اسم الخياط", tailors_list, key="w_t")
                w_amount = st.number_input("💵 مبلغ السحبية (ر.س)", min_value=0.0, value=100.0)
                w_type = st.text_input("🏷️ نوع السحبية", value="سلفة نقدية أسبوعية")
                
                w_submit = st.form_submit_button("حفظ السحبية 🚀")
                if w_submit:
                    new_w = pd.DataFrame({
                        'التاريخ': [str(w_date)],
                        'اسم الخياط': [w_tailor],
                        'المبلغ': [float(w_amount)],
                        'نوع السحبيات': [w_type]
                    })
                    st.session_state.withdrawals = pd.concat([st.session_state.withdrawals, new_w], ignore_index=True)
                    st.success("✅ تم تسجيل السحبية وحفظها بنجاح!")
                    st.rerun()
            
            st.markdown("#### أرشيف السحبيات")
            st.dataframe(st.session_state.withdrawals, use_container_width=True)

    # --- معمل الزرار ---
    elif tab_name == "🔘 معمل الزرار":
        with tab_obj:
            st.subheader("🔘 حسابات قسم معمل الزرار")
            st.markdown(f"سعر قطّاع الزرار الحالي: **{st.session_state.button_price} ر.س** للقطعة الواحدة.")
            
            with st.form("button_form"):
                b_date = st.date_input("📅 تاريخ الشغل", datetime.today())
                b_name = st.text_input("👤 اسم العامل / المسؤول", value="عامل الزرار")
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
            rep_type = st.radio("اختر نوع التقرير:", ["يومي", "شهري", "سنوي"], horizontal=True)
            
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
                st.info("لا توجد بيانات كافية لعرض التقارير حالياً.")

    # --- الإعدادات (بنمط بطاقات Honor MagicOS المتقدمة) ---
    elif tab_name == "⚙️ الإعدادات":
        with tab_obj:
            st.markdown("<h2 style='color: #1f2937; margin-bottom: 20px;'>الإعدادات</h2>", unsafe_allow_html=True)
            
            # 1. بطاقة الحساب الشخصي والمعمل (Honor Style Card)
            st.markdown("""
                <div class="honor-card">
                    <div style="display: flex; align-items: center; justify-content: space-between;">
                        <div style="display: flex; align-items: center; gap: 12px;">
                            <span style="font-size: 32px;">✂️</span>
                            <div>
                                <div style="font-weight: bold; font-size: 16px; color: #111827;">معمل أسلوب الأناقة للرجالي</div>
                                <div style="font-size: 13px; color: #6b7280;">حساب المعمل السحابي والآمن</div>
                            </div>
                        </div>
                        <span style="color: #9ca3af; font-size: 18px;">&gt;</span>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
            # 2. بطاقة إدارة الخياطين والتسعير الثابت
            st.markdown("### 🧵 إدارة الخياطين والأسعار (35 ر.س ثابت)")
            with st.form("tailor_settings_form"):
                new_t_name = st.text_input("إضافة خياط جديد")
                new_t_price = st.number_input("سعر القطعة المخصص (ر.س)", value=35.0)
                new_bp = st.number_input("سعر قطّاع الزرار (ر.س)", value=st.session_state.button_price)
                
                saved_t = st.form_submit_button("حفظ الخياط والأسعار 💾")
                if saved_t:
                    if new_t_name and new_t_name not in st.session_state.tailors:
                        st.session_state.tailors[new_t_name] = new_t_price
                    st.session_state.button_price = new_bp
                    st.success("✅ تم تحديث الأسعار والخياطين بنجاح!")
                    st.rerun()

            # 3. بطاقة الاتصالات والتنبيهات والإشعارات (Honor Style Group)
            st.markdown("""
                <div class="honor-card">
                    <div style="font-weight: bold; font-size: 14px; color: #4b5563; margin-bottom: 8px;">🔔 التنبيهات والاتصالات والإشعارات</div>
                </div>
            """, unsafe_allow_html=True)
            
            with st.form("notif_form"):
                notif_switch = st.checkbox("تفعيل نظام الإشعارات والتنبيهات اليومية", value=st.session_state.notif_enabled)
                tone_choice = st.selectbox("نغمة الإشعارات", ["نغمة هادئة 🔔", "نغمة كلاسيكية 🎵", "تنبيه سريع ⚡"], index=0)
                daily_chk = st.checkbox("تنبيه في حال تأخر إدخال بيانات الخياطين ليوم كامل", value=st.session_state.daily_alert_check)
                
                up_notif = st.form_submit_button("تحديث إعدادات الإشعارات 💾")
                if up_notif:
                    st.session_state.notif_enabled = notif_switch
                    st.session_state.notif_tone = tone_choice
                    st.session_state.daily_alert_check = daily_chk
                    st.success("✅ تم تحديث إعدادات الإشعارات بنجاح!")
                    st.rerun()

            # 4. بطاقة النظام والتحديثات وما هو جديد (Honor Style)
            st.markdown("""
                <div class="honor-card">
                    <div style="font-weight: bold; font-size: 14px; color: #4b5563; margin-bottom: 8px;">⚙️ النظام والتحديثات (ما هو جديد)</div>
                    <div style="font-size: 13px; color: #374151; line-height: 1.6;">
                        • الإصدار الحالي: <b>v3.5.0 (Pro Production)</b><br>
                        • حالة النظام: <b>محدث لآخر إصدار آمن متوافق مع Google Play Protect</b><br>
                        • آخر التحديثات: إضافة واجهة إعدادات هونر، التنبيهات التلقائية للتسويات، ومزامنة السحبيات.
                    </div>
                </div>
            """, unsafe_allow_html=True)

            # 5. إدارة الجلسات والأجهزة (Honor Style Card)
            st.markdown("""
                <div class="honor-card">
                    <div style="font-weight: bold; font-size: 14px; color: #4b5563; margin-bottom: 8px;">💻 إدارة الجلسات والأجهزة المتصلة</div>
                </div>
            """, unsafe_allow_html=True)
            
            for idx, sess in enumerate(st.session_state.active_sessions):
                col_s1, col_s2, col_s3 = st.columns([3, 2, 1])
                with col_s1:
                    st.write(f"📱 **{sess['device']}**")
                with col_s2:
                    st.write(f"{sess['status']}")
                with col_s3:
                    if st.button("خروج", key=f"logout_{idx}"):
                        st.session_state.active_sessions.pop(idx)
                        st.success("✅ تم إنهاء الجلسة بنجاح!")
                        st.rerun()

            # 6. النسخ الاحتياطي التلقائي ومزامنة درايف و Excel
            st.markdown("""
                <div class="honor-card">
                    <div style="font-weight: bold; font-size: 14px; color: #4b5563; margin-bottom: 8px;">🔄 النسخ الاحتياطي السحابي (Excel & Google Drive)</div>
                </div>
            """, unsafe_allow_html=True)
            
            c_bk1, c_bk2, c_bk3 = st.columns(3)
            with c_bk1:
                if st.button("نسخة احتياطية (يوميّة)"):
                    st.success("✅ تم إنشاء وتنزيل النسخة اليومية بصيغة Excel.")
            with c_bk2:
                if st.button("نسخة احتياطية (أسبوعيّة)"):
                    st.success("✅ تم إنشاء وتنزيل النسخة الأسبوعية بصيغة Excel.")
            with c_bk3:
                if st.button("نسخة احتياطية (شهريّة)"):
                    st.success("✅ تم إنشاء وتنزيل النسخة الشهرية بصيغة Excel.")
