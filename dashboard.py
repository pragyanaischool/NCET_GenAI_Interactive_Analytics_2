import streamlit as st
import plotly.express as px
from groq_llm import ask_llm


def init_dashboard():
    if "dashboard_charts" not in st.session_state:
        st.session_state.dashboard_charts = []


def add_to_dashboard(chart_config):
    st.session_state.dashboard_charts.append(chart_config)


def render_dashboard(df):
    st.header("📊 GenAI Dashboard")

    charts = st.session_state.get("dashboard_charts", [])

    if not charts:
        st.info("No charts added yet.")
        return

    for i, chart in enumerate(charts):

        st.subheader(f"Chart {i+1}")

        try:
            x = chart["x"]
            y = chart["y"]
            chart_type = chart["type"]
            color = chart.get("color")

            if chart_type == "bar":
                fig = px.bar(df, x=x, y=y, color=color)

            elif chart_type == "line":
                fig = px.line(df, x=x, y=y, color=color)

            elif chart_type == "scatter":
                fig = px.scatter(df, x=x, y=y, color=color)

            elif chart_type == "pie":
                fig = px.pie(df, names=x, values=y)

            elif chart_type == "histogram":
                fig = px.histogram(df, x=x)

            elif chart_type == "box":
                fig = px.box(df, x=x, y=y)

            else:
                fig = px.bar(df, x=x, y=y)

            st.plotly_chart(fig, use_container_width=True)

        except Exception as e:
            st.error(f"Chart error: {e}")

    # ---------------- DASHBOARD INSIGHTS ----------------
    if st.button("🧠 Generate Dashboard Insights"):

        st.subheader("📊 Dashboard Insights")

        chart_summary = "\n".join([
            f"{c['type']} chart with X={c['x']} and Y={c['y']}"
            for c in charts
        ])

        prompt = f"""
You are a BI expert.

Charts in dashboard:
{chart_summary}

Dataset columns: {df.columns.tolist()}

TASK:
- Summarize overall insights
- Identify key trends
- Highlight important patterns
- Suggest business actions

Output simple text.
"""

        response = ask_llm(prompt)

        st.write(response)
