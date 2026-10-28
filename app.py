
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(
    page_title="BusinessPilot AI",
    page_icon="📊",
    layout="wide"
)

# ---------------- PAGE HEADER ----------------

st.title("📊 BusinessPilot AI")
st.subheader("Business Decision Intelligence Platform")

st.write(
    "Analyze business performance, detect financial problems, "
    "and compare strategies using interactive financial simulations."
)

st.info(
    "Enter monthly business figures below. "
    "All amounts are in Indian Rupees (₹)."
)

# ---------------- USER INPUTS ----------------

st.sidebar.header("Business Financial Inputs")

revenue = st.sidebar.number_input(
    "Monthly Revenue (₹)",
    min_value=1.0,
    value=1500000.0,
    step=50000.0
)

cogs = st.sidebar.number_input(
    "Cost of Goods Sold (₹)",
    min_value=0.0,
    value=750000.0,
    step=10000.0
)

salaries = st.sidebar.number_input(
    "Employee Salaries (₹)",
    min_value=0.0,
    value=200000.0,
    step=10000.0
)

rent = st.sidebar.number_input(
    "Rent (₹)",
    min_value=0.0,
    value=100000.0,
    step=5000.0
)

marketing = st.sidebar.number_input(
    "Marketing Expenses (₹)",
    min_value=0.0,
    value=80000.0,
    step=5000.0
)

other_expenses = st.sidebar.number_input(
    "Other Expenses (₹)",
    min_value=0.0,
    value=70000.0,
    step=5000.0
)

# ---------------- VALIDATION ----------------

if cogs > revenue:
    st.warning(
        "Your cost of goods exceeds revenue. "
        "Check your figures before interpreting the results."
    )

# ---------------- FINANCIAL CALCULATIONS ----------------

gross_profit = revenue - cogs

operating_expenses = (
    salaries + rent + marketing + other_expenses
)

total_costs = cogs + operating_expenses

operating_profit = revenue - total_costs

gross_margin = gross_profit / revenue * 100
operating_margin = operating_profit / revenue * 100

# ---------------- KPI DASHBOARD ----------------

st.header("1. Business Health Dashboard")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Monthly Revenue",
    f"₹{revenue:,.0f}"
)

col2.metric(
    "Gross Profit",
    f"₹{gross_profit:,.0f}"
)

col3.metric(
    "Operating Profit",
    f"₹{operating_profit:,.0f}"
)

col4.metric(
    "Operating Margin",
    f"{operating_margin:.2f}%"
)

# ---------------- HEALTH STATUS ----------------

st.header("2. Business Problem Detector")

if operating_profit < 0:
    st.error(
        f"Critical: Your business has an operating loss "
        f"of ₹{abs(operating_profit):,.0f} per month."
    )

elif gross_margin < 25 or operating_margin < 10:
    st.warning(
        "Your business may need improvement in gross margin "
        "or operating profitability."
    )

else:
    st.success(
        "No major financial warning detected by the current rules."
    )

# ---------------- EXPENSE CHART ----------------

st.header("3. Expense Breakdown")

expense_data = pd.DataFrame({
    "Category": [
        "Cost of Goods",
        "Salaries",
        "Rent",
        "Marketing",
        "Other Expenses"
    ],
    "Amount": [
        cogs,
        salaries,
        rent,
        marketing,
        other_expenses
    ]
})

fig_expenses = px.pie(
    expense_data,
    names="Category",
    values="Amount",
    hole=0.45,
    title="Monthly Cost Distribution"
)

st.plotly_chart(
    fig_expenses,
    use_container_width=True
)

# ---------------- STRATEGY SIMULATOR ----------------

st.header("4. Business Decision Simulator")

price_change = st.slider(
    "Selling Price Change (%)",
    min_value=-20,
    max_value=30,
    value=5
)

demand_change = st.slider(
    "Demand / Sales Volume Change (%)",
    min_value=-50,
    max_value=50,
    value=0
)

marketing_change = st.slider(
    "Marketing Expense Change (%)",
    min_value=-50,
    max_value=100,
    value=0
)

cost_reduction = st.slider(
    "Reduction in Salaries, Rent and Other Expenses (%)",
    min_value=0,
    max_value=30,
    value=0
)

price_multiplier = 1 + price_change / 100
demand_multiplier = 1 + demand_change / 100

projected_revenue = (
    revenue * price_multiplier * demand_multiplier
)

projected_cogs = cogs * demand_multiplier

projected_salaries = salaries * (1 - cost_reduction / 100)
projected_rent = rent * (1 - cost_reduction / 100)
projected_other = other_expenses * (1 - cost_reduction / 100)

projected_marketing = marketing * (
    1 + marketing_change / 100
)

projected_costs = (
    projected_cogs
    + projected_salaries
    + projected_rent
    + projected_other
    + projected_marketing
)

projected_profit = projected_revenue - projected_costs

projected_margin = (
    projected_profit / projected_revenue * 100
    if projected_revenue > 0
    else 0
)

profit_difference = projected_profit - operating_profit

col1, col2, col3 = st.columns(3)

col1.metric(
    "Projected Revenue",
    f"₹{projected_revenue:,.0f}"
)

col2.metric(
    "Projected Operating Profit",
    f"₹{projected_profit:,.0f}",
    delta=f"₹{profit_difference:,.0f} vs current"
)

col3.metric(
    "Projected Profit Margin",
    f"{projected_margin:.2f}%"
)

# ---------------- RECOMMENDATIONS ----------------

st.header("5. Business Recommendations")

recommendations = []

if gross_margin < 25:
    recommendations.append(
        "Review supplier costs, product pricing and product mix."
    )

if operating_margin < 10:
    recommendations.append(
        "Review recurring operating expenses and identify "
        "realistic savings opportunities."
    )

if operating_profit < 0:
    recommendations.append(
        "Prepare a recovery plan covering pricing, costs, "
        "sales and cash flow."
    )

if projected_profit > operating_profit:
    recommendations.append(
        "The selected scenario has a higher projected profit "
        "under the current model assumptions."
    )

if not recommendations:
    recommendations.append(
        "Monitor monthly margins, sales and expenses to maintain "
        "financial performance."
    )

for recommendation in recommendations:
    st.write("•", recommendation)

st.caption(
    "BusinessPilot AI uses transparent financial calculations "
    "and predefined rules. Projections are hypothetical scenarios, "
    "not guarantees of future results or trained AI predictions."
)

# ---------------- DOWNLOAD REPORT ----------------

st.header("6. Download Financial Report")

report = pd.DataFrame({
    "Metric": [
        "Monthly Revenue",
        "Cost of Goods",
        "Gross Profit",
        "Operating Expenses",
        "Total Costs",
        "Operating Profit",
        "Gross Margin (%)",
        "Operating Margin (%)",
        "Projected Revenue",
        "Projected Operating Profit",
        "Projected Profit Margin (%)"
    ],
    "Value": [
        revenue,
        cogs,
        gross_profit,
        operating_expenses,
        total_costs,
        operating_profit,
        gross_margin,
        operating_margin,
        projected_revenue,
        projected_profit,
        projected_margin
    ]
})

st.download_button(
    label="📥 Download Business Report (CSV)",
    data=report.to_csv(index=False).encode("utf-8"),
    file_name="businesspilot_financial_report.csv",
    mime="text/csv"
)
