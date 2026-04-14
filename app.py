import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import plotly.graph_objects as go
import plotly.express as px

# --- 1. SETTINGS ---
st.set_page_config(page_title="TARYAQ | AI Prediction", page_icon="🏗️", layout="wide")

# --- REGION DATA FOR MAP ---
region_data = {
    "قطاع الرياض": {"lat": 24.7136, "lon": 46.6753, "zoom": 10},
    "نيوم": {"lat": 28.0833, "lon": 34.9500, "zoom": 7},
    "جدة": {"lat": 21.5433, "lon": 39.1728, "zoom": 10},
    "الشرقية": {"lat": 26.2833, "lon": 50.2000, "zoom": 9},
    "عسير": {"lat": 18.2164, "lon": 42.5053, "zoom": 9},
    "Riyadh": {"lat": 24.7136, "lon": 46.6753, "zoom": 10},
    "NEOM": {"lat": 28.0833, "lon": 34.9500, "zoom": 7},
    "Jeddah": {"lat": 21.5433, "lon": 39.1728, "zoom": 10},
    "Eastern": {"lat": 26.2833, "lon": 50.2000, "zoom": 9},
    "Asir": {"lat": 18.2164, "lon": 42.5053, "zoom": 9}
}

# --- TRANSLATIONS DICTIONARY ---
translations = {
    "🇸🇦 AR": {
        "dir": "rtl",
        "align": "right",
        "app_title": "نموذج تنبؤي ذكي لإدارة المشاريع وتقليل التأخيرات",
        "idea_desc_title": "💡 وصف الفكرة",
        "idea_desc": "يقترح هذا المشروع تطوير نموذج ذكاء اصطناعي لتحليل بيانات المشاريع السابقة والتنبؤ بالمخاطر المحتملة مثل التأخيرات أو زيادة التكاليف. يعتمد النموذج على تحليل عوامل مثل الطقس، توفر المواد، أداء العمالة، وسلاسل التوريد. يقوم النظام بإعطاء توصيات استباقية لمديري المشاريع لتجنب المشاكل قبل حدوثها. يمكن دمجه مع برامج إدارة المشاريع مثل Primavera أو BIM لتحقيق تكامل شامل. يساهم هذا الحل في رفع كفاءة إدارة المشاريع وتقليل الهدر الزمني والمالي، مما يعزز الاستدامة الاقتصادية. كما أنه يتماشى مع أهداف الملتقى في تطوير حلول قابلة للتطبيق وتحاكي التحديات الواقعية في قطاع البناء.",
        "sidebar_title": "TARYAQ AI CORE",
        "region": "المنطقة",
        "regions_list": ["قطاع الرياض", "نيوم", "جدة", "الشرقية", "عسير"],
        "scale": "حجم المشروع",
        "scale_list": ["صغير", "متوسط", "كبير", "ضخم"],
        "phase": "المرحلة",
        "phases_list": ["دراسة جدوى", "حفر", "صب خرسانة", "تسليم"],
        "labor_eff": "كفاءة العمالة الحالية",
        "update_btn": "🚀 تحديث البيانات",
        "current_risk": "معدل الخطر الحالي",
        "expected_delay": "التأخير المتوقع",
        "days": "يوم",
        "cost_overrun": "تجاوز التكلفة المتوقع",
        "map_title": "حالة المشروع الجغرافية",
        "kpis": "مؤشرات الأداء (KPIs)",
        "weather": "الطقس",
        "materials": "توفر المواد",
        "labor": "أداء العمالة",
        "supply_chain": "سلاسل التوريد",
        "integration": "تكامل فعال",
        "recommendations": "توصيات استباقية عاجلة",
        "rec_supply": "تأمين مواد بديلة للموقع",
        "rec_supply_desc": "لتفادي نقص التوريد المتوقع في الأسابيع القادمة",
        "rec_weather": "تعديل أوقات العمل لتفادي الإجهاد",
        "rec_weather_desc": "بناءً على التنبؤات المناخية القادمة للمنطقة",
        "footer": "طور بواسطة أحمد محمد المسلم"
    },
    "🇬🇧 EN": {
        "dir": "ltr",
        "align": "left",
        "app_title": "Smart Predictive Model for Project Management",
        "idea_desc_title": "💡 Idea Description",
        "idea_desc": "This project proposes an AI model to analyze past project data and predict potential risks such as delays or cost overruns. It analyzes factors like weather, material availability, labor performance, and supply chains to provide proactive recommendations. It integrates with Primavera or BIM to improve efficiency, reduce time/financial waste, and enhance sustainability.",
        "sidebar_title": "TARYAQ AI CORE",
        "region": "Region",
        "regions_list": ["Riyadh", "NEOM", "Jeddah", "Eastern", "Asir"],
        "scale": "Scale",
        "scale_list": ["Small", "Medium", "Large", "Mega"],
        "phase": "Phase",
        "phases_list": ["Feasibility", "Excavation", "Pouring", "Handover"],
        "labor_eff": "Current Labor Efficiency",
        "update_btn": "🚀 Update Data",
        "current_risk": "Current Risk Rate",
        "expected_delay": "Expected Delay",
        "days": "Days",
        "cost_overrun": "Expected Cost Overrun",
        "map_title": "Geographical Project Status",
        "kpis": "KPIs",
        "weather": "Weather Trend",
        "materials": "Material Availability",
        "labor": "Labor Performance",
        "supply_chain": "Supply Chain",
        "integration": "Active Integration",
        "recommendations": "Urgent Proactive Recommendations",
        "rec_supply": "Secure alternative site materials",
        "rec_supply_desc": "To avoid expected supply shortages in coming weeks",
        "rec_weather": "Adjust working hours",
        "rec_weather_desc": "Based on upcoming climate forecasts for the region",
        "footer": "Developed by Ahmad M. Al Musallem"
    }
}

# --- 2. TOP BAR (Language Selection) ---
col_title, col_lang = st.columns([9, 1])
with col_lang:
    lang_choice = st.selectbox("", ["🇸🇦 AR", "🇬🇧 EN"], label_visibility="collapsed")
    t = translations[lang_choice]
with col_title:
    st.markdown(f"<h2 style='margin-top:-10px; color:var(--text-color);'>{t['app_title']}</h2>", unsafe_allow_html=True)

# --- 3. DYNAMIC CSS ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;500;700&display=swap');
    html, body, [class*="css"] {{
        font-family: 'Tajawal', sans-serif !important;
        direction: {t['dir']};
        text-align: {t['align']};
    }}
    div[data-baseweb="select"] {{
        min-width: 80px !important;
        transform: scale(0.85);
        transform-origin: top right;
    }}
    .dash-card {{
        background-color: var(--secondary-background-color);
        border-radius: 12px; padding: 20px; border: 1px solid var(--faded-text-10);
        height: 100%; display: flex; flex-direction: column; justify-content: center;
    }}
    .metric-value {{ font-size: 28px; font-weight: bold; color: #ef4444; margin-top: 5px; }}
    .metric-title {{ font-size: 14px; opacity: 0.8; font-weight: 500; }}
    .alert-box {{
        background-color: rgba(239, 68, 68, 0.05); border: 1px solid rgba(239, 68, 68, 0.2); 
        padding: 15px; border-radius: 8px; margin-bottom: 10px; display: flex; justify-content: space-between; align-items: center;
    }}
    .integration-box {{
        background-color: rgba(59, 130, 246, 0.05); border: 1px solid rgba(59, 130, 246, 0.2); 
        padding: 15px; border-radius: 8px; text-align: center; font-weight: bold; width: 48%;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- 4. SIDEBAR & LOGIC ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3252/3252119.png", width=50)
    st.markdown(f"### {t['sidebar_title']}")
    
    sel_region = st.selectbox(t["region"], t["regions_list"])
    sel_size = st.selectbox(t["scale"], t["scale_list"])
    sel_phase = st.selectbox(t["phase"], t["phases_list"])
    sel_days = st.number_input(t["days"], min_value=1, value=30)
    sel_labor = st.slider(t["labor_eff"], 0.1, 1.0, 0.85)
    
    st.button(t["update_btn"], use_container_width=True)

# AI Calculation Logic
base_delay = (1.0 - sel_labor) * (sel_days * 0.4)
weather_delay = sel_days * 0.15 if sel_region in ["قطاع الرياض", "نيوم", "Riyadh", "NEOM"] else 0
p_var = round(base_delay + weather_delay, 1)

risk_percentage = min(int((p_var / sel_days) * 100) + 15, 95)
cost_overrun_val = min(int((p_var / sel_days) * 35), 100)

# --- 5. IDEA DESCRIPTION ---
with st.expander(t["idea_desc_title"], expanded=True):
    st.info(t["idea_desc"])

# --- 6. PLOTLY HELPERS ---
def create_gauge(val):
    fig = go.Figure(go.Indicator(
        mode="gauge+number", value=val,
        number={'font': {'size': 26}, 'suffix': "%"},
        gauge={'axis': {'range': [None, 100], 'visible': False},
               'bar': {'color': "#ef4444" if val > 60 else "#eab308"},
               'bgcolor': "rgba(128,128,128,0.2)", 'borderwidth': 0}
    ))
    fig.update_layout(height=160, margin=dict(l=10, r=10, t=10, b=10), paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
    return fig

def create_sparkline(color, volatility=1.0):
    data = np.random.randn(15) * volatility
    data = data.cumsum()
    fig = px.line(y=data)
    fig.update_traces(line_color=color, line_width=3)
    fig.update_layout(height=60, margin=dict(l=0, r=0, t=0, b=0), xaxis_visible=False, yaxis_visible=False, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", showlegend=False)
    return fig

# --- 7. MAIN DASHBOARD ---
# Row 1: Metrics, Map, KPI
c1, c2, c3 = st.columns([1, 2, 1])

with c1:
    st.markdown(f"""
    <div class="dash-card">
        <div>
            <div class="metric-title">{t['current_risk']}</div>
            <div class="metric-value">%{risk_percentage}</div>
        </div>
        <hr style="border-color:var(--faded-text-10); margin: 15px 0;">
        <div>
            <div class="metric-title">{t['expected_delay']}</div>
            <div class="metric-value">{p_var} {t['days']}</div>
        </div>
        <hr style="border-color:var(--faded-text-10); margin: 15px 0;">
        <div>
            <div class="metric-title">{t['cost_overrun']}</div>
            <div class="metric-value">%{cost_overrun_val}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with c2:
    r_data = region_data.get(sel_region, {"lat": 24.7136, "lon": 46.6753, "zoom": 10})
    # محاكاة مناطق حمراء وصفراء في الخريطة بناءً على الخطورة
    df_map = pd.DataFrame({
        'lat': [r_data['lat'], r_data['lat'] + 0.02, r_data['lat'] - 0.01], 
        'lon': [r_data['lon'], r_data['lon'] + 0.03, r_data['lon'] - 0.02], 
        'size': [100, 60, 80],
        'color': ["red", "orange", "red"]
    })
    fig_map = px.scatter_mapbox(df_map, lat="lat", lon="lon", size="size", color="color", 
                                color_discrete_map={"red":"#ef4444", "orange":"#eab308"},
                                zoom=r_data['zoom'], mapbox_style="carto-darkmatter")
    fig_map.update_layout(margin=dict(l=0, r=0, t=0, b=0), height=310, paper_bgcolor="rgba(0,0,0,0)", showlegend=False)
    
    st.markdown('<div class="dash-card" style="padding:10px;">', unsafe_allow_html=True)
    st.markdown(f"<div style='margin-bottom:10px; padding:0 10px; font-weight:bold;'>{t['map_title']} - {sel_region}</div>", unsafe_allow_html=True)
    st.plotly_chart(fig_map, use_container_width=True, config={'displayModeBar': False})
    st.markdown('</div>', unsafe_allow_html=True)

with c3:
    st.markdown('<div class="dash-card">', unsafe_allow_html=True)
    st.markdown(f"<div style='font-weight:bold; margin-bottom:5px;'>{t['kpis']}</div>", unsafe_allow_html=True)
    st.plotly_chart(create_gauge(risk_percentage), use_container_width=True, config={'displayModeBar': False})
    st.markdown(f"""
        <div style="text-align:center; margin-top:-10px;">
            <div style="color:#eab308; font-size:24px; font-weight:bold;">%{cost_overrun_val}</div>
            <div class="metric-title">{t['cost_overrun']}</div>
        </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Row 2: Sparklines
st.markdown("<div style='margin-top:15px;'></div>", unsafe_allow_html=True)
sc1, sc2, sc3, sc4 = st.columns(4)
with sc1:
    st.markdown(f"<div class='dash-card' style='padding:15px;'><div class='metric-title'>{t['weather']}</div>", unsafe_allow_html=True)
    st.plotly_chart(create_sparkline("#3b82f6", 1.5), use_container_width=True, config={'displayModeBar': False})
    st.markdown("</div>", unsafe_allow_html=True)
with sc2:
    st.markdown(f"<div class='dash-card' style='padding:15px;'><div class='metric-title'>{t['materials']}</div>", unsafe_allow_html=True)
    st.plotly_chart(create_sparkline("#10b981", 0.5), use_container_width=True, config={'displayModeBar': False})
    st.markdown("</div>", unsafe_allow_html=True)
with sc3:
    st.markdown(f"<div class='dash-card' style='padding:15px;'><div class='metric-title'>{t['labor']}</div>", unsafe_allow_html=True)
    st.plotly_chart(create_sparkline("#eab308", 0.8), use_container_width=True, config={'displayModeBar': False})
    st.markdown("</div>", unsafe_allow_html=True)
with sc4:
    st.markdown(f"<div class='dash-card' style='padding:15px;'><div class='metric-title'>{t['supply_chain']}</div>", unsafe_allow_html=True)
    st.plotly_chart(create_sparkline("#8b5cf6", 2.0), use_container_width=True, config={'displayModeBar': False})
    st.markdown("</div>", unsafe_allow_html=True)

# Row 3: Integrations & Recommendations
st.markdown("<div style='margin-top:15px;'></div>", unsafe_allow_html=True)
r1, r2 = st.columns([1, 2.05])

with r1:
    st.markdown(f"<div class='dash-card'><div class='metric-title' style='margin-bottom:15px;'>{t['integration']}</div>", unsafe_allow_html=True)
    st.markdown("""
        <div style="display:flex; justify-content:space-between;">
            <div class="integration-box"><span style="color:#ef4444; font-size:20px;">P6</span><br><small>Primavera</small></div>
            <div class="integration-box"><span style="color:#3b82f6; font-size:20px;">BIM</span><br><small>Model</small></div>
        </div>
    """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

with r2:
    st.markdown(f"<div class='dash-card'><div class='metric-title' style='margin-bottom:15px;'>{t['recommendations']}</div>", unsafe_allow_html=True)
    st.markdown(f"""
        <div style="display:flex; gap:15px;">
            <div class="alert-box" style="flex:1;">
                <div>
                    <div style="font-weight:bold; color:#ef4444;">{t['rec_supply']}</div>
                    <div style="font-size:12px; margin-top:4px; opacity:0.8;">{t['rec_supply_desc']}</div>
                </div>
                <div>⚠️</div>
            </div>
            <div class="alert-box" style="flex:1;">
                <div>
                    <div style="font-weight:bold; color:#ef4444;">{t['rec_weather']}</div>
                    <div style="font-size:12px; margin-top:4px; opacity:0.8;">{t['rec_weather_desc']}</div>
                </div>
                <div>⚠️</div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# Footer
st.markdown(f"<div style='text-align:center; padding:20px; opacity:0.6; font-size:12px;'>{t['footer']}</div>", unsafe_allow_html=True)
