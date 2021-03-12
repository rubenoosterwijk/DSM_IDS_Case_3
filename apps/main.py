import streamlit as st
import altair as alt
import pandas as pd
import numpy as np
import os, urllib, cv2


# Streamlit encourages well-structured code, like starting execution in a main() function.
def main():
    st.title('Onderzoek naar laadpalen')

    laadpaaldata = pd.read_csv('data\\laadpaaldata.csv')
    st.text(laadpaaldata.info)

    st.text(laadpaaldata.describe())

    # laadpaaldata["OverChargeTime"] = laadpaaldata["ConnectedTime"] - laadpaaldata["ChargeTime"]
    print(laadpaaldata.head())

    st.image('laadpaalafbeelding.jpeg')
    st.header('De data die wij onderzocht hebben:')

    st.markdown("* Bezetting laadpalen")
    st.markdown("* Wat is het verschil tussen laden en bezetten van een laadpaal?")
    st.markdown("* Hoe ziet het gemiddelde laadprofiel er uit?")
    st.markdown("* Wat is de verdeling in vermogens?")
    st.dataframe(laadpaaldata)
    st.line_chart(laadpaaldata)


# Alles wat je runt per pagina moet in de def app(): komen. Anders runt hij de pagina niet.
def app():
    main()
