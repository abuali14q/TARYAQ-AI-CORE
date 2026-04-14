import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import time
import plotly.graph_objects as go
import plotly.express as px

# --- 1. SETTINGS & ADVANCED STYLING ---
st.set_page_config(page_title="TARYAQ | AI Prediction", page_icon="🏗️", layout="wide")

# Custom CSS for Dark Dashboard Theme & RTL Support
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;500;700&display=swap');
    
    /* Apply RTL and Font */
    html, body, [class*="css"] {
        font-family: 'Tajawal', sans-serif !important;
        direction: rtl;
        text-align: right;
    }
    
    /* Dark Theme Backgrounds */
    .stApp {
        background-color: #12161f;
    }
    
    /* Sidebar adjustments for RTL */
    section[data-testid="stSidebar"] {
        background-color: #1a1e27;
        border-left: 1px solid #2d3342;
    }

    /* Dashboard Cards */
    .dash-card {
        background-color: #1a1e27;
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
        margin-bottom: 20px;
        border: 1px solid #2d3342;
        color: white;
    }
    
    .metric-value {
        font-size: 32px;
        font-weight: bold;
        color: #ef4444; /* Red for high risk, adjust dynamically if needed */
        margin-top: 10px;
        margin-bottom: 5px;
    }
    
    .metric-label {
        font-size: 14px;
        color: #94a3b8;
    }

    .header-title {
        color: white;
        font-size: 28px;
        font-weight: bold;
        margin-bottom: 30px;
        display: flex;
        align-items: center;
        gap: 15px;
    }

    /* Alerts and Recommendations */
    .alert-box {
        background-color: #1a1e27;
        border: 1px solid #2d3342;
        padding: 15px;
        border-radius: 8px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 10px;
        color: #cbd5e1;
    }
    
    .alert-icon {
        color: #ef4444;
        font-size: 20px;
    }

    /* Integration Logos */
    .integration-box {
        background-color: #1a1e27;
        border: 1px solid #2d3342;
        padding: 20px;
        border-radius: 8px;
        text-align: center;
        color: white;
        font-weight: bold;
    }

    .footer { position: fixed; left: 0; bottom: 0; width: 100%; text-align: center; color: #8b949e; font-size: 12px; padding: 12px; background-color: #161b22; z-index: 1000; direction: ltr;}
    </style>
    """, unsafe_allow_html=True)

# --- 2. INTELLIGENCE ENGINES (Your existing logic) ---
def simulate_global_search(region, scale, phase):
    global_crises = {
        "Maritime Conflict": "Active tensions in the Red Sea/Bab al-Mandab are rerouting 30% of construction shipments.",
        "Steel Volatility": "Regional industrial shifts causing 15-20% fluctuations in high-tensile steel prices."
    }
    if region in ["NEOM", "Jeddah"]:
        return "Volatile", f"CRITICAL ALERT: {global_crises['Maritime Conflict']}"
    elif region == "Riyadh Sector":
        return "Constrained", f"ALERT: {global_crises['Steel Volatility']}"
    else:
        return "Stable", "Supply chain is currently within nominal thresholds."

def get_refined_weather(region, date):
    month = date.month
    if month in [6, 7, 8, 9]:
        return "Extreme Heat", 47 if region != "Asir" else 29
    elif month in [12, 1, 2]:
        return "Cold/Freezing", 11 if region != "Jeddah" else 22
    else:
        return "Variable", 32

def validate_logic(size, days, phase):
    if size == "Small" and days > 20:
        return False, f"⚠️ ENGINEERING LOGIC ERROR: {days} days is excessive."
    if size in ["Mega", "Infrastructure", "Giga"] and days < 15:
        return False, f"⚠️ SAFETY RISK: {days} days is insufficient."
    return True, ""

phases_list = ["Project Feasibility Study", "Excavation Works", "Pouring Concrete Slabs", "Final Inspection & Project Handover"]

# --- 3. SIDEBAR INPUTS ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3252/3252119.png", width=70)
    st.markdown("### TARYAQ AI CORE")
    
    region = st.selectbox("المنطقة (Region)", ["Riyadh Sector", "NEOM", "Jeddah", "Eastern Province", "Asir"])
    p_size = st.selectbox("حجم المشروع (Scale)", ["Small", "Medium", "Large", "Mega"])
    p_phase = st.selectbox("المرحلة (Phase)", phases_list)
    p_date = st.date_input("تاريخ البدء (Start Date)", datetime.now())
    p_days = st.number_input("المدة المستهدفة (Days)", min_value=1, value=15)
    p_labor = st.slider("مؤشر كفاءة العمالة (Labor Efficiency)", 0.1, 1.0, 0.85)

    is_logical, logic_msg = validate_logic(p_size, p_days, p_phase)
    if not is_logical:
        st.error(logic_msg)

    analyze_btn = st.button("🚀 تحديث لوحة القيادة (Update Dashboard)", use_container_width=True)

# --- 4. PLOTLY CHART HELPERS ---
def create_gauge(value, title):
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        title={'text': title, 'font': {'color': 'white', 'size': 14}},
        number={'font': {'color': 'white', 'size': 24}, 'suffix': "%"},
        gauge={
            'axis': {'range': [None, 100], 'visible': False},
            'bar': {'color': "#ef4444" if value > 70 else ("#eab308" if value > 40 else "#10b981")},
            'bgcolor': "#2d3342",
            'borderwidth': 0,
        }
    ))
    fig.update_layout(height=180, margin=dict(l=10, r=10, t=30, b=10), paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
    return fig

def create_sparkline(color):
    data = np.random.randn(20).cumsum()
    fig = px.line(y=data)
    fig.update_traces(line_color=color, line_width=3)
    fig.update_layout(height=80, margin=dict(l=0, r=0, t=0, b=0),
                      xaxis_visible=False, yaxis_visible=False,
                      paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", showlegend=False)
    return fig

# --- 5. MAIN DASHBOARD ---
if is_logical:
    # Logic Calculation
    w_status, w_temp = get_refined_weather(region, p_date)
    sc_status, sc_intel = simulate_global_search(region, p_size, p_phase)
    
    base_delay = (1.0 - p_labor) * (p_days * 0.5)
    weather_delay = p_days * 0.3 if "Extreme" in w_status else 0
    supply_delay = p_days * 0.4 if sc_status == "Volatile" else 0
    p_var = round(base_delay + weather_delay + supply_delay, 2)
    
    risk_percentage = min(int((p_var / p_days) * 100) + 20, 99) # Simulated risk %
    cost_overrun = min(int((p_var / p_days) * 40), 100)
    
    # Title
    st.markdown('<div class="header-title">🏢 منصة تنبؤ بمخاطر مشاريع البناء (ذكاء اصطناعي)</div>', unsafe_allow_html=True)
    
    # Top Row: Metrics, Map, KPIs
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col1:
        st.markdown(f"""
        <div class="dash-card">
            <div class="metric-label">معدل الخطر الحالي</div>
            <div class="metric-value">%{risk_percentage}</div>
            <hr style="border-color:#2d3342; margin: 15px 0;">
            <div class="metric-label">التأخير المتوقع ({p_var} يوم)</div>
            <div class="metric-value">{p_var} يوم</div>
            <hr style="border-color:#2d3342; margin: 15px 0;">
            <div class="metric-label">تجاوز التكلفة المتوقع</div>
            <div class="metric-value">%{cost_overrun}</div>
        </div>
        """, unsafe_allow_html=True)
        
    with col2:
        # Simulated Map Visualization using Plotly Scatter Mapbox
        df_map = pd.DataFrame({'lat': [24.7136, 24.7200], 'lon': [46.6753, 46.6800], 'size': [50, 80]})
        fig_map = px.scatter_mapbox(df_map, lat="lat", lon="lon", size="size", color_discrete_sequence=["red"], zoom=12, mapbox_style="carto-darkmatter")
        fig_map.update_layout(margin=dict(l=0, r=0, t=0, b=0), height=320, paper_bgcolor="rgba(0,0,0,0)")
        st.markdown('<div class="dash-card" style="padding: 10px;">', unsafe_allow_html=True)
        st.markdown('<div style="color:white; margin-bottom:10px; font-weight:bold;">حالة المشروع الجغرافية</div>', unsafe_allow_html=True)
        st.plotly_chart(fig_map, use_container_width=True, config={'displayModeBar': False})
        st.markdown('</div>', unsafe_allow_html=True)

    with col3:
        st.markdown('<div class="dash-card" style="height: 340px;">', unsafe_allow_html=True)
        st.markdown('<div style="font-weight:bold; margin-bottom:10px;">KPIs</div>', unsafe_allow_html=True)
        st.plotly_chart(create_gauge(risk_percentage, "معدل الخطر الحالي"), use_container_width=True, config={'displayModeBar': False})
        
        st.markdown(f"""
            <div style="text-align: center; margin-top: -20px;">
                <div style="color: #eab308; font-size: 24px; font-weight: bold;">%{cost_overrun}</div>
                <div class="metric-label">تجاوز التكلفة</div>
            </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # Middle Row: Sparklines
    st.markdown('<div style="margin-top: 10px;"></div>', unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)
    
    with c1:
        st.markdown('<div class="dash-card">', unsafe_allow_html=True)
        st.markdown('<div class="metric-label">الطقس</div>', unsafe_allow_html=True)
        st.plotly_chart(create_sparkline("#3b82f6"), use_container_width=True, config={'displayModeBar': False})
        st.markdown('</div>', unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="dash-card">', unsafe_allow_html=True)
        st.markdown('<div class="metric-label">توفر المواد</div>', unsafe_allow_html=True)
        st.plotly_chart(create_sparkline("#10b981"), use_container_width=True, config={'displayModeBar': False})
        st.markdown('</div>', unsafe_allow_html=True)
    with c3:
        st.markdown('<div class="dash-card">', unsafe_allow_html=True)
        st.markdown('<div class="metric-label">أداء العمالة</div>', unsafe_allow_html=True)
        st.plotly_chart(create_sparkline("#eab308"), use_container_width=True, config={'displayModeBar': False})
        st.markdown('</div>', unsafe_allow_html=True)
    with c4:
        st.markdown('<div class="dash-card">', unsafe_allow_html=True)
        st.markdown('<div class="metric-label">سلاسل التوريد</div>', unsafe_allow_html=True)
        st.plotly_chart(create_sparkline("#8b5cf6"), use_container_width=True, config={'displayModeBar': False})
        st.markdown('</div>', unsafe_allow_html=True)

    # Bottom Row: Recommendations and Integrations
    r1, r2 = st.columns([1, 3])
    
    with r1:
        st.markdown('<div class="dash-card">', unsafe_allow_html=True)
        st.markdown('<div class="metric-label" style="margin-bottom: 15px;">تكامل فعال</div>', unsafe_allow_html=True)
        st.markdown("""
        <div style="display: flex; gap: 10px; justify-content: center;">
            <div class="integration-box" style="flex: 1;"><span style="color:#ef4444;">P6</span><br><small>Primavera</small></div>
            <div class="integration-box" style="flex: 1;"><span style="color:#3b82f6;">BIM</span><br><small>Model</small></div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
    with r2:
        st.markdown('<div class="dash-card">', unsafe_allow_html=True)
        st.markdown('<div class="metric-label" style="margin-bottom: 15px;">توصيات استباقية عاجلة</div>', unsafe_allow_html=True)
        
        # Dynamic Recommendations based on logic
        rec1 = "تأمين مواد بديلة للموقع (Supply Chain Alert)" if sc_status != "Stable" else "الاستمرار في الجدول الزمني المعتمد"
        rec2 = "تعديل جدول صب الخرسانة لتفادي الإجهاد الحراري" if "Extreme" in w_status else "تحديث سجل المخاطر الأسبوعي"
        
        st.markdown(f"""
        <div style="display: flex; gap: 15px;">
            <div class="alert-box" style="flex: 1;">
                <div>
                    <div style="font-weight: bold; color: white;">{rec1}</div>
                    <div style="font-size: 12px; margin-top: 5px;">بناءً على تحليلات توريد المواد الحالية</div>
                </div>
                <div class="alert-icon">⚠️</div>
            </div>
            <div class="alert-box" style="flex: 1;">
                <div>
                    <div style="font-weight: bold; color: white;">{rec2}</div>
                    <div style="font-size: 12px; margin-top: 5px;">بناءً على التنبؤات المناخية للمنطقة</div>
                </div>
                <div class="alert-icon">⚠️</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("""
    <div class="footer">
        Developed by Ahmad M. Al Musallem. All rights reserved. <br>
        (طور بواسطة أحمد محمد المسلم وجميع الحقوق محفوظة له)
    </div>
""", unsafe_allow_html=True)
