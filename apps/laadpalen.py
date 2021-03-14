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

    # st.dataframe(laadpaaldata)
    # buffer = io.StringIO()
    # laadpaaldata.info(buf=buffer)
    #
    # s = buffer.getvalue()
    #
    # # De Started en Ended colommen zijn objecten en géén DateTime types.
    # st.text(s)

    mindatum = laadpaaldata['Ended'].iloc[0]
    maxdatum = laadpaaldata['Ended'].iloc[-1]

    start_date = st.date_input(label='Start date',
                               value=mindatum,
                               min_value=mindatum,
                               max_value=maxdatum)

    end_date = st.date_input(label='End date',
                             value=maxdatum,
                             min_value=mindatum,
                             max_value=maxdatum)

    if start_date < end_date:
        st.success('Start date: `%s`\n\nEnd date:`%s`' % (start_date, end_date))
        start_date = pd.to_datetime(start_date)
        end_date = pd.to_datetime(end_date)
        laadpaaldata2 = laadpaaldata.loc[
            ((start_date <= laadpaaldata['Started']) & (end_date >= laadpaaldata['Ended']))]
        st.dataframe(laadpaaldata2)
    else:
        st.error('Error: End date must fall after start date.')

    st.write(mindatum, maxdatum)
    fig, ax = plt.subplots()
    st.write(laadpaaldata.describe())

    st.date_input("Selecteer hier de begindatum", value=laadpaaldata["Started"][0], min_value=None, max_value=None,
                  key=None)
    # st.bar_chart(laadpaaldata["OverChargeTime"])
    #
    # # ax = laadpaaldata["OverChargeTime"].hist(bins=100, range=[0,100])
    #
    # # st.write(alt.Chart(laadpaaldata).mark_bar().encode(
    # #     x=alt.X("Started", bin=True),
    # #     y='count()'
    # # ))
    #
    # # # ax.hist(laadpaaldata["OverChargeTime"], range[0,100])
    # # plt.show()
    #
    # # st.pyplot(fig)
    # # print(laadpaaldata.head())
    # st.line_chart(laadpaaldata)
    # st.pyplot()



# Alles wat je runt per pagina moet in de def app(): komen. Anders runt hij de pagina niet.
def app():
    # Draw Upper Header
    header()
    main()
