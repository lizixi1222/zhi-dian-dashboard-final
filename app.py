import streamlit as st
import csv
import requests
from io import StringIO
import os

os.environ["STREAMLIT_SERVER_FILE_WATCHER_TYPE"] = "none"

st.set_page_config(page_title="调试模式", page_icon="🔍")

st.title("🔍 CSV 格式调试工具")

url = "https://github.com/lizixi1222/zhi-dian-dashboard/releases/download/v1.0-data/1_24_1_4.csv"

try:
    with st.spinner("正在下载 CSV 文件..."):
        response = requests.get(url, timeout=30)
        response.raise_for_status()
    
    st.success("✅ 下载成功！")
    
    # 用 csv 模块读取
    reader = csv.reader(StringIO(response.text))
    
    st.subheader("📋 前10行数据：")
    
    rows = []
    for i, row in enumerate(reader):
        if i >= 10:
            break
        rows.append(row)
        st.write(f"**第{i+1}行:** {row}")
    
    st.subheader("📊 数据统计")
    st.write(f"每行字段数: {[len(r) for r in rows]}")
    
    if rows:
        st.subheader("🔍 猜测字段含义")
        st.write("如果第一行是表头，那么列名应该是：")
        st.code(rows[0])
        
        st.write("如果第一行是数据，那么列名需要手动指定")
    
except Exception as e:
    st.error(f"❌ 错误: {e}")
