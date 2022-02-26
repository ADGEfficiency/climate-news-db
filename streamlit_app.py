import streamlit as st
import numpy as np
import pandas as pd

from climatedb.spiders.guardian import JSONLines

jl = JSONLines("./data-reworked/articles/guardian.jsonlines").read()

articles = pd.DataFrame(jl)

art = articles.iloc[0].to_frame().T

title = art.iloc[0]["title"]
date = art.iloc[0]["date_published"]

st.markdown(f"[{title}]()")
st.markdown(f"{date}")

st.markdown(str(art["body"].iloc[0]))
