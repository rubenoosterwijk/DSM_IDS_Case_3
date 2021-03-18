import streamlit as st
import altair as alt
import pandas as pd
import numpy as np
import os, urllib, cv2
import matplotlib.pyplot as plt
import seaborn as sns
import io


def header():
    st.title('Onderzoek naar laadpalen: Deel 2')
    st.image('laadpaalafbeelding.jpeg')
    st.header('Data visualisatie:')
    st.markdown("* Bezetting laadpalen")
    st.markdown("* Wat is het verschil tussen laden en bezetten van een laadpaal?")
    st.markdown("* Hoe ziet het gemiddelde laadprofiel er uit?")
    st.markdown("* Wat is de verdeling in vermogens?")


def main():
    from datetime import datetime
    laadpaaldata = pd.read_csv("laadpaaldataClean.csv", index_col=0)

    laadpaaldata['Started'] = pd.to_datetime(laadpaaldata['Started'], format='%Y-%m-%d %H:%M:%S')
    laadpaaldata['Ended'] = pd.to_datetime(laadpaaldata['Ended'], format='%Y-%m-%d %H:%M:%S')

    # st.write(laadpaaldata.describe())

    colomns = ["TotalEnergy", "ConnectedTime", "ChargeTime", "MaxPower", "OverCharged", "Weekday"]

    option2 = st.selectbox(
        'Selecteer uw column voor de histogram?',
        (colomns))
    st.write('You selected:', option2)

    if option2=="Weekday":

        week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        optionsdict = {'Monday': 0, 'Tuesday': 1, 'Wednesday': 2, 'Thursday': 3, 'Friday': 4, 'Saturday': 5, 'Sunday': 6}

        week1, week2 = st.select_slider(
            'Select a range for dates created',
            options=week,
            value=('Monday', 'Sunday'))

        week3 = optionsdict[week1]
        week4 = optionsdict[week2]

        st.write(week3, week4)

        st.dataframe(laadpaaldata)
        df2 = laadpaaldata.loc[
            ((laadpaaldata['Weekday'] >= week3) & (laadpaaldata['Weekday'] <= week4))]
        # st.dataframe(df2)

        sns.histplot(data=df2, x=option2)
        st.pyplot()
    else:
        df2 = laadpaaldata
        sns.histplot(data=df2, x=option2)
        st.pyplot()



    # options = st.multiselect(
    #     'Selecteer de weekdagen', ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'],
    #     ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])

    # st.dataframe(df2)

    sns.histplot(data=df2, x="ChargeTime", bins=30, kde=True, element="step")

    plt.axvline(x=laadpaaldata.ChargeTime.mean(), linewidth=1, color='g', label="mean", alpha=0.5)
    plt.axvline(x=laadpaaldata.ChargeTime.median(), linewidth=1, color='y', label="median", alpha=0.5)

    plt.legend(["mean", "median"])
    st.pyplot()

    sns.histplot(data=laadpaaldata, x="ChargeTime", y="ConnectedTime", bins=40, cbar=True, cbar_kws=dict(shrink=.75))

    plt.axvline(x=laadpaaldata.ChargeTime.mean(), linewidth=1, color='g', label="mean", alpha=0.5)
    plt.axvline(x=laadpaaldata.ChargeTime.median(), linewidth=1, color='y', label="median", alpha=0.5)

    plt.legend(["mean", "median"])
    st.pyplot()



    colomns = ["TotalEnergy", "ConnectedTime", "ChargeTime", "MaxPower"]
    col_one_list = laadpaaldata['Started'].tolist()

    start_date = laadpaaldata['Started'].iloc[0]
    end_date = laadpaaldata['Started'].iloc[-1]

    option3 = st.selectbox(
        'Selecteer uw column voor de y-as',
        (colomns))
    st.write('You selected:', option3)


    start_slider, end_slider = st.select_slider(
        'Select a range for dates created',
        options=col_one_list,
        value=(start_date, end_date))

    st.write('Your selected time between', start_slider, 'and', end_slider)
    df = laadpaaldata.loc[
        ((laadpaaldata['Started'] > start_slider) & (laadpaaldata['Ended'] < end_slider))]

    sns.scatterplot(data=df, x="Started", y=option3)
    plt.xticks(rotation=45)

    st.pyplot()


# Alles wat je runt per pagina moet in de def app(): komen. Anders runt hij de pagina niet.
def app():
    # Draw Upper Header
    header()
    main()

