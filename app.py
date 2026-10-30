import streamlit as st
import pandas as pd
import duckdb
from click import option

st.write("SQL test")
option=st.selectbox("What do you want to review",("Join","Group By","Window func"),index=None,placeholder= "Select a theme...")
st.write("You selected: ",option)
data = {"a":[1,2,3],"b":[4,5,6]}
df = pd.DataFrame(data)

input_text=st.text_area("Input Text")
result = duckdb.query(input_text)
st.dataframe(result)
