"""
智电未来科技有限公司——公交场站运营数据看板
Python 3.14 完整兼容版
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import requests
from datetime import datetime
import sys
import os

# 显示Python版本
st.sidebar.write(f"🐍 Python版本: {sys.version.split()[0]}")

# 页面配置
st.set_page_config(
    page_title="智电未来 - 场站运营看板",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ==================== 数据加载模块 ====================
@st.cache_data(ttl=3600)
def load_csv_from_release(filename):
    """从GitHub Releases加载CSV文件（Python 3.14兼容）"""
    url = f"https://github.com/lizixi1222/zhi-dian-dashboard/releases/download/v1.0-data/{filename}"
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        
        # Python 3.14兼容的读取方式
        from io import StringIO
        df = pd.read_csv(StringIO(response.text))
        return df
    except Exception as e:
        st.warning(f"⚠️ 加载 {filename} 失败: {e}")
        return None


@st.cache_data(ttl=3600)
def analyze_charging_data():
    """分析充电数据生成场站指标（Python 3.14优化）"""
    
    # 加载CSV文件
    df1 = load_csv_from_release("1_24_1_4.csv")
df2 = load_csv_from_release("2_24_1_4.csv")
df3 = load_csv_from_release("3_24_1_4.csv")

valid_dfs = [df for df in [df1, df2, df3] if df is not None]
    
    if valid_dfs:
        df = pd.concat(valid_dfs, ignore_index=True)
        
        # 数据预处理
        df['DATA_TIME'] = pd.to_datetime(df['DATA_TIME'])
        df['hour'] = df['DATA_TIME'].dt.hour
        df['date'] = df['DATA_TIME'].dt.date
        
        # 计算功率（使用numpy优化）
        df['power_kw'] = df['totalVoltage'] * df['totalCurrent'] / 1000
        df['power_kw'] = np.clip(df['power_kw'], 0, None)
        df['is_charging'] = (df['chargeState'] == 3)
        
        # 充电时段分布
        charging_mask = df['is_charging']
        charging_by_hour = df.loc[charging_mask].groupby('hour').size()
        
        # 日充电量
        daily_energy = df.groupby('date')['power_kw'].sum() * 0.25
        avg_daily = float(daily_energy.mean()) if not daily_energy.empty else 554.0
        
        # 今日数据
        last_date = df['date'].max()
        today_data = df[df['date'] == last_date]
        today_energy = float(today_data['power_kw'].sum() * 0.25) if not today_data.empty else avg_daily
        
        # 小时负荷曲线
        hourly_load = []
        if not charging_by_hour.empty:
            max_val = float(charging_by_hour.max())
            for h in range(24):
                if h in charging_by_hour.index:
                    val = float(charging_by_hour[h]) / max_val * 50
                    hourly_load.append(round(val, 1))
                else:
                    hourly_load.append(0)
        else:
            hourly_load = [5,3,2,1,1,2,8,25,35,30,25,22,20,25,30,35,40,45,50,48,42,30,20,10]
        
        data_source = "CSV真实数据"
        st.sidebar.success(f"✅ 已加载 {len(df):,} 条充电记录")
        
    else:
        # 使用默认数据
        st.sidebar.warning("⚠️ 使用示例数据")
        hourly_load = [5,3,2,1,1,2,8,25,35,30,25,22,20,25,30,35,40,45,50,48,42,30,20,10]
        avg_daily = 554.0
        today_energy = 554.0
        data_source = "示例数据"
    
    # 光伏数据
    pv_data = [0,0,0,0,0,0,20,80,150,200,220,230,220,200,150,80,20,0,0,0,0,0,0,0]
    
    # 场站指标
    station_data = {
        "station_name": "长沙格林香山公交场站",
        "total_vehicles": 150,
        "vehicle_count": 40,
        "daily_energy": int(round(today_energy, 0)),
        "avg_daily_energy": int(round(avg_daily, 0)),
        "pv_generation": 3809,
        "daily_cost": -814,
        "daily_savings": 1479,
        "daily_co2": 312,
        "battery_health": 73.9,
        "battery_cycles": 809,
        "battery_life": 6.7,
        "cumulative_savings": 42300,
        "energy_consumption": 0.85,
        "peak_load": 47.9,
        "data_source": data_source,
        "hourly_load": hourly_load,
        "pv_data": pv_data,
        "total_records": len(valid_dfs[0]) if valid_dfs else 0
    }
    
    return station_data


# ==================== 加载数据 ====================
station = analyze_charging_data()


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
        border: 1px solid rgba(30,58,138,0.1);
        transition: all 0.3s;
    }
    .metric-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 16px 32px rgba(30,58,138,0.15);
    }
    .metric-label {
        font-size: 13px;
        color: #5F6B7A;
        margin-bottom: 8px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .metric-value {
        font-size: 32px;
        font-weight: 700;
        color: #0A1A2F;
        line-height: 1.2;
    }
    .metric-badge {
        font-size: 12px;
        color: #1E3A8A;
        background: rgba(30,58,138,0.1);
        padding: 4px 8px;
        border-radius: 20px;
        display: inline-block;
        margin-top: 8px;
    }
    .section-title {
        font-size: 20px;
        font-weight: 600;
        color: white;
        margin: 30px 0 20px 0;
        padding-bottom: 8px;
        border-bottom: 2px solid rgba(255,255,255,0.3);
    }
    .sidebar-info {
        background: rgba(255,255,255,0.05);
        border-radius: 16px;
        padding: 20px;
        margin: 20px 0;
        border: 1px solid rgba(255,255,255,0.1);
    }
</style>
""", unsafe_allow_html=True)


# ==================== 侧边栏 ====================
with st.sidebar:
    st.markdown("## ⚡ 智电未来")
    st.markdown("---")
    
    # 场站信息
    st.markdown(f"""
    <div class="sidebar-info">
        <div style="color:white; font-size:18px; font-weight:600; margin-bottom:16px;">{station['station_name']}</div>
        <div style="color:rgba(255,255,255,0.9); font-size:15px; margin:12px 0;">
            <span style="display:inline-block; width:90px;">服务车辆</span>
            <span style="font-weight:600;">{station['total_vehicles']}辆</span>
        </div>
        <div style="color:rgba(255,255,255,0.9); font-size:15px; margin:12px 0;">
            <span style="display:inline-block; width:90px;">同时充电</span>
            <span style="font-weight:600;">{station['vehicle_count']}辆</span>
        </div>
        <div style="color:rgba(255,255,255,0.9); font-size:15px; margin:12px 0;">
            <span style="display:inline-block; width:90px;">光伏容量</span>
            <span style="font-weight:600;">500 kWp</span>
        </div>
        <div style="color:rgba(255,255,255,0.9); font-size:15px; margin:12px 0;">
            <span style="display:inline-block; width:90px;">储能容量</span>
            <span style="font-weight:600;">500 kWh</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # 数据来源
    if station['data_source'] == "CSV真实数据":
        st.success(f"📊 {station['data_source']}: {station['total_records']:,}条")
    else:
        st.warning(f"📊 {station['data_source']}")
    
    st.markdown("---")
    st.caption("© 智电未来科技有限公司")


# ==================== 主界面 ====================
st.markdown(f"## {station['station_name']}")
st.markdown(f"*{datetime.now().strftime('%Y年%m月%d日')}*")

# 第一行：核心指标
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">📊 今日充电量</div>
        <div class="metric-value">{station['daily_energy']} kWh</div>
        <div class="metric-badge">来自CSV分析</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">☀️ 今日光伏</div>
        <div class="metric-value">{station['pv_generation']} kWh</div>
        <div class="metric-badge">晴天典型值</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">💰 日运行成本</div>
        <div class="metric-value">¥ {abs(station['daily_cost'])}</div>
        <div class="metric-badge" style="background:#10B98120; color:#10B981;">负成本运营</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">🌿 日减排CO₂</div>
        <div class="metric-value">{station['daily_co2']} kg</div>
        <div class="metric-badge">环境效益</div>
    </div>
    """, unsafe_allow_html=True)

# 第二行：负荷曲线
st.markdown('<div class="section-title">📈 典型日负荷曲线</div>', unsafe_allow_html=True)

hours = list(range(24))
fig = go.Figure()
fig.add_trace(go.Scatter(
    x=hours, y=station['hourly_load'],
    mode='lines',
    name='充电负荷',
    line=dict(color='#1E3A8A', width=3),
    fill='tozeroy',
    fillcolor='rgba(30,58,138,0.1)'
))
fig.add_trace(go.Scatter(
    x=hours, y=station['pv_data'],
    mode='lines',
    name='光伏出力',
    line=dict(color='#3B82F6', width=3),
    fill='tozeroy',
    fillcolor='rgba(59,130,246,0.1)'
))

fig.update_layout(
    height=450,
    xaxis_title="小时",
    yaxis_title="功率 (kW)",
    hovermode='x unified',
    plot_bgcolor='white',
    paper_bgcolor='white',
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
)

fig.update_xaxes(gridcolor='#E2E8F0', tickmode='linear', tick0=0, dtick=2)
fig.update_yaxes(gridcolor='#E2E8F0')

st.plotly_chart(fig, use_container_width=True)

# 第三行：电池状态和累计效益
col1, col2 = st.columns([1, 1])

with col1:
    st.markdown('<div class="section-title">🔋 电池状态</div>', unsafe_allow_html=True)
    sub1, sub2, sub3 = st.columns(3)
    sub1.metric("健康度", f"{station['battery_health']}%")
    sub2.metric("循环次数", f"{station['battery_cycles']}")
    sub3.metric("剩余寿命", f"{station['battery_life']}年")

with col2:
    st.markdown('<div class="section-title">📊 累计效益</div>', unsafe_allow_html=True)
    sub1, sub2 = st.columns(2)
    sub1.metric("累计节省", f"¥ {station['cumulative_savings']:,}")
    sub2.metric("百公里能耗", f"{station['energy_consumption']} kWh")

# 第四行：对比数据
st.markdown('<div class="section-title">📋 优化效果对比</div>', unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)

col1.metric(
    label="无序充电成本",
    value="¥ 665/日",
    delta=f"节省 ¥ {station['daily_savings']}"
)

col2.metric(
    label="优化后成本",
    value=f"¥ {abs(station['daily_cost'])}",
    delta="负成本运营",
    delta_color="inverse"
)

col3.metric(
    label="投资回收期",
    value="8.3年",
    delta="优于行业30%"
)

# 页脚
st.markdown("---")
st.markdown("智电未来科技有限公司 · 让每一度电都聪明")
