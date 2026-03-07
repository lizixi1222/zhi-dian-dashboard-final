import streamlit as st
import csv
import requests
from io import StringIO
import os
import traceback

os.environ["STREAMLIT_SERVER_FILE_WATCHER_TYPE"] = "none"

st.set_page_config(page_title="调试模式", page_icon="🔍")

st.title("🔍 CSV 格式调试工具")

url = "https://github.com/lizixi1222/zhi-dian-dashboard/releases/download/v1.0-data/1_24_1_4.csv"

try:
    with st.spinner("正在下载 CSV 文件..."):
        response = requests.get(url, timeout=30)
        response.raise_for_status()
    
    st.success("✅ 下载成功！")
    st.write(f"文件大小: {len(response.text):,} 字符")
    
    # 显示前500个字符
    st.text_area("文件开头预览", response.text[:500], height=200)
    
    # 尝试用 csv 模块读取
    try:
        reader = csv.reader(StringIO(response.text))
        rows = []
        for i, row in enumerate(reader):
            if i >= 5:
                break
            rows.append(row)
            st.write(f"第{i+1}行: {row}")
        
        st.write(f"每行列数: {[len(r) for r in rows]}")
        
    except Exception as e:
        st.error(f"CSV解析错误: {e}")
        st.code(traceback.format_exc())
    
except Exception as e:
    st.error(f"下载错误: {e}")
    st.code(traceback.format_exc())
