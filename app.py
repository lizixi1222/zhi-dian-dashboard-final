import streamlit as st
import csv
import requests
from io import StringIO
from collections import defaultdict
import plotly.graph_objects as go
from datetime import datetime

st.set_page_config(page_title="智电未来", page_icon="⚡", layout="wide")

st.title("🚀 正在加载数据...")

@st.cache_data
def load_data_with_csv():
    """用 csv 模块逐行读取，内存占用极小"""
    url = "https://github.com/lizixi1222/zhi-dian-dashboard/releases/download/v1.0-data/1_24_1_4.csv"
    
    try:
        response = requests.get(url, timeout=30)
        reader = csv.reader(StringIO(response.text))
        
        # 读取表头
        headers = next(reader)
        
        # 只读取前 50000 行
        data = []
        for i, row in enumerate(reader):
            if i >= 50000:
                break
            data.append(row)
        
        return headers, data
    except Exception as e:
        st.error(f"加载失败: {e}")
        return None, None

headers, data = load_data_with_csv()

if data:
    st.success(f"✅ 成功加载 {len(data)} 条数据")
    
    # 找到需要的列索引
    try:
        time_idx = headers.index('DATA_TIME')
        voltage_idx = headers.index('totalVoltage')
        current_idx = headers.index('totalCurrent')
    except ValueError:
        st.error("CSV 列名不匹配，请检查")
        st.write("现有列:", headers)
        st.stop()
    
    # 按小时统计
    hour_power = defaultdict(list)
    
    for row in data:
        try:
            hour = int(row[time_idx][11:13])  # 从时间字符串提取小时
            power = float(row[voltage_idx]) * float(row[current_idx]) / 1000
            hour_power[hour].append(power)
        except:
            continue
    
    # 计算每小时平均功率
    hours = list(range(24))
    avg_power = []
    for h in hours:
        if hour_power[h]:
            avg_power.append(sum(hour_power[h]) / len(hour_power[h]))
        else:
            avg_power.append(0)
    
    # 显示图表
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=hours, 
        y=avg_power,
        mode='lines+markers',
        name='充电负荷'
    ))
    fig.update_layout(
        title="充电负荷曲线",
        xaxis_title="小时",
        yaxis_title="平均功率 (kW)",
        height=400
    )
    st.plotly_chart(fig)
    
    # 显示前几行数据
    st.write("数据预览:")
    st.write(data[:5])
