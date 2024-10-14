# from pdfrw import PdfReader, PdfWriter, IndirectPdfDict, PdfDict, PdfName
from pypdf import PdfReader, PdfWriter

# Read the PDF
pdf = PdfReader("5E_CharacterSheet_Fillable.pdf")

def calculate_ability_modifier(score):
    return (score - 10) // 2

def calculate_proficiency(level):
    if level < 1:
        return 0
    return max(1, (2 + (level - 1) // 4))  # Rounded down

def fill_pdf(pdf, ability_scores, total_level, proficiencies):
    output_fields = {}

    ability_fields = {
        'STRmod': 'STR',
        'DEXmod ': 'DEX',
        'CONmod': 'CON',
        'INTmod': 'INT',
        'WISmod': 'WIS',
        'CHamod': 'CHA'
    }
    
    saving_throw_fields = {
        'ST Strength': 'STR',
        'ST Dexterity': 'DEX',
        'ST Constitution': 'CON',
        'ST Intelligence': 'INT',
        'ST Wisdom': 'WIS',
        'ST Charisma': 'CHA'
    }
    
    skill_fields = {
        'Acrobatics': 'DEX',
        'Animal': 'WIS',
        'Arcana': 'INT',
        'Athletics': 'STR',
        'Deception ': 'CHA',
        'History ': 'INT',
        'Insight': 'WIS',
        'Intimidation': 'CHA',
        'Investigation ': 'INT',
        'Medicine': 'WIS',
        'Nature': 'INT',
        'Perception ': 'WIS',
        'Performance': 'CHA',
        'Persuasion': 'CHA',
        'Religion': 'INT',
        'SleightofHand': 'DEX',
        'Stealth ': 'DEX',
        'Survival': 'WIS'
    }

    checkbox_dict = {
        'ST Strength': 'Check Box 11',
        'ST Dexterity': 'Check Box 18',
        'ST Constitution': 'Check Box 19',
        'ST Intelligence': 'Check Box 20',
        'ST Wisdom': 'Check Box 21',
        'ST Charisma': 'Check Box 22',
        'Acrobatics': 'Check Box 23',
        'Animal': 'Check Box 24',
        'Arcana': 'Check Box 25',
        'Athletics': 'Check Box 26',
        'Deception ': 'Check Box 27',
        'History ': 'Check Box 28',
        'Insight': 'Check Box 29',
        'Intimidation': 'Check Box 30',
        'Investigation ': 'Check Box 31',
        'Medicine': 'Check Box 32',
        'Nature': 'Check Box 33',
        'Perception ': 'Check Box 34',
        'Performance': 'Check Box 35',
        'Persuasion': 'Check Box 36',
        'Religion': 'Check Box 37',
        'SleightofHand': 'Check Box 38',
        'Stealth ': 'Check Box 39',
        'Survival': 'Check Box 40'
    }

    proficiency_bonus = calculate_proficiency(total_level)

    for abbr, ability in ability_fields.items():
        score = ability_scores.get(ability, 10)  # Default to 10 if not provided
        modifier = calculate_ability_modifier(score)
        output_fields.update({f'{abbr}': f'{modifier:+d}'})
        output_fields.update({ability: f'{score}'})
        
    for st_field, ability in saving_throw_fields.items():
        score = ability_scores.get(ability, 10)  # Default to 10 if not provided
        modifier = calculate_ability_modifier(score)
        
        if st_field in proficiencies:
            output_fields.update({checkbox_dict[st_field]:'/Yes'})
            modifier += proficiency_bonus
            
        output_fields.update({st_field: f'{modifier:+d}'})
        
    for skill, ability in skill_fields.items():
        score = ability_scores.get(ability, 10)  # Default to 10 if not provided
        modifier = calculate_ability_modifier(score)
        
        if skill in proficiencies:
            output_fields.update({checkbox_dict[skill]:'/Yes'})
            modifier += proficiency_bonus
            
        output_fields.update({skill: f'{modifier:+d}'})
    
    writer = PdfWriter()
    writer.clone_reader_document_root(pdf)

    writer.update_page_form_field_values(
        page= None,
        fields=output_fields,
        auto_regenerate=False
    )
    with open("output.pdf", "wb") as output_stream:
        writer.write(output_stream)

def check_box(field_name):
    fields = pdf.get_fields()
    return fields[field_name] == '/Yes'

ability_scores = {
    'STR': 15,
    'DEX': 12,
    'CON': 14,
    'INT': 10,
    'WIS': 13,
    'CHA': 8
}
fill_pdf(pdf, ability_scores, 5)
