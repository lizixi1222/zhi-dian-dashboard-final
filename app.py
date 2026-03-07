import streamlit as st

st.set_page_config(page_title="测试", page_icon="✅")

st.title("✅ 测试页面")
st.write("如果能看见这个，说明环境正常")

if st.button("点击"):
    st.balloons()
