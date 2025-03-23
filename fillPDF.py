# from pdfrw import PdfReader, PdfWriter, IndirectPdfDict, PdfDict, PdfName
from pypdf import PdfReader, PdfWriter
from pydantic import BaseModel, Field
from typing import Optional
from pypdf import PdfReader, PdfWriter
import base64
import io


def calculate_ability_modifier(score):
    return (score - 10) // 2

def calculate_proficiency(level):
    if level < 1:
        return 0
    return max(1, (2 + (level - 1) // 4))  # Rounded down

def check_box(pdf, field_name):
    fields = pdf.get_fields()
    return fields[field_name] == '/Yes'

def display_classes(classes):
    out = ''
    for item in eval(classes):
        if isinstance(item,list):
            out += " ".join(item[2:] + item[:2])
        elif isinstance(item, str):
            out = eval(classes)[2:] + eval(classes)[:2]
            return out
        out += "/"
    return out

def create_features(text):
    # Calculate the length of the text
    text_length = len(text)
    
    # Calculate size of each section (rounded up to ensure all text is included)
    section_size = -(-text_length // 3)  # Ceiling division
    
    # Split into 3 sections
    section1 = text[:section_size]
    section2 = text[section_size:section_size*2]
    section3 = text[section_size*2:]
    
    return [section1, section2, section3]

def fill_pdf(total_level, proficiencies, features, traits, flavour):
    # Read the PDF
    pdf = PdfReader("fillable.pdf")
    ability_scores = features.Ability_Scores.__dict__

    output_fields = {}
    ability_fields = {
        'STR': 'STRmod',
        'DEX': 'DEXmod ',
        'CON': 'CONmod',
        'INT': 'INTmod',
        'WIS': 'WISmod',
        'CHA': 'CHamod'
    }
    
    saving_throw_fields = {
        'ST Strength': 'STR',
        'ST Dexterity': 'DEX',
        'ST Constitution': 'CON',
        'ST Intelligence': 'INT',
        'ST Wisdom': 'WIS',
        'ST Charisma': 'CHA'
    }
    
    skill_fields = [
        ('Acrobatics', 'DEX', 'acrobatics'),
        ('Animal', 'WIS', 'animal handling'),
        ('Arcana', 'INT', 'arcana'),
        ('Athletics', 'STR', 'athletics'),
        ('Deception', 'CHA', 'deception'),
        ('History', 'INT', 'history'),
        ('Insight', 'WIS', 'insight'),
        ('Intimidation', 'CHA', 'intimidation'),
        ('Investigation', 'INT', 'investigation'),
        ('Medicine', 'WIS', 'medicine'),
        ('Nature', 'INT', 'nature'),
        ('Perception', 'WIS', 'perception'),
        ('Performance', 'CHA', 'performance'),
        ('Persuasion', 'CHA', 'persuasion'),
        ('Religion', 'INT', 'religion'),
        ('SleightofHand', 'DEX', 'slight of hand'),
        ('Stealth ', 'DEX', 'stealth'),
        ('Survival', 'WIS','survival')
        ]
    

    proficiency_bonus = calculate_proficiency(total_level)
    output_fields.update({'ProfBonus':f'{proficiency_bonus:+d}'})

    for ability, ability_mod in ability_fields.items():
        score = ability_scores.get(ability, 10)  # description to 10 if not provided
        modifier = calculate_ability_modifier(score)
        output_fields.update({ability: f'{modifier:+d}'})
        output_fields.update({ability_mod: f'{score}'})
        
    for st_field, ability in saving_throw_fields.items():
        score = ability_scores.get(ability, 10)  # description to 10 if not provided
        modifier = calculate_ability_modifier(score)
        
        if ability.lower() in proficiencies:
            output_fields.update({f'{saving_throw_fields[st_field].capitalize()}Prof':'P'})
            modifier += proficiency_bonus
            
        output_fields.update({st_field: f'{modifier:+d}'})
        
    for skill, ability, skill_id in skill_fields:
        score = ability_scores.get(ability, 10)  # description to 10 if not provided
        modifier = calculate_ability_modifier(score)
        
        if skill_id in proficiencies:
            output_fields.update({f'{skill.capitalize()}Prof':'P'})
            modifier += proficiency_bonus
            
        output_fields.update({skill: f'{modifier:+d}'})
    
    features_column = create_features(features.FeaturesTraits)

    payload = {
        'CLASS  LEVEL': display_classes(traits.CLASS_LEVEL),
        'CLASS  LEVEL2': display_classes(traits.CLASS_LEVEL),
        'AC': str(10 + ability_scores['DEX']),
        'Init': str(10 + int(features.Init) + ability_scores['DEX']),
        'CharacterName2': flavour.CharacterName,
        'CharacterName4': flavour.CharacterName,
        'RACE2': traits.RACE,
        'BACKGROUND2': traits.BACKGROUND,
        'Total': total_level,
        'FeaturesTraits1': features_column[0],
        'FeaturesTraits2': features_column[1],
        'FeaturesTraits3': features_column[2],
    }

    output_fields.update(flavour.__dict__)
    output_fields.update(features.__dict__)
    output_fields.update(payload)

    writer = PdfWriter()
    writer.clone_reader_document_root(pdf)

    writer.update_page_form_field_values(
        page= None,
        fields=output_fields,
        auto_regenerate=False
    )
    
    output_buffer = io.BytesIO()
    writer.write(output_buffer)
    output_buffer.seek(0)
    pdf_bytes = output_buffer.getvalue()

    base64_pdf = base64.b64encode(pdf_bytes).decode('utf-8')
    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="700" height="800" type="application/pdf"></iframe>'
    return pdf_display, pdf_bytes

    # with open("output.pdf", "wb") as output_stream:
    #     writer.write(output_stream)

# fill_pdf(pdf, 5, ['Arcana', 'ST Dexterity'])

payload = {
    'CharacterName': '',
    'CLASS  LEVEL': '',
    'PLAYER NAME': '',
    'RACE': '',
    'BACKGROUND': '',
    'EXPERIENCE POINTS': '',
    'Passive1': '',
    'Passive2': '',
    'Passive3': '',
    'AdditionalSenses': '',
    'Init': '',
    'AC': '',
    'AbilitySaveDC': None,
    'AbilitySaveScore1': None,
    'AbilitySaveScore2': None,
    'AbilitySaveDC2': None,
    'Speed': '',
    'MaxHP': '',
    'CurrentHP': None,
    'TempHP': '',
    'Total': '',
    'HD': None,
    'ProficienciesLang': '',
    'Actions1': '',
    'Actions2': None,
    'Wpn Name': '',
    'Wpn1 AtkBonus': '',
    'Wpn1 Damage': '',
    'Wpn Notes 1': '',
    'Wpn Name 2': None,
    'Wpn2 AtkBonus ': None,
    'Wpn2 Damage ': None,
    'Wpn Notes 2': None,
    'Wpn Name 3': None,
    'Wpn3 AtkBonus  ': None,
    'Wpn3 Damage ': None,
    'Wpn Notes 3': None,
    'Wpn Name 4': None,
    'Wpn4 AtkBonus': None,
    'Wpn4 Damage': None,
    'Wpn Notes 4': None,
    'Wpn Name 5': None,
    'Wpn5 AtkBonus': None,
    'Wpn5 Damage': None,
    'Wpn Notes 5': None,
    'Wpn Name 6': None,
    'Wpn6 AtkBonus': None,
    'Wpn6 Damage': None,
    'Wpn Notes 6': None,
    'CharacterName2': '',
    'CLASS  LEVEL2': '',
    'RACE2': '',
    'BACKGROUND2': '',
    'FeaturesTraits1': '',
    'FeaturesTraits2': '',
    'FeaturesTraits3': '',
    'CP': '',
    'SP': '',
    'EP': '',
    'GP': '',
    'PP': '',
    'Weight Carried': '',
    'Encumbered': '',
    'PushDragLift': '',
    'Eq Name0': None,
    'Eq Qty0': None,
    'Eq Weight0': None,
    'Eq Name1': None,
    'Eq Qty1': None,
    'Eq Weight1': None,
    'Eq Name2': None,
    'Eq Qty2': None,
    'Eq Weight2': None,
    'Eq Name3': None,
    'Eq Qty3': None,
    'Eq Weight3': None,
    'Eq Name4': None,
    'Eq Qty4': None,
    'Eq Weight4': None,
    'CharacterName4': '',
    'GENDER': '',
    'AGE': '',
    'SIZE': 'Medium',
    'HEIGHT': '',
    'WEIGHT': '',
    'ALIGNMENT': '',
    'FAITH': '',
    'SKIN': '',
    'EYES': '',
    'HAIR': '',
    'AlliesOrganizations': '',
    'PersonalityTraits ': '',
    'Ideals': '',
    'Bonds': '',
    'Appearance': '',
    'Flaws': '',
    'Backstory': '',
    'AdditionalNotes1': '',
    'AdditionalNotes2': None
}