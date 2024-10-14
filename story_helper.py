import streamlit as st
from utils import generateResponse
import os
import pyperclip

st.header("DNDBot")

campaign_folders = [folder for folder in os.listdir("campaigns")]
display_campaigns = [foldername.capitalize() for foldername in campaign_folders]

st.write("Select a campaign to work with:")
selected_campaign = st.radio("Choose a campaign:", display_campaigns)

if selected_campaign:
    selected_folder = f"campaigns/{selected_campaign.lower()}"
    files = [f for f in os.listdir(selected_folder) if os.path.isfile(os.path.join(selected_folder, f))]
    display_files = [os.path.splitext(file)[0].replace("_", " ").capitalize() for file in files]
    
    if files:
        selected_files = st.multiselect("Choose files to work with:", display_files)
    else:
        st.write(f"No files found in the {selected_campaign} campaign folder.")
user_prompt = st.text_area("Enter your prompt:", "", max_chars=None, key="user_prompt", help="Type your prompt here. This will query the AI")


generate_button = st.button("Generate Response", use_container_width=True)
if "generate_button" not in st.session_state:
    st.session_state["generate_button"] = False
if "genbutt_counter" not in st.session_state:
    st.session_state["genbutt_counter"] = 0


if generate_button:
    st.session_state["generate_button"] = not st.session_state["generate_button"]
    st.session_state["genbutt_counter"] += 1
    if st.session_state["genbutt_counter"] > 1:
        st.session_state["genbutt_counter"] -= 1
        st.session_state["generate_button"] = not st.session_state["generate_button"]
    
    if user_prompt:
        selected_file_paths = [os.path.join(selected_folder, file) for file in files if os.path.splitext(file)[0].replace("_", " ").capitalize() in selected_files] 
        if 'generated_response' not in st.session_state:
            st.session_state.generated_response = ""
        st.session_state.generated_response = generateResponse(selected_file_paths, user_prompt)
    else:
        st.warning("You must enter a prompt!")

if st.session_state["generate_button"] and user_prompt:
    final_response = st.text_area("Generated Response:", value=st.session_state.generated_response, height=300, key="final_response")
    
    col1, col2 = st.columns(2)
    with col1:
        save_button = st.button("Save text", use_container_width=True, help="The final edited response will save in plans file")
    with col2:
        copy_button = st.button("Copy to clipboard", key="copy_button", use_container_width=True)

    if save_button:
        plans_file_path = next((os.path.join(selected_folder, f) for f in os.listdir(selected_folder) if "plans" in f.lower()), None)
        try:
            with open(plans_file_path, "a") as plans_file:
                plans_file.write(f"\n\n--- Generated Entry ---\n{final_response}\n")
            st.success(f"Text successfully appended to Plans.txt in the {selected_campaign} folder.")
        except IOError:
            st.error(f"An error occurred while trying to save to Plans.txt in the {selected_campaign} folder.")

    if copy_button:
        pyperclip.copy(final_response)
        st.success("Text copied to clipboard!")