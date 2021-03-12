from multiapp import MultiApp
from apps import OpenChargeMap, OpenDataRDW, main, home # import your app modules here

#Maak een instantie van het multipagina framework
app = MultiApp()


# Add all your application here
app.add_app("Home", home.app)
app.add_app("OpenCharge", OpenChargeMap.app)
app.add_app("OpenDataRDW", OpenDataRDW.app)
app.add_app("main", main.app)
# The main app
app.run()