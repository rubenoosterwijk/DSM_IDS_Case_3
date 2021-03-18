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

    # https://opendata.rdw.nl/Voertuigen/Open-Data-RDW-Gekentekende_voertuigen/m9d7-ebf2
    url6 = 'https://opendata.rdw.nl/resource/m9d7-ebf2.csv?$limit=10000'
    df6 = pd.read_csv(url6, usecols=['kenteken', 'datum_tenaamstelling', 'merk'])
    df6.head()

    dfdat = df6[['kenteken', 'datum_tenaamstelling', 'merk']]


    # https://opendata.rdw.nl/Voertuigen/Open-Data-RDW-Gekentekende_voertuigen_brandstof/8ys7-d773
    urlbr = 'https://opendata.rdw.nl/resource/8ys7-d773.csv?$limit=10000'
    dfbr = pd.read_csv(urlbr, low_memory=False, usecols=['kenteken', 'brandstof_omschrijving'])
    dfbr2 = dfbr[['kenteken', 'brandstof_omschrijving']]

    # dfDat en dfBr2 merge van data
    totaal = dfdat.merge(dfbr2, on='kenteken', how='outer', suffixes=('_1', '_2'))

    # Weghalen NAN waardes en de index resetten
    totaal = totaal.dropna()
    totaal = totaal.reset_index(drop=True)

    # Hybrides zijn alle autos die 2x in de lijst voorkomen
    hybrides = totaal[totaal['kenteken'].duplicated(keep='last')]
    hybrides['brandstof_omschrijving'] = hybrides['brandstof_omschrijving'].replace(['Elektriciteit'],'Hybride')
    hybrides['brandstof_omschrijving'] = hybrides['brandstof_omschrijving'].replace(['Benzine'],'Hybride')
    hybrides['brandstof_omschrijving'] = hybrides['brandstof_omschrijving'].replace(['Diesel'],'Hybride')
    hybrides['brandstof_omschrijving'] = hybrides['brandstof_omschrijving'].replace(['Waterstof'],'Hybride')
    hybrides['brandstof_omschrijving'] = hybrides['brandstof_omschrijving'].replace(['LPG'],'Hybride')
    hybrides = hybrides.reset_index(drop=True)

    # hybrides eerst weghalen en dan de opgeschoonde lijst toevoegen
    totaal = totaal.drop_duplicates(subset='kenteken')
    totaal = totaal.reset_index(drop=True)
    totaal = totaal.append(hybrides, ignore_index=True)

    # Beide lijsten omzetten naar een juiste datetime
    hybrides = hybrides.assign(datum_tenaamstelling = pd.to_datetime(hybrides['datum_tenaamstelling'], format='%Y%m%d'))
    totaal = totaal.assign(datum_tenaamstelling = pd.to_datetime(totaal['datum_tenaamstelling'], format='%Y%m%d'))

    # index omzetten naar datetime
    totaal = totaal.set_index('datum_tenaamstelling')
    hybrides = hybrides.set_index('datum_tenaamstelling')

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
    typehoeveelheden = typehoeveelheden.loc[(Typehoeveelheden.index < '1954-12-31') | (Typehoeveelheden.index > '1995-12-31')]

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


# Alles wat je runt per pagina moet in de def app(): komen. Anders runt hij de pagina niet.
def app():
    # 1. Data Verzamelen en ordenen

    st.title('OpendataRDW')

    st.header('Hieronder de omschrijving van de OpenRDWData:')

    st.markdown("* Inladen 2 datasets (datum_tenaamstelling/merk en het type brandstof")
    st.markdown("* Samenvoegen van deze dataset")
    st.markdown("* Eruithalen welk type merk er verkocht wordt en het type brandstof")
    st.markdown("* Opschonen zodat hybride auto's te zien zijn")

    st.markdown("De top 10 meest verkochte merken zijn opgeslagen in een DataFrame en dit zijn:")

    topmerken.head(10)

    st.markdown("Hieronder volgt de grafiek voor een aantal merken en hoeveel deze verkocht zijn over de jaren")

    typehoeveelheden.plot()

    st.markdown("Hieronder volgt de grafiek voor een type brandstof en elektriciteit en hoeveel deze verkocht zijn over de jaren")

    plt.plot(typebrandstof)
    plt.xlabel("jaar")
    plt.ylabel("Aantal auto's")
    plt.title("Type brandstof verkocht over de jaren")
    plt.show()

    plt.plot(typebrandstof['Elektriciteit'])
    plt.xlabel("jaar")
    plt.ylabel("Aantal auto's")
    plt.title("Elektrische auto's verkocht over de jaren")
    plt.show()