"""
COMP 163 - Project 3: Quest Chronicles
Main Game Module - Starter Code

Name: Bryce Joseph

AI Usage: No AI Use

This is the main game file that ties all modules together.
Demonstrates module integration and complete game flow.
"""

# Import all our custom modules
import character_manager
import inventory_system
import quest_handler
import combat_system
import game_data
from custom_exceptions import *

# ============================================================================
# GAME STATE
# ============================================================================

# Global variables for game data
current_character = None
all_quests = {}
all_items = {}
game_running = False

# ============================================================================
# MAIN MENU
# ============================================================================

def main_menu():
    """
    Display main menu and get player choice
    
    Options:
    1. New Game
    2. Load Game
    3. Exit
    
    Returns: Integer choice (1-3)
    """
    # TODO: Implement main menu display
    # Show options
    # Get user input
    # Validate input (1-3)
    # Return choice

    print("Options:\n1. New Game\n2. Load Game\n3. Exit")
    choice = int(input())
    return choice

def new_game():
    """
    Start a new game
    
    Prompts for:
    - Character name
    - Character class
    
    Creates character and starts game loop
    """
    global current_character
    
    # TODO: Implement new game creation
    # Get character name from user
    # Get character class from user
    # Try to create character with character_manager.create_character()
    # Handle InvalidCharacterClassError
    # Save character
    # Start game loop

    global game_running

    character_name = input("Character name: ")
    character_class = input("Character class: ")
    try:
        current_character = character_manager.create_character(character_name, character_class)
    except InvalidCharacterClassError:
        print("Error")
    character_manager.save_character(current_character)
    game_running = True

def load_game():
    """
    Load an existing saved game
    
    Shows list of saved characters
    Prompts user to select one
    """
    global current_character
    
    # TODO: Implement game loading
    # Get list of saved characters
    # Display them to user
    # Get user choice
    # Try to load character with character_manager.load_character()
    # Handle CharacterNotFoundError and SaveFileCorruptedError
    # Start game loop

    characters = character_manager.list_saved_characters()
    print(characters)
    choice = input()
    try:
        current_character = character_manager.load_character(choice)
    except (CharacterNotFoundError, SaveFileCorruptedError, InvalidSaveDataError):
        print("Error")
    game_loop()

# ============================================================================
# GAME LOOP
# ============================================================================

def game_loop():
    """
    Main game loop - shows game menu and processes actions
    """
    global game_running, current_character
    
    game_running = True
    
    # TODO: Implement game loop
    # While game_running:
    #   Display game menu
    #   Get player choice
    #   Execute chosen action
    #   Save game after each action

    while game_running:
        choice = game_menu()
        if choice == 1:
            view_character_stats()
        elif choice == 2:
            view_inventory()
        elif choice == 3:
            quest_menu()
        elif choice == 4:
            explore()
        elif choice == 5:
            shop()
        else:
            game_running = False
        save_game()

def game_menu():
    """
    Display game menu and get player choice
    
    Options:
    1. View Character Stats
    2. View Inventory
    3. Quest Menu
    4. Explore (Find Battles)
    5. Shop
    6. Save and Quit
    
    Returns: Integer choice (1-6)
    """
    # TODO: Implement game menu

    print("Options:\n1. View Character Stats\n2. View Inventory\n3. Quest Menu\n4. Explore (Find Battles)\n5. Shop\n6. Save and Quit")
    choice = int(input())
    return choice

# ============================================================================
# GAME ACTIONS
# ============================================================================

def view_character_stats():
    """Display character information"""
    global current_character
    
    # TODO: Implement stats display
    # Show: name, class, level, health, stats, gold, etc.
    # Use character_manager functions
    # Show quest progress using quest_handler

    for key in current_character:
        if key not in ["inventory", "active_quests", "completed_quests"]:
            print(f"{key}: {current_character[key]}")
        else:
            print(f"{key}: {', '.join(current_character[key])}")

def view_inventory():
    """Display and manage inventory"""
    global current_character, all_items
    
    # TODO: Implement inventory menu
    # Show current inventory
    # Options: Use item, Equip weapon/armor, Drop item
    # Handle exceptions from inventory_system

    item_id = input()
    item_data = all_items[item_id]
    print(current_character["inventory"])
    print("Options:\n1. Use item\n2. Equip weapon\n3. Equip armor\n4. Drop item")
    choice = int(input())
    try:
        if choice == 1:
            inventory_system.use_item(current_character, item_id, item_data)
        elif choice == 2:
            inventory_system.equip_weapon(current_character, item_id, item_data)
        elif choice == 3:
            inventory_system.equip_armor(current_character, item_id, item_data)
        else:
            inventory_system.use_item(current_character, item_id, item_data)
    except (ItemNotFoundError, InvalidItemTypeError):
        print("Error")

def quest_menu():
    """Quest management menu"""
    global current_character, all_quests
    
    # TODO: Implement quest menu
    # Show:
    #   1. View Active Quests
    #   2. View Available Quests
    #   3. View Completed Quests
    #   4. Accept Quest
    #   5. Abandon Quest
    #   6. Complete Quest (for testing)
    #   7. Back
    # Handle exceptions from quest_handler

    print("1. View Active Quests\n2. View Available Quests\n3. View Completed Quests\n4. Accept Quest\n5. Abandon Quest\n6. Complete Quest (for testing)\n7. Back")

def explore():
    """Find and fight random enemies"""
    global current_character
    
    # TODO: Implement exploration
    # Generate random enemy based on character level
    # Start combat with combat_system.SimpleBattle
    # Handle combat results (XP, gold, death)
    # Handle exceptions

    try:
        enemy = combat_system.get_random_enemy_for_level(current_character["level"])
        battle = combat_system.SimpleBattle(current_character, enemy)
        battle.start_battle()
    except (InvalidTargetError, CharacterDeadError):
        print("Error")

def shop():
    """Shop menu for buying/selling items"""
    global current_character, all_items
    
    # TODO: Implement shop
    # Show available items for purchase
    # Show current gold
    # Options: Buy item, Sell item, Back
    # Handle exceptions from inventory_system

    print("Available Items")
    for item_id in all_items:
        print(item_id)
    print()
    item_id = input()
    print(f"Current gold: {current_character['gold']}")
    print("Options:\n1. Buy item\n2. Sell item\n3. Back")
    choice = int(input())
    try:
        if choice == 1:
            inventory_system.purchase_item(current_character, item_id, all_items[item_id])
        elif choice == 2:
            inventory_system.sell_item(current_character, item_id, all_items[item_id])
        else:
            pass
    except (InsufficientResourcesError, InventoryFullError, ItemNotFoundError):
        print("Error")

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def save_game():
    """Save current game state"""
    global current_character
    
    # TODO: Implement save
    # Use character_manager.save_character()
    # Handle any file I/O exceptions

    character_manager.save_character(current_character)

def load_game_data():
    """Load all quest and item data from files"""
    global all_quests, all_items
    
    # TODO: Implement data loading
    # Try to load quests with game_data.load_quests()
    # Try to load items with game_data.load_items()
    # Handle MissingDataFileError, InvalidDataFormatError
    # If files missing, create defaults with game_data.create_default_data_files()

    try:
        all_quests = game_data.load_quests()
        all_items = game_data.load_items()
    except (MissingDataFileError, InvalidDataFormatError, CorruptedDataError):
        game_data.create_default_data_files()

def handle_character_death():
    """Handle character death"""
    global current_character, game_running
    
    # TODO: Implement death handling
    # Display death message
    # Offer: Revive (costs gold) or Quit
    # If revive: use character_manager.revive_character()
    # If quit: set game_running = False

    print(f"{current_character} is dead")
    decision = input("Offer: Revive (costs gold) or Quit")
    if decision == "revive":
        character_manager.revive_character(current_character)
    else:
        game_running = False

def display_welcome():
    """Display welcome message"""
    print("=" * 50)
    print("     QUEST CHRONICLES - A MODULAR RPG ADVENTURE")
    print("=" * 50)
    print("\nWelcome to Quest Chronicles!")
    print("Build your character, complete quests, and become a legend!")
    print()

# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    """Main game execution function"""
    
    # Display welcome message
    display_welcome()
    
    # Load game data
    try:
        load_game_data()
        print("Game data loaded successfully!")
    except MissingDataFileError:
        print("Creating default game data...")
        game_data.create_default_data_files()
        load_game_data()
    except InvalidDataFormatError as e:
        print(f"Error loading game data: {e}")
        print("Please check data files for errors.")
        return
    
    # Main menu loop
    while True:
        choice = main_menu()
        
        if choice == 1:
            new_game()
        elif choice == 2:
            load_game()
        elif choice == 3:
            print("\nThanks for playing Quest Chronicles!")
            break
        else:
            print("Invalid choice. Please select 1-3.")

if __name__ == "__main__":
    main()

