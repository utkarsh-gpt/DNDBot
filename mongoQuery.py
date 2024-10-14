from pymongo import MongoClient
import streamlit as st

client = MongoClient(st.secrets['pymongo_string'])
db = client['5e-data'] 
classes = db['classes']
races = db['races']
displayInfo = db['displayInfo']

def fetchDisplayInfo(field):
    response = displayInfo.find_one({"field":field},{"_id":0, "options":1})

    return response["options"]
