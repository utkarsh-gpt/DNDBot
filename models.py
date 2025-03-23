from pydantic import BaseModel, Field, field_validator, ValidationError, conint
from typing import Optional, List, Literal, Dict, Union, ClassVar
import mongoQuery


ability_examples = """
# Human Fighter
ability_scores = {
    'STR': 16,
    'DEX': 14,
    'CON': 15,
    'INT': 10,
    'WIS': 12,
    'CHA': 8
}

# Elf Wizard
ability_scores = {
    'STR': 8,
    'DEX': 16,
    'CON': 12,
    'INT': 17,
    'WIS': 14,
    'CHA': 10
}

# Dwarf Cleric
ability_scores = {
    'STR': 14,
    'DEX': 8,
    'CON': 16,
    'INT': 10,
    'WIS': 15,
    'CHA': 12
}

# Halfling Rogue
ability_scores = {
    'STR': 10,
    'DEX': 17,
    'CON': 14,
    'INT': 13,
    'WIS': 12,
    'CHA': 11
}

# Half-Orc Barbarian
ability_scores = {
    'STR': 17,
    'DEX': 13,
    'CON': 16,
    'INT': 8,
    'WIS': 10,
    'CHA': 12
}"""

class CharacterFlavour(BaseModel):
    CharacterName: str = Field(description="The name of the character")
    GENDER: str = Field(description="The gender of the character")
    AGE: str = Field(description="The age of the character")
    SIZE: str = Field(description="The size of the character dependant on race")
    HEIGHT: str = Field(description="The height of the character")
    WEIGHT: str = Field(description="The weight of the character")
    ALIGNMENT: str = Field(description="The allignment of the character")
    FAITH: Optional[str] = Field(description="Any faith the character follows")
    PersonalityTraits: str = Field(description="All the personality traits of the character")
    Ideals: str = Field(description="All the character's ideals")
    Bonds: Optional[str] = Field(description="Any bonds the character has")
    Flaws: str = Field(description="Any flaws the character has")
    Backstory: str = Field(description="The backstory of the character")
    SKIN: str = Field(description="The skin color of the character")
    EYES: str = Field(description="The eye color of the character")
    HAIR: str = Field(description="The hair color of the character")
    Speed: str = Field(description="Walking speed derived from the race")
    # AlliesOrganizations: Optional[str] = Field(description="Any allied organization the character is affiliated to.")

# classes = mongoQuery.fetchDisplayInfo('classes')
races = mongoQuery.fetchDisplayInfo('races')
backgrounds = mongoQuery.fetchDisplayInfo('backgrounds')

class CharacterTraits(BaseModel):
    # CLASS_LEVEL: Dict[str,int]= Field(description="The classes and its level in the format, {'Class1':'Class1_level','Class2':'Class2_level',...} .")
    # SUBCLASS: Dict[str,str] = Field(description="The classes and a picked subclasses in the format, {'Class1':'Subclass1','Class2':'Subclass2',...} . If no subclass is provided for a class have the subclass value be None")
    CLASS_LEVEL: str = Field(description="The classes, subclass and levels of the character in the format, [['Class1','Level1','Subclass1'],['Class2','Level2','Subclass2']].")
    RACE: Literal[tuple(races['options'])] = Field(description="The race of the character.")
    BACKGROUND: Literal[tuple(backgrounds['options'])] = Field(description="The background of the character. This is like previous occupation/title")

class AbilityScores(BaseModel):
    STR: int
    DEX: int
    CON: int
    INT: int
    WIS: int
    CHA: int

# class CharacterPayload(BaseModel):
#         Ability_Scores: AbilityScores = Field(description="The ability scores of a character. Make sure they are balanced and all stats do not have high numbers and make sure multiclass requirements are met when two or more classes are picked. 10 in the stat is considered baseline, 15 is considered an expertise and 8 is being terrible at it.")#, examples=ability_examples)  
#         Init: str = Field(description="Any and all initiative bouses from class, background and race. This is only considering the bonuses so add a + or - sign to the number. If no number is found keep it 0")
#         HD: str = Field(description="The hit dice of any one of the classes")
#         ProficienciesLang: str = Field(description="Any and all the language proficiencies from background and race")
#         FeaturesTraits: str = Field(description="All the class features and race features. Seperate the features by source (i.e. class section and race section. For each feature provide their descriptions as well.")
#         GP: str = Field(description="An amount of gold pieces, a currency for the game. Consider that 1000 GP implies wealthy status")
#         Equipment: dict = Field(description="All the equipment as keys and their quantities as values")
       
def createPayload(prof_choices, count):
     
    class CharacterFreature(BaseModel):
        Ability_Scores: AbilityScores = Field(description="The ability scores of a character. Make sure they are balanced and all stats do not have high numbers and make sure multiclass requirements are met when two or more classes are picked. 10 in the stat is considered baseline, 15 is considered an expertise and 8 is being terrible at it.")#, examples=ability_examples)    
        # Skill_Prof: int = Field(description="This is the total count skills of the startingProficiencies.")
        Skill_Prof: List[Literal[prof_choices]] = Field(description=f"Choose excatly {count} skill proficiencies for the character")
        # Passives: List[str] = Field(description="Any the passive perception, insight, investigation bonuses from class, background and race. This is only considering the bonuses so add a + or - sign to the number. If no number is found keep it 0")
        # AdditionalSenses: str = Field(description="")
        Init: str = Field(description="Any and all initiative bouses from class, background and race. This is only considering the bonuses so add a + or - sign to the number. If no number is found keep it 0")
        # AC: str = Field(description="Any and all AC or armor class bouses from class, background and race. This is only considering the bonuses so add a + or - sign to the number. If no number is found keep it 0")
        # Speed: str = Field(description="Walking speed bonuses derived from the class features")
        # Total: str = Field(description="The level of the character")
        HD: str = Field(description="The hit dice of any one of the classes")
        ProficienciesLang: str = Field(description="Any and all the language proficiencies from background and race")
        FeaturesTraits: str = Field(description="All the class features and race features. Seperate the features by source (i.e. class section and race section. For each feature provide their descriptions as well.")
        GP: str = Field(description="An amount of gold pieces, a currency for the game. Consider that 1000 GP implies wealthy status")
        Equipment: dict = Field(description="All the equipment as keys and their quantities as values")
        # AdditionalNotes1: str = Field(description="")
        # AdditionalNotes2: Optional[str] = None
    return CharacterFreature