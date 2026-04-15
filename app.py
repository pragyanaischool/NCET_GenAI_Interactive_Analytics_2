import streamlit as st
import pandas as pd
import plotly.express as px

from groq_llm import ask_llm
from prompt_templates import build_prompt
from utils import extract_json

st.set_page_config(layout="wide")
st.title("PragyanAI GenAI Tableau-like Dashboard")
st.image('PragyanAI_Transperent.png')

# ---------------- DASHBOARD STATE ----------------
if "dashboard_charts" not in st.session_state:
    st.session_state.dashboard_charts = []

if "last_chart" not in st.session_state:
    st.session_state.last_chart = None

# ---------------- Upload ----------------
file = st.file_uploader("Upload CSV", type=["csv"])

if file:
    df = pd.read_csv(file)

    st.subheader("Dataset Preview")
    st.dataframe(df.head())

    columns = df.columns.tolist()

    # ---------------- Sidebar Controls ----------------
    st.sidebar.header("Chart Builder")

    chart_type = st.sidebar.selectbox(
        "Chart Type",
        ["bar", "line", "scatter", "pie", "histogram", "box"]
    )

    x = st.sidebar.selectbox("X-axis", columns)
    y = st.sidebar.selectbox("Y-axis", columns)

    hue = st.sidebar.selectbox("Hue / Color", ["None"] + columns)
    hue = None if hue == "None" else hue

    # ---------------- Generate Chart ----------------
    if st.button("Generate Chart"):

        prompt = build_prompt(chart_type, x, y, hue, columns)
        response = ask_llm(prompt)

        # ---------------- SAFE PARSING ----------------
        parsed = extract_json(response)

        if parsed is None:
            st.warning("LLM parsing failed — using fallback")

            parsed = {
                "python_code": "result_df = df.head(20)",
                "chart": {"type": chart_type, "x": x, "y": y, "color": hue},
                "insights": "Fallback result shown due to parsing issue."
            }

        # ---------------- DATA ----------------
        result_df = df.copy()

        # ---------------- CHART ----------------
        try:
            if chart_type == "bar":
                fig = px.bar(result_df, x=x, y=y, color=hue)

            elif chart_type == "line":
                fig = px.line(result_df, x=x, y=y, color=hue)

            elif chart_type == "scatter":
                fig = px.scatter(result_df, x=x, y=y, color=hue)

            elif chart_type == "pie":
                fig = px.pie(result_df, names=x, values=y)

            elif chart_type == "histogram":
                fig = px.histogram(result_df, x=x)

            elif chart_type == "box":
                fig = px.box(result_df, x=x, y=y)

            st.subheader("Visualization")
            st.plotly_chart(fig, use_container_width=True)

            # 🔥 STORE LAST CHART (KEY FIX)
            st.session_state.last_chart = {
                "type": chart_type,
                "x": x,
                "y": y,
                "color": hue
            }

        except Exception as e:
            st.error(f" Chart error: {e}")

        # ---------------- INSIGHTS ----------------
        if st.button(" Generate Insights"):

            st.subheader(" Insights")

            insights = parsed.get("insights", "No insights available")

            if isinstance(insights, str):
                lines = [line.strip() for line in insights.split(".") if line.strip()]
                for line in lines:
                    st.markdown(f"• {line}")
            else:
                st.write(insights)

            # ---------------- ADVANCED ANALYSIS ----------------
            st.subheader(" Deep Analysis")

            try:
                deep_prompt = f"""
                You are a senior data analyst.

                Dataset columns: {columns}

                Chart used:
                - X: {x}
                - Y: {y}
                - Hue: {hue}

                Initial insights:
                {insights}

                TASK:
                - Expand insights
                - Identify trends
                - Highlight anomalies
                - Give business recommendations

                Output simple text.
                """

                deep_response = ask_llm(deep_prompt)
                st.write(deep_response)

            except Exception:
                st.warning(" Deep analysis failed")

            # ---------------- KPI SUMMARY ----------------
            st.subheader(" Quick Stats")

            try:
                col1, col2, col3 = st.columns(3)

                col1.metric("Rows", len(result_df))
                col2.metric("Columns", len(result_df.columns))

                if y in result_df.columns:
                    col3.metric("Avg Value", round(result_df[y].mean(), 2))

            except:
                pass

            # ---------------- NEXT QUESTIONS ----------------
            st.subheader(" Suggested Questions")

            try:
                suggestion_prompt = f"""
                Based on this dataset and analysis:

                Columns: {columns}
                Insights: {insights}

                Suggest 3 smart next analytical questions.
                Return as a list.
                """

                suggestion_response = ask_llm(suggestion_prompt)

                suggestions = [q.strip("- ").strip() for q in suggestion_response.split("\n") if q.strip()]

                for i, q in enumerate(suggestions):
                    if st.button(q, key=f"insight_suggest_{i}"):
                        st.session_state.query = q
                        st.rerun()

            except:
                st.write("No suggestions available")

        # ---------------- DEBUG ----------------
        with st.expander("Debug (LLM Response)"):
            st.text(response)

    # ---------------- ADD TO DASHBOARD ----------------
    if st.session_state.last_chart is not None:

        if st.button("➕ Add Last Chart to Dashboard"):
            st.session_state.dashboard_charts.append(
                st.session_state.last_chart
            )
            st.success("Added to dashboard!")

    # ================== DASHBOARD SECTION ==================

    st.sidebar.markdown("---")
    st.sidebar.subheader(" Dashboard")

    if st.sidebar.button(" View Dashboard"):

        st.header(" Dashboard View")

        charts = st.session_state.dashboard_charts

        if not charts:
            st.info("No charts added yet.")
        else:

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
            if st.button(" Generate Dashboard Insights"):

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
                - Identify trends
                - Highlight patterns
                - Suggest business actions

                Output simple text.
                """

                try:
                    response = ask_llm(prompt)
                    st.write(response)
                except:
                    st.warning("Insight generation failed")

    # ---------------- DEBUG DASHBOARD ----------------
    with st.expander(" Dashboard Debug"):
        st.write(st.session_state.dashboard_charts)
