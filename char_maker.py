import streamlit as st
from utils import search_spells
from mongoQuery import fetchDisplayInfo

st.header("Character Maker")

helper_text = "Enter the qualities for the character here, 'strong'. 'sneaky' etc. and any backstory points or factions or items that you want the character to use. No need to enter any class or spell information"
user_prompt = st.text_area("Enter Prompt:", help=helper_text)

import os
import json

class_options = fetchDisplayInfo("classes") 
race_options = fetchDisplayInfo("races")

race_selection = st.selectbox("Select Race:", options=race_options, key="selected_race",help="Checkout the [class](https://5e.tools/classes.html) and [race](https://5e.tools/races.html) descriptions")

if 'class_amount' not in st.session_state:
    st.session_state.class_amount = 1  


def validate_levels():
    if sum(total_levels) > 20:
        st.warning("The total levels of all classes must not exceed 20.")
    return sum(total_levels) > 20

col1, col2 = st.columns(2)

class_names = []
total_levels =  []

for i, level in enumerate(range(1,st.session_state.class_amount+1)):
    with col1:
        class_names.append(st.selectbox(f"Select Class {i + 1}:", options=[cls for cls in class_options if cls not in class_names], key=f"class_{i}"))
    with col2:
        total_levels.append(st.number_input(f"Select Level for Class {i + 1}:", min_value=1, max_value=20, key=f"level_{i}"))

class_key = {cls: lvl for cls in  class_names for lvl in total_levels}
level_check = validate_levels()

with col1:
    if st.session_state.class_amount == 13:
        add_class_button = st.button("Add Another Class", use_container_width=True,disabled=True, help="You cannot add anymore classes")
    else:
        add_class_button = st.button("Add Another Class", use_container_width=True)
with col2:
    if st.session_state.class_amount == 1:
        remove_class_button =  st.button("Remove a Class", use_container_width=True,disabled=True, help="You cannot remove anymore classes")
    else:
        remove_class_button = st.button("Remove a Class", use_container_width=True)
if remove_class_button:
    st.session_state.class_amount -= 1
    st.rerun()
if add_class_button:
    st.session_state.class_amount += 1
    st.rerun()


generate_button = st.button("Generate Character", use_container_width=True)

if generate_button:
    if user_prompt:
        st.info("Generating character... This may take a moment.")

        st.success("Character generated successfully!")
    else:
        st.warning("Please enter a character description before generating.")


# spell_level = st.selectbox("Select Spell Level", range(1, 10))

# matching_spells = search_spells(spell_level)

# spell_options = [f"{spell[0]} ({spell[1]})" for spell in matching_spells]

# # Create a multiselect box for the spells
# selected_spells = st.multiselect(
#     f"Select spells of level {spell_level}:",
#     options=spell_options,
#     help="You can select multiple spells from this list."
# )

# # Display the selected spells
# if selected_spells:
#     st.write("You have selected the following spells:")
#     for spell in selected_spells:
#         st.write(f"- {spell}")
# else:
#     st.write(f"No spells of level {spell_level} selected.")

