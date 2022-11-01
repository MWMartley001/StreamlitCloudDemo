# import configobj # for local development
import azure.cosmos.cosmos_client as cosmos_client
import pandas as pd
import numpy as np
import streamlit as st

# For local development below
# config = configobj.ConfigObj('.env')
# CONFIG = {
#     "ENDPOINT": config['ENDPOINT'],
#     "KEY": config['KEY'],
#     "DATABASE": config['DATABASE'],
#     "CONT1": config['CONT1'],
#     "CONT2": config['CONT2'],
#     "CONT3": config['CONT3']
#     }

CONFIG = {
    "ENDPOINT": st.secrets['ENDPOINT'],
    "KEY": st.secrets['KEY'],
    "DATABASE": st.secrets['DATABASE'],
    "CONT1": st.secrets['CONT1'],
    "CONT2": st.secrets['CONT2'],
    "CONT3": st.secrets['CONT3']
}

class CosmosData:
    def __init__(self, url, credential, database):
        self.url = url
        self.credential = credential
        self.database = database
        self.client = None
        self.db = None
    
    def setup_client(self):
        try:
            self.client = cosmos_client.CosmosClient(self.url, self.credential)
        except:
            raise ConnectionError("Error creating the client")

    def setup_db(self):
        try:
            self.db = self.client.get_database_client(self.database)
        except:
            raise ConnectionError("Error establishing database connection")

    def get_container(self,container_id):
        try:
            container = self.db.get_container_client(container_id)
            return container
        except:
            raise ConnectionError("Error connecting to container")

    def get_container_data(self,container, query):
        df_list = []
        try:
            for item in container.query_items(query=query, enable_cross_partition_query=True):
                df_list.append(dict(item))
        except: 
            raise ConnectionError("Error querying database container")
        if len(df_list) > 0:
            return df_list
        else:
            return None    

def is_minted(x):
    if x == 'None': 
        return "Unused"
    else:
        return "Used"

@st.cache(suppress_st_warning=True, allow_output_mutation=True)
def data_prep():
    data = CosmosData(CONFIG["ENDPOINT"], CONFIG["KEY"], CONFIG["DATABASE"])
    data.setup_client()
    data.setup_db()
    data.container1 = data.get_container(CONFIG["CONT1"]) 
    data.container2 = data.get_container(CONFIG["CONT2"])
    data.container3 = data.get_container(CONFIG["CONT3"])
    data.transactions_raw = data.get_container_data(data.container1, 'SELECT * FROM c')
    data.images_raw = data.get_container_data(data.container2, 'SELECT * FROM c')
    data.members_raw = data.get_container_data(data.container3, 'SELECT * FROM c')

    # project specific data manipulations
    df_images = pd.DataFrame(data.images_raw)
    df_images = pd.concat([df_images, pd.DataFrame(list(df_images['keyvalues']))], axis=1)
    images = df_images.loc[:, df_images.columns.isin(["imageURL","uniqueId","collection"])]
    images['uniqueId'].fillna('None', inplace=True)
    images['minted'] = images['uniqueId'].apply(is_minted)
    data.images = images
    df_transactions = pd.DataFrame(data.transactions_raw)
    data.transactions_filtered = df_transactions.loc[:, df_transactions.columns.isin(["name","email","dtInsert","appResponse","dtUpdated","uniqueId"])]
    data.member_images = data.transactions_filtered.merge(images[['imageURL', 'uniqueId']], how='left', on='uniqueId')
    data.members = pd.DataFrame(data.members_raw)
    return data