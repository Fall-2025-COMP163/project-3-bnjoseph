"""
COMP 163 - Project 3: Quest Chronicles
Game Data Module - Starter Code

Name: Bryce Joseph

AI Usage: No AI Use

This module handles loading and validating game data from text files.
"""

import os
from custom_exceptions import (
    InvalidDataFormatError,
    MissingDataFileError,
    CorruptedDataError
)

# ============================================================================
# DATA LOADING FUNCTIONS
# ============================================================================

def load_quests(filename="data/quests.txt"):
    """
    Load quest data from file
    
    Expected format per quest (separated by blank lines):
    QUEST_ID: unique_quest_name
    TITLE: Quest Display Title
    DESCRIPTION: Quest description text
    REWARD_XP: 100
    REWARD_GOLD: 50
    REQUIRED_LEVEL: 1
    PREREQUISITE: previous_quest_id (or NONE)
    
    Returns: Dictionary of quests {quest_id: quest_data_dict}
    Raises: MissingDataFileError, InvalidDataFormatError, CorruptedDataError
    """
    # TODO: Implement this function
    # Must handle:
    # - FileNotFoundError → raise MissingDataFileError
    # - Invalid format → raise InvalidDataFormatError
    # - Corrupted/unreadable data → raise CorruptedDataError

    #if filename != "data/quests.txt":
        #filename = os.path.abspath(filename)
    #else:
        #filename = "/Users/brycejoseph/Downloads/project-3-bnjoseph-main/" + filename
    filename = os.path.abspath(filename)
    if not os.path.isfile(filename):
        raise MissingDataFileError
    else:
        pass
    try:
        file = open(filename, "r")
    except:
        raise CorruptedDataError
    lines = file.readlines()
    dictionary = parse_quest_block(lines)
    for diction in list(dictionary.values()):
        validate_quest_data(diction)
    file.close()
    return dictionary

def load_items(filename="data/items.txt"):
    """
    Load item data from file
    
    Expected format per item (separated by blank lines):
    ITEM_ID: unique_item_name
    NAME: Item Display Name
    TYPE: weapon|armor|consumable
    EFFECT: stat_name:value (e.g., strength:5 or health:20)
    COST: 100
    DESCRIPTION: Item description
    
    Returns: Dictionary of items {item_id: item_data_dict}
    Raises: MissingDataFileError, InvalidDataFormatError, CorruptedDataError
    """
    # TODO: Implement this function
    # Must handle same exceptions as load_quests

    #if filename != "data/items.txt":
        #filename = os.path.abspath(filename)
    #else:
        #filename = "/Users/brycejoseph/Downloads/project-3-bnjoseph-main/" + filename
    filename = os.path.abspath(filename)
    if not os.path.isfile(filename):
        raise MissingDataFileError
    else:
        pass
    try:
        file = open(filename, "r")
    except:
        raise CorruptedDataError
    lines = file.readlines()
    file.close()
    dictionary = parse_item_block(lines)
    for diction in list(dictionary.values()):
        validate_item_data(diction)
    return dictionary

def validate_quest_data(quest_dict):
    """
    Validate that quest dictionary has all required fields
    
    Required fields: quest_id, title, description, reward_xp, 
                    reward_gold, required_level, prerequisite
    
    Returns: True if valid
    Raises: InvalidDataFormatError if missing required fields
    """
    # TODO: Implement validation
    # Check that all required keys exist
    # Check that numeric values are actually numbers

    fields = ["quest_id", "title", "description", "reward_xp",
              "reward_gold", "required_level", "prerequisite"]
    for field in fields:
        if field not in quest_dict:
            raise InvalidDataFormatError
    for field in fields[3:6]:
        if not isinstance(quest_dict[field], int):
            raise InvalidDataFormatError
    return True

def validate_item_data(item_dict):
    """
    Validate that item dictionary has all required fields
    
    Required fields: item_id, name, type, effect, cost, description
    Valid types: weapon, armor, consumable
    
    Returns: True if valid
    Raises: InvalidDataFormatError if missing required fields or invalid type
    """
    # TODO: Implement validation

    fields = ["item_id", "name", "type", "effect", "cost", "description"]
    for field in fields:
        if field not in item_dict:
            raise InvalidDataFormatError
    if not isinstance(item_dict[fields[-2]], int):
        raise InvalidDataFormatError
    if item_dict["type"] not in ["weapon", "armor", "consumable"]:
        raise InvalidDataFormatError
    return True

def create_default_data_files():
    """
    Create default data files if they don't exist
    This helps with initial setup and testing
    """
    # TODO: Implement this function
    # Create data/ directory if it doesn't exist
    # Create default quests.txt and items.txt files
    # Handle any file permission errors appropriately

    if not os.path.isdir("data/"):
        os.mkdir("data/")
    if not os.path.isfile("data/quests.txt"):
        with open("data/quests.txt", "w") as file:
            pass
        file.close()
    if not os.path.isfile("data/items.txt"):
        with open("data/items.txt", "w") as file:
            pass
        file.close()

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def parse_quest_block(lines):
    """
    Parse a block of lines into a quest dictionary
    
    Args:
        lines: List of strings representing one quest
    
    Returns: Dictionary with quest data
    Raises: InvalidDataFormatError if parsing fails
    """
    # TODO: Implement parsing logic
    # Split each line on ": " to get key-value pairs
    # Convert numeric strings to integers
    # Handle parsing errors gracefully

    try:
        dictionary = {}
        quest_id = ""
        for line in lines:
            if line == "\n":
                continue
            else:
                pass
            key, val = line.split(": ")
            key = key.lower()
            val = val.replace("\n", "")
            if key == "quest_id":
                quest_id = val
                dictionary[quest_id] = {"quest_id" : quest_id}
            else:
                if key in ["reward_xp", "reward_gold", "required_level"]:
                    val = int(val)
                dictionary[quest_id][key] = val
        return dictionary
    except:
        raise InvalidDataFormatError

def parse_item_block(lines):
    """
    Parse a block of lines into an item dictionary
    
    Args:
        lines: List of strings representing one item
    
    Returns: Dictionary with item data
    Raises: InvalidDataFormatError if parsing fails
    """
    # TODO: Implement parsing logic

    dictionary = {}
    item_id = ""
    for line in lines:
        if line == "\n":
            continue
        else:
            pass
        key, val = line.split(": ")
        key = key.lower()
        val = val.replace("\n", "")
        if key == "item_id":
            item_id = val
            dictionary[item_id] = {"item_id": item_id}
        else:
            if key == "cost":
                val = int(val)
            dictionary[item_id][key] = val
    return dictionary

# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    print("=== GAME DATA MODULE TEST ===")
    
    # Test creating default files
    # create_default_data_files()
    
    # Test loading quests
    # try:
    #     quests = load_quests()
    #     print(f"Loaded {len(quests)} quests")
    # except MissingDataFileError:
    #     print("Quest file not found")
    # except InvalidDataFormatError as e:
    #     print(f"Invalid quest format: {e}")
    
    # Test loading items
    # try:
    #     items = load_items()
    #     print(f"Loaded {len(items)} items")
    # except MissingDataFileError:
    #     print("Item file not found")
    # except InvalidDataFormatError as e:
    #     print(f"Invalid item format: {e}")

