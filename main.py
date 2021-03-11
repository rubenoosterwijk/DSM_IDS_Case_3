import streamlit as st
import pandas as pd

laadpaaldata = pd.read_csv("laadpaaldata.csv")
laadpaaldata["OverChargeTime"] = laadpaaldata["ConnectedTime"]-laadpaaldata["ChargeTime"]
print(laadpaaldata.head())

st.dataframe(laadpaaldata)
st.line_chart(laadpaaldata)
st.image('laapaalafbeelding.jpeg')
st.text("""
#Potentiële informatie
Hoe ziet een gemiddeld bezetting van een laadpaal er uit?
Wat is het verschil tussen laden en bezetten van een laadpaal?
Hoe ziet het gemiddelde laadprofiel er uit?
Wat is de verdeling in vermogens? Lekker losjes
"""
)
