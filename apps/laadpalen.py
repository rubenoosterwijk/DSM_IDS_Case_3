import streamlit as st
import altair as alt
import pandas as pd
import numpy as np
import os, urllib, cv2
import matplotlib.pyplot as plt
import seaborn as sns


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
    zero = laadpaaldata.loc[((laadpaaldata['OverChargeTime'] == 0) | (laadpaaldata['OverChargeTime'] < 0)), 'OverChargeTime']
    st.dataframe(zero)
    laadpaaldata.loc[((laadpaaldata['OverChargeTime'] == 0) | (laadpaaldata['OverChargeTime'] < 0)), 'OverChargeTime'] = np.nan


    st.text("Alle metingen waar de eindtijd kleiner is dan de starttijd moeten ook weg")
    tijderror = laadpaaldata.loc[laadpaaldata['Ended'] < laadpaaldata['Started'], ['Ended', "Started"]]
    laadpaaldata = laadpaaldata.drop(tijderror.index)
    st.dataframe(tijderror)

    # Zoeken naar twee speciafieke datums met 29 dagen in februari (schikkeljaar), deze zijn niet interperteerbaar.
    st.text("Verder moeten alle rows met op de 29ste van februari (schikkeljaar) ook weg, deze zijn niet interperteerbaar door  pd.to_datetime().")
    st.dataframe(laadpaaldata.loc[laadpaaldata['Started'] == "2018-02-29 07:37:53"])
    st.dataframe(laadpaaldata.loc[laadpaaldata['Ended'] == "2018-02-29 07:46:07"])
    # Deze twee droppen
    laadpaaldata = laadpaaldata.drop(1731)
    laadpaaldata = laadpaaldata.drop(1732)

    import io
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

    # st.pyplot(sns.lineplot(x="Started", y="OverChargeTime", hue="Weekday", data=laadpaaldata))
    return laadpaaldata


def main(laadpaaldata):
    laadpaaldata = convertDataframe(laadpaaldata)
    from datetime import datetime

    mindatum = laadpaaldata['Ended'].iloc[0]
    maxdatum = laadpaaldata['Ended'].iloc[-1]

    start_date = st.date_input(label = 'Start date',
                               value = mindatum,
                               min_value=mindatum,
                               max_value=maxdatum,)

    end_date = st.date_input(label='End date',
                               value=maxdatum,
                               min_value=mindatum,
                               max_value=maxdatum,)

    if start_date < end_date:
        st.success('Start date: `%s`\n\nEnd date:`%s`' % (start_date, end_date))
        start_date = pd.to_datetime(start_date)
        end_date = pd.to_datetime(end_date)
        laadpaaldata2 = laadpaaldata.loc[((start_date <= laadpaaldata['Started']) & (end_date >= laadpaaldata['Ended']))]
        st.dataframe(laadpaaldata2)
    else:
        st.error('Error: End date must fall after start date.')


    # start_time = st.slider(label = "Welke tijds periode wil je ontdekken?",
    #                        min_value = mindatum,
    #                        max_value=maxdatum,
    #                        value = mindatum,
    #                        format = "YY/MM/DD - hh:mm:ss")
    #
    # st.write("Start time:", start_time)


    st.write(mindatum, maxdatum)
    fig, ax = plt.subplots()
    st.write(laadpaaldata.describe())

    st.date_input("Selecteer hier de begindatum", value=laadpaaldata["Started"][0], min_value=None, max_value=None, key=None)
    st.bar_chart(laadpaaldata["OverChargeTime"])

    # ax = laadpaaldata["OverChargeTime"].hist(bins=100, range=[0,100])

    # st.write(alt.Chart(laadpaaldata).mark_bar().encode(
    #     x=alt.X("Started", bin=True),
    #     y='count()'
    # ))

    # # ax.hist(laadpaaldata["OverChargeTime"], range[0,100])
    # plt.show()

    # st.pyplot(fig)
    print(laadpaaldata.head())

    st.line_chart(laadpaaldata)
    st.pyplot()


# ax.plot(laadpaaldata, laadpaaldata["OverChargeTime"], laadpaaldata["Started"])
# plt.show()

# Load Data
laadpaaldata = pd.read_csv('laadpaaldata.csv')
laadpaaldata.sort_values(by='Started')

# Draw Upper Header
st.title('Onderzoek naar laadpalen')
st.image('laadpaalafbeelding.jpeg')
st.header('De data die wij onderzocht hebben:')
st.markdown("* Bezetting laadpalen")
st.markdown("* Wat is het verschil tussen laden en bezetten van een laadpaal?")
st.markdown("* Hoe ziet het gemiddelde laadprofiel er uit?")
st.markdown("* Wat is de verdeling in vermogens?")

main(laadpaaldata)


# ax = sns.boxplot(x=laadpaaldata["OverChargeTime"])
# plt.show()

# Streamlit encourages well-structured code, like starting execution in a main() function.


# Alles wat je runt per pagina moet in de def app(): komen. Anders runt hij de pagina niet.
def app():
    main()
