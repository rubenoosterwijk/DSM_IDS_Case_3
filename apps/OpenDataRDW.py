import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def app():


    st.title('OpendataRDW')

    st.header('Hieronder de omschrijving van de OpenRDWData:')

    st.markdown("* Inladen 2 datasets (datum_tenaamstelling/merk en het type brandstof")
    st.markdown("* Samenvoegen van deze dataset")
    st.markdown("* Eruithalen welk type merk er verkocht wordt en het type brandstof")
    st.markdown("* Opschonen zodat hybride auto's te zien zijn")
