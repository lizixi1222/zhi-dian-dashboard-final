import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import requests
from datetime import datetime
from io import StringIO

st.set_page_config(
    page_title="智电未来 - 场站运营看板",
    page_icon="⚡",
    layout="wide"
)

st.title("🚀 正在加载数据...")

@st.cache_data
def load_sample_data():
    """只读取前10万行数据"""
    url = "https://github.com/lizixi1222/zhi-dian-dashboard/releases/download/v1.0-data/1_24_1_4.csv"
    try:
        response = requests.get(url, timeout=30)
        # 只读取前10万行
        df = pd.read_csv(StringIO(response.text), nrows=100000)
        return df
    except Exception as e:
        st.error(f"加载失败: {e}")
        return None

# 加载数据
df = load_sample_data()

if df is not None:
    st.success(f"✅ 成功加载 {len(df)} 条数据")
    
    # 数据处理
    df['DATA_TIME'] = pd.to_datetime(df['DATA_TIME'])
    df['hour'] = df['DATA_TIME'].dt.hour
    df['power_kw'] = df['totalVoltage'] * df['totalCurrent'] / 1000
    
    # 小时分布
    hourly = df.groupby('hour')['power_kw'].mean()
    hours = list(range(24))
    load_data = [hourly.get(h, 0) for h in hours]
    
    # 显示图表
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=hours, y=load_data, mode='lines'))
    st.plotly_chart(fig)
    
    # 显示数据预览
    st.dataframe(df.head())
