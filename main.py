import streamlit as st
import pandas as pd

st.title('Onderzoek naar laadpalen')

laadpaaldata = pd.read_csv("laadpaaldata.csv")
laadpaaldata["OverChargeTime"] = laadpaaldata["ConnectedTime"]-laadpaaldata["ChargeTime"]
print(laadpaaldata.head())


st.image('laadpaalafbeelding.jpeg')
st.header('De data die wij onderzocht hebben:')

st.markdown("* Bezetting laadpalen")
st.markdown("* Wat is het verschil tussen laden en bezetten van een laadpaal?")
st.markdown("* Hoe ziet het gemiddelde laadprofiel er uit?")
st.markdown("* Wat is de verdeling in vermogens? Lekker losjes")
st.dataframe(laadpaaldata)
st.line_chart(laadpaaldata)




