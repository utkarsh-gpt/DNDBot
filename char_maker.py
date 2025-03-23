import streamlit as st
import utils
from mongoQuery import fetchDisplayInfo
from fillPDF import fill_pdf

st.header("Character Maker")

helper_text = "Enter the qualities for the character here, 'strong'. 'sneaky' etc. and any backstory points or factions or items that you want the character to use. No need to enter any class or spell information"
user_prompt = st.text_area("Enter Prompt:", help=helper_text)

import os
import json

class_options = fetchDisplayInfo("classes") 
# race_options = fetchDisplayInfo("races")

# race_selection = st.selectbox("Select Race:", options=list(race_options), key="selected_race",help="Checkout the [class](https://5e.tools/classes.html) and [race](https://5e.tools/races.html) descriptions")

if 'class_amount' not in st.session_state:
    st.session_state.class_amount = 1  


def validate_levels(lvls):
    if sum(lvls) > 20:
        st.warning("The total levels of all classes must not exceed 20.")
    return sum(lvls) > 20

col1, col2 = st.columns(2)

class_names = {}

for i, level in enumerate(range(1,st.session_state.class_amount+1)):
    with col1:
        cls = st.selectbox(f"Select Class {i + 1}:", options=[cls for cls in class_options['options'] if cls not in class_names], key=f"class_{i}")
    with col2:
        lvl = st.number_input(f"Select Level for Class {i + 1}:", min_value=1, max_value=20, key=f"level_{i}")
    
    if cls in class_names:
        cls = cls + ' ' + str(i)
    class_names[cls] = lvl

validate_levels(class_names.values())


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
    with st.spinner("Please wait as we cook... This can take a minute"):
    
        if user_prompt:
            traits = utils.generateCharacterTraits(user_prompt, class_names)
            # flavour = utils.generateCharacterFlavour(user_prompt, traits.RACE)
            # features, ability_prof = utils.generateCharacterFeatures(user_prompt,traits)
            st.write(traits)
            # st.write(flavour)
            # st.write(features)
            

            # pdf_display, pdf_bytes = fill_pdf(
            #     total_level=sum(class_names.values()), 
            #     proficiencies=features.Skill_Prof+list(ability_prof), 
            #     traits=traits, 
            #     flavour=flavour, 
            #     features=features
            #     )
            # st.markdown(pdf_display, unsafe_allow_html=True)
            # st.download_button(
            #    label="Download Updated PDF",
            #    data=pdf_bytes,
            #    file_name="updated_form.pdf",
            #    mime="application/pdf"
            # )

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

