import streamlit as st
from datetime import datetime, timedelta
import streamlit.components.v1 as components

# ==========================================
# 1. PAGE CONFIGURATION & PWA METADATA
# ==========================================
st.set_page_config(
    page_title="MomsNutriCare",
    page_icon="🤰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inject custom metadata and dynamic PWA manifest to enforce MomsNutriCare branding
st.markdown("""
    <head>
        <title>MomsNutriCare</title>
        <meta name="apple-mobile-web-app-title" content="MomsNutriCare">
        <meta name="application-name" content="MomsNutriCare">
        <meta name="theme-color" content="#ffffff">
    </head>
""", unsafe_allow_html=True)

pwa_manifest_script = """
<script>
  const manifest = {
    "name": "MomsNutriCare",
    "short_name": "MomsNutriCare",
    "start_url": "/",
    "display": "standalone",
    "background_color": "#ffffff",
    "theme_color": "#ffffff",
    "icons": [
      {
        "src": "https://em-content.zobj.net/source/apple/354/pregnant-woman_1f930.png",
        "sizes": "192x192",
        "type": "image/png"
      }
    ]
  };
  const stringManifest = JSON.stringify(manifest);
  const blob = new Blob([stringManifest], {type: 'application/json'});
  const manifestURL = URL.createObjectURL(blob);
  let link = document.createElement('link');
  link.rel = 'manifest';
  link.href = manifestURL;
  document.getElementsByTagName('head')[0].appendChild(link);
</script>
"""
components.html(pwa_manifest_script, height=0, width=0)

# ==========================================
# 2. BRANDING BANNER & HEADER
# ==========================================
st.title("🤰 MomsNutriCare: Clinical MNT Calculator")
st.caption("🔬 **Designed & Engineered by Dn. Areesha Asif Awan** | Clinical Dietitian & Public Health Researcher")
st.markdown("---")

# ==========================================
# 3. SIDEBAR: PATIENT INPUT DATA
# ==========================================
st.sidebar.header("📋 Patient Clinical Inputs")

# Demographics & Anthropometrics
age = st.sidebar.number_input("Age (years)", min_value=15, max_value=50, value=25, step=1)
height_cm = st.sidebar.number_input("Height (cm)", min_value=120.0, max_value=200.0, value=162.0, step=0.1)
pre_weight_kg = st.sidebar.number_input("Pre-Pregnancy Weight (kg)", min_value=30.0, max_value=150.0, value=58.0, step=0.1)

# Obstetrics & Physical Activity
lmp_date = st.sidebar.date_input(
    "Last Menstrual Period (LMP)",
    value=datetime.today() - timedelta(weeks=12)
)

activity_level = st.sidebar.selectbox(
    "Physical Activity Level",
    options=["Sedentary (1.2)", "Lightly Active (1.375)", "Moderately Active (1.55)", "Very Active (1.725)"],
    index=0
)

# Extract Multiplier Numeric Value
activity_multipliers = {
    "Sedentary (1.2)": 1.2,
    "Lightly Active (1.375)": 1.375,
    "Moderately Active (1.55)": 1.55,
    "Very Active (1.725)": 1.725
}
act_factor = activity_multipliers[activity_level]

# Clinical Laboratory Value
hb_level = st.sidebar.number_input("Hemoglobin Level (g/dL)", min_value=5.0, max_value=18.0, value=11.5, step=0.1)

# ==========================================
# 4. CLINICAL COMPUTATIONS
# ==========================================

# A. Gestational Age & EDD (Naegele's Rule)
edd_date = lmp_date + timedelta(days=280)
days_pregnant = (datetime.today().date() - lmp_date).days
gestational_weeks = days_pregnant // 7
gestational_days_rem = days_pregnant % 7

if gestational_weeks < 13:
    trimester = "1st Trimester"
    trimester_addition = 0
elif 13 <= gestational_weeks < 27:
    trimester = "2nd Trimester"
    trimester_addition = 340
else:
    trimester = "3rd Trimester"
    trimester_addition = 452

# B. Anthropometric BMI & IOM Weight Gain Classification
height_m = height_cm / 100.0
bmi = pre_weight_kg / (height_m ** 2)

if bmi < 18.5:
    bmi_category = "Underweight"
    iom_weight_gain = "12.5 - 18.0 kg"
elif 18.5 <= bmi < 25.0:
    bmi_category = "Normal Weight"
    iom_weight_gain = "11.5 - 16.0 kg"
elif 25.0 <= bmi < 30.0:
    bmi_category = "Overweight"
    iom_weight_gain = "7.0 - 11.5 kg"
else:
    bmi_category = "Obese"
    iom_weight_gain = "5.0 - 9.0 kg"

# C. BMR & TEE Calculations (Mifflin-St Jeor)
bmr = (10 * pre_weight_kg) + (6.25 * height_cm) - (5 * age) - 161
baseline_tee = bmr * act_factor
total_caloric_target = baseline_tee + trimester_addition

# ==========================================
# 5. DASHBOARD DISPLAY & RESULTS
# ==========================================

col1, col2 = st.columns(2)

with col1:
    st.subheader("📅 Obstetric & Gestational Profile")
    st.write(f"**Estimated Date of Delivery (EDD):** {edd_date.strftime('%B %d, %Y')}")
    st.write(f"**Current Gestational Age:** {gestational_weeks} weeks, {gestational_days_rem} days")
    st.write(f"**Current Trimester Status:** {trimester}")
    
    st.markdown("---")
    
    st.subheader("⚖️ Pre-Pregnancy BMI & Weight Targets (IOM)")
    st.write(f"**Pre-Pregnancy BMI:** {bmi:.1f} kg/m² ({bmi_category})")
    st.write(f"**Target Gestational Weight Gain:** {iom_weight_gain}")

with col2:
    st.subheader("🔥 Energy Requirement Breakdown (Mifflin-St Jeor)")
    
    st.metric(label="Total Caloric Target", value=f"{round(total_caloric_target)} kcal/day")
    
    st.markdown(f"""
    * **Basal Metabolic Rate (BMR):** $\\approx {round(bmr)}\\text{{ kcal/day}}$
      * *Formula:* $(10 \\times {pre_weight_kg}) + (6.25 \\times {height_cm}) - (5 \\times {age}) - 161$
    * **Baseline TEE:** $\\approx {round(baseline_tee)}\\text{{ kcal/day}}$
      * *Formula:* $\\text{{BMR }} ({round(bmr)}) \\times \\text{{Activity Factor }} ({act_factor})$
    * **Trimester Addition:** $+{trimester_addition}\\text{{ kcal/day}}$ *({trimester})*
    * **Final Energy Requirement:** $\\approx {round(total_caloric_target)}\\text{{ kcal/day}}$
    """)

st.markdown("---")

# ==========================================
# 6. GESTATIONAL ANEMIA SCREENING (WHO)
# ==========================================
st.subheader("🩸 Gestational Anemia Screening (WHO Criteria)")

if hb_level >= 11.0:
    st.success(f"**Normal Hemoglobin Level ({hb_level:.1f} g/dL):** No anemia detected based on WHO trimester cutoff standards.")
elif 10.0 <= hb_level < 11.0:
    st.warning(f"**Mild Gestational Anemia ({hb_level:.1f} g/dL):** MNT & oral iron supplementation recommended.")
elif 7.0 <= hb_level < 10.0:
    st.error(f"**Moderate Gestational Anemia ({hb_level:.1f} g/dL):** Requires therapeutic oral iron trial and dietary enhancement.")
else:
    st.error(f"**Severe Gestational Anemia ({hb_level:.1f} g/dL):** Immediate clinical escalation and urgent medical review required.")

# ==========================================
# 7. FOOTER
# ==========================================
st.markdown("---")
st.caption("© MomsNutriCare | Clinical Decision-Support Tool | Developed for Maternal & Child Health Support")






   
 
