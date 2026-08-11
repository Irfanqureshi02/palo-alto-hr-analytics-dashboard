import streamlit as st
import pandas as pd
import plotly.express as px

# ---------------------------------
# Page Config
# ---------------------------------

st.set_page_config(
    page_title="Palo Alto Networks HR Analytics Dashboard",
    page_icon="📊",
    layout="wide"
)

# ---------------------------------
# Load Data
# ---------------------------------

df = pd.read_csv("employee_engagement_final.csv")


# ---------------------------------
# Sidebar Filters
# ---------------------------------

# st.sidebar.header("🔎 Dashboard Filters")

# department = st.sidebar.multiselect(
#     "Department",
#     options=df["Department"].unique(),
#     default=df["Department"].unique()
# )

# job_role = st.sidebar.multiselect(
#     "Job Role",
#     options=df["JobRole"].unique(),
#     default=df["JobRole"].unique()
# )

# filtered_df = df[
#     (df["Department"].isin(department))
#     &
#     (df["JobRole"].isin(job_role))
# ]


# ---------------------------------
# Sidebar Filters
# ---------------------------------

st.sidebar.header("🎯 Analysis Filters")

department = st.sidebar.selectbox(
    "Department",
    ["All"] + list(df["Department"].unique())
)

if department == "All":
    filtered_df = df
else:
    filtered_df = df[df["Department"] == department]

job_role = st.sidebar.selectbox(
    "Job Role",
    ["All"] + list(filtered_df["JobRole"].unique())
)

if job_role != "All":
    filtered_df = filtered_df[
        filtered_df["JobRole"] == job_role
    ]

# ---------------------------------
# Header
# ---------------------------------

st.title("📊 Employee Engagement, Satisfaction & Burnout Dashboard")

st.markdown("""
### Palo Alto Networks HR Analytics Project

This dashboard provides:

- Engagement Health Overview
- Burnout Risk Analysis
- Role & Career Stage Analysis
- Manager Action Panel
- Strategic Recommendations
""")

st.divider()

# ---------------------------------
# KPI Calculations
# ---------------------------------

# engagement_index = round(df["EngagementIndex"].mean(), 2)

# burnout_rate = round(
#     (df["BurnoutRisk"] == "High").mean() * 100,
#     2
# )

# work_life_balance = round(
#     df["WorkLifeBalance"].mean(),
#     2
# )

# attrition_rate = round(
#     (df["Attrition"] == "Yes").mean() * 100,
#     2
# )

engagement_index = round(
    filtered_df["EngagementIndex"].mean(), 2
)

burnout_rate = round(
    (filtered_df["BurnoutRisk"] == "High").mean() * 100,
    2
)

work_life_balance = round(
    filtered_df["WorkLifeBalance"].mean(),
    2
)

attrition_rate = round(
    (filtered_df["Attrition"] == "Yes").mean() * 100,
    2
)
# ---------------------------------
# KPI Cards
# ---------------------------------

col1, col2, col3, col4 = st.columns(4)

col1.metric("📈 Engagement Index", engagement_index)
col2.metric("🔥 Burnout Risk", f"{burnout_rate}%")
col3.metric("⚖️ Work-Life Balance", work_life_balance)
col4.metric("🚪 Attrition Rate", f"{attrition_rate}%")

# ---------------------------------
# Executive Summary
# ---------------------------------

st.subheader("📋 Executive Summary")

st.info(f"""
Average Engagement Index: {engagement_index}

Burnout Risk Employees: {burnout_rate}%

Attrition Rate: {attrition_rate}%

Work-Life Balance Score: {work_life_balance}

Key Finding:
Employees with high burnout risk demonstrate lower engagement
and significantly higher attrition probability.
""")

# ---------------------------------
# Sidebar Filters
# ---------------------------------

# st.sidebar.header("🔎 Dashboard Filters")

# department = st.sidebar.multiselect(
#     "Department",
#     options=df["Department"].unique(),
#     default=df["Department"].unique()
# )

# job_role = st.sidebar.multiselect(
#     "Job Role",
#     options=df["JobRole"].unique(),
#     default=df["JobRole"].unique()
# )

# filtered_df = df[
#     (df["Department"].isin(department))
#     &
#     (df["JobRole"].isin(job_role))
# ]



# =================================
# MODULE 1
# Engagement Health Overview
# =================================

st.header("📊 Engagement Health Overview")

col1, col2 = st.columns(2)

with col1:

    fig = px.box(
        filtered_df,
        x="Attrition",
        y="EngagementIndex",
        color="Attrition",
        title="Engagement Index vs Attrition"
    )

    st.plotly_chart(fig, use_container_width=True)

with col2:

    dept_engagement = (
        filtered_df
        .groupby("Department")["EngagementIndex"]
        .mean()
        .reset_index()
    )

    fig = px.bar(
        dept_engagement,
        x="Department",
        y="EngagementIndex",
        title="Average Engagement by Department"
    )

    st.plotly_chart(fig, use_container_width=True)

# =================================
# MODULE 2
# Burnout Risk Dashboard
# =================================

st.header("🔥 Burnout Risk Dashboard")

burnout = (
    filtered_df["BurnoutRisk"]
    .value_counts()
    .reset_index()
)

burnout.columns = ["BurnoutRisk", "Count"]

col1, col2 = st.columns(2)

with col1:

    fig = px.bar(
        burnout,
        x="BurnoutRisk",
        y="Count",
        title="Burnout Risk Distribution"
    )

    st.plotly_chart(fig, use_container_width=True)

with col2:

    fig = px.pie(
        burnout,
        names="BurnoutRisk",
        values="Count",
        hole=0.5,
        title="Burnout Risk Share"
    )

    st.plotly_chart(fig, use_container_width=True)

# =================================
# MODULE 3
# Role & Career Stage Analysis
# =================================

st.header("👨‍💼 Role & Career Stage Analysis")

role_engagement = (
    filtered_df
    .groupby("JobRole")["EngagementIndex"]
    .mean()
    .sort_values()
    .reset_index()
)

fig = px.bar(
    role_engagement,
    x="EngagementIndex",
    y="JobRole",
    orientation="h",
    title="Engagement by Job Role"
)

st.plotly_chart(fig, use_container_width=True)

if "TenureGroup" in filtered_df.columns:

    tenure = (
        filtered_df
        .groupby("TenureGroup")["EngagementIndex"]
        .mean()
        .reset_index()
    )

    fig = px.line(
        tenure,
        x="TenureGroup",
        y="EngagementIndex",
        markers=True,
        title="Tenure vs Engagement"
    )

    st.plotly_chart(fig, use_container_width=True)

# =================================
# MODULE 4
# Manager Action Panel
# =================================

st.header("🚨 Manager Action Panel")



low_engagement = filtered_df[
    filtered_df["EngagementIndex"] < 2.5
]

col1, col2 = st.columns(2)

with col1:

    dept_count = (
        low_engagement["Department"]
        .value_counts()
    )

    fig = px.bar(
        x=dept_count.index,
        y=dept_count.values,
        title="Low Engagement Employees by Department"
    )

    st.plotly_chart(fig, use_container_width=True)

with col2:

    role_count = (
        low_engagement["JobRole"]
        .value_counts()
    )

    fig = px.bar(
        x=role_count.index,
        y=role_count.values,
        title="Low Engagement Employees by Job Role"
    )

    st.plotly_chart(fig, use_container_width=True)


# =================================
# High Risk Employees
# =================================

st.header("🚨 High Risk Employees")

high_risk = filtered_df[
    filtered_df["BurnoutRisk"] == "High"
]

st.dataframe(
    high_risk[
        [
            "Department",
            "JobRole",
            "WorkLifeBalance",
            "JobSatisfaction",
            "EngagementIndex",
            "BurnoutRisk"
        ]
    ]
)


# =================================
# Data Table
# =================================

st.header("📄 Employee Data")

display_cols = [
    "Age",
    "Department",
    "JobRole",
    "JobLevel",
    "MonthlyIncome",
    "WorkLifeBalance",
    "JobSatisfaction",
    "EnvironmentSatisfaction",
    "Attrition",
    "EngagementIndex",
    "BurnoutRisk",
    "TenureGroup"
]

st.dataframe(filtered_df[display_cols])

csv = filtered_df[display_cols].to_csv(index=False)

st.download_button(
    "📥 Download Filtered Data",
    csv,
    "employee_data.csv",
    "text/csv"
)

# =================================
# Recommendations
# =================================

st.header("🎯 Strategic Recommendations")

st.success("""
1. Prioritize High Burnout Employees

2. Focus on Sales Executives and Research Scientists

3. Improve Work-Life Balance Programs

4. Conduct Quarterly Engagement Surveys

5. Strengthen Manager-Led Intervention Plans

6. Monitor Early Attrition Indicators

7. Improve Career Growth Discussions
""")