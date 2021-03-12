import streamlit as st
from multiapp import MultiApp
from apps import OpenChargeMap, OpenDataRDW, main, home # import your app modules here
import os

path = "C:\\Users\\ruben\\Data Science\\Minor Data Science - Introduction to Data Science\\Case beschrijvingen\\Case 3\\DSM_IDS_Case_3"

#Maak een instantie van het multipagina framework
app = MultiApp()


# Add all your application here
app.add_app("Home", home.app)
app.add_app("OpenCharge", OpenChargeMap.app)
app.add_app("OpenDataRDW", OpenDataRDW.app)
app.add_app("main", main.app)
# The main app
app.run()