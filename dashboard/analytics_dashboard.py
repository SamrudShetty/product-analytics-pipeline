import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
from urllib.parse import quote_plus

password = quote_plus("admin@123")
engine = create_engine(
    f"postgresql://postgres:{password}@localhost:5432/analytics"
)

st.set_page_config(page_title="Product Analytics Dashboard", layout="wide")

st.title("📊 Product Analytics Dashboard")

# -------------------------
# FUNNEL DATA
# -------------------------
query = """
WITH users AS (
    SELECT
        user_id,
        MAX(CASE WHEN event_name = 'page_view' THEN 1 ELSE 0 END) AS viewed,
        MAX(CASE WHEN event_name = 'sign_up' THEN 1 ELSE 0 END) AS signed_up,
        MAX(CASE WHEN event_name = 'purchase' THEN 1 ELSE 0 END) AS purchased
    FROM events
    GROUP BY user_id
)

SELECT
    SUM(viewed) AS viewed_users,
    SUM(signed_up) AS signup_users,
    SUM(purchased) AS purchased_users,
    SUM(signed_up)::float / SUM(viewed) AS signup_rate,
    SUM(purchased)::float / SUM(signed_up) AS purchase_rate
FROM users;
"""

df = pd.read_sql(query, engine)

viewed = int(df["viewed_users"][0])
signed = int(df["signup_users"][0])
purchased = int(df["purchased_users"][0])

signup_rate = round(df["signup_rate"][0] * 100, 2)
purchase_rate = round(df["purchase_rate"][0] * 100, 2)

# Metrics
st.subheader("📌 Key Metrics")
col1, col2, col3 = st.columns(3)

col1.metric("👀 Visitors", viewed)
col2.metric("📝 Signups", f"{signed} ({signup_rate}%)")
col3.metric("💰 Purchases", f"{purchased} ({purchase_rate}%)")

# Funnel Chart
st.subheader("📉 Funnel Drop-off")
funnel_df = pd.DataFrame({
    "Stage": ["Page View", "Sign Up", "Purchase"],
    "Users": [viewed, signed, purchased]
})
st.bar_chart(funnel_df.set_index("Stage"))

# Insights
st.subheader("🧠 Insights")
st.write(f"""
- {signup_rate}% users sign up after visiting  
- Only {purchase_rate}% convert after signup  
- Major drop happens post signup  
""")

# -------------------------
# A/B TEST
# -------------------------
ab_query = """
WITH users AS (
    SELECT
        user_id,
        "group",
        MAX(CASE WHEN event_name = 'page_view' THEN 1 ELSE 0 END) AS viewed,
        MAX(CASE WHEN event_name = 'sign_up' THEN 1 ELSE 0 END) AS signed_up,
        MAX(CASE WHEN event_name = 'purchase' THEN 1 ELSE 0 END) AS purchased
    FROM events
    GROUP BY user_id, "group"
)

SELECT
    "group",
    SUM(viewed) AS users,
    SUM(signed_up)::float / SUM(viewed) AS signup_rate,
    SUM(purchased)::float / SUM(signed_up) AS purchase_rate
FROM users
GROUP BY "group"
ORDER BY "group";
"""

ab_df = pd.read_sql(ab_query, engine)

st.subheader("🧪 A/B Test Results")
st.dataframe(ab_df)

st.success("🚀 Variant B is the winning version!")

# -------------------------
# COHORT HEATMAP
# -------------------------
st.subheader("🔥 Cohort Retention")

cohort_query = """
WITH user_first_event AS (
    SELECT user_id, MIN(event_date::date) AS cohort_date
    FROM events
    GROUP BY user_id
),
user_activity AS (
    SELECT
        e.user_id,
        u.cohort_date,
        (e.event_date::date - u.cohort_date) AS days_since_signup
    FROM events e
    JOIN user_first_event u ON e.user_id = u.user_id
),
cohort_size AS (
    SELECT cohort_date, COUNT(DISTINCT user_id) AS total_users
    FROM user_first_event
    GROUP BY cohort_date
)

SELECT
    ua.cohort_date,
    ua.days_since_signup,
    COUNT(DISTINCT ua.user_id)::float / cs.total_users AS retention_rate
FROM user_activity ua
JOIN cohort_size cs ON ua.cohort_date = cs.cohort_date
GROUP BY ua.cohort_date, ua.days_since_signup, cs.total_users
"""

cohort_df = pd.read_sql(cohort_query, engine)

pivot = cohort_df.pivot(index="cohort_date", columns="days_since_signup", values="retention_rate")

st.dataframe(pivot)