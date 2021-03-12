import requests
import pandas as pd
import numpy as np
import seaborn as sns

response = requests.get("https://api.openchargemap.io/v3/referencedata/")
print(response.status_code)
print(response.text)
response.json()

key=f7903c6a-d2cd-4a10-b012-260c3536974f