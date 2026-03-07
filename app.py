import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import requests
from datetime import datetime

st.set_page_config(
    page_title="智电未来 - 测试",
    page_icon="⚡",
    layout="wide"
)

st.title("✅ 智电未来 - 第二步测试")
st.write("基础框架加载成功")

# 简单的数据
data = pd.DataFrame({
    'x': [1,2,3,4,5],
    'y': [10,20,15,25,30]
})

fig = go.Figure()
fig.add_trace(go.Scatter(x=data['x'], y=data['y'], mode='lines+markers'))
st.plotly_chart(fig)

if st.button("点击测试"):
    st.balloons()
