import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns

laadpaaldata = pd.read_csv("laadpaaldata.csv")
laadpaaldata["OverChargeTime"] = laadpaaldata["ConnectedTime"]-laadpaaldata["ChargeTime"]
print(laadpaaldata.head())


st.text("""
#Potentiële informatie
Hoe ziet een gemiddeld bezetting van een laadpaal er uit?
Wat is het verschil tussen laden en bezetten van een laadpaal?
Hoe ziet het gemiddelde laadprofiel er uit?
Wat is de verdeling in vermogens?
"""
)