import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import requests

#Bud De data van de locaties van de laadpalen verstrekken. Onthoud je gaat met de map werken en je moet dus een maar weergeven op streamlit.
#Kijk alvast naar voorbeelden op de site of we met de map exrtra interactieve dingen kunnen doen (widget gebruik)

#Onderling even uitmaken wie wat gaat onderzoeken


response = requests.get("https://api.openchargemap.io/v3/poi/?output=csv&countrycode=NL&key=f7903c6a-d2cd-4a10-b012-260c3536974f")
print(response.status_code)
print(response.text)

import streamlit as st

# Alles wat je runt per pagina moet in de def app(): komen. Anders runt hij de pagina niet.
def app():
    st.title('Home')

    st.write('This is the `home page` of this multi-page app.')

    st.write('In this app, we will be building a simple classification model using the Iris dataset.')