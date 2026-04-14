import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import plotly.graph_objects as go
import plotly.express as px

# --- 1. SETTINGS ---
st.set_page_config(page_title="TARYAQ | AI Prediction", page_icon="🏗️", layout="wide")

# --- TRANSLATIONS DICTIONARY ---
translations = {
    "🇸🇦 AR": {
        "dir": "rtl",
        "align": "right",
        "app_title": "🏢 منصة تنبؤ بمخاطر مشاريع البناء",
        "sidebar_title": "TARYAQ AI CORE",
        "region": "المنطقة",
        "regions_list": ["قطاع الرياض", "نيوم", "جدة", "الشرقية", "عسير"],
        "scale": "حجم المشروع",
        "scale_list": ["صغير", "متوسط", "كبير", "ضخم"],
        "phase": "المرحلة",
        "phases_list": ["دراسة جدوى", "حفر", "صب خرسانة", "تسليم"],
        "update_btn": "🚀 تحديث",
        "current_risk": "الخطر الحالي",
        "expected_delay": "التأخير المتوقع",
        "days": "يوم",
        "cost_overrun": "تجاوز التكلفة",
        "footer": "طور بواسطة أحمد محمد المسلم"
    },
    "🇬🇧 EN": {
        "dir": "ltr",
        "align": "left",
        "app_title": "🏢 Project Risk Prediction Platform",
        "sidebar_title": "TARYAQ AI CORE",
        "region": "Region",
        "regions_list": ["Riyadh", "NEOM", "Jeddah", "Eastern", "Asir"],
        "scale": "Scale",
        "scale_list": ["Small", "Medium", "Large", "Mega"],
        "phase": "Phase",
        "phases_list": ["Feasibility", "Excavation", "Pouring", "Handover"],
        "update_btn": "🚀 Update",
        "current_risk": "Current Risk",
        "expected_delay": "Expected Delay",
        "days": "Days",
        "cost_overrun": "Cost Overrun",
        "footer": "Developed by Ahmad M. Al Musallem"
    }
}

# --- 2. TOP BAR (Language Selection) ---
# إنشاء صف علوي يحتوي على العنوان في جهة واللغة في أقصى الزاوية
col_title, col_lang = st.columns([8, 1])

with col_lang:
    # خيار لغة مصغر جداً وبدون تسمية توضيحية
    lang_choice = st.selectbox("", ["🇸🇦 AR", "🇬🇧 EN"], label_visibility="collapsed")
    t = translations[lang_choice]

with col_title:
    st.markdown(f"<h2 style='margin-top:-10px;'>{t['app_title']}</h2>", unsafe_allow_html=True)

# --- 3. DYNAMIC CSS ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;500;700&display=swap');
    html, body, [class*="css"] {{
        font-family: 'Tajawal', sans-serif !important;
        direction: {t['dir']};
        text-align: {t['align']};
    }}
    /* تصغير حجم صندوق اختيار اللغة */
    div[data-baseweb="select"] {{
        min-width: 80px !important;
        transform: scale(0.85);
        transform-origin: top right;
    }}
    .dash-card {{
        background-color: var(--secondary-background-color);
        border-radius: 12px; padding: 20px; border: 1px solid var(--faded-text-10);
    }}
    .metric-value {{ font-size: 28px; font-weight: bold; color: #ef4444; }}
    </style>
    """, unsafe_allow_html=True)

# --- 4. SIDEBAR ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3252/3252119.png", width=50)
    st.markdown(f"### {t['sidebar_title']}")
    
    region = st.selectbox(t["region"], t["regions_list"])
    p_size = st.selectbox(t["scale"], t["scale_list"])
    p_phase = st.selectbox(t["phase"], t["phases_list"])
    p_date = st.date_input("Start Date", datetime.now())
    p_days = st.number_input(t["days"], min_value=1, value=15)
    
    st.button(t["update_btn"], use_container_width=True)

# --- 5. MAIN CONTENT ---
c1, c2, c3 = st.columns(3)

with c1:
    st.markdown(f"""<div class="dash-card">
        <div style="opacity:0.8;">{t['current_risk']}</div>
        <div class="metric-value">%27</div>
    </div>""", unsafe_allow_html=True)

with c2:
    st.markdown(f"""<div class="dash-card">
        <div style="opacity:0.8;">{t['expected_delay']}</div>
        <div class="metric-value">1.13 {t['days']}</div>
    </div>""", unsafe_allow_html=True)

with c3:
    st.markdown(f"""<div class="dash-card">
        <div style="opacity:0.8;">{t['cost_overrun']}</div>
        <div class="metric-value">%3</div>
    </div>""", unsafe_allow_html=True)

# الخريطة (مثال مبسط)
st.markdown("---")
st.markdown(f"#### {t['region']}: {region}")
df_map = pd.DataFrame({'lat': [24.7136], 'lon': [46.6753]})
st.map(df_map, zoom=10)

# Footer
st.markdown(f"<div style='text-align:center; padding:20px; opacity:0.6;'>{t['footer']}</div>", unsafe_allow_html=True)
