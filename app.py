"""
智电未来科技有限公司——公交场站运营数据看板
完整版（含CSV加载）
"""

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


# ==================== 数据加载 ====================
@st.cache_data(ttl=3600)
def load_csv_from_release(filename):
    url = f"https://github.com/lizixi1222/zhi-dian-dashboard/releases/download/v1.0-data/{filename}"
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        df = pd.read_csv(StringIO(response.text))
        return df
    except Exception as e:
        st.warning(f"加载 {filename} 失败: {e}")
        return None


@st.cache_data(ttl=3600)
def analyze_charging_data():
    df1 = load_csv_from_release("1_24_1_4.csv")
    df2 = load_csv_from_release("2_24_1_4.csv")
    df3 = load_csv_from_release("3_24_1_4.csv")
    
    valid_dfs = [df for df in [df1, df2, df3] if df is not None]
    
    if valid_dfs:
        df = pd.concat(valid_dfs, ignore_index=True)
        st.sidebar.success(f"✅ 已加载 {len(df):,} 条记录")
        
        # 数据处理
        df['DATA_TIME'] = pd.to_datetime(df['DATA_TIME'])
        df['hour'] = df['DATA_TIME'].dt.hour
        df['power_kw'] = df['totalVoltage'] * df['totalCurrent'] / 1000
        df['is_charging'] = (df['chargeState'] == 3)
        
        # 小时分布
        hourly = df[df['is_charging']].groupby('hour').size()
        hourly_load = []
        for h in range(24):
            if h in hourly.index:
                val = hourly[h] / hourly.max() * 50
                hourly_load.append(round(val, 1))
            else:
                hourly_load.append(0)
        
        data_source = "CSV真实数据"
    else:
        hourly_load = [5,3,2,1,1,2,8,25,35,30,25,22,20,25,30,35,40,45,50,48,42,30,20,10]
        data_source = "示例数据"
    
    pv_data = [0,0,0,0,0,0,20,80,150,200,220,230,220,200,150,80,20,0,0,0,0,0,0,0]
    
    station = {
        "station_name": "长沙格林香山公交场站",
        "total_vehicles": 150,
        "vehicle_count": 40,
        "daily_energy": 554,
        "pv_generation": 3809,
        "daily_cost": -814,
        "daily_savings": 1479,
        "daily_co2": 312,
        "battery_health": 73.9,
        "battery_cycles": 809,
        "battery_life": 6.7,
        "cumulative_savings": 42300,
        "energy_consumption": 0.85,
        "data_source": data_source,
        "hourly_load": hourly_load,
        "pv_data": pv_data
    }
    
    return station


station = analyze_charging_data()
hours = list(range(24))


# ==================== CSS样式 ====================
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #0A1A2F 0%, #1E3A8A 100%);
    }
    .metric-card {
        background: white;
        border-radius: 20px;
        padding: 24px;
        box-shadow: 0 8px 24px rgba(0,0,0,0.12);
        margin: 10px 0;
    }
    .metric-value {
        font-size: 32px;
        font-weight: 700;
        color: #0A1A2F;
    }
    .section-title {
        color: white;
        font-size: 20px;
        margin: 30px 0 20px 0;
    }
</style>
""", unsafe_allow_html=True)


# ==================== 侧边栏 ====================
with st.sidebar:
    st.markdown("## ⚡ 智电未来")
    st.markdown(f"**{station['station_name']}**")
    st.markdown(f"服务车辆: {station['total_vehicles']}辆")
    st.markdown(f"同时充电: {station['vehicle_count']}辆")
    st.info(f"数据: {station['data_source']}")


# ==================== 主界面 ====================
st.markdown(f"## {station['station_name']}")

col1, col2, col3, col4 = st.columns(4)
col1.metric("今日充电量", f"{station['daily_energy']} kWh")
col2.metric("今日光伏", f"{station['pv_generation']} kWh")
col3.metric("日运行成本", f"¥ {abs(station['daily_cost'])}")
col4.metric("日减排CO₂", f"{station['daily_co2']} kg")

# 负荷曲线
fig = go.Figure()
fig.add_trace(go.Scatter(x=hours, y=station['hourly_load'], mode='lines', name='充电负荷'))
fig.add_trace(go.Scatter(x=hours, y=station['pv_data'], mode='lines', name='光伏出力'))
fig.update_layout(height=400)
st.plotly_chart(fig, use_container_width=True)

# 电池状态
st.subheader("🔋 电池状态")
col1, col2, col3 = st.columns(3)
col1.metric("健康度", f"{station['battery_health']}%")
col2.metric("循环次数", f"{station['battery_cycles']}")
col3.metric("剩余寿命", f"{station['battery_life']}年")
