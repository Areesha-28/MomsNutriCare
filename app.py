import streamlit as st
from datetime import datetime, timedelta

# 1. Page Configuration & Browser Branding
st.set_page_config(
    page_title="MomsNutriCare | By Dn. Areesha Asif Awan",
    page_icon="🤰",
    layout="wide"
)

# 2. Main Title & Branding Banner
st.title("🤰 MomsNutriCare: Clinical MNT Calculator")
st.caption("🔬 **Designed & Engineered by Dn. Areesha Asif Awan** | Clinical Dietitian & Public Health Researcher")
st.markdown("---")

# 3. Sidebar - Patient Clinical Inputs
st.sidebar.header("📋 Patient Clinical Inputs")

# Date of Last Menstrual Period (LMP)
lmp_date = st.sidebar.date_input(
    "Last Menstrual Period (LMP) Date",
    value=datetime.today() - timedelta(weeks=12),
    max_value=datetime.today()
)

# Patient Anthropometrics
age = st.sidebar.number_input("Age (years)", min_value=15, max_value=50, value=25)
height_cm = st.sidebar.number_input("Height (cm)", min_value=120.0, max_value=200.0, value=162.0)
pre_weight_kg = st.sidebar.number_input("Pre-Pregnancy Weight (kg)", min_value=30.0, max_value=150.0, value=58.0)
curr_weight_kg = st.sidebar.number_input("Current Weight (kg)", min_value=30.0, max_value=160.0, value=61.0)

# Physical Activity Level
activity_level = st.sidebar.selectbox(
    "Physical Activity Level",
    options=[
        "Sedentary (Little or no exercise)",
        "Lightly Active (1-3 days/week)",
        "Moderately Active (3-5 days/week)",
        "Very Active (6-7 days/week)"
    ]
)

# Clinical Check - Hemoglobin Level
hb_level = st.sidebar.number_input("Current Hemoglobin Level (g/dL)", min_value=5.0, max_value=18.0, value=11.5, step=0.1)

# Sidebar Developer Profile
st.sidebar.markdown("---")
st.sidebar.subheader("👩‍⚕️ About the Creator")
st.sidebar.write("**Dn. Areesha Asif Awan**")
st.sidebar.write("• Clinical Dietitian & Nutritionist")
st.sidebar.write("• BS Human Nutrition & Dietetics")
st.sidebar.write("• Instagram: **@LeanGlow by Dn Areesha Asif**")

# --- CALCULATIONS ---

# 1. Obstetric Dates (EDD & Gestational Age via Naegele's Rule)
edd_date = lmp_date + timedelta(days=280)
days_pregnant = (datetime.today().date() - lmp_date).days
gestational_weeks = max(0, days_pregnant // 7)
gestational_days = max(0, days_pregnant % 7)

# Trimester Determination
if gestational_weeks < 13:
    trimester = "1st Trimester"
    caloric_addition = 0
elif 13 <= gestational_weeks < 27:
    trimester = "2nd Trimester"
    caloric_addition = 340
else:
    trimester = "3rd Trimester"
    caloric_addition = 452

# 2. Pre-Pregnancy BMI Calculation
height_m = height_cm / 100.0
bmi = pre_weight_kg / (height_m ** 2)

if bmi < 18.5:
    bmi_category = "Underweight"
    target_weight_gain = (12.5, 18.0)
    weekly_rate_2nd_3rd = 0.51
elif 18.5 <= bmi < 25.0:
    bmi_category = "Normal Weight"
    target_weight_gain = (11.5, 16.0)
    weekly_rate_2nd_3rd = 0.42
elif 25.0 <= bmi < 30.0:
    bmi_category = "Overweight"
    target_weight_gain = (7.0, 11.5)
    weekly_rate_2nd_3rd = 0.28
else:
    bmi_category = "Obese"
    target_weight_gain = (5.0, 9.0)
    weekly_rate_2nd_3rd = 0.22

# 3. Energy Expenditure (Mifflin-St Jeor Equation)
bmr = (10 * pre_weight_kg) + (6.25 * height_cm) - (5 * age) - 161

activity_multipliers = {
    "Sedentary (Little or no exercise)": 1.2,
    "Lightly Active (1-3 days/week)": 1.375,
    "Moderately Active (3-5 days/week)": 1.55,
    "Very Active (6-7 days/week)": 1.725
}
pal = activity_multipliers[activity_level]
tee_baseline = bmr * pal
total_caloric_target = tee_baseline + caloric_addition

# 4. Weight Gain Trajectory Check
current_weight_gain = curr_weight_kg - pre_weight_kg
if gestational_weeks <= 12:
    expected_gain_range = (0.5, 2.0)
else:
    expected_min = 1.0 + ((gestational_weeks - 12) * (weekly_rate_2nd_3rd * 0.8))
    expected_max = 2.0 + ((gestational_weeks - 12) * (weekly_rate_2nd_3rd * 1.2))
    expected_gain_range = (expected_min, expected_max)

# --- DASHBOARD DISPLAY ---

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Estimated Due Date (EDD)", edd_date.strftime("%b %d, %Y"))
    st.caption(f"Status: **{gestational_weeks} Wks {gestational_days} Days** ({trimester})")

with col2:
    st.metric("Pre-Pregnancy BMI", f"{bmi:.1f} kg/m²", delta=bmi_category, delta_color="off")
    st.caption(f"Target Total Gain: **{target_weight_gain[0]} - {target_weight_gain[1]} kg**")

with col3:
    st.metric("Total Daily Energy Target", f"{int(total_caloric_target)} kcal/day")
    st.caption(f"Baseline TEE ({int(tee_baseline)} kcal) + {caloric_addition} kcal ({trimester})")

st.divider()

# Detailed Clinical Findings
left_col, right_col = st.columns(2)

with left_col:
    st.subheader("📊 Weight Gain Trajectory")
    st.write(f"- **Current Weight Gain:** `{current_weight_gain:+.1f} kg`")
    st.write(f"- **Expected Gain for Week {gestational_weeks}:** `{expected_gain_range[0]:.1f} to {expected_gain_range[1]:.1f} kg`")
    
    if current_weight_gain < expected_gain_range[0]:
        st.warning("⚠️ **Under Weight Gain:** Below expected IOM trajectory for gestational age.")
    elif current_weight_gain > expected_gain_range[1]:
        st.info("ℹ️ **Above Target Gain:** Exceeds expected IOM rate for gestational age.")
    else:
        st.success("✅ **On Track:** Weight gain is within recommended IOM guidelines.")

with right_col:
    st.subheader("🩸 Gestational Anemia Screening (WHO Guidelines)")
    
    anemia_threshold = 10.5 if trimester == "2nd Trimester" else 11.0
    
    if hb_level < anemia_threshold:
        st.error(f"🚨 **Gestational Anemia Flag:** Hb ({hb_level} g/dL) is below WHO threshold ({anemia_threshold} g/dL) for {trimester}.")
        st.write("• Evaluate elemental iron supplementation (60–120 mg/day under clinical supervision).")
        st.write("• Pair iron with Vitamin C-rich foods; separate from calcium/tea/coffee.")
    else:
        st.success(f"✅ **Hemoglobin Normal:** Hb ({hb_level} g/dL) is within normal limits for {trimester}.")

st.divider()

# Essential Micronutrient Targets
st.subheader("💊 Daily Gestational Micronutrient Targets")
m_col1, m_col2, m_col3 = st.columns(3)
m_col1.metric("Elemental Iron", "27 mg/day", help="Essential for hemoglobin synthesis and fetal iron stores.")
m_col2.metric("Folate (DFE)", "600 mcg/day", help="Crucial for neural tube defect prevention.")
m_col3.metric("Dietary Calcium", "1,000 mg/day", help="Supports maternal bone density and fetal skeletal growth.")

st.markdown("---")

# Footer Copyright & Ownership Badge
st.markdown(
    """
    <div style="text-align: center; color: gray; font-size: 14px;">
        © 2026 <b>MomsNutriCare</b> | Designed & Developed by <b>Dn. Areesha Asif Awan</b><br>
        <i>Clinical Decision-Support Tool based on Institute of Medicine (IOM) & World Health Organization (WHO) Guidelines</i>
    </div>
    """,
    unsafe_allow_html=True
)
