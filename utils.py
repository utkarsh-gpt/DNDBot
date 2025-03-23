from anthropic import Anthropic
from instructor import Instructor, Mode, patch, from_anthropic
import os
import json
import streamlit as st
import mongoQuery
import models

@st.cache_resource
def init_api():
    client = Instructor(
        client=Anthropic(api_key=st.secrets["anthropic"]["api_key"]),
        create=patch(
            create=Anthropic(api_key=st.secrets["anthropic"]["api_key"]).beta.prompt_caching.messages.create,
            mode=Mode.ANTHROPIC_TOOLS,
    ),
        mode=Mode.ANTHROPIC_TOOLS,
        )
    return client
MODEL = "claude-3-haiku-20240307"

def generateResponse(filepaths, prompt):
    client = init_api()
    data = {}
    messages = [{"role": "user", "content": []}]

    for item in filepaths:
        with open(item,'r') as f:
            data[item] = f.read()

            
        messages[0]["content"].append(
            {
            "type": "text",
            "text": f"<{item}>{data[item]}</{item}>",
            "cache_control": {"type": "ephemeral"}
            }
        )
    
    messages[0]["content"].append(
        {
        "type": "text",
        "text": prompt
        }
    )

    system_prompt = """
    You are an AI assistant for a Dungeon Master (DM) in a Dungeons & Dragons game. Your primary function is to aid the DM by answering questions about the provided context and generating ideas when asked about topics outside the given information.

    ## Core Functions:
    1. Answer questions based on the provided context accurately and concisely.
    2. When asked about topics not in the context, generate creative ideas that fit the genre (Funny, Witty, Action, or Intense).
    3. Assist with rules clarifications, character creation, world-building, and encounter design.
    4. Offer suggestions for plot twists, NPC interactions, and quest ideas.

    ## Content Guidelines:
    - You can generate content related to fantasy violence, sexual themes, and anatomy when appropriate for the game's context.
    - Avoid real-world political discussions or pushing any specific agendas.
    - Keep responses relevant to the fantasy setting of the game.

    ## Interaction Style:
    - Be concise yet informative in your responses.
    - Use a tone that matches the current mood of the game (e.g., humorous for lighter moments, serious for intense situations).
    - Encourage creativity and improvisation from the DM and players.

    ## When Lacking Information:
    If asked about something not in your provided context:
    1. Clearly state that the information isn't in your current context.
    2. Offer to generate an idea that fits one of these genres: Funny, Witty, Action, or Intense.
    3. Create a suitable response based on the chosen genre and the general theme of D&D.

    Remember, your goal is to enhance the D&D experience by supporting the DM's creativity and helping to create an engaging, immersive game world."""

    response = client.messages.create(
            model=MODEL,
            system=system_prompt,
            max_tokens=300,
            messages=messages,
            extra_headers={"anthropic-beta": "prompt-caching-2024-07-31"}
    )

    return response.content[0].text


def generateCharacterTraits(prompt: str, classes: dict):
    
    client = init_api()

    subclassLevels = {
    'Artificer': 3,
    'Barbarian': 3,
    'Bard': 3,
    'Cleric': 1,
    'Druid': 2,
    'Fighter': 3,
    'Monk': 3,
    'Paladin': 3,
    'Ranger': 3,
    'Rogue': 3,
    'Sorcerer': 1,
    'Warlock': 1,
    'Wizard': 2
    }

    classDict = {}
    for className in classes.keys():
        if classes[className] >= subclassLevels[className]: 
            subclassOptions = mongoQuery.fetchDisplayInfo('classes', className)
            classDict[className] = subclassOptions['options']
    
    races = mongoQuery.fetchDisplayInfo('races')
    backgrounds = mongoQuery.fetchDisplayInfo('backgrounds')

    print(classDict)
    print(classes)

    messages = [{"role": "user", "content": [
        {
            "type": "text",
            "text": f"Based on the description pick out a race from the list {races} and a background {backgrounds} that is best fitting for the character. If no context is provided then pick at random. ",
            "cache_control": {"type": "ephemeral"}
        },
        {
            "type": "text",
            "text": f"Based on the description pick out a subclass for each of the classes in <classes>{str(classes)}</classes>, pick from the list of subclasses that are given for each class. The data is given in the schema 'Class' :{'Subclass : description'} : <subclasses>{str(classDict)}</subclasses>",
            "cache_control": {"type": "ephemeral"}
        },
        {
            "type": "text",
            "text": f"<description>{prompt}</description>",
            "cache_control": {"type": "ephemeral"}
        },
            ]}]
    # print(messages)
    response = client.messages.create(
            model=MODEL,
            system="Act as a helpful assisstant for a Game Masters for Dungeons and Dragons. Make a JSON object with values reflecting that of creating a character based on the character description given in the user prompt and pick out the best RACE, BACKGROUND, CLASSES and SUBCLASSES that fit from the options provided. Display multiple classes if more than one is provided ",
            max_tokens=100,
            messages=messages,
            # extra_headers={"anthropic-beta": "prompt-caching-2024-07-31"},
            response_model= models.CharacterTraits,
            max_retries = 5   
    )

    return response

def generateCharacterFlavour(prompt: str, race):
    
    client = init_api()

    messages = [{"role": "user", "content": [
        {
            "type": "text",
            "text": f"<description>{prompt}</description>",
            "cache_control": {"type": "ephemeral"}
        },
        {
            "type": "text",
            "text": f"<race>{str(race)}</race>",
            "cache_control": {"type": "ephemeral"}
        }]}]

    response = client.messages.create(
            model=MODEL,
            system="Act as a helpful assisstant for Dungeons and Dragons. Generate creative and interesting flavour for a character based on the user prompt. Generate a name, ideals, flaws, alignment, personality amd a backstory for the character. Also generate the gender, age, weight and height.",
            max_tokens=1000,
            messages=messages,
            # extra_headers={"anthropic-beta": "prompt-caching-2024-07-31"},
            response_model= models.CharacterFlavour,
            max_retries = 3   
    )

    return response

def generateCharacterFeatures(prompt: str, traits: models.CharacterTraits):

    client = init_api()
    
    picked_race = mongoQuery.fetchRFB('races', traits.RACE)
    # picked_background = mongoQuery.fetchRFB('backgrounds', traits.BACKGROUND)

    trait_description = ''
    choices = set()
    ability_saves = set()
    for item in eval(traits.CLASS_LEVEL):
        if item[2]:
            class_info = mongoQuery.fetchClass(item[0], item[2], item[1])
            trait_description += str(class_info)
            ability_saves.update(class_info['class_details']['proficiency'])
            if 'any' in class_info['class_details']['startingProficiencies']['skills'][0]:
                choices = {'Acrobatics', 'Animal', 'Arcana', 'Athletics', 'Deception', 'History', 'Insight', 'Intimidation', 'Investigation', 'Medicine', 'Nature', 'Perception', 'Performance', 'Persuasion', 'Religion', 'Sleight of Hand', 'Stealth ', 'Survival'}
                count = class_info['class_details']['startingProficiencies']['skills'][0]['any']
            else:
                choices.update(set(class_info['class_details']['startingProficiencies']['skills'][0]['choose']['from']))
                count = class_info['class_details']['startingProficiencies']['skills'][0]['choose']["count"]
    
    payload = models.createPayload(tuple(choices), int(count))
    messages = [{"role": "user", "content": [
        {
            "type": "text",
            "text": f"<description>{prompt}</description>",
            "cache_control": {"type": "ephemeral"}
        },
        {
            "type": "text",
            "text": f"<features>{str(picked_race) + "\n\n" + "\n\n" + str(trait_description)}</features>",   # + str(picked_background) 
            "cache_control": {"type": "ephemeral"}
        }
        ]}]
    

    response = client.messages.create(
            model=MODEL,
            system="Act as a helpful assisstant for a Game Masters for Dungeons and Dragons. Extract the features from the given data and input them into the correct fields.",
            max_tokens=1000,
            messages=messages,
            extra_headers={"anthropic-beta": "prompt-caching-2024-07-31"},
            response_model= payload,  
            max_retries = 7 
    )


    return response, ability_saves




def search_spells(level):
    spells_folder = '5e-data/spells'
    matching_spells = []

    for filename in os.listdir(spells_folder):
        file_path = os.path.join(spells_folder, filename)
        with open(file_path, 'r') as file:
            data = json.load(file)
            for spell in data['spell']:
                if 'level' in spell and spell['level'] == level:
                    matching_spells.append((spell['name'], spell['source']))

    return matching_spells
