import pytest
import pandas as pd
from src.data.data import CosmosData, is_minted

@pytest.fixture(scope="module")
def create_data():
    return CosmosData("bad_url","bad_credential","fake_db")

@pytest.fixture(scope="function")
def create_df_minted():
    return pd.DataFrame({"Unique_Id":["None",1]})

def test_initialize_client(create_data):
    with pytest.raises(ConnectionError) as exp:
        create_data.setup_client()
    assert str(exp.value) == "Error creating the client"

def test_db_connect(create_data):
    with pytest.raises(ConnectionError) as exp:
        create_data.setup_db()
    assert str(exp.value) == "Error establishing database connection"  

def test_container_connect(create_data):
    with pytest.raises(ConnectionError) as exp:
        create_data.get_container("Container_id") 
    assert str(exp.value) == "Error connecting to container"  

def test_container_query(create_data):
    with pytest.raises(ConnectionError) as exp:
        create_data.get_container_data("data.container1", "SELECT * FROM c")
    assert str(exp.value) == "Error querying database container"

def test_is_minted(create_df_minted):
    sample = create_df_minted
    sample['minted'] = sample['Unique_Id'].apply(is_minted)
    assert sample['minted'].isin(['Used','Unused']).all()


