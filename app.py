import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import time

# --- 1. SETTINGS & ADVANCED STYLING - RECREATING THE DASHBOARD STYLE ---
# Set wide layout and dark theme
st.set_page_config(page_title="TARYAQ | ENGINEERING INTELLIGENCE", page_icon="🏗️", layout="wide")

# CSS to mimic the deep dark theme, layout, and panel borders of the dashboard image
st.markdown("""
    <style>
    /* Global Styles */
    .main { 
        background-color: #0c0e12; 
        color: #ccd3e1; 
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    .main-header {
        color: #ccd3e1;
        font-size: 20px;
        padding-bottom: 20px;
        border-bottom: 1px solid #1a1e27;
        margin-bottom: 30px;
    }
    .user-avatar-placeholder {
        height: 40px;
        width: 40px;
        background-color: #ccd3e1;
        border-radius: 50%;
        display: inline-block;
        margin-right: 15px;
        vertical-align: middle;
    }

    /* Container Panels */
    .dashboard-panel {
        background-color: #16191f;
        border-radius: 12px;
        border: 1px solid #1a1e27;
        padding: 20px;
        margin-bottom: 20px;
        color: #ccd3e1;
        box-shadow: 0 4px 10px rgba(0,0,0,0.5);
    }
    .dashboard-panel h3 {
        color: #8996b0;
        font-size: 16px;
        margin-top: 0;
        margin-bottom: 15px;
    }

    /* Metric Styling - Large and with dynamic colors for risk/safe */
    .metric-value {
        font-size: 40px;
        font-weight: bold;
    }
    .metric-red {
        color: #e55353;
    }
    .metric-green {
        color: #1aae3b;
    }
    .metric-yellow {
        color: #f7cc48;
    }
    .metric-label {
        font-size: 14px;
        color: #8996b0;
    }

    /* Specific Dashboard Component Styles */
    .map-placeholder {
        height: 200px;
        background-color: #1a1e27;
        border-radius: 8px;
        display: flex;
        align-items: center;
        justify-content: center;
        color: #ccd3e1;
        font-style: italic;
    }
    .gauge-placeholder {
        height: 150px;
        background-color: #1a1e27;
        border-radius: 8px;
        display: flex;
        align-items: center;
        justify-content: center;
        color: #ccd3e1;
    }

    /* Material circles simulation */
    .material-circles-container {
        display: flex;
        gap: 15px;
    }
    .material-circle {
        height: 30px;
        width: 30px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: bold;
        font-size: 12px;
        color: white;
    }

    /* Recommendations tiles */
    .recommendation-tile {
        background-color: #1a1e27;
        border-radius: 8px;
        padding: 15px;
        color: #ccd3e1;
        border: 1px solid #1a1e27;
    }
    .recommendation-alert-icon {
        color: #e55353;
        margin-right: 10px;
    }
    .recommendation-sub-text {
        font-size: 12px;
        color: #8996b0;
        margin-top: 5px;
    }

    /* Footer and long-form report */
    .footer { position: fixed; left: 0; bottom: 0; width: 100%; text-align: center; color: #8b949e; font-size: 12px; padding: 12px; background-color: #161b22; border-top: 1px solid #30363d; z-index: 1000; }
    .report-card { background-color: #ffffff; color: #1a1a1a; padding: 45px; border-radius: 15px; line-height: 1.9; text-align: justify; box-shadow: 0 15px 35px rgba(0,0,0,0.3); border-left: 10px solid #3b82f6; }
    h1, h2, h3 { color: #3b82f6; font-family: 'Segoe UI', sans-serif; }
    .stButton>button { border-radius: 8px; font-weight: bold; transition: 0.3s; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. INTELLIGENCE ENGINES ---
def simulate_global_search(region, scale, phase):
    global_crises = {
        "Maritime Conflict": "Active tensions in the Red Sea/Bab al-Mandab are rerouting 30% of construction shipments. High impact on NEOM/Jeddah projects.",
        "Resource Wars": "Global shortage in specialized semiconductors for HVAC/BMS systems due to international conflicts.",
        "Steel Volatility": "Regional industrial shifts causing 15-20% fluctuations in high-tensile steel prices.",
        "Energy Crisis": "Fluctuating fuel prices impacting logistics and transportation costs within the Kingdom."
    }
    
    if region in ["NEOM", "Jeddah"]:
        status = "Volatile"
        intel = f"CRITICAL ALERT: {global_crises['Maritime Conflict']} Material deliveries for {phase} delayed by 18-24 days."
    elif region == "Riyadh Sector":
        status = "Constrained"
        intel = f"ALERT: {global_crises['Steel Volatility']} and Energy costs are affecting the local supply chain for {scale} projects."
    else:
        status = "Stable"
        intel = "Supply chain is currently within nominal thresholds. Local MODON hubs are mitigating global friction."
    return status, intel

def get_refined_weather(region, date):
    month = date.month
    if month in [12, 1, 2]: # Winter
        status = "Cold/Freezing" if region in ["Riyadh Sector", "NEOM", "Asir"] else "Clear/Mild"
        temp = 11 if region != "Jeddah" else 22
        if region == "Asir": status = "Dense Fog"
    elif month in [6, 7, 8, 9]: # Summer
        status = "Extreme Heat"
        temp = 47 if region != "Asir" else 29
        if region in ["Jeddah", "Eastern Province"]: status = "Extreme Heat/Humid"
    elif month in [3, 4, 5]: # Spring
        status = "Sandstorms" if region in ["Riyadh Sector", "NEOM"] else "Variable"
        temp = 32
        if region == "Asir": status = "Heavy Rain/Thunderstorms"
    else: # Autumn
        status = "Strong Winds"
        temp = 35
    return status, temp

# --- 3. DATA & VALIDATION ---
phases_list = [
    "Project Feasibility Study", "Architect & Consultant Selection", "Concept Architectural Design",
    "Structural, MEP & Civil Drawings", "Building Permit Acquisition", "Contractor Bidding & Selection",
    "Contract Signing & Bill of Quantities (BOQ)", "Site Handover to Contractor", "Preparation of Shop Drawings",
    "Site Mobilization & Temporary Facilities", "Site Clearing & Grubbing", "Land Surveying & Setting Out",
    "Excavation Works", "Anti-Termite Soil Treatment", "Blinding Concrete (Lean Concrete)",
    "Foundation Waterproofing (Batten)", "Foundation Reinforcement & Formwork", "Pouring Foundation Concrete",
    "Column Neck Reinforcement & Formwork", "Pouring Column Necks", "Bitumen Coating for Underground Structures",
    "Backfilling & Compaction (Layers)", "Ground Beam (Plinth Beam) Construction", "Under-slab MEP Piping Installation",
    "Ground Floor Column Reinforcement", "Pouring Ground Floor Columns", "Slab-on-Grade & Upper Slab Formwork",
    "Slab Reinforcement & Conduit Placement", "Pouring Concrete Slabs", "Masonry Works (Blockwork)",
    "Electrical Conduit Installation (First Fix)", "Plumbing & Drainage Piping (First Fix)", "HVAC Copper Pipe Routing",
    "Door & Window Frame Installation", "Internal Plastering Works", "External Rendering (Plastering)",
    "Firefighting & Gas System Installation", "Roof & Wet Area Waterproofing", "False Ceiling & Gypsum Works",
    "Thermal Insulation for Facades", "Floor & Wall Tiling Works", "Internal Painting (Primer & Putty)",
    "Sanitary Ware Installation", "Electrical Switchgear & Panel Installation", "Lighting Fixture Installation",
    "HVAC Unit Installation (Indoor/Outdoor)", "Joinery (Doors, Windows & Cabinets)", "Final Coat Painting",
    "Post-Construction Cleaning", "Final Inspection & Project Handover"
]

def validate_logic(size, days, phase):
    if size == "Small" and days > 20 and phase not in ["Building Permit Acquisition"]:
        return False, f"⚠️ ENGINEERING LOGIC ERROR: {days} days is excessive for a 'Small' scale {phase} project. Please re-verify."
    if size in ["Mega", "Infrastructure", "Giga"] and days < 15:
        return False, f"⚠️ SAFETY RISK: {days} days is insufficient for '{size}' scale of {phase}. Potential for structural failure or safety violations."
    return True, ""

# --- 4. SIDEBAR - INTEGRATED AS PART OF THE OVERALL UI ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3252/3252119.png", width=70)
    st.title("TARYAQ AI CORE")
    st.markdown("##### *Advanced Infrastructure Intel*")
    st.divider()
    
    region = st.selectbox("Strategic Region", ["Riyadh Sector", "Eastern Province", "NEOM", "Jeddah", "Madinah", "Asir"])
    p_size = st.selectbox("Project Scale", ["Small", "Medium", "Large", "Mega", "Giga", "Infrastructure"])
    p_phase = st.selectbox("Operational Phase (50 Task List)", phases_list)
    p_date = st.date_input("Commencement Date", datetime.now())
    p_days = st.number_input("Target Duration (Days)", min_value=1, value=15)
    p_labor = st.slider("Workforce Efficiency Index", 0.1, 1.0, 0.85)

    is_logical, logic_msg = validate_logic(p_size, p_days, p_phase)
    if not is_logical:
        st.markdown(f"<div class='logic-error-box'>{logic_msg}</div>", unsafe_allow_html=True)

    st.divider()
    analyze_btn = st.button("🚀 EXECUTE STRATEGIC SCAN", use_container_width=True)

# --- 5. MAIN BODY - RECREATING THE DASHBOARD LAYOUT & OUTPUT ---
st.markdown("<div class='main-header'><span class='user-avatar-placeholder'></span> منصه تنبؤ بمخاطر مشاريع البناء (ذكاء اصطناعي) </div>", unsafe_allow_html=True)

if analyze_btn and is_logical:
    with st.spinner("Analyzing Global Geopolitics & Regional Telemetry..."):
        time.sleep(1.2)
        
        w_status, w_temp = get_refined_weather(region, p_date)
        sc_status, sc_intel = simulate_global_search(region, p_size, p_phase)
        
        # Original complex delay calculation logic preserved
        base_delay = (1.0 - p_labor) * (p_days * 0.5)
        weather_delay = p_days * 0.3 if "Extreme" in w_status or "Sandstorms" in w_status else 0
        supply_delay = p_days * 0.4 if sc_status == "Volatile" else (p_days * 0.15 if sc_status == "Constrained" else 0)
        p_var = round(base_delay + weather_delay + supply_delay, 2)
        
        is_safe = p_var < 4.0
        
        # Layout matching the dashboard grid
        row1_col1, row1_col2, row1_col3 = st.columns([1, 2, 1])
        
        with row1_col1:
            st.markdown(f"""
                <div class='dashboard-panel'>
                    <h3>Predicted Key Metrics</h3>
                    <div style='display: flex; gap: 15px; flex-wrap: wrap;'>
                        <div><div class='metric-label'> معدل الخطر الحالي (85%) </div><div class='metric-value'> 85% </div></div>
                        <div><div class='metric-label'> التأخير المتوقع (15 يوم) </div><div class='metric-value metric-red'> {p_var} Days </div></div>
                        <div><div class='metric-label'> تجاوز التكلفة المتوقع (%) </div><div class='metric-value'> 12% </div></div>
                    </div>
                    <div class='metric-label' style='margin-top: 15px;'> * Cost Overrun and Risk Rate are placeholders. Delay is calculated. </div>
                </div>
            """, unsafe_allow_html=True)
            
        with row1_col2:
            st.markdown("""
                <div class='dashboard-panel'>
                    <h3>خريطه المشروع</h3>
                    <div class='map-placeholder'> (Map Placeholder with Risk Zones) </div>
                </div>
            """, unsafe_allow_html=True)
            
        with row1_col3:
            st.markdown("""
                <div class='dashboard-panel'>
                    <h3>KPIs</h3>
                    <div class='gauge-placeholder'> (Gauge Chart Placeholder for Risk) </div>
                    <div class='metric-label'> Risk Rate: Current 85% | Predicted 34% (Placeholders) </div>
                </div>
            """, unsafe_allow_html=True)

        row2_col1, row2_col2, row2_col3, row2_col4 = st.columns(4)
        
        with row2_col1:
            st.markdown("""<div class='dashboard-panel'><h3>الطقس</h3></div>""", unsafe_allow_html=True)
            # Simplified line chart, generic data
            df_weather = pd.DataFrame(np.random.randn(10, 1), columns=['Weather Trend'])
            st.line_chart(df_weather, height=100)
            
        with row2_col2:
            st.markdown("""
                <div class='dashboard-panel'>
                    <h3>توفر المواد</h3>
                    <div class='material-circles-container'>
                        <div class='material-circle' style='background-color: #3b82f6;'> 8% </div>
                        <div class='material-circle' style='background-color: #1aae3b;'> 15% </div>
                        <div class='material-circle' style='background-color: #1aae3b;'> 15% </div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
        with row2_col3:
            st.markdown("""<div class='dashboard-panel'><h3>أداء العماله</h3></div>""", unsafe_allow_html=True)
            # Generic line chart
            df_labor = pd.DataFrame(np.random.randn(10, 1), columns=['Labor Trend'])
            st.line_chart(df_labor, height=100)
            
        with row2_col4:
            st.markdown("""<div class='dashboard-panel'><h3>سلاسل التوريد</h3></div>""", unsafe_allow_html=True)
            # Generic stepped line chart simulation
            df_supply = pd.DataFrame(np.random.randn(10, 1), columns=['Supply Status'])
            st.line_chart(df_supply, height=100)

        row3_col1, row3_col2 = st.columns([1, 3])
        
        with row3_col1:
            st.markdown("""
                <div class='dashboard-panel'>
                    <h3>تكامل النعال</h3>
                    <div style='display: flex; gap: 15px; justify-content: space-around; font-size: 14px;'>
                        <div style='text-align: center;'> Primavera <br> <img src="https://logowik.com/content/uploads/images/primavera8558.logowik.com.webp" style='max-height: 20px;'> </div>
                        <div style='text-align: center;'> BIM <br> <img src="https://static.wixstatic.com/media/f5d134_5a046c827c1b4835a22d861d84813583~mv2.png/v1/fill/w_130,h_130,al_c,q_85,usm_0.66_1.00_0.01,enc_auto/BIM%20Logo.png" style='max-height: 20px;'> </div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
        with row3_col2:
            st.markdown(f"""
                <div class='dashboard-panel'>
                    <h3>توصيات استباقيه عاجله</h3>
                    <div style='display: flex; gap: 10px; flex-wrap: wrap;'>
                        <div class='recommendation-tile'>
                            <div><span class='recommendation-alert-icon'>⚠️</span>تأمين صهاريج مياه إضافية لموقع أ</div>
                            <div class='recommendation-sub-text'> لتخزين الموارد المائية الأساسية</div>
                        </div>
                         <div class='recommendation-tile'>
                            <div><span class='recommendation-alert-icon'>⚠️</span>توفير مولدات طاقة إضافية لموقع أ</div>
                            <div class='recommendation-sub-text'> لتجنب انقطاع التيار الكهربائي في اوقات التشغيل القصوى</div>
                        </div>
                         <div class='recommendation-tile'>
                            <div><span class='recommendation-alert-icon'>⚠️</span>توفير معدات السلامة الشخصية (PPE)</div>
                            <div class='recommendation-sub-text'> لزيادة الوعي بسلامة العمالة</div>
                        </div>
                    </div>
                </div>
            """, unsafe_allow_html=True)

        st.divider()

        # DYNAMIC REPORT (LONG FORM) - Placed below the dashboard section, using calculated data
        st.markdown("<div class='report-card'>", unsafe_allow_html=True)
        st.header(f"📑 STRATEGIC DOSSIER: {p_phase.upper()}")
        
        # Original long-form report logic and Arabic text preserved
        st.subheader("I. BRIEF OVERVIEW & EXECUTIVE SUMMARY")
        st.write(f"""The TARYAQ AI Engineering Engine has processed the parameters for the **{p_phase}** milestone in the **{region}**. 
        Our system has cross-referenced the current selection with the **Knowledge Bank (PROJECT DATA)** and global satellite intelligence. 
        We have detected a temporal variance of **{p_var} days** against your baseline of **{p_days} days**. 
        {'The operation is currently classified as STABLE. Current momentum allows for strategic buffering.' if is_safe else 
        'The operation is classified as CRITICAL. Systemic slippage is imminent without immediate structural intervention.'} 
        This dossier provides a comprehensive 360-degree view of the risks and mitigation strategies required for project success.""")

        st.subheader("II. POTENTIAL STRATEGIC RISKS")
        if is_safe:
            st.write(f"""Risk indicators are currently green. However, at an efficiency index of **{p_labor}**, the Project Manager must monitor 'Secondary Friction' factors. 
            The primary risk for **{p_phase}** in **{region}** during **{p_date.strftime('%B')}** is not systemic failure, but 'Micro-Delays' in inspection approvals. 
            Ensure all Quality Assurance (QA) documentation is pre-verified to maintain this stable trajectory.""")
        else:
            st.write(f"""1. **Critical Path Compression:** A delay of **{p_var} days** in the **{p_phase}** phase will trigger a domino effect on subsequent MEP and Finishing activities.
            2. **Thermal Fatigue:** The current temperature of **{w_temp}°C** in **{region}** increases the risk of labor exhaustion and material degradation (specifically for concrete and external facades).
            3. **Operational Bottleneck:** The combination of **{p_size}** scale and current global logistics volatility creates a high-pressure environment for on-site management.""")

        st.subheader("III. SUPPLY CHAIN STATUS & GLOBAL CRISIS IMPACT")
        st.write(f"**Current Logistics Profile: {sc_status}**")
        st.write(f"""**Intel Report:** {sc_intel} 
        The global construction market is currently facing unprecedented volatility. For the **{p_phase}** in **{region}**, 
        TARYAQ identifies that the Red Sea maritime routes are significantly impacted by regional conflicts. 
        We recommend an immediate pivot to **Local Procurement (MODON)** for at least 40% of standard materials to bypass international shipping blockades. 
        Failing to secure secondary local supply lines may increase the phase cost by up to 15% due to expedited freight surcharges.""")

        st.subheader("IV. WEATHER IMPACT ANALYSIS")
        st.write(f"**Condition:** {w_status} | **Peak Temp:** {w_temp}°C")
        st.write(f"""Meteorological modeling for **{region}** during the deployment window of **{p_date.strftime('%Y')}** shows that **{w_status}** is the dominant operational constraint. {'This environment is mathematically optimal for structural execution.' if w_temp < 35 else 
        f'The current thermal load represents a direct safety hazard for daylight outdoor labor. Historical data from our Knowledge Bank suggests a 22% decrease in productivity when temperatures exceed 40°C.'} 
        AI recommendations include adjusting concrete pouring schedules and using chilled aggregates to maintain structural integrity.""")

        st.subheader("V. WORKFORCE COORDINATION STRATEGY")
        if is_safe:
            st.write(f"Current workforce momentum is excellent. We suggest maintaining the {p_labor} efficiency via standard incentive programs. However, Project Managers should initiate 'Cross-Training' sessions for laborers to ensure flexibility as the project moves into the next complex phase.")
        else:
            st.write(f"""1. **Nocturnal Rotation:** Pivot 75% of high-intensity labor for **{p_phase}** to the night window (9:00 PM - 5:00 AM) to counteract the **{w_temp}°C** heat.
            2. **Supervision Surge:** Deploy 2 additional Site Engineers to identify bottlenecks in real-time and push the efficiency index towards 0.95.
            3. **Micro-Recovery Protocol:** Implement mandatory 15-minute hydration and cooling breaks every 75 minutes of exposure.""")

        st.subheader("VI. ESTIMATED ADDITIONAL COSTS")
        cost_est = "2-5% (Contingency Buffer)" if is_safe else "12-20% (Emergency Recovery Cost)"
        st.warning(f"""**Estimated Financial Impact: {cost_est} of Phase Budget.** The financial surge is primarily driven by:
        * Premium nocturnal labor rates to mitigate the **{p_var} day** delay.
        * Increased costs of local sourcing versus pre-negotiated international contracts.
        * Specialized cooling equipment and additives for **{p_phase}** materials.""")

        st.subheader("VII. STRATEGIC SOLUTIONS & ADVICE")
        if is_safe:
            st.success(f"**MANAGER TIP:** You are ahead of the risk curve. Utilize this buffer to finalize long-lead item orders for the next 3 phases. Your current stability is an asset; don't waste it.")
        else:
            st.markdown(f"""
            * **Buffer Injection:** Inject a safety buffer of **{round(p_var * 1.3, 1)} days** into the master Gantt chart immediately.
            * **Local MODON Sourcing:** Immediately contact verified local suppliers in **{region}** for secondary stock of critical path items.
            * **Thermal Mitigation:** Use liquid nitrogen or ice-shaved aggregates for all concrete and wet-works to ensure adherence to KSA structural standards under **{w_status}** conditions.
            """)

        st.markdown("</div>", unsafe_allow_html=True)
        
        full_report_text = f"TARYAQ TECHNICAL DOSSIER\nProject Phase: {p_phase}\nRegion: {region}\nVariance: {p_var}\n..."
        st.download_button("📥 DOWNLOAD FULL ENGINEERING REPORT", full_report_text, file_name=f"TARYAQ_{p_phase}_Report.txt")

else:
    st.info("👈 Enter project parameters in the sidebar and click 'EXECUTE STRATEGIC SCAN' to generate the technical dossier and dashboard.")

# --- FOOTER --- Preserved as is
st.markdown(f"""
    <div class="footer">
        Developed by Ahmad M. Al Musallem. All rights reserved. <br>
        (طور بواسطة أحمد محمد المسلم  وجميع الحقوق محفوظة له)
    </div>
    """, unsafe_allow_html=True)
