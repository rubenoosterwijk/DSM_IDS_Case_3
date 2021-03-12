import streamlit as st
import pandas as pd

# -*- coding: utf-8 -*-
# Copyright 2018-2019 Streamlit Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# This demo lets you to explore the Udacity self-driving car image dataset.
# More info: https://github.com/streamlit/demo-self-driving

import streamlit as st
import altair as alt
import pandas as pd
import numpy as np
import os, urllib, cv2

# Streamlit encourages well-structured code, like starting execution in a main() function.
def main():
    st.title('Onderzoek naar laadpalen')

    laadpaaldata1 = pd.read_csv('data\\laadpaaldata.csv')
    laadpaaldata = pd.read_csv('data\\convertcsv.csv')

    # laadpaaldata["OverChargeTime"] = laadpaaldata["ConnectedTime"] - laadpaaldata["ChargeTime"]
    print(laadpaaldata.head())

    st.image('laadpaalafbeelding.jpeg')
    st.header('De data die wij onderzocht hebben:')

    st.markdown("* Bezetting laadpalen")
    st.markdown("* Wat is het verschil tussen laden en bezetten van een laadpaal?")
    st.markdown("* Hoe ziet het gemiddelde laadprofiel er uit?")
    st.markdown("* Wat is de verdeling in vermogens?")
    st.dataframe((laadpaaldata).head())
    st.line_chart(laadpaaldata)



# Alles wat je runt per pagina moet in de def app(): komen. Anders runt hij de pagina niet.
def app():
    main()
