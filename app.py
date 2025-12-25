import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import arabic_reshaper
from bidi.algorithm import get_display
import os
import uuid
import datetime

# تنظیمات اولیه
st.set_page_config(page_title="دنیای هوشمند درسبان", layout="wide", page_icon="🏫")

# تنظیم فونت فارسی (با فونت fallback)
try:
    font_path = "Vazir.ttf"
    if os.path.exists(font_path):
        fm.fontManager.addfont(font_path)
        font_prop = fm.FontProperties(fname=font_path)
        plt.rcParams['font.family'] = font_prop.get_name()
    else:
        # اگر فونت دانلود نشد، از فونت پیش‌فرض استفاده کن
        plt.rcParams['font.family'] = 'DejaVu Sans'
except:
    pass

plt.rcParams['axes.unicode_minus'] = False

# CSS برای راست‌چین
st.markdown("""
<style>
* {
    direction: rtl;
    text-align: right;
    font-family: 'Vazir', 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

.stButton > button {
    width: 100%;
    border-radius: 10px;
    padding: 10px;
    font-weight: bold;
}

.stTextInput > div > div > input {
    text-align: right;
}

.stSelectbox > div > div > select {
    text-align: right;
}

.sidebar .sidebar-content {
    direction: rtl;
}

.main-header {
    background: linear-gradient(90deg, #4f46e5, #7c3aed);
    color: white;
    padding: 20px;
    border-radius: 10px;
    margin-bottom: 20px;
    text-align: center;
}
</style>
""", unsafe_allow_html=True)

# تابع اصلاح متن فارسی برای نمودارها
def fix_rtl(text):
    if not isinstance(text, str):
        return text
    try:
        reshaped = arabic_reshaper.reshape(text)
        return get_display(reshaped)
    except:
        return text

# --- داده‌های نمونه (Demo Mode) ---
DEMO_MODE = True

if DEMO_MODE:
    # داده‌های دمو
    demo_users = [
        {"نام_کاربر": "admin", "رمز_عبور": "admin123", "نام_کامل": "مدیر سیستم", "نقش": "مدیر سامانه", "مدرسه": "شهید بهشتی"},
        {"نام_کاربر": "teacher1", "رمز_عبور": "teacher123", "نام_کامل": "فاطمه سیفی پور", "نقش": "آموزگار", "مدرسه": "شهید بهشتی"},
        {"نام_کاربر": "student1", "رمز_عبور": "student123", "نام_کامل": "علی محمدی", "نقش": "دانش‌آموز", "مدرسه": "شهید بهشتی", "student": "علی محمدی"}
    ]
    
    demo_scores = [
        {"student": "علی محمدی", "درس": "ریاضی", "نمره": 4, "تاریخ": "2024-01-15"},
        {"student": "علی محمدی", "درس": "ریاضی", "نمره": 3, "تاریخ": "2024-02-20"},
        {"student": "علی محمدی", "درس": "علوم", "نمره": 2, "تاریخ": "2024-01-10"},
        {"student": "رضا کریمی", "درس": "ریاضی", "نمره": 3, "تاریخ": "2024-01-15"},
        {"student": "سارا احمدی", "درس": "ادبیات", "نمره": 4, "تاریخ": "2024-02-01"}
    ]

# --- توابع احراز هویت (Demo) ---
def authenticate(username, password):
    if DEMO_MODE:
        for user in demo_users:
            if user["نام_کاربر"] == username and user["رمز_عبور"] == password:
                return user
    return None

# --- صفحه ورود ---
def login_page():
    st.markdown('<div class="main-header"><h1>🏫 دنیای هوشمند درسبان</h1><p>سیستم مدیریت مدرسه هوشمند</p></div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        with st.container():
            st.subheader("🔐 ورود به سیستم")
            
            username = st.text_input("نام کاربری", key="login_user")
            password = st.text_input("رمز عبور", type="password", key="login_pass")
            
            if st.button("🚪 ورود به پنل", use_container_width=True):
                user = authenticate(username, password)
                if user:
                    st.session_state.user = user
                    st.success("✅ ورود موفقیت‌آمیز!")
                    st.rerun()
                else:
                    st.error("❌ نام کاربری یا رمز عبور اشتباه است")
            
            st.divider()
            
            # اطلاعات دمو
            with st.expander("💡 اطلاعات حساب‌های دمو"):
                st.write("""
                **مدیر سیستم:**
                - کاربری: `admin`
                - رمز: `admin123`
                
                **آموزگار:**
                - کاربری: `teacher1`
                - رمز: `teacher123`
                
                **دانش‌آموز:**
                - کاربری: `student1`
                - رمز: `student123`
                """)
            
            st.markdown("---")
            st.caption("🌸 طراحی شده توسط فاطمه سیفی‌پور | نسخه دمو")

# --- پنل مدیر سیستم (دمو) ---
def show_superadmin_panel():
    st.title("👨‍💼 پنل مدیر سیستم")
    st.markdown("**حالت دمو: تمام داده‌ها نمونه هستند**")
    
    tab1, tab2, tab3 = st.tabs(["🏫 مدیریت مدارس", "👥 مدیریت کاربران", "📊 گزارش‌ها"])
    
    with tab1:
        st.subheader("مدارس نمونه")
        schools = pd.DataFrame([
            {"نام مدرسه": "دبستان شهید بهشتی", "کد مدرسه": "SB1001", "تعداد دانش‌آموزان": 150},
            {"نام مدرسه": "متوسطه علامه حلی", "کد مدرسه": "AH2002", "تعداد دانش‌آموزان": 300},
            {"نام مدرسه": "دبیرستان فرزانگان", "کد مدرسه": "FZ3003", "تعداد دانش‌آموزان": 200}
        ])
        st.dataframe(schools, use_container_width=True)
    
    with tab2:
        st.subheader("کاربران سیستم")
        users_df = pd.DataFrame(demo_users)
        st.dataframe(users_df[["نام_کاربر", "نام_کامل", "نقش", "مدرسه"]], use_container_width=True)
    
    with tab3:
        st.subheader("آمار کلی")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("تعداد مدارس", 3)
        with col2:
            st.metric("تعداد کاربران", len(demo_users))
        with col3:
            st.metric("تعداد دانش‌آموزان", 5)

# --- پنل آموزگار (دمو) ---
def show_teacher_panel():
    user = st.session_state.user
    st.title(f"👩‍🏫 پنل آموزگار: {user['نام_کامل']}")
    
    tab1, tab2, tab3 = st.tabs(["📝 مدیریت نمرات", "📊 گزارش‌های فردی", "📈 آمار کلاسی"])
    
    with tab1:
        st.subheader("ثبت نمره جدید")
        col1, col2, col3 = st.columns(3)
        with col1:
            student = st.selectbox("دانش‌آموز", ["علی محمدی", "رضا کریمی", "سارا احمدی", "مریم حسینی"])
        with col2:
            lesson = st.selectbox("درس", ["ریاضی", "علوم", "ادبیات", "هنر"])
        with col3:
            score = st.selectbox("نمره", [1, 2, 3, 4])
        
        if st.button("✅ ثبت نمره"):
            st.success(f"نمره {score} برای {student} در درس {lesson} ثبت شد")
    
    with tab2:
        st.subheader("گزارش دانش‌آموزان")
        scores_df = pd.DataFrame(demo_scores)
        
        selected_student = st.selectbox("انتخاب دانش‌آموز", scores_df["student"].unique())
        student_scores = scores_df[scores_df["student"] == selected_student]
        
        if not student_scores.empty:
            # نمودار پیشرفت
            fig, ax = plt.subplots(figsize=(10, 4))
            for lesson in student_scores["درس"].unique():
                lesson_data = student_scores[student_scores["درس"] == lesson]
                ax.plot(lesson_data["تاریخ"], lesson_data["نمره"], marker='o', label=fix_rtl(lesson))
            
            ax.set_xlabel(fix_rtl("تاریخ"))
            ax.set_ylabel(fix_rtl("نمره"))
            ax.set_title(fix_rtl(f"روند پیشرفت {selected_student}"))
            ax.legend()
            ax.grid(True, alpha=0.3)
            st.pyplot(fig)
            
            # جدول نمرات
            st.dataframe(student_scores, use_container_width=True)
    
    with tab3:
        st.subheader("آمار کل کلاس")
        scores_df = pd.DataFrame(demo_scores)
        
        # نمودار میانگین نمرات
        avg_scores = scores_df.groupby("درس")["نمره"].mean().reset_index()
        
        fig, ax = plt.subplots(figsize=(8, 4))
        bars = ax.bar([fix_rtl(x) for x in avg_scores["درس"]], avg_scores["نمره"])
        ax.set_xlabel(fix_rtl("درس"))
        ax.set_ylabel(fix_rtl("میانگین نمره"))
        ax.set_title(fix_rtl("میانگین نمرات در دروس مختلف"))
        
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height + 0.05,
                   f'{height:.2f}', ha='center', va='bottom')
        
        st.pyplot(fig)

# --- پنل دانش‌آموز (دمو) ---
def show_student_panel():
    user = st.session_state.user
    student_name = user.get("student", user["نام_کامل"])
    
    st.title(f"🎓 پنل دانش‌آموز: {student_name}")
    
    # کارنامه
    st.subheader("📘 کارنامه تحصیلی")
    
    scores_df = pd.DataFrame([s for s in demo_scores if s["student"] == student_name])
    
    if not scores_df.empty:
        col1, col2 = st.columns(2)
        
        with col1:
            # میانگین نمرات
            avg_score = scores_df["نمره"].mean()
            st.metric("میانگین کل نمرات", f"{avg_score:.2f}")
            
            # بهترین درس
            best_subject = scores_df.groupby("درس")["نمره"].mean().idxmax()
            st.metric("بهترین درس", best_subject)
        
        with col2:
            # نمودار دایره‌ای
            fig, ax = plt.subplots(figsize=(6, 6))
            subject_counts = scores_df["درس"].value_counts()
            ax.pie(subject_counts.values, labels=[fix_rtl(x) for x in subject_counts.index], 
                   autopct='%1.1f%%', startangle=90)
            ax.set_title(fix_rtl("توزیع نمرات در دروس"))
            st.pyplot(fig)
        
        # جدول نمرات
        st.dataframe(scores_df, use_container_width=True)
        
        # دانلود گزارش
        csv = scores_df.to_csv(index=False).encode('utf-8-sig')
        st.download_button(
            label="📥 دانلود کارنامه (CSV)",
            data=csv,
            file_name=f"کارنامه_{student_name}.csv",
            mime="text/csv",
        )
    else:
        st.info("هنوز نمره‌ای برای شما ثبت نشده است.")

# --- داشبورد اصلی ---
def main_dashboard():
    user = st.session_state.user
    role = user.get("نقش", "دانش‌آموز")
    
    # نوار بالایی
    col1, col2 = st.columns([4, 1])
    with col1:
        st.markdown(f"### 👋 خوش آمدید، **{user['نام_کامل']}**")
    with col2:
        if st.button("🚪 خروج"):
            del st.session_state.user
            st.rerun()
    
    st.divider()
    
    # نمایش پنل بر اساس نقش
    if role == "مدیر سامانه":
        show_superadmin_panel()
    elif role == "آموزگار":
        show_teacher_panel()
    elif role == "دانش‌آموز":
        show_student_panel()
    else:
        # پنل عمومی برای سایر نقش‌ها
        st.info(f"پنل {role} در حال توسعه است")

# --- برنامه اصلی ---
def main():
    if "user" not in st.session_state:
        login_page()
    else:
        main_dashboard()

if __name__ == "__main__":
    main()
