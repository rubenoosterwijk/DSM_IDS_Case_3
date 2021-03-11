import streamlit as st
import pandas as pd
import numpy as np

laadpaaldata = pd.read_csv("laadpaaldata.csv")
print(laadpaaldata.columns)


st.text("""

#Potentiële informatie
Hoe ziet een gemiddeld bezetting van een laadpaal er uit?
Wat is het verschil tussen laden en bezetten van een laadpaal?
Hoe ziet het gemiddelde laadprofiel er uit?
Wat is de verdeling in vermogens?
….

"""
)