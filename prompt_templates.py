def build_prompt(chart_type, x, y, hue, df_columns):

    return f"""
You are a Data Visualization Expert.

Dataset columns: {df_columns}

User selected:
- Chart: {chart_type}
- X: {x}
- Y: {y}
- Hue: {hue}

TASK:
- Generate pandas transformation if needed
- Suggest chart configuration
- Generate insights

STRICT RULES:
- Output ONLY valid JSON
- Do NOT include explanation outside JSON
- Do NOT use markdown (no ```json)
- Response MUST start with {{ and end with }}
- DO NOT use import
- DO NOT use matplotlib or seaborn
- DataFrame is df
- MUST create result_df

OUTPUT:

{{
 "python_code": "...",
 "chart": {{
    "type": "{chart_type}",
    "x": "{x}",
    "y": "{y}",
    "color": "{hue}"
 }},
 "insights": "..."
}}
"""
