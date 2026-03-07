import streamlit as st

st.set_page_config(page_title="测试页面", page_icon="✅")

st.title("🎉 部署测试成功！")
st.write("如果看到这个页面，说明Streamlit可以正常运行。")

if st.button("点击测试"):
    st.balloons()
