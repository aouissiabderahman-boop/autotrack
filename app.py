import streamlit as st
import pandas as pd
import datetime

# --- إعدادات الصفحة ---
st.set_page_config(page_title="AutoTrack-DZ Link", page_icon="🚗", layout="centered")

# --- محاكاة قاعدة البيانات (في التطبيق الحقيقي نربطها بـ Google Sheets) ---
# سنقوم بإنشاء ملف CSV تجريبي إذا لم يكن موجوداً
try:
    df = pd.read_csv('cars_data.csv')
    # تأكد أن أعمدة البيانات نصية لتجنب مشاكل الأرقام
    df['VIN'] = df['VIN'].astype(str)
except FileNotFoundError:
    data = {
        'VIN': ['123456', 'DZ-2026-99', 'G-550-X'],
        'Customer': ['محمد أمين', 'سارة ب.', 'شركة الرضا'],
        'Car_Model': ['Geely Coolray', 'Changan Uni-K', 'DFSK Glory'],
        'Status': ['في البحر', 'وصلت الميناء', 'تم التسليم'],
        'Ship_Name': ['GLOVIS STAR', 'IVORY ARROW', '-'],
        'Arrival_Date': ['2026-01-15', '2026-01-02', '2025-12-20'],
        'Last_Update': ['2026-01-01', '2026-01-01', '2025-12-25']
    }
    df = pd.DataFrame(data)
    df.to_csv('cars_data.csv', index=False)

# --- دالة لحفظ البيانات ---
def save_data(dataframe):
    dataframe.to_csv('cars_data.csv', index=False)

# --- الواجهة الجانبية (Sidebar) - لوحة التحكم ---
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/3097/3097180.png", width=100)
st.sidebar.title("AutoTrack-DZ 🇩🇿")
page = st.sidebar.radio("اختر الواجهة", ["تتبع طلبيتي 🔍", "دخول الإدارة 🔐"])

# ==========================================
# 1. واجهة العميل (Client Interface)
# ==========================================
if page == "تتبع طلبيتي 🔍":
    st.title("تتبع رحلة سيارتك لحظة بلحظة 🚗")
    st.markdown("أدخل **رقم الهيكل (VIN)** أو **رقم الطلب** لمعرفة مكان سيارتك الآن.")

    search_query = st.text_input("رقم الهيكل / رقم الطلب", placeholder="مثال: DZ-2026-99")

    if st.button("بحث عن السيارة"):
        if search_query:
            result = df[df['VIN'] == search_query]
            
            if not result.empty:
                car = result.iloc[0]
                
                # عرض تفاصيل العميل
                st.success(f"مرحباً بك، **{car['Customer']}**")
                
                # كارت المعلومات
                col1, col2 = st.columns(2)
                with col1:
                    st.info(f"🚘 السيارة: **{car['Car_Model']}**")
                with col2:
                    st.warning(f"📅 موعد الوصول المتوقع: **{car['Arrival_Date']}**")

                # شريط الحالة (Timeline)
                st.markdown("---")
                st.subheader("📍 الحالة الحالية:")
                
                status_list = ["تم تأكيد الطلب", "في البحر", "وصلت الميناء", "تحت الجمركة", "جاهزة للتسليم", "تم التسليم"]
                current_status = car['Status']
                
                # منطق عرض شريط التقدم
                try:
                    step_index = status_list.index(current_status)
                    progress_val = (step_index + 1) / len(status_list)
                    st.progress(progress_val)
                except:
                    st.progress(0)

                # عرض الحالة بتصميم جميل
                if current_status == "في البحر":
                    st.markdown(f"### 🌊 الحالة: {current_status}")
                    st.markdown(f"🚢 اسم الباخرة: **{car['Ship_Name']}**")
                    st.markdown("السيارة تبحر حالياً باتجاه الجزائر.")
                elif current_status == "وصلت الميناء":
                    st.markdown(f"### ⚓ الحالة: {current_status}")
                    st.markdown("السيارة وصلت بسلام وتم تفريغها في الميناء.")
                elif current_status == "تحت الجمركة":
                    st.markdown(f"### 📋 الحالة: {current_status}")
                    st.markdown("ملفك حالياً قيد المعالجة لدى مصالح الجمارك.")
                elif current_status == "جاهزة للتسليم":
                    st.balloons()
                    st.markdown(f"### ✅ الحالة: {current_status}")
                    st.success("مبروك! سيارتك جاهزة للاستلام. يرجى التواصل معنا.")
                else:
                    st.markdown(f"### ℹ️ الحالة: {current_status}")

                st.caption(f"آخر تحديث للنظام: {car['Last_Update']}")

            else:
                st.error("عذراً، لم نجد سيارة بهذا الرقم. يرجى التأكد من الرقم أو التواصل مع الإدارة.")
        else:
            st.warning("يرجى كتابة الرقم أولاً.")

# ==========================================
# 2. واجهة الإدارة (Admin Dashboard)
# ==========================================
elif page == "دخول الإدارة 🔐":
    st.header("لوحة تحكم الموظفين")
    password = st.text_input("كلمة المرور", type="password")

    if password == "admin123":  # كلمة مرور تجريبية
        st.success("تم الدخول بنجاح")
        
        # 1. إضافة سيارة جديدة
        with st.expander("➕ إضافة طلب جديد"):
            new_vin = st.text_input("رقم الهيكل (VIN)")
            new_cust = st.text_input("اسم العميل")
            new_model = st.selectbox("نوع السيارة", ["Geely Coolray", "Changan Uni-K", "Chery Tiggo", "DFSK Glory"])
            
            if st.button("حفظ الطلب"):
                new_row = {
                    'VIN': new_vin, 'Customer': new_cust, 'Car_Model': new_model,
                    'Status': 'تم تأكيد الطلب', 'Ship_Name': '-', 
                    'Arrival_Date': '-', 'Last_Update': str(datetime.date.today())
                }
                df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
                save_data(df)
                st.success("تمت الإضافة!")
                st.rerun()

        # 2. تحديث حالة سيارة
        st.subheader("تحديث الحالات")
        edited_df = st.data_editor(df, num_rows="dynamic")
        
        if st.button("حفظ التغييرات"):
            save_data(edited_df)
            st.success("تم تحديث قاعدة البيانات بنجاح!")
    
    elif password:
        st.error("كلمة المرور خاطئة")

# --- تذييل الصفحة ---
st.markdown("---")
st.markdown("Developed for **Monsieur Accessoires** | Powered by AutoTrack-DZ System")
