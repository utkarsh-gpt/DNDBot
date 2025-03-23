from pymongo import MongoClient
import json
import streamlit as st
import random

@st.cache_resource
def init_connection():
    return MongoClient(st.secrets['mongo']['pymongo_string'])

client = init_connection()
db = client['5e-data'] 


def fetchDisplayInfo(field, extra_arg=''):
    projection = {"_id":0, "options": 1} if not extra_arg else {'_id':0, "options":f'$options.{extra_arg}'}

    response = db['displayInfo'].find_one(
        {"field": field},
        projection    
        )

    return response

def fetchClass(className, subclass, level):
    include_subclass = True if subclass else False

    pipeline = [
        ## STAGE 1: Match the class
        {'$match': {'name': className}},
        ## STAGE 2: Combine the class and subclass features
        {
        '$project': {'_id': 0, "name": 1, "details": 1, "subclass": f"$subclass.{subclass}" if include_subclass else 2,
                     'features': {'$objectToArray': {'$mergeObjects': ['$details.classFeatures',f'$subclass.{subclass}.subclassFeatures'] if include_subclass else ["$details.classFeatures"]
                                                     }}}
        },
        ## STAGE 3: Remove the class and subclass features 
        {
        "$unset":['details.classFeatures','subclass.subclassFeatures']
        },
        ## STAGE 4: Check level and return appropriate features
        {
        '$project': {'_id': 0, "name": 1, "details": 1, "subclass": 1,
            'features': {
                '$filter': {
                    'input': '$features',
                    'as': 'feature',
                    'cond': {'$let': {'vars': {'convertedLevel': {'$convert': {
                        'input': '$$feature.v.level',
                        'to': 'int',
                        'onError': '$$feature.v.level'  # Return original value if conversion fails
                        }}},
                        'in': {
                            '$cond': {
                            'if': { '$eq': [{ '$type': '$$convertedLevel' }, 'string'] },
                            'then': False, # Include if conversion failed (still a string)
                            'else': { '$lte': ['$$convertedLevel', level] }  # Compare if conversion succeeded 
                            }}}}}}}
        },
        ## STAGE 4: 
        {'$project': {'_id':0, "class_name":"$name" ,'class_details':"$details" ,"subclass":{"$mergeObjects":[{"name":subclass},"$subclass"]}, 'features': {"$arrayToObject": "$features"}}}
    ]
    if not include_subclass:
        pipeline.append({"$unset":"subclass"})
    
    response = db['classes'].aggregate(pipeline)
    
    return response.next()

def fetchRFB(collection , query, source='Any'):
    # Fetch races, feats, backgrounds
    db_response = db[collection].find_one(
        {'name':query},
        {"_id":0}
    )

    if source == 'Any':
        sources = db_response['sources']
        source = random.choice(list(sources.keys()))

    response = {"name":db_response['name'],f"source:{source}":{source:db_response['sources'][source]}}
    return response
