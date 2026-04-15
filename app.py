import streamlit as st
import pandas as pd
import plotly.express as px

from groq_llm import ask_llm
from prompt_templates import build_prompt
from utils import extract_json

st.set_page_config(layout="wide")
st.title("📊 GenAI Tableau-like Dashboard")

# ---------------- Upload ----------------
file = st.file_uploader("Upload CSV", type=["csv"])

if file:
    df = pd.read_csv(file)

    st.subheader("📊 Dataset Preview")
    st.dataframe(df.head())

    columns = df.columns.tolist()

    # ---------------- Sidebar Controls ----------------
    st.sidebar.header("📊 Chart Builder")

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
            st.warning("⚠️ LLM parsing failed — using fallback")

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

            st.subheader("📊 Visualization")
            st.plotly_chart(fig, use_container_width=True)

        except Exception as e:
            st.error(f"❌ Chart error: {e}")

        # ---------------- INSIGHTS ----------------
        if st.button("🧠 Generate Insights"):
            st.subheader("💡 Insights")
            st.write(parsed.get("insights", "No insights available"))

        # ---------------- DEBUG ----------------
        with st.expander("🔍 Debug (LLM Response)"):
            st.text(response)
