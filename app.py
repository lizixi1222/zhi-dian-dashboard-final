import streamlit as st
import requests
from io import StringIO

st.set_page_config(page_title="测试", page_icon="✅")

st.title("✅ 极简测试页面")

try:
    # 只测试网络连接，不加载CSV
    response = requests.get("https://www.baidu.com", timeout=5)
    st.success(f"网络连接正常，状态码: {response.status_code}")
    
    st.info("下一步将测试CSV下载...")
    
except Exception as e:
    st.error(f"错误: {e}")

if st.button("点击测试"):
    st.balloons()
