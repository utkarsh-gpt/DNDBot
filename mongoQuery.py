from pymongo import MongoClient
import streamlit as st

@st.cache_resource
def init_connection():
    return MongoClient(st.secrets["mongo"]['pymongo_string'])

client = init_connection()
db = client['5e-data'] 
classes = db['classes']
races = db['races']
displayInfo = db['displayInfo']

@st.cache_data(ttl=600)
def fetchDisplayInfo(field):
    response = displayInfo.find_one({"field":field},{"_id":0, "options":1})

    return response["options"]
