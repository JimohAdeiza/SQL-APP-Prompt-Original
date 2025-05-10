import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px
from openai import OpenAI  # New import

# Initialize OpenAI client using v1 format
client = OpenAI(api_key=st.secrets["openai_api_key"])

# Load DB schema (to guide LLM)
def get_schema():
    return """
Tables:
- merchants(id, name, onboarded_date, location)
- transactions(id, merchant_id, amount, date)
"""

# Convert prompt to SQL using OpenAI v1
def prompt_to_sql(prompt):
    schema = get_schema()
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": f"You convert natural language to SQL. Use this schema: {schema}"},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content

# Run SQL and get result
def run_query(sql):
    conn = sqlite3.connect("sample.db")
    try:
        df = pd.read_sql_query(sql, conn)
    except Exception as e:
        return None, str(e)
    return df, None

# Streamlit UI
st.title("🧠 Prompt-to-SQL Analytics")

prompt = st.text_area("Enter your prompt", "List all merchants and their locations")
if st.button("Generate Report"):
    with st.spinner("Generating SQL..."):
        sql = prompt_to_sql(prompt)
        st.code(sql, language='sql')
        df, error = run_query(sql)
        if error:
            st.error(f"SQL Error: {error}")
        else:
            st.dataframe(df)
            if 'amount' in df.columns:
                fig = px.bar(df, x=df.columns[0], y='amount')
                st.plotly_chart(fig)
