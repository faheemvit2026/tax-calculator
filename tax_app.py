import streamlit as st
import plotly.graph_objects as go

# 1. Page Configuration
st.set_page_config(page_title="TaxPro India", page_icon="🏦", layout="wide")

# 2. Custom Styling (The "Cool" Factor)
st.markdown("""
    <style>
    .main { background-color: #f0f2f6; }
    div.stButton > button:first-child {
        background-color: #007bff; color: white; border-radius: 10px;
    }
    .metric-card {
        background-color: white; padding: 20px; border-radius: 12px;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Sidebar for Manual Amendments (The "Update" Factor)
with st.sidebar:
    st.header("⚙️ Law Amendments")
    st.write("Update these if the Government changes slabs.")
    
    std_deduction = st.number_input("Standard Deduction (₹)", value=75000)
    rebate_limit = st.number_input("Section 87A Rebate Limit (₹)", value=1200000)
    
    st.subheader("Edit Tax Slabs")
    # This table allows you to update rates/limits on the live site
    slab_data = st.data_editor([
        {"Limit": 400000, "Rate (%)": 0},
        {"Limit": 800000, "Rate (%)": 5},
        {"Limit": 1200000, "Rate (%)": 10},
        {"Limit": 1600000, "Rate (%)": 15},
        {"Limit": 2000000, "Rate (%)": 20},
        {"Limit": 2400000, "Rate (%)": 25},
        {"Limit": 100000000, "Rate (%)": 30},
    ])

# 4. Main Body
st.title("🏦 TaxPro India AI")
st.markdown("### Compute Income Tax & Plan Savings")

col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.subheader("💰 Income Details")
    salary = st.number_input("Annual Gross Salary (₹)", value=1500000, step=10000)
    other_inc = st.number_input("Other Income (Interest/Bonus) (₹)", value=0)
    total_gross = salary + other_inc
    taxable_income = max(0, total_gross - std_deduction)
    
    st.write(f"**Final Taxable Income:** ₹{taxable_income:,}")

with col2:
    st.subheader("📊 Tax Computation")
    
    # Calculation Logic
    tax = 0
    if taxable_income > rebate_limit:
        prev_limit = 0
        for slab in slab_data:
            limit = slab["Limit"]
            rate = slab["Rate (%)"] / 100
            if taxable_income > prev_limit:
                amt = min(taxable_income, limit) - prev_limit
                tax += amt * rate
                prev_limit = limit

    cess = tax * 0.04
    total_tax = tax + cess

    # Professional Metrics
    m1, m2 = st.columns(2)
    m1.metric("Total Tax Liability", f"₹{total_tax:,.0f}")
    m2.metric("Effective Tax Rate", f"{(total_tax/total_gross*100):.2f}%" if total_gross > 0 else "0%")

    # Visualization
    if total_tax > 0:
        fig = go.Figure(data=[go.Pie(labels=['Take Home', 'Tax', 'Cess'], 
                                     values=[total_gross-total_tax, tax, cess], 
                                     hole=.5, marker_colors=['#28a745', '#dc3545', '#ffc107'])])
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.success("🎉 You are in the Zero-Tax zone!")

# 5. Planning Section
st.divider()
st.subheader("💡 Tax Planning Tips")
tabs = st.tabs(["Salaried", "Business", "Investments"])
with tabs[0]:
    st.write("- Ask HR about **NPS Tier 1** (Corporate model) for an extra 14% deduction.")
    st.write("- Check if your **HRA** is optimized vs the New Regime benefit.")