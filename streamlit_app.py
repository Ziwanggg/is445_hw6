import streamlit as st
import pandas as pd
import altair as alt

st.title("Exploring Illinois License Records")

st.write(
    "This app explores license categories, status, and counties "
    "using the Fall 2022 course dataset."
)

url = "https://raw.githubusercontent.com/UIUC-iSchool-DataViz/is445_data/main/licenses_fall2022.csv"

data = pd.read_csv(
    url,
    usecols=["License Type", "License Status", "State", "County"]
)

st.write(data.head())
