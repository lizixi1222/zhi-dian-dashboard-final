import streamlit as st
import pandas as pd
import requests
from io import StringIO

st.set_page_config(page_title="测试", page_icon="✅")
st.title("✅ 测试页面")

try:
    url = "https://github.com/lizixi1222/zhi-dian-dashboard/releases/download/v1.0-data/1_24_1_4.csv"
    response = requests.get(url, timeout=10)
    df = pd.read_csv(StringIO(response.text))
    st.success(f"成功加载 {len(df)} 条数据")
    st.dataframe(df.head())
except Exception as e:
    st.error(f"错误: {e}")
