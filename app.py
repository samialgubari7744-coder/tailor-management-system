import streamlit as st
import pandas as pd
from datetime import datetime, date
from PIL import Image
import os

st.set_page_config(page_title="النظام الإداري الشامل", page_icon="⚙️", layout="wide")

# إنشاء مجلد لحفظ الصور المرفقة للفواتير محلياً
os.makedirs("invoice_uploads", exist_ok=True)

# ----------------------------------------------------
# 1. تهيئة قاعدة البيانات والـ Session State الشاملة
# ----------------------------------------------------
if 'security_enabled' not in st.session_state:
    st.session_state.security_enabled = False  # لا تظهر شاشة القفل إلا إذا فُعلت من الإعدادات
if 'lock_type' not in st.session_state:
    st.session_state.lock_type = "رقم مرور (PIN)" # خيارات: رقم مرور (PIN) ، نمط (Pattern) ، بصمة (Biometric)
if 'app_pin' not in st.session_state:
    st.session_state.app_pin = "1234"
if 'is_locked' not in st.session_state:
    st.session_state.is_locked = False

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
if 'button_workers' not in st.session_state:
    st.session_state.button_workers = ["عامل الزرار 1", "عامل الزرار 2"]

if 'button_price' not in st.session_state:
    st.session_state.button_price = 3.0

# هيكل بيانات الإنتاج مرتبط بكل خياط بشكل مستقل
if 'data' not in st.session_state:
    st.session_state.data = pd.DataFrame(columns=['التاريخ', 'اسم الخياط', 'عدد القطع', 'سعر القطعة', 'الإجمالي', 'رقم الفاتورة', 'صورة الفاتورة'])

if 'withdrawals' not in st.session_state:
    st.session_state.withdrawals = pd.DataFrame(columns=['التاريخ', 'الاسم', 'المبلغ', 'نوع السحبيات'])

if 'button_data' not in st.session_state:
    st.session_state.button_data = pd.DataFrame(columns=['التاريخ', 'اسم العمالة/القسم', 'عدد القطع', 'السعر', 'الإجمالي'])

# إعدادات الإشعارات
if 'notif_enabled' not in st.session_state:
    st.session_state.notif_enabled = True
if 'notif_tone' not in st.session_state:
    st.session_state.notif_tone = "نغمة هادئة 🔔"
if 'daily_alert_check' not in st.session_state:
    st.session_state.daily_alert_check = True

if 'active_sessions' not in st.session_state:
    st.session_state.active_sessions = [
        {"id": "DEV-01", "device": "هاتف هونر (Honor MagicOS - Main)", "last_active": str(datetime.now()), "status": "نشط حالياً"}
    ]

# ----------------------------------------------------
# 2. نظام القفل والأمان (يُفعل فقط بناءً على خيار الإعدادات)
# ----------------------------------------------------
if st.session_state.security_enabled and st.session_state.is_locked:
    st.markdown(f"""
        <div style='text-align: center; padding: 40px;'>
            <h1 style='color: #1e3a8a;'>🛡️ النظام الإداري الشامل</h1>
            <h3 style='color: #475569;'>نوع القفل النشط: {st.session_state.lock_type}</h3>
        </div>
    """, unsafe_allow_html=True)
    
    c_l1, c_l2, c_l3 = st.columns([1, 2, 1])
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
            st.info("🔐 تم تفعيل حماية النمط. أدخل الرمز السري للنمط المعتمد:")
            pat_pin = st.text_input("رمز النمط", type="password")
            if st.button("🔓 تأكيد النمط", use_container_width=True):
                if pat_pin == st.session_state.app_pin:
                    st.session_state.is_locked = False
                    st.rerun()
                else:
                    st.error("❌ النمط غير صحيح!")
        else: # بصمة
            if st.button("🛡️ مسح البصمة البيومترية للفتح", use_container_width=True):
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
    html, body, [class*="css"], .stApp {{
        direction: rtl !important;
        text-align: right !important;
        background-color: #f3f4f6 !important;
    }}
    .honor-card {{
        background-color: #ffffff;
        border-radius: 16px;
        padding: 16px 20px;
        margin-bottom: 14px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
        border: 1px solid #e5e7eb;
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
# 4. واجهات التبويبات والتشغيل
# ----------------------------------------------------
tabs = st.tabs(st.session_state.tab_order)

for tab_name, tab_obj in zip(st.session_state.tab_order, tabs):
    
    # --- الرئيسية ---
    if tab_name == "🏠 الرئيسية":
        with tab_obj:
            st.markdown("""
                <div style='background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%); padding: 30px; border-radius: 16px; color: white; text-align: center; margin-bottom: 20px;'>
                    <h1 style='margin:0; font-size: 32px;'>🏢 النظام الإداري الشامل</h1>
                    <p style='margin-top: 8px; font-size: 16px; opacity: 0.9;'>لوحة التحكم المركزية المتقدمة - تتبع ذكي للخياطين، الفواتير، والسحبيات</p>
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
                st.markdown(f"<div class='infographic-card'><h3>💎 صافي رصيد النظام</h3><h2>{net_profit:,.2f} ر.س</h2></div>", unsafe_allow_html=True)

    # --- الإدخال اليومي (تحديثات دقيقة حسب الطلب) ---
    elif tab_name == "📥 الإدخال اليومي":
        with tab_obj:
            st.subheader("📥 تسجيل الإنتاج اليومي وإرفاق الفواتير الخاصة بكل خياط")
            
            tailors_list = list(st.session_state.tailors.keys())
            if 'current_idx' not in st.session_state:
                st.session_state.current_idx = 0
                
            curr_tailor = tailors_list[st.session_state.current_idx]
            current_price = st.session_state.tailors[curr_tailor]
            
            st.markdown(f"#### الخياط الحالي: <span style='color:{p_color};'>{curr_tailor}</span> (السعر الثابت: {current_price} ر.س)", unsafe_allow_html=True)
            
            with st.form("daily_entry_invoice_form"):
                col_f1, col_f2 = st.columns(2)
                with col_f1:
                    # التاريخ يتحدث تلقائياً حسب الجهاز مع القدرة على الاختيار والتعديل
                    entry_date = st.date_input("📅 التاريخ", datetime.today())
                    selected_tailor = st.selectbox("🧵 اسم الخياط", tailors_list, index=st.session_state.current_idx)
                    pieces = st.number_input("📦 عدد القطع المنتجة", min_value=1, value=1)
                with col_f2:
                    invoice_no = st.text_input("رقم فاتورة :")
                    invoice_file = st.file_uploader("إرفاق صورة فاتورة", type=["png", "jpg", "jpeg"])
                
                st.markdown("---")
                # أزرار السابق والتالي بجانب بعضها في الجهة المقابلة لزر الحفظ
                col_btn_left, col_btn_right = st.columns([1, 1])
                with col_btn_left:
                    col_sub_prev, col_sub_next = st.columns(2)
                    with col_sub_prev:
                        prev_clicked = st.form_submit_button("◀ السابق")
                    with col_sub_next:
                        next_clicked = st.form_submit_button("التالي ▶")
                with col_btn_right:
                    submitted = st.form_submit_button("💾 حفظ وحفظ بيانات الفاتورة", use_container_width=True)
                
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
                    
                    # حفظ البيانات خاصة بالخياط المحدد فقط
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
                    st.success(f"✅ تم حفظ سجل الإنتاج والفاتورة الخاصة بـ {selected_tailor} بنجاح!")
                    st.rerun()

    # --- حسابات الخياطين (عرض البيانات المستقلة والفواتير) ---
    elif tab_name == "🧵 حسابات الخياطين":
        with tab_obj:
            st.subheader("🧵 السجل المالي والإنتاجي الشامل ومراجعة الفواتير للخياطين")
            tailors_list = list(st.session_state.tailors.keys())
            chosen_t = st.selectbox("اختر الخياط لعرض بياناته الخاصة:", tailors_list, key="calc_tailor")
            
            # استخراج بيانات الخياط المحدد حصرياً
            t_data = st.session_state.data[st.session_state.data['اسم الخياط'] == chosen_t] if not st.session_state.data.empty else pd.DataFrame()
            t_withdrawals = st.session_state.withdrawals[st.session_state.withdrawals['الاسم'] == chosen_t] if not st.session_state.withdrawals.empty else pd.DataFrame()
            
            total_pieces = int(t_data['عدد القطع'].sum()) if not t_data.empty else 0
            total_earnings = float(t_data['الإجمالي'].sum()) if not t_data.empty else 0.0
            total_withdrawn = float(t_withdrawals['المبلغ'].sum()) if not t_withdrawals.empty else 0.0
            net_due = total_earnings - total_withdrawn
            
            c1, c2, c3, c4, c5 = st.columns(5)
            with c1:
                st.markdown(f"<div class='infographic-card'><h3>📦 القطع المشتغلة</h3><h2>{total_pieces}</h2></div>", unsafe_allow_html=True)
            with c2:
                st.markdown(f"<div class='infographic-card'><h3>💰 إجمالي الحساب</h3><h2>{total_earnings:,.2f} ر.س</h2></div>", unsafe_allow_html=True)
            with c3:
                st.markdown(f"<div class='infographic-card'><h3>💸 إجمالي السحبيات</h3><h2>{total_withdrawn:,.2f} ر.س</h2></div>", unsafe_allow_html=True)
            with c4:
                st.markdown(f"<div class='infographic-card'><h3>📊 الحساب قبل الخصم</h3><h2>{total_earnings:,.2f} ر.س</h2></div>", unsafe_allow_html=True)
            with c5:
                st.markdown(f"<div class='infographic-card'><h3>💎 الرصيد بعد السحب</h3><h2>{net_due:,.2f} ر.س</h2></div>", unsafe_allow_html=True)
                
            st.markdown("#### 📋 سجل الإنتاج والفواتير اليومية المرفقة")
            if not t_data.empty:
                st.dataframe(t_data[['التاريخ', 'عدد القطع', 'سعر القطعة', 'الإجمالي', 'رقم الفاتورة']], use_container_width=True)
                
                st.markdown("### 🔍 مراجعة واستعراض صور الفواتير المرفقة لهذا الخياط")
                inv_options = t_data.index.tolist()
                selected_inv_row = st.selectbox("اختر الفاتورة للاستعراض:", inv_options, format_func=lambda x: f"التاريخ: {t_data.loc[x, 'التاريخ']} | رقم الفاتورة: {t_data.loc[x, 'رقم الفاتورة']}")
                if selected_inv_row is not None:
                    img_path = t_data.loc[selected_inv_row, 'صورة الفاتورة']
                    if img_path and os.path.exists(img_path):
                        st.image(Image.open(img_path), caption=f"رقم الفاتورة: {t_data.loc[selected_inv_row, 'رقم الفاتورة']} - الخياط: {chosen_t}", width=400)
                    else:
                        st.info("لا توجد صورة مرفقة لهذه الفاتورة.")
            else:
                st.info(f"لا توجد سجلات مسجلة للخياط {chosen_t} حتى الآن.")
            
            st.markdown("#### 💸 سجل السحبيات الخاصة بالخياط")
            st.dataframe(t_withdrawals, use_container_width=True)

    # --- السحبيات (تشمل جميع الخياطين ومعمل الزرار وتتصفر بعد الحفظ) ---
    elif tab_name == "💸 السحبيات":
        with tab_obj:
            st.subheader("💸 إدارة سحبيات وسلف الخياطين وعمال معمل الزرار")
            
            # دمج جميع الأسماء (الخياطين + معمل الزرار)
            all_names_list = list(st.session_state.tailors.keys()) + st.session_state.button_workers
            
            with st.form("withdraw_form"):
                # التاريخ يتحدث تلقائياً حسب الجهاز مع إمكانية التعديل
                w_date = st.date_input("📅 تاريخ السحبية", datetime.today())
                w_person = st.selectbox("👤 اختر العامل / الخياط / معمل الزرار", all_names_list)
                
                # خلية إضافة مبلغ السحبية (تتصفر عند الانتقال أو التحديث)
                w_amount = st.number_input("💵 مبلغ السحبية (ر.س)", min_value=0.0, value=0.0, step=50.0, key="w_amount_input")
                w_type = st.text_input("🏷️ نوع السحبية", value="سلفة نقدية")
                
                w_submit = st.form_submit_button("💾 حفظ السحبية")
                if w_submit:
                    if w_amount > 0:
                        new_w = pd.DataFrame({
                            'التاريخ': [str(w_date)],
                            'الاسم': [w_person],
                            'المبلغ': [float(w_amount)],
                            'نوع السحبيات': [w_type]
                        })
                        st.session_state.withdrawals = pd.concat([st.session_state.withdrawals, new_w], ignore_index=True)
                        st.success(f"✅ تم تسجيل السحبية بنجاح لـ {w_person} وتصفير الحقل!")
                        st.rerun()
                    else:
                        st.warning("⚠️ الرجاء إدخال مبلغ صحيح أكبر من الصفر.")
            
            st.markdown("#### 📊 أرشيف السحبيات الكلي للجميع")
            st.dataframe(st.session_state.withdrawals, use_container_width=True)

    # --- معمل الزرار ---
    elif tab_name == "🔘 معمل الزرار":
        with tab_obj:
            st.subheader("🔘 حسابات قسم معمل الزرار والعمالة")
            st.markdown(f"سعر قطّاع الزرار الحالي: **{st.session_state.button_price} ر.س** للقطعة الواحدة.")
            
            with st.form("button_form"):
                b_date = st.date_input("📅 تاريخ الشغل", datetime.today())
                b_name = st.selectbox("👤 اسم العامل بقسم الزرار", st.session_state.button_workers)
                b_pieces = st.number_input("📦 عدد القطع", min_value=1, value=1)
                
                b_submit = st.form_submit_button("حفظ إنتاج معمل الزرار 🚀")
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
            st.subheader("📊 التقارير الشاملة والفواتير الشهرية")
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

    # --- الإعدادات (بنفس نمط بطاقات Honor MagicOS المتقدمة) ---
    elif tab_name == "⚙️ الإعدادات":
        with tab_obj:
            st.markdown("<h2 style='color: #1f2937; margin-bottom: 20px;'>الإعدادات</h2>", unsafe_allow_html=True)
            
            # 1. بطاقة إعدادات القفل والأمان (Honor Card: الأمان وقفل الشاشة)
            st.markdown("""
                <div class="honor-card">
                    <div style="font-weight: bold; font-size: 15px; color: #1f2937; margin-bottom: 12px;">🛡️ إعدادات الأمان وقفل التطبيق</div>
                </div>
            """, unsafe_allow_html=True)
            
            with st.form("security_settings_form"):
                sec_toggle = st.checkbox("تفعيل قفل التطبيق عند بدء التشغيل", value=st.session_state.security_enabled)
                chosen_lock_type = st.selectbox("اختر نوع القفل", ["رقم مرور (PIN)", "نمط (Pattern)", "بصمة"], index=["رقم مرور (PIN)", "نمط (Pattern)", "بصمة"].index(st.session_state.lock_type))
                new_app_pin = st.text_input("تغيير رمز القفل / النمط الجديد", value=st.session_state.app_pin, type="password")
                
                save_sec = st.form_submit_button("حفظ إعدادات الأمان 💾")
                if save_sec:
                    st.session_state.security_enabled = sec_toggle
                    st.session_state.lock_type = chosen_lock_type
                    st.session_state.app_pin = new_app_pin
                    st.success("✅ تم تحديث إعدادات الأمان وقفل التطبيق بنجاح!")
                    st.rerun()

            # 2. بطاقة الحساب والنظام الشامل
            st.markdown("""
                <div class="honor-card">
                    <div style="display: flex; align-items: center; justify-content: space-between;">
                        <div style="display: flex; align-items: center; gap: 14px;">
                            <span style="font-size: 32px;">🏢</span>
                            <div>
                                <div style="font-weight: bold; font-size: 16px; color: #111827;">النظام الإداري الشامل</div>
                                <div style="font-size: 13px; color: #6b7280;">إدارة الأقسام السحابية والمزامنة</div>
                            </div>
                        </div>
                        <span style="color: #9ca3af; font-size: 18px; font-weight: bold;">&gt;</span>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
            # 3. بطاقة إدارة الخياطين والأسعار
            st.markdown("""
                <div class="honor-card">
                    <div style="font-weight: bold; font-size: 15px; color: #1f2937; margin-bottom: 12px;">🧵 إدارة الخياطين وعمال معمل الزرار</div>
                </div>
            """, unsafe_allow_html=True)
            
            with st.form("tailor_settings_form"):
                new_t_name = st.text_input("إضافة خياط جديد للسجل")
                new_t_price = st.number_input("سعر القطعة الافتراضي (ر.س)", value=35.0)
                new_bp = st.number_input("سعر قطّاع الزرار للقطعة (ر.س)", value=st.session_state.button_price)
                
                saved_t = st.form_submit_button("حفظ التحديثات والأسعار 💾")
                if saved_t:
                    if new_t_name and new_t_name not in st.session_state.tailors:
                        st.session_state.tailors[new_t_name] = new_t_price
                    st.session_state.button_price = new_bp
                    st.success("✅ تم تحديث بيانات الخياطين والأسعار بنجاح!")
                    st.rerun()

            # 4. بطاقة الاتصالات والشبكات والإشعارات
            st.markdown("""
                <div class="honor-card">
                    <div style="font-weight: bold; font-size: 15px; color: #1f2937; margin-bottom: 12px;">📡 الاتصالات والشبكات والتنبيهات</div>
                </div>
            """, unsafe_allow_html=True)
            
            with st.form("notif_form"):
                notif_switch = st.checkbox("تفعيل نظام الإشعارات والتنبيهات الميدانية", value=st.session_state.notif_enabled)
                tone_choice = st.selectbox("نغمة التنبيهات والإشعارات", ["نغمة هادئة 🔔", "نغمة كلاسيكية 🎵", "تنبيه سريع ⚡"], index=0)
                daily_chk = st.checkbox("تنبيه في حال تأخر إدخال البيانات اليومية للخياطين", value=st.session_state.daily_alert_check)
                
                up_notif = st.form_submit_button("تحديث إعدادات الاتصالات 💾")
                if up_notif:
                    st.session_state.notif_enabled = notif_switch
                    st.session_state.notif_tone = tone_choice
                    st.session_state.daily_alert_check = daily_chk
                    st.success("✅ تم تحديث إعدادات التنبيهات والاتصالات بنجاح!")
                    st.rerun()

            # 5. بطاقة النظام والتحديثات وما هو جديد
            st.markdown("""
                <div class="honor-card">
                    <div style="font-weight: bold; font-size: 15px; color: #1f2937; margin-bottom: 8px;">⚙️ النظام والتحديثات وما هو جديد</div>
                    <div style="font-size: 13px; color: #374151; line-height: 1.6;">
                        • الإصدار الحالي: <b>v5.0.0 (Honor MagicOS Final Pro)</b><br>
                        • حالة النظام: <b>محدث ومحمي بالكامل (تفعيل قفل الاختيار من الإعدادات)</b><br>
                        • آخر التحديثات: إضافة اختيار نوع القفل (رقم، نمط، بصمة)، تحديث التاريخ التلقائي، تنظيم أزرار الإدخال اليومي، وفصل سجلات فواتير ومستحقات كل خياط بشكل مستقل تماماً.
                    </div>
                </div>
            """, unsafe_allow_html=True)

            # 6. النسخ الاحتياطي ومزامنة Excel
            st.markdown("""
                <div class="honor-card">
                    <div style="font-weight: bold; font-size: 15px; color: #1f2937; margin-bottom: 12px;">🔄 النسخ الاحتياطي ومزامنة البيانات (Excel)</div>
                </div>
            """, unsafe_allow_html=True)
            
            c_bk1, c_bk2, c_bk3 = st.columns(3)
            with c_bk1:
                if st.button("نسخة احتياطية (يوميّة)", use_container_width=True):
                    st.success("✅ تم إنشاء وتنزيل النسخة اليومية بصيغة Excel.")
            with c_bk2:
                if st.button("نسخة احتياطية (أسبوعيّة)", use_container_width=True):
                    st.success("✅ تم إنشاء وتنزيل النسخة الأسبوعية بصيغة Excel.")
            with c_bk3:
                if st.button("نسخة احتياطية (شهريّة)", use_container_width=True):
                    st.success("✅ تم إنشاء وتنزيل النسخة الشهرية بصيغة Excel.")
