import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import requests
from datetime import datetime
from io import StringIO

st.set_page_config(page_title="智电未来", layout="wide")

st.title("✅ 智电未来 - 新仓库测试")

try:
    # 测试网络
    r = requests.get("https://www.baidu.com", timeout=5)
    st.success("网络连接正常")
    
    # 生成示例数据
    hours = list(range(24))
    load_data = [5,3,2,1,1,2,8,25,35,30,25,22,20,25,30,35,40,45,50,48,42,30,20,10]
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=hours, y=load_data, mode='lines', name='充电负荷'))
    st.plotly_chart(fig)
    
except Exception as e:
    st.error(f"错误: {e}")
