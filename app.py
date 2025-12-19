import streamlit as st
import subprocess
import sys

st.set_page_config(page_title="Wind", page_icon="🌬️")
st.title("🌬️ Wind")
st.write("Enter a city to get the weather.")

city = st.text_input("City", placeholder="Boulder, CO")

if st.button("Get weather") and city:
    # Runs your existing CLI script and prints its output
    result = subprocess.run(
        [sys.executable, "weather.py", city],
        capture_output=True,
        text=True
    )
    if result.returncode == 0:
        st.code(result.stdout)
    else:
        st.error(result.stderr or "Something went wrong.")
