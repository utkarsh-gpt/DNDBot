import json
from pymongo import MongoClient
import os

client = MongoClient('mongodb+srv://utkarshgupta0122:u5eyBtIlug8TSK9K@dndbot.2xnuz.mongodb.net/?retryWrites=true&w=majority&appName=DNDBot')
db = client['5e-data']  # Replace with your actual database name
collection = db['displayInfo']  # Replace with your actual collection name

with open('5e-data/races.json', 'r') as f:
    data = json.load(f)

race_options = sorted(list({rc['name'] for rc in data['race']}))

collection.insert_one({"field":"races","options":race_options})




# with open('5e-data/races.json', 'r') as file:
#     data = json.load(file)


### Race Pasring

# def get_race(race):
#     race_schema = {
#         'ability': race.get('ability', None), 
#         'size': race.get('size', None), 
#         'feats': race.get('feats', None),  
#         'srd': race.get('srd', None), 
#         'entries': race.get('entries', None), 
#         'lineage': race.get('lineage', None), 
#         'speed': race.get('speed', None)
#     }
#     return race_schema
# race_dict = {}
# for race in data['race']:
#     if race['name'] not in race_dict:
#         race_dict[race['name']] = {'sources' : {race.get('source'): get_race(race)}}   
#     else:
#         race_dict[race['name']]['sources'].update({race.get('source'): get_race(race)}) 

#### Class Parsing

# import os

# classes_folder = '5e-data/classes/'
# classFiles = [f for f in os.listdir(classes_folder) if f.endswith('.json')]

# for class_file in classFiles:
#     with open(os.path.join(classes_folder, class_file), 'r') as file:
#         class_data = json.load(file)

#     class_features = class_data['class'][0].get('classFeatures')
#     subclasses = class_data['subclass']
#     feature_description = class_data['classFeature']
#     sub_feature_description = class_data['subclassFeature']
#     classFeatures = {}
#     subclassFeatures = {}

#     for feature in class_features:
#         if type(feature) is str:
#             parser = feature.split('|')
#         else:
#             parser = feature['classFeature'].split('|')
#         feature_name =  parser[0]
#         level = parser[-1]

#         for feature in feature_description:
#             if feature['name'] == feature_name:
#                 description = feature['entries']
        
#         classFeatures.update({
#             feature_name : {'level':level, 'description': description}
#         })

#     for i, cls in enumerate(subclasses):
#         features = cls['subclassFeatures']
#         for feature in features:
#             if type(feature) is str:
#                 parser = feature.split('|')
#             else:
#                 parser = feature['classFeature'].split('|')
#             feature_name =  parser[0]
#             level = parser[-1]

#             for feature in sub_feature_description:
#                 if feature['name'] == feature_name:
#                     description = feature['entries']

#             subclassFeatures.update({
#                 feature_name : {'level':level, 'description': description}
#             })
#         class_data['subclass'][i]['subclassFeatures'] = subclassFeatures

#     class_data['class'][0]['classFeatures'] = classFeatures

#     del class_data['subclassFeature']
#     del class_data['classFeature']

#     collection.insert_one(class_data)

