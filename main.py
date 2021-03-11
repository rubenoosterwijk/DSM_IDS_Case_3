import streamlit as st
import pandas as pd

st.title('Onderzoek laadpalen')

laadpaaldata = pd.read_csv("laadpaaldata.csv")
laadpaaldata["OverChargeTime"] = laadpaaldata["ConnectedTime"]-laadpaaldata["ChargeTime"]
print(laadpaaldata.head())

st.button('Hit me')
st.image('laadpaalafbeelding.jpeg')
st.dataframe(laadpaaldata)
st.line_chart(laadpaaldata)

st.text("""
#Potentiële informatie
Hoe ziet een gemiddeld bezetting van een laadpaal er uit?
Wat is het verschil tussen laden en bezetten van een laadpaal?
Hoe ziet het gemiddelde laadprofiel er uit?
Wat is de verdeling in vermogens? Lekker losjes
"""
)
