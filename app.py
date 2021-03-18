from multiapp import MultiApp
from apps import OpenChargeMap, OpenDataRDW, laadpalen, home, laadpalendata # import your app modules here

#Maak een instantie van het multipagina framework
app = MultiApp()


# Add all your application here
app.add_app("Home", home.app)
app.add_app("OpenChargeMap", OpenChargeMap.app)
app.add_app("OpenDataRDW", OpenDataRDW.app)
app.add_app("Laadpalen Data Manipulatie", laadpalendata.app)
app.add_app("Laadpalen Data Visualisatie", laadpalen.app)
# The main app
app.run()