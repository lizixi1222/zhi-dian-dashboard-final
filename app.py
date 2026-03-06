import streamlit as st
import platform

st.set_page_config(page_title="智电未来", layout="wide")

st.title("✅ 智电未来科技有限公司")
st.write("Python版本:", platform.python_version())

if st.button("点击测试"):
    st.balloons()
