import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import requests
from datetime import datetime

st.set_page_config(
    page_title="智电未来 - 第四步",
    page_icon="⚡",
    layout="wide"
)

st.title("✅ 第四步 - 加载真实数据")

@st.cache_data
def load_csv_from_release(filename):
    url = f"https://github.com/lizixi1222/zhi-dian-dashboard/releases/download/v1.0-data/{filename}"
    try:
        response = requests.get(url, timeout=30)
        df = pd.read_csv(pd.compat.StringIO(response.text))
        return df
    except Exception as e:
        st.error(f"加载 {filename} 失败: {e}")
        return None

# 加载数据
with st.spinner("正在加载CSV文件..."):
    df1 = load_csv_from_release("1_24_1_4.csv")
    df2 = load_csv_from_release("2_24_1_4.csv")
    df3 = load_csv_from_release("3_24_1_4.csv")

valid_dfs = [df for df in [df1, df2, df3] if df is not None]

if valid_dfs:
    df = pd.concat(valid_dfs, ignore_index=True)
    st.success(f"✅ 成功加载 {len(df):,} 条记录")
    st.dataframe(df.head(10))  # 显示前10行
else:
    st.error("没有加载到任何数据")
