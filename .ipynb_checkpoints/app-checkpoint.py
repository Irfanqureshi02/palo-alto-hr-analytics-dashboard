import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(
    page_title="Employee Engagement Dashboard",
    layout="wide"
)

# Load CSV
df = pd.read_csv("employee_engagement_final.csv")

st.title("📊 Employee Engagement, Satisfaction & Burnout Dashboard")
st.write("Palo Alto Networks HR Analytics Project")

### KPI Cards

# KPI Calculations
engagement_index = round(df['EngagementIndex'].mean(), 2)

burnout_rate = round(
    ((df['BurnoutRisk'] == 'High').sum() / len(df)) * 100,
    2
)

work_life_balance = round(
    df['WorkLifeBalance'].mean(),
    2
)

attrition_rate = round(
    (df['Attrition'] == 'Yes').mean() * 100,
    2
)

# KPI Cards
# col1, col2, col3, col4 = st.columns(4)

# with col1:
#     st.metric("Engagement Index", engagement_index)

# with col2:
#     st.metric("Burnout Risk %", f"{burnout_rate}%")

# with col3:
#     st.metric("Work-Life Balance", work_life_balance)

# with col4:
#     st.metric("Attrition Rate", f"{attrition_rate}%")

col1, col2, col3, col4 = st.columns(4)

col1.metric("📈 Engagement Index", engagement_index)
col2.metric("🔥 Burnout Risk", f"{burnout_rate}%")
col3.metric("⚖️ Work-Life Balance", work_life_balance)
col4.metric("🚪 Attrition Rate", f"{attrition_rate}%")

##Executive Summary

st.subheader("📋 Executive Summary")

st.info(f"""
• Average Engagement Score: {engagement_index}

• Burnout Risk Employees: {burnout_rate}%

• Attrition Rate: {attrition_rate}%

• Work-Life Balance Score: {work_life_balance}

• High Burnout employees show significantly higher attrition risk.
""")


##Sidebar Department Filter

st.sidebar.header("Filters")

department = st.sidebar.multiselect(
    "Select Department",
    options=df['Department'].unique(),
    default=df['Department'].unique()
)

filtered_df = df[df['Department'].isin(department)]

##Burnout Risk Chart

import plotly.express as px

burnout_count = filtered_df['BurnoutRisk'].value_counts()

fig = px.bar(
    x=burnout_count.index,
    y=burnout_count.values,
    title="Burnout Risk Distribution"
)

st.plotly_chart(fig, use_container_width=True)


burnout = filtered_df['BurnoutRisk'].value_counts()

fig = px.pie(
    values=burnout.values,
    names=burnout.index,
    hole=0.5,
    title="Burnout Risk Distribution"
)

st.plotly_chart(fig, use_container_width=True)



## Engagement vs Attrition (Box Plot)
import plotly.express as px

fig = px.box(
    filtered_df,
    x="Attrition",
    y="EngagementIndex",
    color="Attrition",
    title="Engagement Index vs Attrition"
)

st.plotly_chart(fig, use_container_width=True)

#Low Engagement by Department
low_engagement = filtered_df[
    filtered_df['EngagementIndex'] < 2.5
]

dept_count = low_engagement['Department'].value_counts()

fig = px.bar(
    x=dept_count.index,
    y=dept_count.values,
    title="Low Engagement Employees by Department",
    labels={"x":"Department","y":"Employees"}
)

st.plotly_chart(fig, use_container_width=True)

# Low Engagement by Job Role

role_count = low_engagement['JobRole'].value_counts()

fig = px.bar(
    x=role_count.index,
    y=role_count.values,

   title="Low Engagement Employees by Job Role"
)

st.plotly_chart(fig, use_container_width=True)





st.subheader("🎯 Recommendations")

st.success("""
1. Monitor high burnout employees.
2. Focus on Sales Executives and Research Scientists.
3. Improve work-life balance initiatives.
4. Conduct engagement surveys quarterly.
5. Strengthen manager-led interventions.
""")



burnout_counts = (
    df['BurnoutRisk']
    .value_counts()
    .reset_index()
)

burnout_counts.columns = ['BurnoutRisk', 'Count']


fig_burnout = px.bar(
    burnout_counts,
    x='BurnoutRisk',
    y='Count',
    title='Burnout Risk Distribution'
)

attrition_counts = (
    df['Attrition']
    .value_counts()
    .reset_index()
)

attrition_counts.columns = ['Attrition', 'Count']

fig_attrition = px.pie(
    attrition_counts,
    names='Attrition',
    values='Count',
    title='Attrition Distribution'
)
fig_attrition = px.pie(
    attrition_counts,
    names='Attrition',
    values='Count',
    title='Attrition Distribution'
)

# Yahan lagana hai
col1, col2 = st.columns(2)

with col1:
    st.plotly_chart(fig_burnout, use_container_width=True)

with col2:
    st.plotly_chart(fig_attrition, use_container_width=True)


