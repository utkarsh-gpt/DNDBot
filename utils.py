from anthropic import Anthropic
import os
import json
import streamlit as st

client = Anthropic(api_key=st.secrets["anthropic"]["api_key"])
MODEL = "claude-3-haiku-20240307"

def generateResponse(filepaths, prompt):
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

    response = client.messages.create(
            model=MODEL,
            system="Act as a helpful assisstant for a Game Masters for Dungeons and Dragons. Provide any help fetching information through the provided context or produce storytelling suggestions when prompted.",
            max_tokens=300,
            messages=messages,
            extra_headers={"anthropic-beta": "prompt-caching-2024-07-31"}
    )

    return response.content[0].text


def generateCharacterSheet(schema_path, prompt):
    
    messages = [{"role": "user", "content": []}]

    response = client.messages.create(
            model=MODEL,
            system="Act as a helpful assisstant for a Game Masters for Dungeons and Dragons. Using the schema given, create a character based on the user prompt.",
            max_tokens=300,
            messages=messages,
            extra_headers={"anthropic-beta": "prompt-caching-2024-07-31"}
    )

    return response


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