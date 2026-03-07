import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import requests
from datetime import datetime

st.set_page_config(
    page_title="智电未来 - 第三步",
    page_icon="⚡",
    layout="wide"
)

st.title("✅ 第三步 - 数据加载函数测试")

# 定义数据加载函数（先不调用）
@st.cache_data
def load_csv_from_release(filename):
    url = f"https://github.com/lizixi1222/zhi-dian-dashboard/releases/download/v1.0-data/{filename}"
    try:
        response = requests.get(url, timeout=10)
        df = pd.read_csv(pd.compat.StringIO(response.text))
        return df
    except Exception as e:
        st.error(f"加载失败: {e}")
        return None

st.success("函数定义成功，尚未调用")
