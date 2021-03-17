import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import requests
import json as js
import folium
import streamlit_folium
from branca.element import Template, MacroElement

# iterate over rows with iterrows()
types = ['Fast Charge AC',
         'Rapid Charge DC']

template = """
{% macro html(this, kwargs) %}

<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>jQuery UI Draggable - Default functionality</title>
  <link rel="stylesheet" href="//code.jquery.com/ui/1.12.1/themes/base/jquery-ui.css">

  <script src="https://code.jquery.com/jquery-1.12.4.js"></script>
  <script src="https://code.jquery.com/ui/1.12.1/jquery-ui.js"></script>

  <script>
  $( function() {
    $( "#maplegend" ).draggable({
                    start: function (event, ui) {
                        $(this).css({
                            right: "auto",
                            top: "auto",
                            bottom: "auto"
                        });
                    }
                });
});

  </script>
</head>
<body>


<div id='maplegend' class='maplegend' 
    style='position: absolute; z-index:9999; border:2px solid grey; background-color:rgba(255, 255, 255, 0.8);
     border-radius:6px; padding: 10px; font-size:14px; right: 20px; bottom: 20px;'>

<div class='legend-title'>Legenda (type meetpunt)</div>
<div class='legend-scale'>
  <ul class='legend-labels'>
    <li><span style='background:green;opacity:0.7;'></span>DC</li>
    <li><span style='background:blue;opacity:0.7;'></span>AC</li>


  </ul>
</div>
</div>

</body>
</html>

<style type='text/css'>
  .maplegend .legend-title {
    text-align: left;
    margin-bottom: 5px;
    font-weight: bold;
    font-size: 90%;
    }
  .maplegend .legend-scale ul {
    margin: 0;
    margin-bottom: 5px;
    padding: 0;
    float: left;
    list-style: none;
    }
  .maplegend .legend-scale ul li {
    font-size: 80%;
    list-style: none;
    margin-left: 0;
    line-height: 18px;
    margin-bottom: 2px;
    }
  .maplegend ul.legend-labels li span {
    display: block;
    float: left;
    height: 16px;
    width: 30px;
    margin-right: 5px;
    margin-left: 0;
    border: 1px solid #999;
    }
  .maplegend .legend-source {
    font-size: 80%;
    color: #777;
    clear: both;
    }
  .maplegend a {
    color: #777;
    }
</style>
{% endmacro %}"""



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

    macro = MacroElement()
    macro._template = Template(template)
    m.get_root().add_child(macro)

    #HIER COLORPLETH TOEVOEGEN \|/




    folium.LayerControl().add_to(m)
    folium_static(m)


# Alles wat je runt per pagina moet in de def app(): komen. Anders runt hij de pagina niet.
def app():
    st.header('Kort overzicht van de data:')

    openchargemap = loadData()

    st.text(openchargemap.info())

    st.text(openchargemap.describe())

    # openchargemap["OverChargeTime"] = openchargemap["ConnectedTime"] - openchargemap["ChargeTime"]


    print(openchargemap.head())

    st.image('laadpaalafbeelding.jpeg')
    st.header('De data die wij onderzocht hebben in Nederland:')

    st.markdown("* Hoeveel laadpalen zijn er per laadpaaltype?")
    st.markdown("* Wat zijn de kosten per laadpaal?")
    st.markdown("* Hoeveel laadpalen zijn er in de loop van de jaren bijgekomen?")
    st.markdown("* Waar staan de laadpalen in Nederland en per stad?")

    sns.histplot(data=openchargemap,
                 x="ChargerType",
                 shrink=.2,
                 hue="ChargerType")

    st.header('Als eerst hebben we de data gecleaned:')

    st.dataframe(openchargemap)
    st.line_chart(openchargemap)

    plekken = ["Amsterdam",
               "Rotterdam",
               "Den Haag",
               "Utrecht",
               "Nederland"]



    st.write('You selected:', option)

    user_input = st.text_input("label goes here", "Nederland")

    xd = openchargemap.sort_values(by=['DateCreated'])

    col_one_list = xd['DateCreated'].tolist()

    start_date = openchargemap['DateCreated'].iloc[0]
    end_date = openchargemap['DateCreated'].iloc[-1]

    start_slider, end_slider = st.select_slider(
        'Select a range for dates created',
        options=col_one_list,
        value=(start_date, end_date))

    st.write('Your selected time between', start_slider, 'and', end_slider)

    df = openchargemap.loc[((openchargemap['DateCreated'] > start_slider) & (openchargemap['DateCreated']< end_slider))]
    drawMap(df, user_input)


