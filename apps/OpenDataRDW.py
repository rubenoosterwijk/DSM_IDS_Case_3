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

    totaal = pd.read_csv("../totaal2.csv")
    totaal.reset_index(level=0, inplace=True)
    totaal = totaal.assign(datum_tenaamstelling=pd.to_datetime(totaal['datum_tenaamstelling'], format='%Y'))

    # index omzetten naar datetime
    totaal = totaal.set_index('datum_tenaamstelling')

    # index omzetten naar datetime

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
    typehoeveelheden = typehoeveelheden.loc[(typehoeveelheden.index < '1954-12-31') | (typehoeveelheden.index > '1995-12-31')]

    # Hieronder een lijst met de types brandstoffen
    typebrandstof = pd.DataFrame()
    typebrandstof['TOTAAL'] = totaal2.aantal.resample('Y').sum()
    totaal2['brandstof_omschrijving'].unique()

    typebrandstof['Benzine'] = totaal[totaal['brandstof_omschrijving'] == 'Benzine'].aantal.resample('Y').sum()
    typebrandstof['Diesel'] = totaal[totaal['brandstof_omschrijving'] == 'Diesel'].aantal.resample('Y').sum()
    typebrandstof['Elektriciteit'] = totaal[totaal['brandstof_omschrijving'] == 'Elektriciteit'].aantal.resample('Y').sum()
    typebrandstof['Hybride'] = totaal[totaal['brandstof_omschrijving'] == 'Hybride'].aantal.resample('Y').sum()
    typebrandstof['Waterstof'] = totaal[totaal['brandstof_omschrijving'] == 'Waterstof'].aantal.resample('Y').sum()

    typehoeveelheden = typebrandstof.drop(columns='TOTAAL')

    # verkrijg de top 10 verkochte auto's
    n = 10
    topmerken = pd.DataFrame(totaal['merk'].value_counts()[:n].index.tolist())
    topmerken.index = np.arange(1, len(topmerken)+1)
    topmerken = topmerken[0].rename('Merk')

    totaalhead = totaal.head(10)
    totaalhead['jaar'] = pd.DatetimeIndex(totaalhead.index).year
    totaalhead = totaalhead.reset_index(drop=True)
    totaalhead = totaalhead.set_index('jaar')
    totaalhead = totaalhead.drop('nummer', axis=1)
    totaalhead = totaalhead.drop('aantal', axis=1)
    totaalhead = totaalhead.drop('index', axis=1)

    typebrandstof = typebrandstof.loc[(typebrandstof.index > '2000')]
    typebrandstof = typebrandstof.loc[(typebrandstof.index > '2000')]

    return totaalhead, typehoeveelheden, typebrandstof, topmerken

# Alles wat je runt per pagina moet in de def app(): komen. Anders runt hij de pagina niet.
def app():

    totaalexample, datatype, databrandstof, datamerk = loadDatardw()

    st.title('OpendataRDW')

    st.header('Hieronder de omschrijving van de verzameling en dataverwerking OpenRDWData:')

    st.markdown("* Inladen 2 datasets (datum_tenaamstelling/merk en het type brandstof")
    st.markdown("* Samenvoegen van deze dataset")
    st.markdown("* Eruithalen welk type merk er verkocht wordt en het type brandstof")
    st.markdown("* Opschonen zodat hybride auto's te zien zijn")

    st.header('Importeren en opschonen data')
    st.markdown("Allereerst zijn 2 datasets ingeladen die betrekking hadden tot de datum/tenaamstelling en het type brandstof")
    st.markdown("Deze datasets zijn samengevoegd door middel van een pandas.merge, om vervolgens een totale dataframe te verkrijgen")
    st.dataframe(totaalexample)

    st.markdown("Het kenteken is hier niet meer van belang, omdat de data al opgeschoond is in jupyter. Daarnaast nam een kolom met de waardes van kentekens teveel ruimte op max 100Mb was helaas toegestaan")

    st.header("Meest verkochte auto's op basis van merk")
    st.markdown("De top 10 meest verkochte merken zijn opgeslagen in een DataFrame en dit zijn:")
    st.dataframe(datamerk)

    st.markdown("Hieronder volgt de grafiek voor een aantal merken en hoeveel deze verkocht zijn over de jaren")

    st.line_chart(datatype)

    st.header("Verkochte auto's op basis van type brandstof")
    st.markdown("Hieronder volgt de grafiek voor een type brandstof hoeveel deze verkocht zijn over de jaren")

    st.line_chart(databrandstof)

    st.markdown("Hieronder volgt de grafiek voor alleen elektrische auto's hoeveel deze verkocht zijn over de jaren")

    st.line_chart(databrandstof['Elektriciteit'])

    st.header("Hybride auto's")

    st.markdown("Hieronder volgt de grafiek voor alleen hybride auto's hoeveel deze verkocht zijn over de jaren")

    st.bar_chart(databrandstof[['Hybride', 'Elektriciteit']])


