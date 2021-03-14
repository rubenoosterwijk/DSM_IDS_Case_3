import streamlit as st
import altair as alt
import pandas as pd
import numpy as np
import os, urllib, cv2
import matplotlib.pyplot as plt
import seaborn as sns
import io


def convertDataframe(laadpaaldata):
    st.header("Dataframe corrigeren")

    st.text("Ons dataframe aan het begin...")
    st.dataframe(laadpaaldata)

    st.text("Uitrekening hoeveel tijd men daadwerkelijk niet aan het laden is")
    laadpaaldata["OverChargeTime"] = laadpaaldata["ConnectedTime"] - laadpaaldata["ChargeTime"]
    st.dataframe(laadpaaldata["OverChargeTime"])

    st.text("Bepalen wie wel en wie niet aan het overladen was")
    laadpaaldata["OverCharged"] = laadpaaldata["OverChargeTime"] > 0
    st.dataframe(laadpaaldata[["OverCharged", "OverChargeTime"]])

    st.text("Alle deze negatieve metingen of 0 metingen in 'OverChargeTime' maken we NaN, want dit zijn foute metingen")
    zero = laadpaaldata.loc[
        ((laadpaaldata['OverChargeTime'] == 0) | (laadpaaldata['OverChargeTime'] < 0)), 'OverChargeTime']
    st.dataframe(zero)
    laadpaaldata.loc[
        ((laadpaaldata['OverChargeTime'] == 0) | (laadpaaldata['OverChargeTime'] < 0)), 'OverChargeTime'] = np.nan

    st.text("Alle metingen waar de eindtijd kleiner is dan de starttijd moeten ook weg")
    tijderror = laadpaaldata.loc[laadpaaldata['Ended'] < laadpaaldata['Started'], ['Ended', "Started"]]
    laadpaaldata = laadpaaldata.drop(tijderror.index)
    st.dataframe(tijderror)

    # Zoeken naar twee speciafieke datums met 29 dagen in februari (schikkeljaar), deze zijn niet interperteerbaar.
    st.text(
        "Verder moeten alle rows met op de 29ste van februari (schikkeljaar) ook weg, deze zijn niet interperteerbaar door  pd.to_datetime().")
    st.dataframe(laadpaaldata.loc[laadpaaldata['Started'] == "2018-02-29 07:37:53"])
    st.dataframe(laadpaaldata.loc[laadpaaldata['Ended'] == "2018-02-29 07:46:07"])
    # Deze twee droppen
    laadpaaldata = laadpaaldata.drop(1731)
    laadpaaldata = laadpaaldata.drop(1732)

    buffer = io.StringIO()
    laadpaaldata.info(buf=buffer)
    s = buffer.getvalue()

    # De Started en Ended colommen zijn objecten en géén DateTime types.
    st.text(s)

    # Nu de data van de beide geen ongeldige combinaties van dag en maand heeft, kunnen we de colommen converteren naar een datetime64[ns] type
    laadpaaldata['Started'] = pd.to_datetime(laadpaaldata['Started'], format='%Y-%m-%d %H:%M:%S')
    laadpaaldata['Ended'] = pd.to_datetime(laadpaaldata['Ended'], format='%Y-%m-%d %H:%M:%S')

    # Hier voegen we drie colommen toe die de dag en maand afzonderlijk bijhouden. Deze kunnen we later makkelijk oproepen met onze seaborn visualisaties.
    laadpaaldata['Month'] = laadpaaldata['Started'].dt.month
    laadpaaldata['Day'] = laadpaaldata['Started'].dt.day

    # We kunnen pas de weekday uitvinden op basis van de index van de dataframe, hiervoor maken we de index gelijk aan de colom "Started"
    laadpaaldata.sort_values(by='Started')
    laadpaaldata = laadpaaldata.set_index("Started")
    laadpaaldata['Weekday'] = laadpaaldata.index.weekday

    laadpaaldata = laadpaaldata.reset_index()

    # laadpaaldata.info()
    # laadpaaldata.describe()

    laadpaaldata.info(buf=buffer)
    s = buffer.getvalue()

    # De Started en Ended colommen zijn objecten en géén DateTime types.
    st.text(s)
    st.dataframe(laadpaaldata)

    laadpaaldata.to_csv("laadpaaldataClean.csv")

    # st.pyplot(sns.lineplot(x="Started", y="OverChargeTime", hue="Weekday", data=laadpaaldata))
    return laadpaaldata


@st.cache(allow_output_mutation=True)
def loadData():
    laadpaaldata = pd.read_csv('laadpaaldata.csv')
    laadpaaldata.sort_values(by='Started')
    return laadpaaldata


def header():
    st.title('Onderzoek naar laadpalen: Deel 1')
    st.image('laadpaalafbeelding.jpeg')
    st.header('Data manipulatie:')
    st.markdown("* Welke data hebben we?")
    st.markdown("* Welke data kunnen/moeten we weggooien?")
    st.markdown("* Hoe kunnen we het verschil tussen laden en bezetten van een laadpaal analyseren?")
    st.markdown("* Welke handige informatie kunnen we nog meer toevoegen/bepalen?")


# Alles wat je runt per pagina moet in de def app(): komen. Anders runt hij de pagina niet.
def app():
    header()
    laadpaaldata = loadData()
    convertDataframe(laadpaaldata)
