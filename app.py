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
# 3. SIDEBAR: PATIENT INPUT DATA & CREATOR CREDIT
# ==========================================
st.sidebar.markdown("### 👩‍⚕️ **App Creator**")
st.sidebar.info("**Dn. Areesha Asif Awan**\n\n*Clinical Dietitian & Public Health Researcher*")
st.sidebar.markdown("---")

st.sidebar.header("📋 Patient Clinical Inputs")

# Demographics & Anthropometrics
age = st.sidebar.number_input("Age (years)", min_value=15, max_value=50, value=25, step=1)
height_cm = st.sidebar.number_input("Height (cm)", min_value=120.0, max_value=200.0, value=162.0, step=0.1)
pre_weight_kg = st.sidebar.number_input("Pre-Pregnancy Weight (kg)", min_value=30.0, max_value=150.0, value=58.0, step=0.1)
current_weight_kg = st.sidebar.number_input("Current Weight (kg)", min_value=30.0, max_value=160.0, value=62.0, step=0.1)

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
gestational_weeks = max(0, days_pregnant // 7)
gestational_days_rem = max(0, days_pregnant % 7)

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

# Weight Gain Parameters based on Institute of Medicine (IOM) Guidelines
if bmi < 18.5:
    bmi_category = "Underweight"
    iom_total_gain = "12.5 - 18.0 kg"
    trimester_1_gain = "1.0 - 3.0 kg"
    weekly_rate_2nd_3rd = 0.51
    weekly_rate_str = "0.44 - 0.58 kg/week"
elif 18.5 <= bmi < 25.0:
    bmi_category = "Normal Weight"
    iom_total_gain = "11.5 - 16.0 kg"
    trimester_1_gain = "1.0 - 2.0 kg"
    weekly_rate_2nd_3rd = 0.42
    weekly_rate_str = "0.35 - 0.50 kg/week"
elif 25.0 <= bmi < 30.0:
    bmi_category = "Overweight"
    iom_total_gain = "7.0 - 11.5 kg"
    trimester_1_gain = "0.5 - 2.0 kg"
    weekly_rate_2nd_3rd = 0.28
    weekly_rate_str = "0.23 - 0.33 kg/week"
else:
    bmi_category = "Obese"
    iom_total_gain = "5.0 - 9.0 kg"
    trimester_1_gain = "0.5 - 2.0 kg"
    weekly_rate_2nd_3rd = 0.22
    weekly_rate_str = "0.17 - 0.27 kg/week"

# C. Actual Weight Gain Analysis
actual_weight_gain = current_weight_kg - pre_weight_kg

# Expected Target Weight Gain Calculation for Current Week
if gestational_weeks <= 12:
    expected_target_min = 0.5
    expected_target_max = 2.0
else:
    weeks_past_1st_trimester = gestational_weeks - 12
    base_1st_tri = 1.5
    expected_target_min = base_1st_tri + (weeks_past_1st_trimester * (weekly_rate_2nd_3rd - 0.07))
    expected_target_max = base_1st_tri + (weeks_past_1st_trimester * (weekly_rate_2nd_3rd + 0.07))

# D. BMR & TEE Calculations (Mifflin-St Jeor)
bmr = (10 * pre_weight_kg) + (6.25 * height_cm) - (5 * age) - 161
baseline_tee = bmr * act_factor
total_caloric_target = baseline_tee + trimester_addition

# ==========================================
# 5. DASHBOARD DISPLAY & RESULTS
# ==========================================

# Output Clinical Validation Tag
st.success("🔬 **Clinical Assessment Results** | Designed & Validated by **Dn. Areesha Asif Awan**, Clinical Dietitian")

col1, col2 = st.columns(2)

with col1:
    st.subheader("📅 Obstetric & Gestational Profile")
    st.write(f"**Estimated Date of Delivery (EDD):** {edd_date.strftime('%B %d, %Y')}")
    st.write(f"**Current Gestational Age:** {gestational_weeks} weeks, {gestational_days_rem} days")
    st.write(f"**Current Trimester Status:** {trimester}")
    
    st.markdown("---")
    
    st.subheader("⚖️ BMI & Trimester Weight Gain Targets (IOM)")
    st.write(f"**Pre-Pregnancy BMI:** {bmi:.1f} kg/m² ({bmi_category})")
    st.write(f"**Total Recommended Weight Gain:** {iom_total_gain}")
    st.write(f"**1st Trimester Total Target:** {trimester_1_gain}")
    st.write(f"**2nd & 3rd Trimester Rate:** {weekly_rate_str}")

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
# 6. ACTUAL VS EXPECTED WEIGHT GAIN EVALUATION
# ==========================================
st.subheader("📈 Gestational Weight Gain Progress")

col3, col4, col5 = st.columns(3)
col3.metric(label="Current Weight", value=f"{current_weight_kg:.1f} kg")
col4.metric(label="Total Weight Gained", value=f"{actual_weight_gain:+.1f} kg")
col5.metric(label=f"Target Gain at Week {gestational_weeks}", value=f"{expected_target_min:.1f} - {expected_target_max:.1f} kg")

if actual_weight_gain < expected_target_min:
    st.warning(f"⚠️ **Below Target:** Actual weight gain ({actual_weight_gain:+.1f} kg) is below the expected target range ({expected_target_min:.1f} to {expected_target_max:.1f} kg) for Week {gestational_weeks}. Review caloric intake and nutrient density.")
elif actual_weight_gain > expected_target_max:
    st.info(f"⚠️ **Above Target:** Actual weight gain ({actual_weight_gain:+.1f} kg) exceeds the recommended target range ({expected_target_min:.1f} to {expected_target_max:.1f} kg) for Week {gestational_weeks}. Monitor glycemic control and physical activity.")
else:
    st.success(f"✅ **On Target:** Actual weight gain ({actual_weight_gain:+.1f} kg) is within the recommended IOM range for Week {gestational_weeks}.")

st.markdown("---")

# ==========================================
# 7. GESTATIONAL ANEMIA SCREENING (WHO)
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
# 8. FOOTER WITH COMPLETE BRANDING
# ==========================================
st.markdown("---")
st.caption("© MomsNutriCare | **Designed & Engineered by Dn. Areesha Asif Awan** | Clinical Dietitian & Public Health Researcher")

  

    


  






   








   
 
