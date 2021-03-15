import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import requests
import json as js


# Bud De data van de locaties van de laadpalen verstrekken. Onthoud je gaat met de map werken en je moet dus een maar weergeven op streamlit.
# Kijk alvast naar voorbeelden op de site of we met de map exrtra interactieve dingen kunnen doen (widget gebruik)

# Onderling even uitmaken wie wat gaat onderzoeken


# Alles wat je runt per pagina moet in de def app(): komen. Anders runt hij de pagina niet.
def app():

    openchargemap = pd.read_csv('laadpaallocaties.csv')

    st.text(openchargemap.info())

    st.text(openchargemap.describe())

    # openchargemap["OverChargeTime"] = openchargemap["ConnectedTime"] - openchargemap["ChargeTime"]
    print(openchargemap.head())

    st.image('laadpaalafbeelding.jpeg')
    st.header('De data die wij onderzocht hebben:')

    st.markdown("* Bezetting laadpalen")
    st.markdown("* Wat is het verschil tussen laden en bezetten van een laadpaal?")
    st.markdown("* Hoe ziet het gemiddelde laadprofiel er uit?")
    st.markdown("* Wat is de verdeling in vermogens?")
    st.dataframe(openchargemap)
    st.line_chart(openchargemap)
