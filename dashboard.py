import streamlit as st
import pandas as pd
import sqlite3

# Database connect
conn = sqlite3.connect("nextgen.db")

# Load tables
applicants = pd.read_sql("SELECT * FROM applicants;", conn)
interns = pd.read_sql("SELECT * FROM interns;", conn)
scores = pd.read_sql("SELECT * FROM hackathon_scores;", conn)

# Domain filter
domain_list = ['All'] + sorted([str(x) for x in applicants['Domain Applied'].dropna().unique().tolist()])
selected_domain = st.selectbox("Select Domain", domain_list)


if selected_domain != 'All':
    applicants = applicants[applicants['Domain Applied'] == selected_domain]
    interns = interns[interns['domain'] == selected_domain]
    scores = scores[scores['domain'] == selected_domain]

# Funnel
st.subheader("📊 Funnel")
st.metric("Total Applicants", len(applicants))
st.metric("Completed Interns", len(interns[interns['completion_status'] == 'Completed']))

# Completion rate per domain
st.subheader("✅ Completion Rate per Domain")
completion_rate = interns.groupby("domain")["completion_status"].apply(lambda x: (x=="Completed").mean()*100)
st.bar_chart(completion_rate)

# Average hackathon score per domain
st.subheader("🎯 Average Hackathon Score per Domain")
avg_scores = scores.groupby("domain")["score"].mean()
st.bar_chart(avg_scores)

# Leaderboard
st.subheader("🏆 Top 10 Performers")
top10 = scores.sort_values("score", ascending=False).head(10)
st.dataframe(top10)