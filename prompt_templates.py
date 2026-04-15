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
1. Generate pandas transformation (if needed)
2. Suggest correct Plotly chart config
3. Provide insights

RULES:
- No imports
- No matplotlib
- Only pandas logic
- DataFrame is df
- Create result_df

OUTPUT JSON:

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
