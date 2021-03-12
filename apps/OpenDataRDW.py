import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns


#Loran Ris

#Data importeren van de rdw, en kijken welke visualisaties ermee gemaakt kunnen worden en of je al aan de data integrireieit kan werken.


# Alles wat je runt per pagina moet in de def app(): komen. Anders runt hij de pagina niet.
def app():
    st.title('Home')

    st.write('This is the `home page` of this multi-page app.')

    st.write('In this app, we will be building a simple classification model using the Iris dataset.')