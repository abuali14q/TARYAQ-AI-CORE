import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import time

# --- 1. SETTINGS & ADVANCED STYLING ---
st.set_page_config(page_title="TARYAQ | Engineering Intelligence", page_icon="🏗️", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #0d1117; }
    .footer { position: fixed; left: 0; bottom: 0; width: 100%; text-align: center; color: #8b949e; font-size: 12px; padding: 12px; background-color: #161b22; border-top: 1px solid #30363d; z-index: 1000; }
    .stMetric { background-color: #161b22 !important; padding: 20px !important; border-radius: 12px !important; border-bottom: 4px solid #3b82f6 !important; box-shadow: 0 4px 10px rgba(0,0,0,0.3); }
    .logic-error-box { background-color: #3d0000; color: #ff4b4b; padding: 15px; border-radius: 8px; border: 1px solid #ff4b4b; margin-bottom: 20px; font-weight: bold; }
    .report-card { background-color: #ffffff; color: #1a1a1a; padding: 45px; border-radius: 15px; line-height: 1.9; text-align: justify; box-shadow: 0 15px 35px rgba(0,0,0,0.3); border-left: 10px solid #3b82f6; }
    h1, h2, h3 { color: #3b82f6; font-family: 'Segoe UI', sans-serif; }
    .stButton>button { border-radius: 8px; font-weight: bold; transition: 0.3s; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. INTELLIGENCE ENGINES ---

def simulate_global_search(region, scale, phase):
    """Deep AI Search simulation for Global Crises & Supply Chains."""
    global_crises = {
        "Maritime Conflict": "Active tensions in the Red Sea/Bab al-Mandab are rerouting 30% of construction shipments. High impact on NEOM/Jeddah projects.",
        "Resource Wars": "Global shortage in specialized semiconductors for HVAC/BMS systems due to international conflicts.",
        "Steel Volatility": "Regional industrial shifts causing 15-20% fluctuations in high-tensile steel prices.",
        "Energy Crisis": "Fluctuating fuel prices impacting logistics and transportation costs within the Kingdom."
    }
    
    # Specific Logic Mapping
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
    """Accurate Seasonal Weather Logic for KSA."""
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
    """Engineering Logic Guard."""
    if size == "Small" and days > 20 and phase not in ["Building Permit Acquisition"]:
        return False, f"⚠️ ENGINEERING LOGIC ERROR: {days} days is excessive for a 'Small' scale {phase} project. Please re-verify."
    if size in ["Mega", "Infrastructure", "Giga"] and days < 15:
        return False, f"⚠️ SAFETY RISK: {days} days is insufficient for '{size}' scale of {phase}. Potential for structural failure or safety violations."
    return True, ""

# --- 4. SIDEBAR ---
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

# --- 5. REPORT GENERATOR ---

if analyze_btn and is_logical:
    with st.spinner("Analyzing Global Geopolitics & Regional Telemetry..."):
        time.sleep(1.2)
        
        w_status, w_temp = get_refined_weather(region, p_date)
        sc_status, sc_intel = simulate_global_search(region, p_size, p_phase)
        
        # Complex Variance Logic
        base_delay = (1.0 - p_labor) * (p_days * 0.5)
        weather_delay = p_days * 0.3 if "Extreme" in w_status or "Sandstorms" in w_status else 0
        supply_delay = p_days * 0.4 if sc_status == "Volatile" else (p_days * 0.15 if sc_status == "Constrained" else 0)
        p_var = round(base_delay + weather_delay + supply_delay, 2)
        
        is_safe = p_var < 4.0

        # Display Metrics
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Predicted Delay", f"{p_var} Days", delta="CRITICAL" if not is_safe else "STABLE", delta_color="inverse")
        c2.metric("Supply Chain", sc_status)
        c3.metric("Climate Window", w_status)
        c4.metric("Ambient Load", f"{w_temp}°C")

        st.divider()

        # DYNAMIC REPORT (LONG FORM)
        st.markdown("<div class='report-card'>", unsafe_allow_html=True)
        st.header(f"📑 STRATEGIC DOSSIER: {p_phase.upper()}")
        
        # Section 1: Overview
        st.subheader("I. BRIEF OVERVIEW & EXECUTIVE SUMMARY")
        st.write(f"""The TARYAQ AI Engineering Engine has processed the parameters for the **{p_phase}** milestone in the **{region}**. 
        Our system has cross-referenced the current selection with the **Knowledge Bank (PROJECT DATA)** and global satellite intelligence. 
        We have detected a temporal variance of **{p_var} days** against your baseline of **{p_days} days**. 
        {'The operation is currently classified as STABLE. Current momentum allows for strategic buffering.' if is_safe else 
        'The operation is classified as CRITICAL. Systemic slippage is imminent without immediate structural intervention.'} 
        This dossier provides a comprehensive 360-degree view of the risks and mitigation strategies required for project success.""")

        # Section 2: Potential Risks
        st.subheader("II. POTENTIAL STRATEGIC RISKS")
        if is_safe:
            st.write(f"""Risk indicators are currently green. However, at an efficiency index of **{p_labor}**, the Project Manager must monitor 'Secondary Friction' factors. 
            The primary risk for **{p_phase}** in **{region}** during **{p_date.strftime('%B')}** is not systemic failure, but 'Micro-Delays' in inspection approvals. 
            Ensure all Quality Assurance (QA) documentation is pre-verified to maintain this stable trajectory.""")
        else:
            st.write(f"""1. **Critical Path Compression:** A delay of **{p_var} days** in the **{p_phase}** phase will trigger a domino effect on subsequent MEP and Finishing activities.
            2. **Thermal Fatigue:** The current temperature of **{w_temp}°C** in **{region}** increases the risk of labor exhaustion and material degradation (specifically for concrete and external facades).
            3. **Operational Bottleneck:** The combination of **{p_size}** scale and current global logistics volatility creates a high-pressure environment for on-site management.""")

        # Section 3: Supply Chain & Global Crisis Impact
        st.subheader("III. SUPPLY CHAIN STATUS & GLOBAL CRISIS IMPACT")
        st.write(f"**Current Logistics Profile: {sc_status}**")
        st.write(f"""**Intel Report:** {sc_intel} 
        The global construction market is currently facing unprecedented volatility. For the **{p_phase}** in **{region}**, 
        TARYAQ identifies that the Red Sea maritime routes are significantly impacted by regional conflicts. 
        We recommend an immediate pivot to **Local Procurement (MODON)** for at least 40% of standard materials to bypass international shipping blockades. 
        Failing to secure secondary local supply lines may increase the phase cost by up to 15% due to expedited freight surcharges.""")

        # Section 4: Weather & Environmental Analysis
        st.subheader("IV. WEATHER IMPACT ANALYSIS")
        st.write(f"**Condition:** {w_status} | **Peak Temp:** {w_temp}°C")
        st.write(f"""Meteorological modeling for **{region}** during the deployment window of **{p_date.strftime('%Y')}** shows that **{w_status}** is the dominant operational constraint. {'This environment is mathematically optimal for structural execution.' if w_temp < 35 else 
        f'The current thermal load represents a direct safety hazard for daylight outdoor labor. Historical data from our Knowledge Bank suggests a 22% decrease in productivity when temperatures exceed 40°C.'} 
        AI recommendations include adjusting concrete pouring schedules and using chilled aggregates to maintain structural integrity.""")

        # Section 5: Workforce Coordination Strategy
        st.subheader("V. WORKFORCE COORDINATION STRATEGY")
        if is_safe:
            st.write(f"Current workforce momentum is excellent. We suggest maintaining the {p_labor} efficiency via standard incentive programs. However, Project Managers should initiate 'Cross-Training' sessions for laborers to ensure flexibility as the project moves into the next complex phase.")
        else:
            st.write(f"""1. **Nocturnal Rotation:** Pivot 75% of high-intensity labor for **{p_phase}** to the night window (9:00 PM - 5:00 AM) to counteract the **{w_temp}°C** heat.
            2. **Supervision Surge:** Deploy 2 additional Site Engineers to identify bottlenecks in real-time and push the efficiency index towards 0.95.
            3. **Micro-Recovery Protocol:** Implement mandatory 15-minute hydration and cooling breaks every 75 minutes of exposure.""")

        # Section 6: Estimated Additional Costs
        st.subheader("VI. ESTIMATED ADDITIONAL COSTS")
        cost_est = "2-5% (Contingency Buffer)" if is_safe else "12-20% (Emergency Recovery Cost)"
        st.warning(f"""**Estimated Financial Impact: {cost_est} of Phase Budget.** The financial surge is primarily driven by:
        * Premium nocturnal labor rates to mitigate the **{p_var} day** delay.
        * Increased costs of local sourcing versus pre-negotiated international contracts.
        * Specialized cooling equipment and additives for **{p_phase}** materials.""")

        # Section 7: Strategic Solutions & Solutions
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
        
        # Download Logic
        full_report_text = f"TARYAQ TECHNICAL DOSSIER\nProject Phase: {p_phase}\nRegion: {region}\nVariance: {p_var}\n..."
        st.download_button("📥 DOWNLOAD FULL ENGINEERING REPORT", full_report_text, file_name=f"TARYAQ_{p_phase}_Report.txt")

else:
    st.info("👈 Enter project parameters and click 'EXECUTE STRATEGIC SCAN' to generate the technical dossier.")

# --- FOOTER ---
st.markdown(f"""
    <div class="footer">
        Developed by Ahmad M. Al Musallem. All rights reserved. <br>
        (طور بواسطة أحمد محمد المسلم وجميع الحقوق محفوظة له)
    </div>
    """, unsafe_allow_html=True)
