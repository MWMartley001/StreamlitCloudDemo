from data.data import data_prep
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px


# project specific charts with custom layout
data = data_prep()
options = list(zip(data.member_images['name'], data.member_images['email'], data.member_images['imageURL']))
col1, col2, col3 = st.columns([.4, .2, .4])
col1.markdown('<h3 style="text-align:center;color:black;font-weight:bolder;font-size:70px;">Member Images</h3>',unsafe_allow_html=True)
option = col1.selectbox("Select a Token Recipient",options)
col1.image(option[2])

options = list(data.images["collection"].unique())
col3.markdown('<h3 style="text-align:center;color:black;font-weight:bolder;font-size:70px;">Image Collections</h3>',unsafe_allow_html=True)
option = col3.selectbox("Select Image Collection",options)
token_data = data.images[data.images["collection"]==option]
pie_data = token_data["minted"].value_counts()
col3.write(px.pie(pie_data, values=pie_data, names=pie_data.index, width=400, height=400))

archived_members = data.members[data.members['status']=='2']
new_members = data.members[data.members['status']=='1']
members_with_tokens = data.members[data.members['status']=='3']
st.markdown('<h1 style="text-align:center;color:black;font-weight:bolder;font-size:70px;">Membership</h1>',unsafe_allow_html=True)
col1, col2, col3 = st.columns([.3, .3, .3])
col1.metric("Archived Members", len(archived_members))
col2.metric("Members with Tokens", len(members_with_tokens))
col3.metric("New Members Active (Under 60 days)", len(new_members))

new_members = data.members[~data.members["dtInsert"].isnull()]
new_members = new_members.groupby(by="dtInsert").size().reset_index(name="counts")
new_members = new_members.sort_values(by=["dtInsert"], ascending=True)
new_members['dtInsert'] = pd.to_datetime(new_members['dtInsert']).dt.strftime('%d/%m/%Y')
hist = px.bar(data_frame=new_members, x="dtInsert", y="counts", barmode="group",
 labels={"counts": "# New Members", 'dtInsert': "Date Joined"})
st.write(hist)