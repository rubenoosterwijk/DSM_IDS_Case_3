import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt


# Loran Ris

# Data importeren van de rdw, en kijken welke visualisaties ermee gemaakt kunnen worden en of je al aan de data integrireieit kan werken.
@st.cache
def loadDatardw():
    pd.options.mode.chained_assignment = None

    totaal = pd.read_csv("totaal.csv", index_col=0)

    # nieuwe lijst maken waarmee gerekend kan worden
    totaal2 = totaal
    totaal2['nummer'] = np.arange(1, len(totaal2) + 1)
    totaal2['aantal'] = 1

    typehoeveelheden = pd.DataFrame()
    typehoeveelheden['TOTAAL'] = totaal2.aantal.resample('Y').sum()
    typehoeveelheden['TOYOTA'] = totaal[totaal['merk'] == 'TOYOTA'].aantal.resample('Y').sum()
    typehoeveelheden['TESLA'] = totaal[totaal['merk'] == 'TESLA'].aantal.resample('Y').sum()
    typehoeveelheden['HONDA'] = totaal[totaal['merk'] == 'HONDA'].aantal.resample('Y').sum()
    typehoeveelheden['VOLKSWAGEN'] = totaal[totaal['merk'] == 'VOLKSWAGEN'].aantal.resample('Y').sum()
    typehoeveelheden['AUDI'] = totaal[totaal['merk'] == 'AUDI'].aantal.resample('Y').sum()
    typehoeveelheden['BMW'] = totaal[totaal['merk'] == 'BMW'].aantal.resample('Y').sum()
    typehoeveelheden = typehoeveelheden.drop(columns='TOTAAL')
    typehoeveelheden = typehoeveelheden.loc[
        (typehoeveelheden.index < '1954-12-31') | (typehoeveelheden.index > '1995-12-31')]

    # Hieronder een lijst met de types brandstoffen
    typebrandstof = pd.DataFrame()
    typebrandstof['TOTAAL'] = totaal2.aantal.resample('Y').sum()
    totaal2['brandstof_omschrijving'].unique()

    typebrandstof['Benzine'] = totaal[totaal['brandstof_omschrijving'] == 'Benzine'].aantal.resample('Y').sum()
    typebrandstof['Diesel'] = totaal[totaal['brandstof_omschrijving'] == 'Diesel'].aantal.resample('Y').sum()
    typebrandstof['Elektriciteit'] = totaal[totaal['brandstof_omschrijving'] == 'Elektriciteit'].aantal.resample(
        'Y').sum()
    typebrandstof['Hybride'] = totaal[totaal['brandstof_omschrijving'] == 'Hybride'].aantal.resample('Y').sum()
    typebrandstof['Waterstof'] = totaal[totaal['brandstof_omschrijving'] == 'Waterstof'].aantal.resample('Y').sum()

    typehoeveelheden = typebrandstof.drop(columns='TOTAAL')

    # verkrijg de top 10 verkochte auto's
    n = 10
    topmerken = pd.DataFrame(totaal['merk'].value_counts()[:n].index.tolist())
    return typehoeveelheden, typebrandstof, topmerken


# Alles wat je runt per pagina moet in de def app(): komen. Anders runt hij de pagina niet.
def app():
    datatype, databrandstof, datamerk = loadDatardw()

    st.text(datatype.info())

    st.title('OpendataRDW')

    st.header('Hieronder de omschrijving van de OpenRDWData:')

    st.markdown("* Inladen 2 datasets (datum_tenaamstelling/merk en het type brandstof")
    st.markdown("* Samenvoegen van deze dataset")
    st.markdown("* Eruithalen welk type merk er verkocht wordt en het type brandstof")
    st.markdown("* Opschonen zodat hybride auto's te zien zijn")

    st.markdown("De top 10 meest verkochte merken zijn opgeslagen in een DataFrame en dit zijn:")

    st.write(datamerk.head(10))

    st.markdown("Hieronder volgt de grafiek voor een aantal merken en hoeveel deze verkocht zijn over de jaren")

    datatype.plot()

    st.pyplot()

    st.markdown(
        "Hieronder volgt de grafiek voor een type brandstof en elektriciteit en hoeveel deze verkocht zijn over de jaren")

    plt.plot(databrandstof)
    plt.xlabel("jaar")
    plt.ylabel("Aantal auto's")
    plt.title("Type brandstof verkocht over de jaren")
    plt.show()

    st.pyplot()

    plt.plot(databrandstof['Elektriciteit'])
    plt.xlabel("jaar")
    plt.ylabel("Aantal auto's")
    plt.title("Elektrische auto's verkocht over de jaren")
    plt.show()
    st.pyplot()
