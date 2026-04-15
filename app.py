import streamlit as st
import pandas as pd
import numpy as np
import time
from datetime import datetime
import plotly.graph_objects as go
import plotly.express as px
from ai_analysis import AIProjectAnalyzer

# --- Initialize Session State ---
if 'show_dashboard' not in st.session_state:
    st.session_state.show_dashboard = False
if 'is_loading' not in st.session_state:
    st.session_state.is_loading = False

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
        "app_title": "نموذج تنبؤي "
        " لإدارة المشاريع وتقليل التأخيرات",
        "idea_desc_title": "💡 وصف الفكرة",
        "idea_desc": "يقترح هذا المشروع تطوير نموذج ذكاء اصطناعي لتحليل بيانات المشاريع السابقة والتنبؤ بالمخاطر المحتملة مثل التأخيرات أو زيادة التكاليف. يعتمد النموذج على تحليل عوامل مثل الطقس، توفر المواد، أداء العمالة، وسلاسل التوريد. يقوم النظام بإعطاء توصيات استباقية لمديري المشاريع لتجنب المشاكل قبل حدوثها. يمكن دمجه مع برامج إدارة المشاريع مثل Primavera أو BIM لتحقيق تكامل شامل. يساهم هذا الحل في رفع كفاءة إدارة المشاريع وتقليل الهدر الزمني والمالي، مما يعزز الاستدامة الاقتصادية. كما أنه يتماشى مع أهداف الملتقى في تطوير حلول قابلة للتطبيق وتحاكي التحديات الواقعية في قطاع البناء.",
        "sidebar_title": "استباق",
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
        "temp": "درجة الحرارة",
        "humidity": "الرطوبة",
        "condition": "الحالة",
        "wind": "سرعة الرياح",
        "future_features": "المميزات المستقبلية",
        "future_feature_label": "ميزة مستقبلية",
        "import_xer": "استيراد ملف XER",
        "import_data": "استيراد بيانات ",
        "parameters": "المعطيات",
        "start_date": "تاريخ البدء",
        "project_budget": "ميزانية المشروع (ريال سعودي)",
        "expected_risks": "المخاطر المتوقعة ",
        "footer": "طور بواسطة فريق الشرقيه",
        "inflation_rate": "معدل التضخم المتوقع",
        "carbon_footprint": "البصمة الكربونية",
        "requirements_compliance": "مطابقة الاشتراطات",
        "inflation_unit": "%",
        "carbon_unit": "طن CO₂",
        "compliance_status": "مطابق",
        "compliance_fail": "غير مطابق",
        "report_title": "تقرير تحليلي مفصل",
        "report_intro": "بناءً على المعطيات المدخلة وتحليل نموذج الذكاء الاصطناعي، يظهر المشروع <b>معدل خطر حالي يبلغ {risk_percentage}%</b>. هذا المؤشر يعكس الاحتمالية الكلية لحدوث تحديات قد تؤثر سلباً على سير العمل، ويتأثر بعوامل متعددة مثل كفاءة العمالة، حجم المشروع، والظروف البيئية. يعد فهم هذا المعدل حيويًا لاتخاذ قرارات استباقية للتخفيف من المخاطر المحتملة وضمان استقرار المشروع.",
        "report_delay": "فيما يخص التأخير الزمني، يتوقع النظام <b>تأخيرًا إجماليًا قدره {p_var} {days}</b>. وقد تم تحديد <b>{delay_primary_reason}</b> كسبب رئيسي لهذا التأخير. يشمل تحليل التأخير تقييمًا دقيقًا لتأثير كفاءة العمالة، والظروف الجوية في المنطقة المختارة ({sel_region})، وحجم المشروع ({sel_size})، بالإضافة إلى مدى كفاية الميزانية المخصصة ({sel_budget} ريال سعودي)، وتعقيد المخاطر المتوقعة المدخلة يدويًا. هذه التنبؤات توفر نظرة شاملة للتحديات الزمنية القادمة.",
        "report_cost_overrun": "أما بالنسبة للتكلفة، فالتوقعات تشير إلى <b>تجاوز في التكلفة بنسبة {cost_overrun_val}%</b> من الميزانية الأصلية. يرتبط هذا التجاوز بشكل مباشر بالتأخيرات المتوقعة والعوامل التي تؤثر على كفاءة التنفيذ وتوفر الموارد. يعتبر التحكم في التكلفة وتجنب تجاوزاتها أحد الأهداف الأساسية لأي مشروع ناجح، ويقدم هذا التنبؤ تحذيرًا مبكرًا لإعادة تقييم الميزانيات وتخصيص الموارد بشكل أفضل.",
        "report_environmental_economic": "بخصوص المؤشرات البيئية والاقتصادية، يبلغ <b>معدل التضخم المتوقع {inflation_rate}{inflation_unit}</b>. يتأثر هذا المعدل بمدة المشروع الكلية (على أساس {sel_days} يومًا) والمنطقة الجغرافية، مما يشير إلى التأثيرات الاقتصادية المحتملة على تكاليف المواد والعمالة على المدى الطويل. بالإضافة إلى ذلك، تم تقدير <b>البصمة الكربونية للمشروع بحوالي {carbon_footprint} {carbon_unit}</b>. هذا التقدير يعتمد على حجم المشروع والمنطقة الجغرافية وكفاءة العمالة، ويسلط الضوء على الأثر البيئي للمشروع، مما يدعم مبادرات الاستدامة والامتثال للمعايير البيئية.",
        "report_compliance": "وأخيرًا، يوضح تقييم <b>مطابقة الاشتراطات أن المشروع {compliance_percentage:.0f}% {kpis} {compliance_text}</b> للمعايير المحددة. هذا المؤشر الشامل يجمع بين تقييم كفاءة العمالة، ومدى كفاية الميزانية، وواقعية الجدول الزمني، وتقييم المخاطر، والامتثال البيئي. يشير إلى مدى التزام المشروع بالمتطلبات والمعايير الفنية والتشغيلية، مما يعكس جودة التخطيط والتنفيذ الكلي. يساهم هذا التقرير المفصل في تمكين متخذي القرار من فهم أعمق لوضع المشروع واتخاذ الإجراءات التصحيحية اللازمة لضمان نجاحه واستدامته.",
        "exec_summary_title": "ملخص تنفيذي",
        "exec_summary": "يوضح التحليل الشامل للمشروع معدل خطر حالي بنسبة <b>{risk_percentage}%</b> مع توقعات بتأخير إجمالي قدره <b>{p_var} يوم</b> بسبب <b>{delay_primary_reason}</b>. تشير التقديرات إلى تجاوز في التكلفة بنسبة <b>{cost_overrun_val}%</b> من الميزانية المخصصة البالغة <b>{sel_budget} ريال سعودي</b>. معدل التضخم المتوقع يبلغ <b>{inflation_rate}%</b> والبصمة الكربونية حوالي <b>{carbon_footprint} طن</b>. يحقق المشروع معدل مطابقة للمتطلبات بنسبة <b>{compliance_percentage:.0f}%</b> على مقياس الكفاءة الشامل. يتطلب الوضع الحالي اهتماماً عاجلاً بإدارة سلسلة التوريد وتحسين كفاءة الموارد البشرية.",
        "key_metrics": "المؤشرات الرئيسية",
        "detailed_report_title": "📊 تقرير مفصل",
        "recommendations_title": "🚨 التوصيات الاستباقية العاجلة"
    },
    "🇬🇧 EN": {
        "dir": "ltr",
        "align": "left",
        "app_title": "Smart Predictive Model for Project Management",
        "idea_desc_title": "💡 Idea Description",
        "idea_desc": "This project proposes an AI model to analyze past project data and predict potential risks such as delays or cost overruns. It analyzes factors like weather, material availability, labor performance, and supply chains to provide proactive recommendations. It integrates with Primavera or BIM to improve efficiency, reduce time/financial waste, and enhance sustainability.",
        "sidebar_title": "istabaq",
        "region": "Region",
        "regions_list": ["Riyadh Sector", "Eastern Province", "NEOM", "Jeddah", "Madinah", "Asir"],
        "scale": "Scale",
        "scale_list": ["Small", "Medium", "Large", "Mega", "Giga", "Infrastructure"],
        "phase": "Phase",
        "phases_list": [
    "Project Feasibility Study", "Architect & Consultant Selection", "Concept Architectural Design",
    "Structural, MEP & Civil Drawings", "Building Permit Acquisition", "Contractor Bidding & Selection",
    "Contract Signing & Bill of Quantities (BOQ)", "Site Handover to Contractor", "Preparation of Shop Drawings",
    "Site Mobilization & Temporary Facilities", "Site Clearing & Grubbing", "Land Surveying & Setting Out",
    "Excavation Works", "Anti-Termite Soil Treatment", "Blinding Coذcrete (Lean Concrete)",
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
    "Post-Construction Cleaning", "Final Inspection & Project Handover"],
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
        "temp": "Temperature",
        "humidity": "Humidity",
        "condition": "Condition",
        "wind": "Wind Speed",
        "future_features": "Future Features",
        "future_feature_label": "Future Feature",
        "import_xer": "Import XER File",
        "import_data": "Import Excel/CSV Data",
        "project_budget": "Project Budget (SAR)",
        "expected_risks": "Expected Risks (Text)",
         "footer": "طور بواسطة فريق الشرقيه",
        "parameters": "Parameters",
        "start_date": "Start Date",
        "inflation_rate": "Expected Inflation Rate",
        "carbon_footprint": "Carbon Footprint",
        "requirements_compliance": "Compliance with Regulations",
        "inflation_unit": "%",
        "carbon_unit": "tons CO₂",
        "compliance_status": "Compliant",
        "compliance_fail": "Non-Compliant",
        "report_title": "Detailed Analytical Report",
        "report_intro": "Based on the entered data and the AI model analysis, the project shows a <b>current risk rate of {risk_percentage}%</b>. This indicator reflects the overall probability of encountering challenges that could negatively impact workflow and is influenced by multiple factors such as labor efficiency, project size, and environmental conditions. Understanding this rate is crucial for taking proactive decisions to mitigate potential risks and ensure project stability.",
        "report_delay": "Regarding time delays, the system predicts a <b>total delay of {p_var} {days}</b>. <b>{delay_primary_reason}</b> has been identified as the main reason for this delay. The delay analysis includes a precise evaluation of the impact of labor efficiency, weather conditions in the selected region ({sel_region}), project size ({sel_size}), as well as the adequacy of the allocated budget ({sel_budget} SAR), and the complexity of manually entered expected risks. These predictions provide a comprehensive overview of upcoming temporal challenges.",
        "report_cost_overrun": "As for cost, forecasts indicate a <b>cost overrun of {cost_overrun_val}%</b> of the original budget. This overrun is directly linked to expected delays and factors affecting execution efficiency and resource availability. Controlling costs and avoiding overruns is a primary objective of any successful project, and this prediction provides an early warning to re-evaluate budgets and better allocate resources.",
        "report_environmental_economic": "Concerning environmental and economic indicators, the <b>expected inflation rate is {inflation_rate}{inflation_unit}</b>. This rate is influenced by the total project duration (based on {sel_days} days) and the geographical region, indicating potential economic impacts on material and labor costs in the long term. Additionally, the project's <b>carbon footprint is estimated at {carbon_footprint} {carbon_unit}</b>. This estimation relies on project size, geographical region, and labor efficiency, highlighting the project's environmental impact, which supports sustainability initiatives and compliance with environmental standards.",
        "report_compliance": "Finally, the <b>compliance evaluation shows that the project is {compliance_percentage:.0f}% {kpis} {compliance_text}</b> with the specified standards. This comprehensive indicator combines an assessment of labor efficiency, budget adequacy, schedule realism, risk assessment, and environmental compliance. It indicates the extent of the project's adherence to technical and operational requirements, reflecting the overall quality of planning and execution. This detailed report enables decision-makers to gain a deeper understanding of the project's status and take necessary corrective actions to ensure its success and sustainability.",
        "exec_summary_title": "Executive Summary",
        "exec_summary": "The comprehensive project analysis reveals a <b>current risk rate of {risk_percentage}%</b> with expectations of a total delay of <b>{p_var} days</b> caused by <b>{delay_primary_reason}</b>. Estimates indicate a cost overrun of <b>{cost_overrun_val}%</b> from the allocated budget of <b>{sel_budget} SAR</b>. The expected inflation rate stands at <b>{inflation_rate}%</b> with carbon footprint approximately <b>{carbon_footprint} tons</b>. The project achieves <b>{compliance_percentage:.0f}%</b> compliance rate on the efficiency scale. The current situation requires immediate attention to supply chain management and improving human resource efficiency.",
        "key_metrics": "Key Metrics",
        "detailed_report_title": "📊 Detailed Report",
        "recommendations_title": "🚨 Urgent Recommendations"
    }
}

# --- 2. TOP BAR (Language Selection) ---
top_col1, top_col2, top_col3 = st.columns([8, 1, 1])
with top_col3:
    lang_choice = st.selectbox("", ["🇸🇦 AR", "🇬🇧 EN"], label_visibility="collapsed")
    t = translations[lang_choice]
with top_col1:
    st.markdown(f"<h2 style='margin-top:-10px; margin-bottom:5px; color:var(--text-color); direction:{t['dir']}; text-align:{t['align']};'>Smart Prediction Dashboard</h2>", unsafe_allow_html=True)

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
        transform-origin: top { "left" if t['dir'] == "rtl" else "right"};
    }}
    .dash-card {{
        background: #ffffff;
        border-radius: 12px; padding: 20px; border: 1px solid rgba(0, 0, 0, 0.05);
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03);
        height: 100%; display: flex; flex-direction: column; justify-content: center;
    }}
    @media (prefers-color-scheme: dark) {{
        .dash-card {{
            background: linear-gradient(135deg, rgba(30, 41, 59, 0.7) 0%, rgba(15, 23, 42, 0.7) 100%);
            border-color: rgba(148, 163, 184, 0.2);
            box-shadow: none;
        }}
    }}
    .metric-value {{ font-size: 32px; font-weight: 700; color: #ef4444; margin-top: 8px; }}
    .metric-title {{ font-size: 13px; opacity: 0.75; font-weight: 500; color: rgba(51, 65, 85, 0.85); }}
    @media (prefers-color-scheme: dark) {{
        .metric-title {{ color: rgba(226, 232, 240, 0.75); }}
    }}
    .metric-label {{ font-size: 13px; opacity: 0.65; font-weight: 400; color: rgba(71, 85, 105, 0.7); margin-top: 3px; }}
    @media (prefers-color-scheme: dark) {{
        .metric-label {{ color: rgba(226, 232, 240, 0.6); }}
    }}
    .section-title {{ font-size: 14px; opacity: 0.9; font-weight: 600; color: rgba(30, 41, 59, 0.9); margin-bottom: 12px; }}
    @media (prefers-color-scheme: dark) {{
        .section-title {{ color: rgba(226, 232, 240, 0.85); }}
    }}
    .alert-box {{
        background: #fff5f5; 
        border: 1px solid rgba(239, 68, 68, 0.1); 
        padding: 16px; border-radius: 10px; margin-bottom: 12px; display: flex; justify-content: space-between; align-items: flex-start;
        flex-direction: { "row-reverse" if t['dir'] == "rtl" else "row"};
        gap: 12px;
    }}
    @media (prefers-color-scheme: dark) {{
        .alert-box {{
            background: linear-gradient(135deg, rgba(30, 41, 59, 0.8) 0%, rgba(20, 30, 48, 0.8) 100%);
            border-color: rgba(239, 68, 68, 0.3);
        }}
    }}
    }}
    .alert-title {{ font-weight: 600; color: #ef4444; font-size: 13px; }}
    .alert-desc {{ font-size: 11px; margin-top: 4px; opacity: 0.7; color: rgba(71, 85, 105, 0.7); }}
    @media (prefers-color-scheme: dark) {{
        .alert-desc {{ color: rgba(226, 232, 240, 0.6); }}
    }}
    .integration-box {{
        background: #f8fafc;
        border: 1px solid rgba(59, 130, 246, 0.1); 
        padding: 20px; border-radius: 10px; text-align: center; font-weight: 600; width: 48%;
        color: rgba(30, 41, 59, 0.95);
    }}
    @media (prefers-color-scheme: dark) {{
        .integration-box {{
            background: linear-gradient(135deg, rgba(30, 41, 59, 0.8) 0%, rgba(15, 23, 42, 0.8) 100%);
            color: rgba(226, 232, 240, 0.9);
        }}
    }}
    .future-box {{
        background: #fafafa;
        border: 1px dashed rgba(148, 163, 184, 0.3);
        padding: 15px; border-radius: 10px; text-align: center; height: 100%;
        display: flex; flex-direction: column; justify-content: center; align-items: center;
        transition: all 0.3s ease;
    }}
    .future-label {{
        font-size: 10px; text-transform: uppercase; letter-spacing: 1px;
        background: rgba(148, 163, 184, 0.2); padding: 2px 8px; border-radius: 4px;
        margin-bottom: 8px; opacity: 0.8;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- 4. SIDEBAR & LOGIC ---
with st.sidebar:
    st.image("logo.png", width=80) 
    st.markdown(f"### {t['parameters']}", unsafe_allow_html=True)
    
    # Mandatory inputs with selection dropdown
    sel_region = st.selectbox(t["region"], t["regions_list"])
    sel_size = st.selectbox(t["scale"], t["scale_list"])
    sel_phase = st.selectbox(t["phase"], t["phases_list"])
    sel_start_date = st.date_input(t["start_date"])
    
    sel_days = st.number_input(t["days"], min_value=1, value=30)
    sel_budget = st.number_input(t["project_budget"], min_value=0, value=1000000, step=100000)
    
    # Optional input (risks)
    sel_expected_risks = st.text_area(t["expected_risks"], placeholder=t["expected_risks"], height=150)
    
    # Labor efficiency as number input instead of slider
    sel_labor = st.number_input(t["labor_eff"], min_value=0.1, max_value=1.0, value=0.85, step=0.05)
    
    # Update button
    st.markdown("<div style='margin-top: 20px;'></div>", unsafe_allow_html=True)
    if st.button(t["update_btn"], use_container_width=True, type="primary", key="update_button"):
        st.session_state.is_loading = True
        st.session_state.show_dashboard = False
    
    # Import Features Section
    st.divider()
    st.markdown(f"<div style='text-align:{t['align']}; direction:{t['dir']};'><h4 style='margin-top:10px; margin-bottom:10px;'>🚀 {t['future_features']}</h4></div>", unsafe_allow_html=True)
    
    # Two Import Options with File Upload Buttons
    imp_col1, imp_col2 = st.columns(2)
    
    with imp_col1:
        st.markdown(f"""
            <div style="position:relative; opacity:0.6;">
                <div style="font-weight:600; font-size:12px; color:rgba(30, 41, 59, 0.6); text-align:center; margin-bottom:8px;">
                    <span style="opacity:0.5; font-size:10px;">مستقبلا</span><br>
                    📄 {t['import_xer']}
                </div>
        """, unsafe_allow_html=True)
        st.file_uploader("", type=["xer"], key="xer_upload", disabled=True)
        st.markdown("</div>", unsafe_allow_html=True)
    
    with imp_col2:
        st.markdown(f"""
            <div style="position:relative; opacity:0.6;">
                <div style="font-weight:600; font-size:12px; color:rgba(30, 41, 59, 0.6); text-align:center; margin-bottom:8px;">
                    <span style="opacity:0.5; font-size:10px;">مستقبلا</span><br>
                    📊 {t['import_data']}
                </div>
        """, unsafe_allow_html=True)
        st.file_uploader("", type=["xlsx", "csv"], key="csv_upload", disabled=True)
        st.markdown("</div>", unsafe_allow_html=True)

# --- LOADING STATE ---
if st.session_state.is_loading:
    # Show loading message
    st.markdown("""
    <div style="text-align: center; padding: 60px 20px;">
        <div style="font-size: 48px; margin-bottom: 20px;">⚙️</div>
        <h2 style="color: #334155; margin-bottom: 20px;">جاري التحليل... | Analyzing...</h2>
        <p style="font-size: 16px; color: #64748b; margin-bottom: 20px;">
            يتم معالجة بيانات المشروع بواسطة محرك الذكاء الاصطناعي
        </p>
        <p style="font-size: 14px; color: #94a3b8;">
            Processing project data with AI Engine
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Fake loading indicator with progress bar
    progress_bar = st.progress(0)
    for i in range(4):
        progress_percentage = int((i / 4) * 100)
        progress_bar.progress(progress_percentage)
        time.sleep(1)
    
    progress_bar.progress(100)
    st.session_state.is_loading = False
    st.session_state.show_dashboard = True
    st.rerun()

# --- ADVANCED AI ANALYSIS ENGINE ---
ai_analyzer = AIProjectAnalyzer()

# Calculate advanced delay analysis
delay_analysis = ai_analyzer.calculate_advanced_delay(
    labor_eff=sel_labor,
    region=sel_region,
    size=sel_size,
    budget=sel_budget,
    days=sel_days,
    risk_desc=sel_expected_risks
)

delay_reasons = delay_analysis['components']
total_delay = delay_analysis['total']
p_var = round(total_delay, 1)

# Determine primary reason with AI
primary_reason_key = delay_analysis['primary_factor']
reason_map = {
    "labor": "كفاءة العمالة منخفضة | Low labor efficiency",
    "weather": "تأثر بالعوامل المناخية | Weather impact",
    "scale": "حجم المشروع كبير | Large project scale",
    "budget": "الميزانية غير كافية | Budget constraints",
    "risks": "تعقيدات مخاطر عالية | High risk complexity"
}
delay_primary_reason = reason_map.get(primary_reason_key, "عوامل متعددة | Multiple factors")

# Advanced AI Risk Calculation
risk_percentage = ai_analyzer.calculate_ai_risk_percentage(
    delay=total_delay,
    days=sel_days,
    labor_eff=sel_labor,
    budget=sel_budget
)

# Advanced Cost Overrun Calculation
cost_overrun_val = ai_analyzer.calculate_advanced_cost_overrun(
    delay=total_delay,
    days=sel_days,
    budget=sel_budget,
    labor_eff=sel_labor
)

# Advanced Inflation Rate
inflation_rate = ai_analyzer.calculate_advanced_inflation(
    region=sel_region,
    days=sel_days,
    budget=sel_budget
)

# Advanced Carbon Footprint
carbon_footprint = ai_analyzer.calculate_advanced_carbon(
    region=sel_region,
    size=sel_size,
    days=sel_days,
    labor_eff=sel_labor
)

# Generate AI Insights
ai_insights = ai_analyzer.generate_ai_insights(
    delay_analysis=delay_analysis,
    cost_overrun=cost_overrun_val,
    risk_level=risk_percentage,
    compliance=0  # Will be calculated below
)

# Predict timeline scenarios
timeline_scenarios = ai_analyzer.predict_timeline_scenarios(
    current_delay=total_delay,
    days=sel_days
)

# 3. REQUIREMENTS COMPLIANCE ASSESSMENT
# Scoring system based on project parameters
compliance_score = 0
max_compliance_score = 10

# Check different compliance criteria
# 1. Labor Efficiency (max 2 points)
if sel_labor > 0.85:
    compliance_score += 2
elif sel_labor > 0.70:
    compliance_score += 1

# 2. Budget Adequacy (max 2 points)
budget_per_day = sel_budget / sel_days if sel_days > 0 else 0
if budget_per_day > 50000:
    compliance_score += 2
elif budget_per_day > 20000:
    compliance_score += 1

# 3. Project Duration Realism (max 2 points)
if sel_days <= 365:
    compliance_score += 2
elif sel_days <= 730:
    compliance_score += 1

# 4. Risk Assessment (max 2 points)
if risk_percentage < 30:
    compliance_score += 2
elif risk_percentage < 60:
    compliance_score += 1

# 5. Environmental Compliance (max 2 points)
if carbon_footprint < 100:
    compliance_score += 2
elif carbon_footprint < 300:
    compliance_score += 1

# Determine overall compliance status
compliance_percentage = (compliance_score / max_compliance_score) * 100
is_compliant = compliance_percentage >= 60  # 60% or higher = compliant

# 4. SUPPLY CHAIN STATUS CALCULATION
sc_val = 92
if sel_size in ["ضخم", "Mega"]: sc_val -= 15
elif sel_size in ["كبير", "Large"]: sc_val -= 8
if risk_percentage > 70: sc_val -= 12
elif risk_percentage > 40: sc_val -= 5
supply_chain_status = max(15, min(98, sc_val))

# --- 5. PLOTLY HELPERS ---
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
    """Create an enhanced line chart similar to the reference image"""
    data = np.random.randn(15) * volatility
    data = data.cumsum()
    
    fig = go.Figure()
    
    # Add the line with better styling
    fig.add_trace(go.Scatter(
        y=data,
        mode='lines+markers',
        line=dict(
            color=color,
            width=4,
            shape='spline'
        ),
        marker=dict(
            size=8,
            color=color,
            line=dict(width=2, color='white')
        ),
        fill='tozeroy',
        fillcolor=f'rgba({int(color[1:3], 16)}, {int(color[3:5], 16)}, {int(color[5:7], 16)}, 0.1)',
        hovertemplate='<b>Value:</b> %{y:.1f}<extra></extra>'
    ))
    
    fig.update_layout(
        height=150,
        margin=dict(l=0, r=0, t=5, b=0),
        xaxis=dict(
            visible=False,
            showgrid=False,
            zeroline=False
        ),
        yaxis=dict(
            visible=True,
            showgrid=True,
            gridwidth=1,
            gridcolor='rgba(200, 200, 200, 0.2)',
            zeroline=False
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        showlegend=False,
        hovermode='x unified'
    )
    
    return fig, data

def create_kpi_line_chart(value, color, max_val=100):
    """Create a line chart for KPI display"""
    # Generate realistic data for the trend
    trend_data = np.linspace(max_val * 0.3, value, 12)
    trend_data = trend_data + np.random.randn(12) * (max_val * 0.05)
    trend_data = np.clip(trend_data, 0, max_val)
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        y=trend_data,
        mode='lines+markers',
        line=dict(
            color=color,
            width=3,
            shape='spline'
        ),
        marker=dict(
            size=6,
            color=color,
            line=dict(width=1, color='white')
        ),
        fill='tozeroy',
        fillcolor=f'rgba({int(color[1:3], 16)}, {int(color[3:5], 16)}, {int(color[5:7], 16)}, 0.08)',
        hovertemplate='<b>Trend:</b> %{y:.0f}%<extra></extra>'
    ))
    
    fig.update_layout(
        height=120,
        margin=dict(l=0, r=0, t=5, b=0),
        xaxis=dict(visible=False, showgrid=False),
        yaxis=dict(
            visible=True,
            showgrid=True,
            gridwidth=0.5,
            gridcolor='rgba(200, 200, 200, 0.15)',
            range=[0, max_val],
            zeroline=False
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        showlegend=False
    )
    
    return fig

def get_weather_data(region):
    """Get weather information for the selected region"""
    weather_info = {
        "قطاع الرياض": {"temp": "38°C", "condition": "صافي", "humidity": "25%", "wind": "15 كم/س"},
        "Riyadh": {"temp": "38°C", "condition": "Clear", "humidity": "25%", "wind": "15 km/h"},
        "نيوم": {"temp": "32°C", "condition": "صافي جزئياً", "humidity": "35%", "wind": "20 كم/س"},
        "NEOM": {"temp": "32°C", "condition": "Partly Clear", "humidity": "35%", "wind": "20 km/h"},
        "جدة": {"temp": "34°C", "condition": "غائم", "humidity": "65%", "wind": "18 كم/س"},
        "Jeddah": {"temp": "34°C", "condition": "Cloudy", "humidity": "65%", "wind": "18 km/h"},
        "الشرقية": {"temp": "36°C", "condition": "صافي", "humidity": "40%", "wind": "12 كم/س"},
        "Eastern": {"temp": "36°C", "condition": "Clear", "humidity": "40%", "wind": "12 km/h"},
        "عسير": {"temp": "28°C", "condition": "ممطر", "humidity": "55%", "wind": "25 كم/س"},
        "Asir": {"temp": "28°C", "condition": "Rainy", "humidity": "55%", "wind": "25 km/h"}
    }
    return weather_info.get(region, {"temp": "N/A", "condition": "N/A", "humidity": "N/A", "wind": "N/A"})

def create_kpi_donut(value, color, max_val=100):
    fig = go.Figure(go.Pie(
        values=[value, max_val-value],
        labels=['', ''],
        hole=0.7,
        marker_colors=[color, '#f0f0f0'],
        textinfo='none',
        sort=False
    ))
    fig.update_layout(
        showlegend=False,
        margin=dict(l=0, r=0, t=0, b=0),
        height=100,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    return fig

# --- 7. MAIN DASHBOARD ---
# Show dashboard automatically with real-time updates
if st.session_state.show_dashboard:
    # Executive Summary
    st.markdown(f"""
<div class="dash-card" style="padding:15px; margin-bottom:15px; background: linear-gradient(135deg, #f0f4ff 0%, #fffbf0 100%); border-left: 4px solid #3b82f6;">
    <div style="font-weight: 600; margin-bottom: 10px; font-size: 16px;">📋 {t.get('exec_summary_title', t.get('exec_summary', 'ملخص تنفيذي | Executive Summary'))}</div>
    <p style="margin: 0; line-height: 1.6; font-size: 13px; color: #333; direction:{t['dir']}; text-align:{t['align']};">
        {t['exec_summary'].format(risk_percentage=risk_percentage, p_var=p_var, delay_primary_reason=delay_primary_reason, cost_overrun_val=cost_overrun_val, sel_budget=sel_budget, inflation_rate=inflation_rate, carbon_footprint=carbon_footprint, compliance_percentage=compliance_percentage)}
    </p>
</div>
""", unsafe_allow_html=True)

    # Row 1: KPIs Grid Layout
    st.markdown(f"<h3 style='margin: 15px 0 10px 0; direction:{t['dir']}; text-align:{t['align']};'>{t['key_metrics']}</h3>", unsafe_allow_html=True)

    # KPI Data: (emoji, label, value, max_value, color_logic_func, status_func, suffix)
    kpi_configs = [
        ('⚠️', t['current_risk'], risk_percentage, 100, 
         lambda v: '#ef4444' if v > 60 else '#eab308' if v > 30 else '#10b981',
         lambda v: 'Critical' if v > 60 else 'Warning' if v > 30 else 'Low', '%'),
        
        ('⏱️', t['expected_delay'], p_var, 50,
         lambda v: '#ef4444' if v > 30 else '#eab308' if v > 15 else '#10b981',
         lambda v: 'Severe' if v > 30 else 'Moderate' if v > 15 else 'Minor', t['days']),
        
        ('💰', t['cost_overrun'], cost_overrun_val, 100,
         lambda v: '#ef4444' if v > 30 else '#eab308' if v > 10 else '#10b981',
         lambda v: 'Critical' if v > 30 else 'Warning' if v > 10 else 'Good', '%'),
        
        ('👷', t['labor_eff'], round(sel_labor*100), 100,
         lambda v: '#10b981' if v > 85 else '#eab308' if v > 70 else '#ef4444',
         lambda v: 'Excellent' if v > 85 else 'Average' if v > 70 else 'Poor', '%'),
        
        ('📈', t['inflation_rate'], inflation_rate, 8,
         lambda v: '#ef4444' if v > 4.5 else '#eab308' if v > 2.5 else '#10b981',
         lambda v: 'High' if v > 4.5 else 'Moderate' if v > 2.5 else 'Low', t['inflation_unit']),
        
        ('🚚', t['supply_chain'], supply_chain_status, 100,
         lambda v: '#10b981' if v > 80 else '#eab308' if v > 55 else '#ef4444',
         lambda v: 'Stable' if v > 80 else 'Caution' if v > 55 else 'Disrupted', '%'),
    ]

    # Display KPis in 3x2 grid
    kpi_cols = st.columns(3)
    for idx, (emoji, label, value, max_val, color_func, status_func, suffix) in enumerate(kpi_configs):
        col_idx = idx % 3
        color = color_func(value)
        status = status_func(value)
        
        with kpi_cols[col_idx]:
            # Card container with dynamic background color
            st.markdown(f"""
            <div style="background-color:{color}15; border:2px solid {color}; border-radius:12px; padding:16px; margin-bottom:12px;">
                <div style="display:flex; justify-content:space-between; align-items:top; margin-bottom:10px;">
                    <div style="font-size:18px; font-weight:600;">{emoji} {label}</div>
                    <div style="font-size:12px; font-weight:600; color:{color}; background-color:{color}25; padding:4px 8px; border-radius:6px;">{status}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Line chart instead of donut
            fig_kpi = create_kpi_line_chart(value, color, max_val)
            st.plotly_chart(fig_kpi, use_container_width=True, config={'displayModeBar': False})
            
            # Display value
            st.markdown(f"""
            <div style="text-align: center; padding: 10px 0;">
                <div style="font-size:28px; font-weight:700; color:{color};">{value}{suffix}</div>
                <div style="font-size:11px; color:#666; margin-top:4px;">Current Value</div>
            </div>
            """, unsafe_allow_html=True)
            
            # Spacing between rows
            if (idx + 1) % 3 == 0:
                st.markdown("<div style='margin-bottom:8px;'></div>", unsafe_allow_html=True)

    # Row 2: Sparklines with numeric values
    st.markdown("<div style='margin-top:10px;'></div>", unsafe_allow_html=True)
    sp1, sp2, sp3, sp4 = st.columns(4)

    # Supply Chain - Calculate value based on region and delay
    supply_chain_value = int(80 - (total_delay * 0.5))
    if sel_region in ["قطاع الرياض", "نيوم", "Riyadh", "NEOM"]:
        supply_chain_value = max(60, supply_chain_value - 10)
    
    fig_weather, data_weather = create_sparkline("#3b82f6", 1.5)
    with sp1:
        st.markdown(f"<div class='dash-card' style='padding:10px;'>", unsafe_allow_html=True)
        st.markdown(f"<div class='section-title' style='margin-bottom:8px;'>🚛 {t['supply_chain']}</div>", unsafe_allow_html=True)
        st.plotly_chart(fig_weather, use_container_width=True, config={'displayModeBar': False})
        st.markdown(f"""
        <div style="text-align: center; padding-top: 5px; border-top: 1px solid rgba(59, 130, 246, 0.2);">
            <div style="font-size: 20px; font-weight: 700; color: #3b82f6;">{supply_chain_value}%</div>
            <div style="font-size: 11px; opacity: 0.7;">Availability</div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # Labor Performance - Based on labor efficiency input
    labor_performance = int(sel_labor * 100)
    
    fig_materials, data_materials = create_sparkline("#10b981", 0.5)
    with sp2:
        st.markdown(f"<div class='dash-card' style='padding:10px;'>", unsafe_allow_html=True)
        st.markdown(f"<div class='section-title' style='margin-bottom:8px;'>👷 {t['labor']}</div>", unsafe_allow_html=True)
        st.plotly_chart(fig_materials, use_container_width=True, config={'displayModeBar': False})
        st.markdown(f"""
        <div style="text-align: center; padding-top: 5px; border-top: 1px solid rgba(16, 185, 129, 0.2);">
            <div style="font-size: 20px; font-weight: 700; color: #10b981;">{labor_performance}%</div>
            <div style="font-size: 11px; opacity: 0.7;">Efficiency</div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # Material Availability - Based on project size
    size_multiplier = {"صغير": 90, "متوسط": 80, "كبير": 70, "ضخم": 60, "Small": 90, "Medium": 80, "Large": 70, "Mega": 60, "Giga": 50, "Infrastructure": 55}
    material_availability = size_multiplier.get(sel_size, 75)
    
    fig_labor, data_labor = create_sparkline("#eab308", 0.8)
    with sp3:
        st.markdown(f"<div class='dash-card' style='padding:10px;'>", unsafe_allow_html=True)
        st.markdown(f"<div class='section-title' style='margin-bottom:8px;'>🔨 {t['materials']}</div>", unsafe_allow_html=True)
        st.plotly_chart(fig_labor, use_container_width=True, config={'displayModeBar': False})
        st.markdown(f"""
        <div style="text-align: center; padding-top: 5px; border-top: 1px solid rgba(234, 179, 8, 0.2);">
            <div style="font-size: 20px; font-weight: 700; color: #eab308;">{material_availability}%</div>
            <div style="font-size: 11px; opacity: 0.7;">Available</div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # Weather Information Display
    weather_data = get_weather_data(sel_region)
    with sp4:
        st.markdown(f"<div class='dash-card' style='padding:10px;'>", unsafe_allow_html=True)
        st.markdown(f"<div class='section-title' style='margin-bottom:8px;'>☁️ {t['weather']}</div>", unsafe_allow_html=True)
        st.markdown(f"""
        <div style="background-color: rgba(139, 92, 246, 0.05); border-radius: 8px; padding: 12px; border: 1px solid rgba(139, 92, 246, 0.2);">
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px; font-size: 13px;">
                <div>
                    <div style="opacity: 0.7; font-size: 11px; margin-bottom: 3px;">🌡️ {t.get('temp', 'Temperature')}</div>
                    <div style="font-weight: 600; color: #8b5cf6; font-size: 14px;">{weather_data['temp']}</div>
                </div>
                <div>
                    <div style="opacity: 0.7; font-size: 11px; margin-bottom: 3px;">📊 {t.get('humidity', 'Humidity')}</div>
                    <div style="font-weight: 600; color: #8b5cf6; font-size: 14px;">{weather_data['humidity']}</div>
                </div>
                <div>
                    <div style="opacity: 0.7; font-size: 11px; margin-bottom: 3px;">🌥️ {t.get('condition', 'Condition')}</div>
                    <div style="font-weight: 600; color: #8b5cf6; font-size: 12px;">{weather_data['condition']}</div>
                </div>
                <div>
                    <div style="opacity: 0.7; font-size: 11px; margin-bottom: 3px;">💨 {t.get('wind', 'Wind')}</div>
                    <div style="font-weight: 600; color: #8b5cf6; font-size: 14px;">{weather_data['wind']}</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # Row 3: Map, Compliance, Integration
    st.markdown("<div style='margin-top:10px;'></div>", unsafe_allow_html=True)
    map_col, info_col = st.columns([2, 1])

    with map_col:
        r_data = region_data.get(sel_region, {"lat": 24.7136, "lon": 46.6753, "zoom": 10})
        df_map = pd.DataFrame({
            'lat': [r_data['lat'], r_data['lat'] + 0.02, r_data['lat'] - 0.01], 
            'lon': [r_data['lon'], r_data['lon'] + 0.03, r_data['lon'] - 0.02], 
            'size': [100, 60, 80],
            'color': ["red", "orange", "red"]
        })
        fig_map = px.scatter_mapbox(df_map, lat="lat", lon="lon", size="size", color="color", 
                                    color_discrete_map={"red":"#ef4444", "orange":"#eab308"},
                                    zoom=r_data['zoom'], mapbox_style="open-street-map")
        fig_map.update_layout(margin=dict(l=0, r=0, t=0, b=0), height=250, paper_bgcolor="rgba(0,0,0,0)", showlegend=False)
        
        st.markdown(f"<div class='dash-card' style='padding:10px;'>", unsafe_allow_html=True)
        st.markdown(f"<div class='section-title'>🗺️ {t['map_title']}</div>", unsafe_allow_html=True)
        st.plotly_chart(fig_map, use_container_width=True, config={'displayModeBar': False})
        st.markdown('</div>', unsafe_allow_html=True)

    with info_col:
        # Compliance
        compliance_color = "#10b981" if is_compliant else "#ef4444"
        compliance_text = t['compliance_status'] if is_compliant else t['compliance_fail']
        st.markdown(f"""
        <div class="dash-card" style="padding:10px; margin-bottom:10px;">
            <div class="metric-title">📋 {t['requirements_compliance']}</div>
            <div class="metric-label" style="color:{compliance_color}; font-size:20px;">{compliance_text}</div>
        </div>
        """, unsafe_allow_html=True)

        # Supply Chain Status
        sc_color = "#10b981" if supply_chain_status > 80 else "#eab308" if supply_chain_status > 55 else "#ef4444"
        st.markdown(f"""
        <div class="dash-card" style="padding:10px;">
            <div class="metric-title">🚚 {t['supply_chain']}</div>
            <div class="metric-label" style="color:{sc_color}; font-size:20px;">{supply_chain_status}%</div>
        </div>
        """, unsafe_allow_html=True)

    # Row 4: Recommendations
    st.markdown("<div style='margin-top:10px;'></div>", unsafe_allow_html=True)
    st.markdown(f"<h3 style='margin: 10px 0; direction:{t['dir']}; text-align:{t['align']};'>{t.get('recommendations_title', '🚨 ' + t['recommendations'])}</h3>", unsafe_allow_html=True)
    rec_col1, rec_col2 = st.columns(2)

    with rec_col1:
        st.markdown(f"""
        <div class="dash-card" style="padding:12px; background: #fff3cd; border: 1px solid #ffc107;">
            <div style="font-weight:600; color: #856404; margin-bottom:8px;">{t['rec_supply']}</div>
            <div style="font-size:12px; color: #856404;">{t['rec_supply_desc']}</div>
        </div>
        """, unsafe_allow_html=True)

    with rec_col2:
        st.markdown(f"""
        <div class="dash-card" style="padding:12px; background: #fff3cd; border: 1px solid #ffc107;">
            <div style="font-weight:600; color: #856404; margin-bottom:8px;">{t['rec_weather']}</div>
            <div style="font-size:12px; color: #856404;">{t['rec_weather_desc']}</div>
        </div>
        """, unsafe_allow_html=True)

    # AI-Powered Insights Section
    st.markdown("<div style='margin-top:15px;'></div>", unsafe_allow_html=True)
    st.markdown(f"<h3 style='margin: 10px 0; color: #ef4444;'>🤖  Insights | استنتاجات </h3>", unsafe_allow_html=True)
    
    # Risk Severity Indicator
    severity_colors = {
        'Critical': '#ef4444',
        'High': '#f59e0b',
        'Medium': '#eab308',
        'Low': '#10b981'
    }
    severity_color = severity_colors.get(ai_insights['severity'], '#6b7280')
    
    insight_col1, insight_col2, insight_col3 = st.columns(3)
    
    with insight_col1:
        st.markdown(f"""
        <div class="dash-card" style="padding:12px; background: {severity_color}15; border: 2px solid {severity_color};">
            <div style="font-weight:600; font-size:12px; color:{severity_color}; margin-bottom:8px;">Risk Severity</div>
            <div style="font-size:20px; font-weight:700; color:{severity_color};">{ai_insights['severity']}</div>
            <div style="font-size:11px; opacity:0.7; margin-top:8px;">Confidence: {ai_insights['confidence']*100:.0f}%</div>
        </div>
        """, unsafe_allow_html=True)
    
    with insight_col2:
        st.markdown(f"""
        <div class="dash-card" style="padding:12px; background: #f3f4f615; border: 2px solid #3b82f6;">
            <div style="font-weight:600; font-size:12px; color:#3b82f6; margin-bottom:8px;">Primary Recommendation</div>
            <div style="font-size:12px; color:#333; line-height:1.5;">{ai_insights['primary_recommendation']}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with insight_col3:
        st.markdown(f"""
        <div class="dash-card" style="padding:12px; background: #10b98115; border: 2px solid #10b981;">
            <div style="font-weight:600; font-size:12px; color:#10b981; margin-bottom:8px;">Timeline Scenarios</div>
            <div style="font-size:11px; line-height:1.5;">
                <div>✓ Best: {timeline_scenarios['best_case']} days</div>
                <div>→ Realistic: {timeline_scenarios['realistic_case']} days</div>
                <div>✗ Worst: {timeline_scenarios['worst_case']} days</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Secondary Recommendations
    st.markdown("<div style='margin-top:12px;'></div>", unsafe_allow_html=True)
    st.markdown(f"<div style='font-weight:600; font-size:13px; margin-bottom:8px;'>Secondary Recommendations:</div>", unsafe_allow_html=True)
    
    for idx, rec in enumerate(ai_insights['secondary_recommendations'], 1):
        st.markdown(f"""
        <div style="padding:10px; background:#f9fafb; border-left: 3px solid #3b82f6; margin-bottom:8px; border-radius:4px;">
            <div style="font-size:12px; color:#333;"><b>{idx}.</b> {rec}</div>
        </div>
        """, unsafe_allow_html=True)

    # Delay Contributing Factors Analysis
    st.markdown("<div style='margin-top:15px;'></div>", unsafe_allow_html=True)
    st.markdown(f"<h3 style='margin: 10px 0;'>📈 Delay Contributing Factors | العوامل المساهمة في التأخيرات</h3>", unsafe_allow_html=True)
    
    delay_factors = delay_reasons
    total_factors = sum(delay_factors.values())
    
    factor_cols = st.columns(len(delay_factors))
    factor_labels_ar = {
        'labor': 'كفاءة العمالة',
        'weather': 'الطقس',
        'scale': 'حجم المشروع',
        'budget': 'الميزانية',
        'risks': 'المخاطر'
    }
    factor_labels_en = {
        'labor': 'Labor Efficiency',
        'weather': 'Weather',
        'scale': 'Project Scale',
        'budget': 'Budget',
        'risks': 'Risks'
    }
    
    factor_colors = {
        'labor': '#ef4444',
        'weather': '#3b82f6',
        'scale': '#8b5cf6',
        'budget': '#f59e0b',
        'risks': '#06b6d4'
    }
    
    for idx, (factor, value) in enumerate(delay_factors.items()):
        percentage = (value / total_factors * 100) if total_factors > 0 else 0
        label_en = factor_labels_en.get(factor, factor)
        label_ar = factor_labels_ar.get(factor, factor)
        color = factor_colors.get(factor, '#6b7280')
        
        with factor_cols[idx]:
            st.markdown(f"""
            <div class="dash-card" style="padding:12px; background: {color}15; border: 2px solid {color}; text-align:center;">
                <div style="font-size:11px; opacity:0.8;">{label_ar}</div>
                <div style="font-size:11px; opacity:0.8;">{label_en}</div>
                <div style="font-size:22px; font-weight:700; color:{color}; margin:8px 0;">{percentage:.0f}%</div>
                <div style="font-size:10px; opacity:0.7;">{value:.1f} days</div>
            </div>
            """, unsafe_allow_html=True)

    # Row 5: Detailed Report
    st.markdown(f"<h3 style='margin: 15px 0 10px 0; direction:ltr; text-align:left;'>📊 Detailed Analytical Report</h3>", unsafe_allow_html=True)
    
    # Timeline Scenario Visualization
    st.markdown("<div style='margin: 15px 0 10px 0;'><h4 style='margin:0;'>📅 Project Timeline Scenarios</h4></div>", unsafe_allow_html=True)
    
    scenario_data = [
        ('✅ Best Case', timeline_scenarios['best_case'], '#10b981'),
        ('→ Realistic Case', timeline_scenarios['realistic_case'], '#f59e0b'),
        ('⚠️ Worst Case', timeline_scenarios['worst_case'], '#ef4444')
    ]
    
    scenario_cols = st.columns(3)
    for col_idx, (label, days_val, color) in enumerate(scenario_data):
        with scenario_cols[col_idx]:
            st.markdown(f"""
            <div class="dash-card" style="padding:15px; background: {color}15; border: 2px solid {color}; text-align:center;">
                <div style="font-weight:600; color:{color}; margin-bottom:8px;">{label}</div>
                <div style="font-size:28px; font-weight:700; color:{color};">{days_val}</div>
                <div style="font-size:12px; opacity:0.7; margin-top:8px;">Days Delay</div>
                <div style="font-size:11px; opacity:0.6; margin-top:4px;">±{timeline_scenarios['confidence_interval']} days</div>
            </div>
            """, unsafe_allow_html=True)
    st.markdown(f"""
<div class="dash-card" style="padding:15px; direction:ltr; text-align:left;">
    <p>
        Based on the entered data and the AI model analysis, the project shows a <b>current risk rate of {risk_percentage}%</b>. This indicator reflects the overall probability of encountering challenges that could negatively impact workflow and is influenced by multiple factors such as labor efficiency, project size, and environmental conditions. Understanding this rate is crucial for taking proactive decisions to mitigate potential risks and ensure project stability.
    </p>
    <p>
        Regarding time delays, the system predicts a <b>total delay of {p_var} {t['days']}</b>. <b>{delay_primary_reason}</b> has been identified as the main reason for this delay. The delay analysis includes a precise evaluation of the impact of labor efficiency, weather conditions in the selected region ({sel_region}), project size ({sel_size}), as well as the adequacy of the allocated budget ({sel_budget} SAR), and the complexity of manually entered expected risks. These predictions provide a comprehensive overview of upcoming temporal challenges.
    </p>
    <p>
        As for cost, forecasts indicate a <b>cost overrun of {cost_overrun_val}%</b> of the original budget. This overrun is directly linked to expected delays and factors affecting execution efficiency and resource availability. Controlling costs and avoiding overruns is a primary objective of any successful project, and this prediction provides an early warning to re-evaluate budgets and better allocate resources.
    </p>
    <p>
        Concerning environmental and economic indicators, the <b>expected inflation rate is {inflation_rate}{t['inflation_unit']}</b>. This rate is influenced by the total project duration (based on {sel_days} days) and the geographical region, indicating potential economic impacts on material and labor costs in the long term. Additionally, the project's <b>carbon footprint is estimated at {carbon_footprint} {t['carbon_unit']}</b>. This estimation relies on project size, geographical region, and labor efficiency, highlighting the project's environmental impact, which supports sustainability initiatives and compliance with environmental standards.
    </p>
    <p>
        Finally, the <b>compliance evaluation shows that the project is {compliance_percentage:.0f}% {t['kpis']} {t['compliance_status'] if is_compliant else t['compliance_fail']}</b> with the specified standards. This comprehensive indicator combines an assessment of labor efficiency, budget adequacy, schedule realism, risk assessment, and environmental compliance. It indicates the extent of the project's adherence to technical and operational requirements, reflecting the overall quality of planning and execution. This detailed report enables decision-makers to gain a deeper understanding of the project's status and take necessary corrective actions to ensure its success and sustainability.
    </p>
</div>
""", unsafe_allow_html=True)

    # Row 4: Future Features (Removed - using import features in sidebar instead)

    # Footer
    st.markdown(f"""
        <div style="margin-top: 20px; padding: 15px; text-align: center; border-top: 1px solid rgba(148, 163, 184, 0.1);">
            <p style="opacity: 0.6; font-size: 12px; margin: 0;">{t['footer']} | 2026</p>
        </div>
""", unsafe_allow_html=True)


    import base64

    # دالة لقراءة الصورة وتحويلها لتتناسب مع الـ HTML
    def get_base64_of_bin_file(bin_file):
        try:
            with open(bin_file, 'rb') as f:
                data = f.read()
            return base64.b64encode(data).decode()
        except FileNotFoundError:
            return "" # في حال لم يجد الصورة لا يعطي خطأ

    # استدعاء اللوقو (تأكد أن اسم الصورة مطابق لاسم الملف لديك)
    logo_base64 = get_base64_of_bin_file("logo.png")
    logo_html = f'<div style="text-align: center; margin-bottom: 15px; max-width: 100%; overflow: hidden;"><img src="data:image/png;base64,{logo_base64}" style="width: 180px; height: auto; object-fit: contain; max-width: 100%; display: block; margin: 0 auto;"></div>' if logo_base64 else ''


    # AI-Generated Summary Report
    report_intro = t['report_intro'].format(risk_percentage=risk_percentage)

    report_delay = t['report_delay'].format(
        p_var=p_var,
        days=t['days'],
        delay_primary_reason=delay_primary_reason,
        sel_region=sel_region,
        sel_size=sel_size,
        sel_budget=sel_budget
    )

    report_cost_overrun = t['report_cost_overrun'].format(cost_overrun_val=cost_overrun_val)

    report_environmental_economic = t['report_environmental_economic'].format(
        inflation_rate=inflation_rate,
        inflation_unit=t['inflation_unit'],
        sel_days=sel_days,
        carbon_footprint=carbon_footprint,
        carbon_unit=t['carbon_unit']
    )

    report_compliance = t['report_compliance'].format(
        compliance_percentage=compliance_percentage,
        kpis=t['kpis'],
        compliance_text=compliance_text
    )

    # عرض التقرير مع اللوقو
    st.markdown(f"""
        <div style="margin-top: 20px; padding: 20px; background: white; border-radius: 18px; border: 1px solid #f0f0f0; direction:{t['dir']}; text-align:{t['align']}; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);">
            
            {logo_html}
            
            <h3 style="margin-bottom: 10px; margin-top: 0; color:#1e293b; border-bottom: 2px solid #f0f0f0; padding-bottom: 8px;">{t['report_title']}</h3>
            <p style="color:#475569; line-height:1.8;">{report_intro}</p>
            <p style="color:#475569; line-height:1.8;">{report_delay}</p>
            <p style="color:#475569; line-height:1.8;">{report_cost_overrun}</p>
            <p style="color:#475569; line-height:1.8;">{report_environmental_economic}</p>
            <p style="color:#475569; line-height:1.8;">{report_compliance}</p>
        </div>
""", unsafe_allow_html=True)

else:
    st.markdown(f"""
    <div style="text-align: center; padding: 60px 20px;">
        <div style="font-size: 48px; margin-bottom: 20px;">📊</div>
        <h2 style="color: #334155; margin-bottom: 10px;">Welcome to istibaq</h2>
        <h2 style="color: #334155; margin-bottom: 30px;">مرحباً بك في استباق</h2>
        <p style="font-size: 16px; color: #64748b; margin-bottom: 20px;">
            Please fill in the project parameters in the sidebar and click "Update Data" to view the analysis
        </p>
        <p style="font-size: 16px; color: #64748b; margin-bottom: 30px;">
            يرجى ملء معاملات المشروع في الشريط الجانبي والضغط على "تحديث البيانات" لعرض التحليل
        </p>
        <div style="background: linear-gradient(135deg, #f0f4ff 0%, #fffbf0 100%); padding: 20px; border-radius: 12px; color: #475569;">
            📝 Configure your project &nbsp;|&nbsp; 🚀 Click Update &nbsp;|&nbsp; 📊 View Results
        </div>
    </div>
    """, unsafe_allow_html=True)
