"""
COMP 163 - Project 3: Quest Chronicles
Combat System Module - Starter Code

Name: Bryce Joseph

AI Usage: No AI Use

Handles combat mechanics
"""

from custom_exceptions import (
    InvalidTargetError,
    CombatNotActiveError,
    CharacterDeadError,
    AbilityOnCooldownError
)
#random imported for use
import random

# ============================================================================
# ENEMY DEFINITIONS
# ============================================================================

def create_enemy(enemy_type):
    """
    Create an enemy based on type
    
    Example enemy types and stats:
    - goblin: health=50, strength=8, magic=2, xp_reward=25, gold_reward=10
    - orc: health=80, strength=12, magic=5, xp_reward=50, gold_reward=25
    - dragon: health=200, strength=25, magic=15, xp_reward=200, gold_reward=100
    
    Returns: Enemy dictionary
    Raises: InvalidTargetError if enemy_type not recognized
    """
    # TODO: Implement enemy creation
    # Return dictionary with: name, health, max_health, strength, magic, xp_reward, gold_reward

    types = ["goblin", "orc", "dragon"]
    if enemy_type not in types:
        raise InvalidTargetError
    else:
        pass
    dictionary = {"name": enemy_type}
    if enemy_type == "goblin":
        dictionary["health"] = 50
        dictionary["max_health"] = 50
        dictionary["strength"] = 8
        dictionary["magic"] = 2
        dictionary["xp_reward"] = 25
        dictionary["gold_reward"] = 10
    elif enemy_type == "orc":
        dictionary["health"] = 80
        dictionary["max_health"] = 80
        dictionary["strength"] = 12
        dictionary["magic"] = 5
        dictionary["xp_reward"] = 50
        dictionary["gold_reward"] = 25
    else:
        dictionary["health"] = 200
        dictionary["max_health"] = 200
        dictionary["strength"] = 25
        dictionary["magic"] = 15
        dictionary["xp_reward"] = 200
        dictionary["gold_reward"] = 100
    dictionary["name"] = dictionary["name"].capitalize()
    return dictionary

def get_random_enemy_for_level(character_level):
    """
    Get an appropriate enemy for character's level
    
    Level 1-2: Goblins
    Level 3-5: Orcs
    Level 6+: Dragons
    
    Returns: Enemy dictionary
    """
    # TODO: Implement level-appropriate enemy selection
    # Use if/elif/else to select enemy type
    # Call create_enemy with appropriate type

    if 1 <= character_level <= 2:
        return create_enemy("goblin")
    elif 3 <= character_level <= 5:
        return create_enemy("orc")
    else:
        return create_enemy("dragon")

# ============================================================================
# COMBAT SYSTEM
# ============================================================================

class SimpleBattle:
    """
    Simple turn-based combat system
    
    Manages combat between character and enemy
    """
    
    def __init__(self, character, enemy):
        """Initialize battle with character and enemy"""
        # TODO: Implement initialization
        # Store character and enemy
        # Set combat_active flag
        # Initialize turn counter

        self.character = character
        self.enemy = enemy
        self.combat_active = False
        self.turn_counter = 0
    
    def start_battle(self):
        """
        Start the combat loop
        
        Returns: Dictionary with battle results:
                {'winner': 'player'|'enemy', 'xp_gained': int, 'gold_gained': int}
        
        Raises: CharacterDeadError if character is already dead
        """
        # TODO: Implement battle loop
        # Check character isn't dead
        # Loop until someone dies
        # Award XP and gold if player wins

        self.combat_active = True
        if self.character["health"] <= 0:
            raise CharacterDeadError
        initial_gold = self.character["gold"]
        while self.check_battle_end() is not None:
            self.turn_counter += 1
            self.player_turn()
            self.enemy_turn()
        results = {"winner": self.check_battle_end(), "xp_gained": self.character["experience"],
                   "gold_gained": self.character["gold"] - initial_gold}
        self.combat_active = False
        return results
    
    def player_turn(self):
        """
        Handle player's turn
        
        Displays options:
        1. Basic Attack
        2. Special Ability (if available)
        3. Try to Run
        
        Raises: CombatNotActiveError if called outside of battle
        """
        # TODO: Implement player turn
        # Check combat is active
        # Display options
        # Get player choice
        # Execute chosen action

        if not self.combat_active:
            raise CombatNotActiveError
        damage = self.calculate_damage(self.character, self.enemy)
        self.apply_damage(self.enemy, damage)
    
    def enemy_turn(self):
        """
        Handle enemy's turn - simple AI
        
        Enemy always attacks
        
        Raises: CombatNotActiveError if called outside of battle
        """
        # TODO: Implement enemy turn
        # Check combat is active
        # Calculate damage
        # Apply to character

        if not self.combat_active:
            raise CombatNotActiveError
        damage = self.calculate_damage(self.enemy, self.character)
        self.apply_damage(self.character, damage)
    
    def calculate_damage(self, attacker, defender):
        """
        Calculate damage from attack
        
        Damage formula: attacker['strength'] - (defender['strength'] // 4)
        Minimum damage: 1
        
        Returns: Integer damage amount
        """
        # TODO: Implement damage calculation

        damage = attacker['strength'] - (defender['strength'] // 4)
        if damage < 1:
            damage = 1
        return damage
    
    def apply_damage(self, target, damage):
        """
        Apply damage to a character or enemy
        
        Reduces health, prevents negative health
        """
        # TODO: Implement damage application

        target["health"] -= damage
        if target["health"] < 0:
            target["health"] = 0
    
    def check_battle_end(self):
        """
        Check if battle is over
        
        Returns: 'player' if enemy dead, 'enemy' if character dead, None if ongoing
        """
        # TODO: Implement battle end check

        if self.enemy["health"] <= 0:
            return "player"
        elif self.character["health"] <= 0:
            return "enemy"
        else:
            return None
    
    def attempt_escape(self):
        """
        Try to escape from battle
        
        50% success chance
        
        Returns: True if escaped, False if failed
        """
        # TODO: Implement escape attempt
        # Use random number or simple calculation
        # If successful, set combat_active to False

        if random.randint(1, 2) == 1:
            return True
        else:
            return False

# ============================================================================
# SPECIAL ABILITIES
# ============================================================================

def use_special_ability(character, enemy):
    """
    Use character's class-specific special ability
    
    Example abilities by class:
    - Warrior: Power Strike (2x strength damage)
    - Mage: Fireball (2x magic damage)
    - Rogue: Critical Strike (3x strength damage, 50% chance)
    - Cleric: Heal (restore 30 health)
    
    Returns: String describing what happened
    Raises: AbilityOnCooldownError if ability was used recently
    """
    # TODO: Implement special abilities
    # Check character class
    # Execute appropriate ability
    # Track cooldowns (optional advanced feature)

    if character["class"] == "Warrior":
        warrior_power_strike(character, enemy)
    elif character["class"] == "Mage":
        mage_fireball(character, enemy)
    elif character["class"] == "Rogue":
        rogue_critical_strike(character, enemy)
    else:
        cleric_heal(character)

def warrior_power_strike(character, enemy):
    """Warrior special ability"""
    # TODO: Implement power strike
    # Double strength damage

    damage = 2 * character['strength'] - (enemy['strength'] // 4)
    if damage < 1:
        damage = 1
    enemy["health"] -= damage
    if enemy["health"] < 0:
        enemy["health"] = 0

def mage_fireball(character, enemy):
    """Mage special ability"""
    # TODO: Implement fireball
    # Double magic damage

    damage = 2 * character['magic'] - (enemy['magic'] // 4)
    if damage < 1:
        damage = 1
    enemy["health"] -= damage
    if enemy["health"] < 0:
        enemy["health"] = 0

def rogue_critical_strike(character, enemy):
    """Rogue special ability"""
    # TODO: Implement critical strike
    # 50% chance for triple damage

    if random.randint(1,2) == 1:
        damage = character['strength'] - (enemy['strength'] // 4)
    else:
        damage = 3 * character['strength'] - (enemy['strength'] // 4)
    if damage < 1:
        damage = 1
    enemy["health"] -= damage
    if enemy["health"] < 0:
        enemy["health"] = 0

def cleric_heal(character):
    """Cleric special ability"""
    # TODO: Implement healing
    # Restore 30 HP (not exceeding max_health)

    character["health"] += 30
    if character["health"] > character["max_health"]:
        character["health"] = character["max_health"]

# ============================================================================
# COMBAT UTILITIES
# ============================================================================

def can_character_fight(character):
    """
    Check if character is in condition to fight
    
    Returns: True if health > 0 and not in battle
    """
    # TODO: Implement fight check

    if character["health"] > 0:
        return True
    return False

def get_victory_rewards(enemy):
    """
    Calculate rewards for defeating enemy
    
    Returns: Dictionary with 'xp' and 'gold'
    """
    # TODO: Implement reward calculation

    dictionary = {"xp": enemy["xp_reward"], "gold": enemy["gold_reward"]}
    return dictionary

def display_combat_stats(character, enemy):
    """
    Display current combat status
    
    Shows both character and enemy health/stats
    """
    # TODO: Implement status display
    print(f"\n{character['name']}: HP={character['health']}/{character['max_health']}")
    print(f"{enemy['name']}: HP={enemy['health']}/{enemy['max_health']}")
    pass

def display_battle_log(message):
    """
    Display a formatted battle message
    """
    # TODO: Implement battle log display
    print(f">>> {message}")
    pass

# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    print("=== COMBAT SYSTEM TEST ===")
    
    # Test enemy creation
    # try:
    #     goblin = create_enemy("goblin")
    #     print(f"Created {goblin['name']}")
    # except InvalidTargetError as e:
    #     print(f"Invalid enemy: {e}")
    
    # Test battle
    # test_char = {
    #     'name': 'Hero',
    #     'class': 'Warrior',
    #     'health': 120,
    #     'max_health': 120,
    #     'strength': 15,
    #     'magic': 5
    # }
    #
    # battle = SimpleBattle(test_char, goblin)
    # try:
    #     result = battle.start_battle()
    #     print(f"Battle result: {result}")
    # except CharacterDeadError:
    #     print("Character is dead!")

