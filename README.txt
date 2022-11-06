## Table of Contents
1. [General Info](#general-info)
2. [Technologies](#technologies)
3. [Installation](#installation)
4. [Further Information](#further)
### General Info
***
This is a boilerplate project from a streamlit app used for BI purposes on a web3 project. 
## Technologies
***
A list of technologies used within the project:
Azure Cosmos DB
Python
Streamlit 
## Installation
***
A little intro about the installation. 
```
1. git clone https://github.com/MWMartley001/StreamlitCloudDemo.git
FOR CLOUD DEPLOYMENT
2. modify the secrets.toml file accordingly
3. modify data_prep function in data.py according to your needs
4. modify app.py according to your needs
5. setup account with streamlit cloud (https://streamlit.io/cloud)
6. connect the github repo to streamlit cloud per the step by step setup instructions
7. copy the contents of the secrets.toml file to the secrets window that appears
FOR LOCAL DEVELOPMENT/TESTING
2. setup a venv
3. pip install requirements.txt
4. create a .env file 
5. modify the .env file using the same template as the secrets.toml file
6. modify data_prep function in data.py according to your needs
7. modify app.py according to your needs
```
## Further information
***
See the PDF Streamlit Cloud App for more info into the project it supports as well as visuals of the features.
The unit tests can be expanded for happy path testing when adding valid values for the .env file.
