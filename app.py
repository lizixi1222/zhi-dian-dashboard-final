import streamlit as st
import sys
import traceback

st.set_page_config(page_title="调试模式", page_icon="🔍")

st.title("🔍 调试模式 - 查看错误")

try:
    # 导入所有库
    import pandas as pd
    import numpy as np
    import plotly.graph_objects as go
    import requests
    from datetime import datetime
    from io import StringIO
    
    st.success("✅ 所有库导入成功")
    
    # 测试网络
    try:
        r = requests.get("https://www.baidu.com", timeout=5)
        st.success(f"✅ 网络正常: {r.status_code}")
    except Exception as e:
        st.error(f"❌ 网络错误: {e}")
    
    # 尝试加载CSV
    try:
        url = "https://github.com/lizixi1222/zhi-dian-dashboard/releases/download/v1.0-data/1_24_1_4.csv"
        r = requests.get(url, timeout=10)
        df = pd.read_csv(StringIO(r.text))
        st.success(f"✅ CSV加载成功: {len(df)}行")
        st.dataframe(df.head())
    except Exception as e:
        st.error(f"❌ CSV加载失败: {e}")
        st.code(traceback.format_exc())
        
except Exception as e:
    st.error(f"❌ 致命错误: {e}")
    st.code(traceback.format_exc())
