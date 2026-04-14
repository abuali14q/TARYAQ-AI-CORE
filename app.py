import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import plotly.graph_objects as go
import plotly.express as px

# --- 1. SETTINGS & ADVANCED STYLING ---
st.set_page_config(page_title="TARYAQ | AI Prediction", page_icon="🏗️", layout="wide")

# --- REGION COORDINATES & DATA ---
region_data = {
    "Riyadh Sector": {"lat": 24.7136, "lon": 46.6753, "zoom": 10, "ar": "قطاع الرياض", "en": "Riyadh Sector"},
    "NEOM": {"lat": 28.0833, "lon": 34.9500, "zoom": 7, "ar": "نيوم", "en": "NEOM"},
    "Jeddah": {"lat": 21.5433, "lon": 39.1728, "zoom": 10, "ar": "جدة", "en": "Jeddah"},
    "Eastern Province": {"lat": 26.2833, "lon": 50.2000, "zoom": 9, "ar": "المنطقة الشرقية", "en": "Eastern Province"},
    "Asir": {"lat": 18.2164, "lon": 42.5053, "zoom": 9, "ar": "عسير", "en": "Asir"}
}

phases_ar = ["دراسة جدوى المشروع", "أعمال الحفر", "صب البلاطات الخرسانية", "الفحص النهائي وتسليم المشروع"]
phases_en = ["Project Feasibility Study", "Excavation Works", "Pouring Concrete Slabs", "Final Inspection"]

# --- TRANSLATIONS DICTIONARY ---
translations = {
    "🇸🇦 العربية": {
        "dir": "rtl",
        "align": "right",
        "app_title": "🏢 منصة تنبؤ بمخاطر مشاريع البناء (ذكاء اصطناعي)",
        "sidebar_title": "TARYAQ AI CORE",
        "region": "المنطقة",
        "regions_list": [r["ar"] for r in region_data.values()],
        "scale": "حجم المشروع",
        "scale_list": ["صغير", "متوسط", "كبير", "ضخم"],
        "phase": "المرحلة",
        "phases_list": phases_ar,
        "start_date": "تاريخ البدء",
        "target_days": "المدة المستهدفة (أيام)",
        "labor_eff": "مؤشر كفاءة العمالة",
        "update_btn": "🚀 تحديث لوحة القيادة",
        "current_risk": "معدل الخطر الحالي",
        "expected_delay": "التأخير المتوقع",
        "days": "يوم",
        "cost_overrun": "تجاوز التكلفة المتوقع",
        "map_title": "حالة المشروع الجغرافية - ",
        "kpis": "مؤشرات الأداء (KPIs)",
        "weather": "الطقس",
        "materials": "توفر المواد",
        "labor": "أداء العمالة",
        "supply_chain": "سلاسل التوريد",
        "integration": "تكامل فعال",
        "recommendations": "توصيات استباقية عاجلة",
        "rec_supply_alert": "تأمين مواد بديلة للموقع",
        "rec_supply_desc": "بناءً على تحليلات توريد المواد الحالية",
        "rec_supply_ok": "الاستمرار في الجدول الزمني المعتمد",
        "rec_weather_alert": "تعديل جدول صب الخرسانة لتفادي الإجهاد الحراري",
        "rec_weather_desc": "بناءً على التنبؤات المناخية للمنطقة",
        "rec_weather_ok": "تحديث سجل المخاطر الأسبوعي",
        "footer": "طور بواسطة أحمد محمد المسلم وجميع الحقوق محفوظة له",
        "ai_insight_title": "🤖 تحليل الذكاء الاصطناعي المباشر:",
        "ai_insight_text": "بناءً على المعطيات في **{0}**، فإن الطقس المتوقع هو **{1}** وحالة سلاسل التوريد **{2}**. نسبة الخطر الحالية **{3}%**."
    },
    "🇬🇧 English": {
        "dir": "ltr",
        "align": "left",
        "app_title": "🏢 Construction Project Risk Prediction (AI)",
        "sidebar_title": "TARYAQ AI CORE",
        "region": "Region",
        "regions_list": [r["en"] for r in region_data.values()],
        "scale": "Project Scale",
        "scale_list": ["Small", "Medium", "Large", "Mega"],
        "phase": "Phase",
        "phases_list": phases_en,
        "start_date": "Start Date",
        "target_days": "Target Duration (Days)",
        "labor_eff": "Labor Efficiency Index",
        "update_btn": "🚀 Update Dashboard",
        "current_risk": "Current Risk Rate",
        "expected_delay": "Expected Delay",
        "days": "Days",
        "cost_overrun": "Expected Cost Overrun",
        "map_title": "Geographical Project Status - ",
        "kpis": "Key Performance Indicators (KPIs)",
        "weather": "Weather",
        "materials": "Material Availability",
        "labor": "Labor Performance",
        "supply_chain": "Supply Chain",
        "integration": "Active Integration",
        "recommendations": "Urgent Proactive Recommendations",
        "rec_supply_alert": "Secure alternative site materials",
        "rec_supply_desc": "Based on current material supply analytics",
        "rec_supply_ok": "Continue with approved schedule",
        "rec_weather_alert": "Adjust concrete pouring to avoid thermal stress",
        "rec_weather_desc": "Based on regional climate forecasts",
        "rec_weather_ok": "Update weekly risk register",
        "footer": "Developed by Ahmad M. Al Musallem. All rights reserved.",
        "ai_insight_title": "🤖 Live AI Analysis:",
        "ai_insight_text": "Based on data for **{0}**, the expected weather is **{1}** and supply chain is **{2}**. Current risk rate is **{3}%**."
    }
}

# --- 2. SIDEBAR & LANGUAGE SELECTION ---
with st.sidebar:
    lang_choice = st.selectbox("🌐 اختر اللغة / Select Language", ["🇸🇦 العربية", "🇬🇧 English"])
    t = translations[lang_choice] 
    is_arabic = lang_choice == "🇸🇦 العربية"
    
    st.image("https://cdn-icons-png.flaticon.com/512/3252/3252119.png", width=70)
    st.markdown(f"### {t['sidebar_title']}")
    
    selected_region_display = st.selectbox(t["region"], t["regions_list"])
    p_size = st.selectbox(t["scale"], t["scale_list"])
    p_phase = st.selectbox(t["phase"], t["phases_list"])
    p_date = st.date_input(t["start_date"], datetime.now())
    p_days = st.number_input(t["target_days"], min_value=1, value=15)
    p_labor = st.slider(t["labor_eff"], 0.1, 1.0, 0.85)

    analyze_btn = st.button(t["update_btn"], use_container_width=True)

# Find internal region key based on selection
internal_region = list(region_data.keys())[t["regions_list"].index(selected_region_display)]

# --- 3. DYNAMIC CSS INJECTION ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;500;700&display=swap');
    
    html, body, [class*="css"] {{
        font-family: 'Tajawal', sans-serif !important;
        direction: {t['dir']};
        text-align: {t['align']};
    }}
    
    .stApp {{ background-color: #12161f; }}
    section[data-testid="stSidebar"] {{ background-color: #1a1e27; border-right: 1px solid #2d3342; border-left: 1px solid #2d3342; }}

    .dash-card {{
        background-color: #1a1e27; border-radius: 12px; padding: 20px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
        margin-bottom: 20px; border: 1px solid #2d3342; color: white;
    }}
    
    .metric-value {{ font-size: 32px; font-weight: bold; color: #ef4444; margin-top: 10px; margin-bottom: 5px; }}
    .metric-label {{ font-size: 14px; color: #94a3b8; }}
    .header-title {{ color: white; font-size: 28px; font-weight: bold; margin-bottom: 20px; display: flex; align-items: center; gap: 15px; }}
    
    .ai-speech-box {{
        background: linear-gradient(90deg, rgba(59,130,246,0.1) 0%, rgba(16,185,129,0.05) 100%);
        border-left: 4px solid #3b82f6; border-right: 4px solid #3b82f6;
        padding: 15px 20px; border-radius: 8px; margin-bottom: 25px; color: #e2e8f0; font-size: 16px;
    }}

    .alert-box {{
        background-color: #1a1e27; border: 1px solid #2d3342; padding: 15px; border-radius: 8px; 
        display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px; color: #cbd5e1;
    }}
    .alert-icon {{ color: #ef4444; font-size: 20px; }}

    .integration-box {{
        background-color: #1a1e27; border: 1px solid #2d3342; padding: 20px; border-radius: 8px; 
        text-align: center; color: white; font-weight: bold;
    }}

    .footer {{ position: fixed; left: 0; bottom: 0; width: 100%; text-align: center; color: #8b949e; font-size: 12px; padding: 12px; background-color: #161b22; z-index: 1000; direction: ltr;}}
    .js-plotly-plot .plotly {{ direction: ltr !important; }}
    </style>
    """, unsafe_allow_html=True)

# --- 4. INTELLIGENCE ENGINES ---
def simulate_global_search(region_key):
    if region_key in ["NEOM", "Jeddah"]: return "Volatile"
    elif region_key == "Riyadh Sector": return "Constrained"
    else: return "Stable"

def get_refined_weather(date):
    month = date.month
    if month in [6, 7, 8, 9]: return "Extreme Heat"
    elif month in [12, 1, 2]: return "Cold"
    else: return "Variable"

# --- 5. PLOTLY CHART HELPERS ---
def create_gauge(value, title):
    fig = go.Figure(go.Indicator(
        mode="gauge+number", value=value,
        title={'text': title, 'font': {'color': 'white', 'size': 14}},
        number={'font': {'color': 'white', 'size': 24}, 'suffix': "%"},
        gauge={
            'axis': {'range': [None, 100], 'visible': False},
            'bar': {'color': "#ef4444" if value > 70 else ("#eab308" if value > 40 else "#10b981")},
            'bgcolor': "#2d3342", 'borderwidth': 0,
        }
    ))
    fig.update_layout(height=180, margin=dict(l=10, r=10, t=30, b=10), paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
    return fig

def create_sparkline(color):
    data = np.random.randn(20).cumsum()
    fig = px.line(y=data)
    fig.update_traces(line_color=color, line_width=3)
    fig.update_layout(height=80, margin=dict(l=0, r=0, t=0, b=0), xaxis_visible=False, yaxis_visible=False, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
    return fig

# --- 6. MAIN DASHBOARD ---
# Logic Calculation
w_status_en = get_refined_weather(p_date)
sc_status_en = simulate_global_search(internal_region)

# Translations for dynamic text
weather_dict = {"Extreme Heat": "حرارة شديدة", "Cold": "بارد", "Variable": "متقلب"}
sc_dict = {"Volatile": "مضطربة", "Constrained": "مقيدة", "Stable": "مستقرة"}

w_status_display = weather_dict[w_status_en] if is_arabic else w_status_en
sc_status_display = sc_dict[sc_status_en] if is_arabic else sc_status_en

base_delay = (1.0 - p_labor) * (p_days * 0.5)
weather_delay = p_days * 0.3 if w_status_en == "Extreme Heat" else 0
supply_delay = p_days * 0.4 if sc_status_en == "Volatile" else 0
p_var = round(base_delay + weather_delay + supply_delay, 2)

risk_percentage = min(int((p_var / p_days) * 100) + 20, 99)
cost_overrun_val = min(int((p_var / p_days) * 40), 100)

# Dashboard Title
st.markdown(f'<div class="header-title">{t["app_title"]}</div>', unsafe_allow_html=True)

# AI Speech Box
ai_text_formatted = t["ai_insight_text"].format(selected_region_display, w_status_display, sc_status_display, risk_percentage)
st.markdown(f"""
<div class="ai-speech-box">
    <strong>{t["ai_insight_title"]}</strong><br>
    {ai_text_formatted}
</div>
""", unsafe_allow_html=True)

# Top Row: Metrics, Map, KPIs
col1, col2, col3 = st.columns([1, 2, 1])

with col1:
    st.markdown(f"""
    <div class="dash-card">
        <div class="metric-label">{t["current_risk"]}</div>
        <div class="metric-value">%{risk_percentage}</div>
        <hr style="border-color:#2d3342; margin: 15px 0;">
        <div class="metric-label">{t["expected_delay"]} ({p_var} {t["days"]})</div>
        <div class="metric-value">{p_var} {t["days"]}</div>
        <hr style="border-color:#2d3342; margin: 15px 0;">
        <div class="metric-label">{t["cost_overrun"]}</div>
        <div class="metric-value">%{cost_overrun_val}</div>
    </div>
    """, unsafe_allow_html=True)
    
with col2:
    # Dynamic Map Based on Region
    r_data = region_data[internal_region]
    df_map = pd.DataFrame({'lat': [r_data['lat']], 'lon': [r_data['lon']], 'size': [100]})
    fig_map = px.scatter_mapbox(df_map, lat="lat", lon="lon", size="size", color_discrete_sequence=["#ef4444"], zoom=r_data['zoom'], mapbox_style="carto-darkmatter")
    fig_map.update_layout(margin=dict(l=0, r=0, t=0, b=0), height=320, paper_bgcolor="rgba(0,0,0,0)")
    
    st.markdown('<div class="dash-card" style="padding: 10px;">', unsafe_allow_html=True)
    st.markdown(f'<div style="color:white; margin-bottom:10px; font-weight:bold;">{t["map_title"]} {selected_region_display}</div>', unsafe_allow_html=True)
    st.plotly_chart(fig_map, use_container_width=True, config={'displayModeBar': False})
    st.markdown('</div>', unsafe_allow_html=True)

with col3:
    st.markdown('<div class="dash-card" style="height: 340px;">', unsafe_allow_html=True)
    st.markdown(f'<div style="font-weight:bold; margin-bottom:10px;">{t["kpis"]}</div>', unsafe_allow_html=True)
    st.plotly_chart(create_gauge(risk_percentage, t["current_risk"]), use_container_width=True, config={'displayModeBar': False})
    st.markdown(f"""
        <div style="text-align: center; margin-top: -20px;">
            <div style="color: #eab308; font-size: 24px; font-weight: bold;">%{cost_overrun_val}</div>
            <div class="metric-label">{t["cost_overrun"]}</div>
        </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Middle Row: Sparklines
c1, c2, c3, c4 = st.columns(4)
with c1:
    st.markdown(f'<div class="dash-card"><div class="metric-label">{t["weather"]}</div>', unsafe_allow_html=True)
    st.plotly_chart(create_sparkline("#3b82f6"), use_container_width=True, config={'displayModeBar': False})
    st.markdown('</div>', unsafe_allow_html=True)
with c2:
    st.markdown(f'<div class="dash-card"><div class="metric-label">{t["materials"]}</div>', unsafe_allow_html=True)
    st.plotly_chart(create_sparkline("#10b981"), use_container_width=True, config={'displayModeBar': False})
    st.markdown('</div>', unsafe_allow_html=True)
with c3:
    st.markdown(f'<div class="dash-card"><div class="metric-label">{t["labor"]}</div>', unsafe_allow_html=True)
    st.plotly_chart(create_sparkline("#eab308"), use_container_width=True, config={'displayModeBar': False})
    st.markdown('</div>', unsafe_allow_html=True)
with c4:
    st.markdown(f'<div class="dash-card"><div class="metric-label">{t["supply_chain"]}</div>', unsafe_allow_html=True)
    st.plotly_chart(create_sparkline("#8b5cf6"), use_container_width=True, config={'displayModeBar': False})
    st.markdown('</div>', unsafe_allow_html=True)

# Bottom Row: Recommendations and Integrations
r1, r2 = st.columns([1, 3])

with r1:
    st.markdown(f'<div class="dash-card"><div class="metric-label" style="margin-bottom: 15px;">{t["integration"]}</div>', unsafe_allow_html=True)
    st.markdown("""
    <div style="display: flex; gap: 10px; justify-content: center;">
        <div class="integration-box" style="flex: 1;"><span style="color:#ef4444;">P6</span><br><small>Primavera</small></div>
        <div class="integration-box" style="flex: 1;"><span style="color:#3b82f6;">BIM</span><br><small>Model</small></div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
with r2:
    st.markdown(f'<div class="dash-card"><div class="metric-label" style="margin-bottom: 15px;">{t["recommendations"]}</div>', unsafe_allow_html=True)
    
    # Dynamic Recommendations
    rec1 = t["rec_supply_alert"] if sc_status_en != "Stable" else t["rec_supply_ok"]
    desc1 = t["rec_supply_desc"] if sc_status_en != "Stable" else ""
    icon1 = "⚠️" if sc_status_en != "Stable" else "✅"
    
    rec2 = t["rec_weather_alert"] if w_status_en == "Extreme Heat" else t["rec_weather_ok"]
    desc2 = t["rec_weather_desc"] if w_status_en == "Extreme Heat" else ""
    icon2 = "⚠️" if w_status_en == "Extreme Heat" else "✅"
    
    st.markdown(f"""
    <div style="display: flex; gap: 15px;">
        <div class="alert-box" style="flex: 1;">
            <div>
                <div style="font-weight: bold; color: white;">{rec1}</div>
                <div style="font-size: 12px; margin-top: 5px;">{desc1}</div>
            </div>
            <div class="alert-icon">{icon1}</div>
        </div>
        <div class="alert-box" style="flex: 1;">
            <div>
                <div style="font-weight: bold; color: white;">{rec2}</div>
                <div style="font-size: 12px; margin-top: 5px;">{desc2}</div>
            </div>
            <div class="alert-icon">{icon2}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown(f"""
    <div class="footer">
        {t["footer"]}
    </div>
""", unsafe_allow_html=True)
