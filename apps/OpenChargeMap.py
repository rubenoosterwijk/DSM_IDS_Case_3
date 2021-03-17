import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import requests
import json as js
import folium

# iterate over rows with iterrows()
types = ['Fast Charge AC',
         'Rapid Charge DC']

def color_producer(type):
    if type == "Fast Charge AC":
        return 'blue'
    if type == "Rapid Charge DC":
        return 'green'

# Bud De data van de locaties van de laadpalen verstrekken. Onthoud je gaat met de map werken en je moet dus een maar weergeven op streamlit.
# Kijk alvast naar voorbeelden op de site of we met de map exrtra interactieve dingen kunnen doen (widget gebruik)

# Onderling even uitmaken wie wat gaat onderzoeken
@st.cache
def loadData():
    df = pd.read_csv('laadpaallocaties.csv')

    df["UsageCost"] = df["UsageCost"].replace(np.nan, 'Onbekend', regex=True)
    nonnullfactor = 0.1

    df = df.loc[:, df.isnull().mean() < nonnullfactor]
    df = df.drop_duplicates()
    df = df.reset_index(drop=True)

    conditions = [
        (df['Connections/0/LevelID'] == 1),
        (df['Connections/0/LevelID'] == 2),
        (df['Connections/0/LevelID'] == 3)
    ]
    values = ['Slow Charge AC', 'Fast Charge AC', 'Rapid Charge DC']

    df['ChargerType'] = np.select(conditions, values)
    return df


def drawMap(df, optie):
    import streamlit as st
    from streamlit_folium import folium_static
    import folium

    cors = {"Amsterdam": [52.3702157, 4.8951679],
               "Rotterdam": [51.9244201, 4.4777325],
               "Den Haag": [52.0704978,	4.3006999],
               "Utrecht": [52.0893191, 5.1101691],
               "Nederland": [52.0893191, 5.1101691]
    }

    if optie == "Nederland":
        control = True
        plek = cors[optie]
        zoom = 7
    else:
        control = False
        plek = cors[optie]
        zoom = 12

    m = folium.Map(location=plek,
                   zoom_start=zoom,
                   iles="openstreetmap",
                   zoom_control=control,
                   scrollWheelZoom=control,
                   dragging=control,
                   control_scale = True)
    # add marker for Liberty Bell

    # call to render Folium map in Streamlit

    loc = 'Laadpalen Nederland'
    title_html = '''
                 <h3 align="center" style="font-size:16px"><b>{}</b></h3>
                 '''.format(loc)

    m.get_root().html.add_child(folium.Element(title_html))

    for x in types:

        a = df.loc[(df['ChargerType'] == x)]

        feature_group = folium.FeatureGroup(x)

        for index, row in a.iterrows():
            meting = row["Connections/0/PowerKW"]
            metingstr = str(meting)
            message1 = 'Vermogen: '
            cost = row["UsageCost"]
            message = message1 + metingstr + " KW " + cost + " eu/uur"
            locatie = [row['AddressInfo/Latitude'], row['AddressInfo/Longitude']]
            postcode = str(row["AddressInfo/Postcode"])
            plaats = str(row["AddressInfo/Town"])
            adres = str(row['AddressInfo/AddressLine1'])
            totadres = plaats + ", " + adres + ", " + postcode
            #         print (totadres)
            popup = totadres
            #     print(locatie)

            folium.CircleMarker(
                location=locatie,
                popup=popup,
                tooltip=message,
                radius=10,
                color=color_producer(row["ChargerType"]),
                fill=True,
                fillOpacity=0.4).add_to(feature_group)

        feature_group.add_to(m)

    folium.LayerControl().add_to(m)
    folium_static(m)


# Alles wat je runt per pagina moet in de def app(): komen. Anders runt hij de pagina niet.
def app():
    openchargemap = loadData()



    st.text(openchargemap.info())

    st.text(openchargemap.describe())

    # openchargemap["OverChargeTime"] = openchargemap["ConnectedTime"] - openchargemap["ChargeTime"]
    print(openchargemap.head())

    st.image('laadpaalafbeelding.jpeg')
    st.header('De data die wij onderzocht hebben:')

    st.markdown("* Bezetting laadpalen")
    st.markdown("* Wat is het verschil tussen laden en bezetten van een laadpaal?")
    st.markdown("* Hoe ziet het gemiddelde laadprofiel er uit?")
    st.markdown("* Wat is de verdeling in vermogens?")
    st.dataframe(openchargemap)
    st.line_chart(openchargemap)

    plekken = ["Amsterdam",
               "Rotterdam",
               "Den Haag",
               "Utrecht",
               "Nederland"]

    option = st.selectbox(
        'How would you like to be contacted?',
        (plekken))

    st.write('You selected:', option)

    user_input = st.text_input("label goes here", "Amsterdam")

    drawMap(openchargemap, user_input)


app()
