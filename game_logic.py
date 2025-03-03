import random
import json
import os
from datetime import datetime

class Person:
    def __init__(self, name, age, gender, occupation, traits=None, skills=None, relations=None):
        self.name = name
        self.age = age
        self.gender = gender
        self.occupation = occupation  # King, Knight, Farmer, etc.
        self.traits = traits or self.generate_traits()
        self.skills = skills or self.generate_skills()
        self.health = 100
        self.wealth = self.starting_wealth()
        self.relations = relations or {}  # key: person_id, value: relationship score (-100 to 100)
        self.spouse = None
        self.children = []
        self.parents = []
        self.reputation = 50  # 0-100 scale
        self.alive = True
        self.events = []  # History of life events
        
    def generate_traits(self):
        # Personality traits influence dialogue options and event outcomes
        all_traits = ["brave", "cowardly", "ambitious", "content", "honest", "deceitful", 
                      "loyal", "treacherous", "kind", "cruel", "pious", "cynical"]
        
        # Each person has 2-4 traits
        num_traits = random.randint(2, 4)
        return random.sample(all_traits, num_traits)
    
    def generate_skills(self):
        # Different skills for different occupations
        base_skills = {
            "combat": random.randint(1, 10),
            "diplomacy": random.randint(1, 10),
            "stewardship": random.randint(1, 10),
            "farming": random.randint(1, 10),
            "crafting": random.randint(1, 10),
            "medicine": random.randint(1, 10),
            "trading": random.randint(1, 10)
        }
        
        # Boost skills related to occupation
        if self.occupation == "Knight":
            base_skills["combat"] += 5
        elif self.occupation == "King":
            base_skills["diplomacy"] += 5
            base_skills["stewardship"] += 3
        elif self.occupation == "Farmer":
            base_skills["farming"] += 5
        elif self.occupation == "Merchant":
            base_skills["trading"] += 5
        
        return base_skills
    
    def starting_wealth(self):
        # Starting wealth based on occupation
        wealth_map = {
            "King": random.randint(800, 1000),
            "Noble": random.randint(400, 700),
            "Knight": random.randint(200, 400),
            "Merchant": random.randint(150, 300),
            "Craftsman": random.randint(80, 200),
            "Tavern Owner": random.randint(100, 250),
            "Farmer": random.randint(30, 120),
            "Beggar": random.randint(0, 20)
        }
        return wealth_map.get(self.occupation, 50)
    
    def age_up(self):
        self.age += 1
        # Check for natural death chance based on age
        if self.age > 40:  # Medieval life expectancy was low
            death_chance = (self.age - 40) * 2  # 2% increase per year after 40
            if self.health < 50:
                death_chance += 10  # Poor health increases death chance
            
            if random.randint(1, 100) <= death_chance:
                self.die(cause="Natural causes")
                return False
        return True
    
    def die(self, cause="Unknown"):
        self.alive = False
        self.events.append(f"Died at age {self.age} due to {cause}")
        return self.get_heir()
    
    def get_heir(self):
        # Return eldest child who can continue the lineage
        if not self.children:
            return None
        
        # Sort by age, oldest first
        eligible_children = [child for child in self.children if child.age >= 16 and child.alive]
        if eligible_children:
            return eligible_children[0]
        return None

class World:
    def __init__(self):
        self.year = 1200
        self.characters = {}  # All characters in the world
        self.player = None
        self.locations = self.generate_locations()
        self.current_events = []  # Current active events
        self.history = []  # Historical events
        
    def generate_locations(self):
        # Generate kingdom, cities, villages, etc.
        locations = {
            "Kingdom of Westoria": {
                "type": "kingdom",
                "ruler": None,  # Will be assigned
                "cities": ["Crownhaven", "Eastport", "Northkeep"],
                "villages": ["Millvale", "Riverside", "Oakhill", "Pinedale"],
                "prosperity": 70,
                "stability": 65
            },
            "Kingdom of Eastmark": {
                "type": "kingdom",
                "ruler": None,
                "cities": ["Easthold", "Southbay"],
                "villages": ["Greenmeadow", "Stonecrest"],
                "prosperity": 60,
                "stability": 80
            }
        }
        
        # Expand with details for each location
        all_locations = {}
        for kingdom, k_data in locations.items():
            all_locations[kingdom] = k_data
            
            # Add cities
            for city in k_data["cities"]:
                all_locations[city] = {
                    "type": "city",
                    "kingdom": kingdom,
                    "buildings": ["Castle", "Market", "Cathedral", "Blacksmith"],
                    "population": random.randint(2000, 8000),
                    "prosperity": random.randint(50, 90)
                }
            
            # Add villages
            for village in k_data["villages"]:
                all_locations[village] = {
                    "type": "village",
                    "kingdom": kingdom,
                    "buildings": ["Tavern", "Mill", "Church", "Farms"],
                    "population": random.randint(100, 1000),
                    "prosperity": random.randint(30, 70)
                }
        
        return all_locations
    
    def advance_time(self):
        # Simulate one season (3 months)
        # Process random events, character actions, etc.
        self.generate_events()
        
        # Age up all characters
        to_remove = []
        for char_id, character in self.characters.items():
            if character.alive:
                survived = character.age_up()
                if not survived and char_id == self.player.id:
                    heir = character.get_heir()
                    if heir:
                        self.player = heir
                        print(f"You have died. You now continue as your heir, {heir.name}.")
                    else:
                        print("You have died without an heir. Game over.")
                        return False
            
        # Clean up dead characters without heirs
        for char_id in to_remove:
            del self.characters[char_id]
            
        return True
    
    def generate_events(self):
        # Generate random events in the world
        event_types = ["war", "plague", "festival", "trade_boom", "famine", "religious_event"]
        
        # 20% chance for a major event
        if random.random() < 0.2:
            event_type = random.choice(event_types)
            if event_type == "war":
                kingdoms = list(filter(lambda k: self.locations[k]["type"] == "kingdom", self.locations.keys()))
                if len(kingdoms) >= 2:
                    k1, k2 = random.sample(kingdoms, 2)
                    event = {
                        "type": "war",
                        "participants": [k1, k2],
                        "duration": random.randint(1, 8),  # Seasons
                        "intensity": random.randint(1, 10),
                        "started": self.year
                    }
                    self.current_events.append(event)
                    self.history.append(f"War erupted between {k1} and {k2} in {self.year}")
            
            # More event types implementation...
        
        # Generate personal events for player
        self.generate_personal_events()
    
    def generate_personal_events(self):
        # These are events specifically for the player
        occupation = self.player.occupation
        
        events = []
        if occupation == "King":
            events = [
                "A neighboring kingdom proposes a marriage alliance",
                "Your subjects are complaining about high taxes",
                "A noble is plotting against you",
                "Foreign envoys have arrived with gifts"
            ]
        elif occupation == "Knight":
            events = [
                "A tournament is being held",
                "Your lord asks you to lead troops against bandits",
                "A damsel seeks your protection",
                "You've been challenged to a duel"
            ]
        elif occupation == "Farmer":
            events = [
                "The crops are failing",
                "Bandits are stealing livestock",
                "The landowner wants to increase your rent",
                "A traveling merchant offers to buy your harvest upfront"
            ]
        
        if events and random.random() < 0.3:  # 30% chance for a personal event
            return random.choice(events)
        
        return None

class Game:
    def __init__(self):
        self.world = World()
        self.player = None
        self.turn = 1
        self.save_directory = "saves/"
        
    def new_game(self):
        print("=== MEDIEVAL LIFE SIMULATOR ===")
        print("Welcome to a world of possibilities in medieval times!")
        
        # Character creation
        name = input("Enter your character's name: ")
        
        gender_choice = input("Choose gender (m/f): ").lower()
        gender = "male" if gender_choice.startswith("m") else "female"
        
        age = random.randint(16, 30)  # Start as a young adult
        
        print("\nChoose your starting occupation:")
        occupations = ["King", "Noble", "Knight", "Merchant", "Farmer", "Craftsman", "Tavern Owner", "Beggar"]
        for i, occ in enumerate(occupations, 1):
            print(f"{i}. {occ}")
            
        occ_choice = int(input("Enter number (or 0 for random): "))
        if occ_choice == 0:
            occupation = random.choice(occupations)
        else:
            occupation = occupations[occ_choice - 1]
            
        # Create player character
        self.player = Person(name, age, gender, occupation)
        self.world.player = self.player
        
        # Start first turn
        self.start_turn()
    
    def start_turn(self):
        while True:
            self.display_status()
            choice = self.display_main_menu()
            
            if choice == "1":
                self.explore()
            elif choice == "2":
                self.interact()
            elif choice == "3":
                self.manage_resources()
            elif choice == "4":
                self.check_relationships()
            elif choice == "5":
                # Advance time (1 season)
                print("\nAdvancing time (1 season)...")
                if not self.world.advance_time():
                    print("Game over.")
                    break
                self.turn += 1
            elif choice == "6":
                self.save_game()
            elif choice == "7":
                self.load_game()
            elif choice == "8":
                print("Exiting game. Goodbye!")
                break
    
    def display_status(self):
        p = self.player
        print("\n" + "=" * 50)
        print(f"Year: {self.world.year}, Turn: {self.turn}")
        print(f"Name: {p.name} | Age: {p.age} | Occupation: {p.occupation}")
        print(f"Health: {p.health} | Wealth: {p.wealth} | Reputation: {p.reputation}")
        
        # Display relevant skills based on occupation
        relevant_skills = []
        if p.occupation in ["King", "Noble"]:
            relevant_skills = ["diplomacy", "stewardship"]
        elif p.occupation == "Knight":
            relevant_skills = ["combat", "diplomacy"]
        elif p.occupation == "Farmer":
            relevant_skills = ["farming", "crafting"]
        elif p.occupation in ["Merchant", "Tavern Owner"]:
            relevant_skills = ["trading", "diplomacy"]
            
        print("Skills:", end=" ")
        for skill in relevant_skills:
            print(f"{skill.capitalize()}: {p.skills[skill]}", end=" | ")
        print()
        
        # Display traits
        print("Traits:", ", ".join(p.traits))
        
        # Family status
        if p.spouse:
            print(f"Spouse: {p.spouse.name}")
        else:
            print("Spouse: None")
            
        if p.children:
            print(f"Children: {len(p.children)}")
        else:
            print("Children: None")
        
        print("=" * 50)
    
    def display_main_menu(self):
        print("\nWhat would you like to do?")
        print("1. Explore")
        print("2. Interact with others")
        print("3. Manage resources")
        print("4. Check relationships")
        print("5. End turn (advance 1 season)")
        print("6. Save game")
        print("7. Load game")
        print("8. Exit game")
        
        choice = input("> ")
        return choice
    
    def explore(self):
        # Implement exploration options based on occupation
        print("\n=== EXPLORATION ===")
        
        if self.player.occupation == "King":
            print("1. Inspect the castle")
            print("2. Visit the city")
            print("3. Tour the countryside")
            print("4. Meet with foreign dignitaries")
        elif self.player.occupation == "Knight":
            print("1. Patrol the roads")
            print("2. Visit the training grounds")
            print("3. Explore nearby villages")
            print("4. Hunt in the royal forest")
        elif self.player.occupation == "Farmer":
            print("1. Check your fields")
            print("2. Visit the village market")
            print("3. Explore the nearby forest")
            print("4. Visit neighboring farms")
        # More occupation-specific options...
        
        print("0. Return to main menu")
        
        choice = input("> ")
        if choice == "0":
            return
        
        # Process exploration choice
        print("You explore and discover something interesting...")
        # Implement random events based on exploration choice
    
    def interact(self):
        # Social interactions
        print("\n=== SOCIAL INTERACTIONS ===")
        print("1. Find a spouse")
        print("2. Talk to family")
        print("3. Meet with others of your profession")
        print("4. Seek audience with nobility")
        print("0. Return to main menu")
        
        choice = input("> ")
        if choice == "0":
            return
            
        # Process interaction choice
        
    def manage_resources(self):
        # Resource management based on occupation
        print("\n=== RESOURCE MANAGEMENT ===")
        
        if self.player.occupation == "King":
            print("1. Collect taxes")
            print("2. Build improvements")
            print("3. Organize army")
            print("4. Adjust laws")
        elif self.player.occupation == "Farmer":
            print("1. Tend crops")
            print("2. Buy seeds")
            print("3. Sell harvest")
            print("4. Improve farm")
        # More occupation-specific options...
        
        print("0. Return to main menu")
        
        choice = input("> ")
        if choice == "0":
            return
        
        # Process resource management choice
    
    def check_relationships(self):
        # View and manage relationships
        print("\n=== RELATIONSHIPS ===")
        
        if self.player.spouse:
            print(f"Spouse: {self.player.spouse.name}")
            # Show relationship details
            
        if self.player.children:
            print("\nChildren:")
            for child in self.player.children:
                print(f"- {child.name}, Age: {child.age}")
                
        print("\nOther relationships:")
        for person_id, relation_value in self.player.relations.items():
            person = self.world.characters.get(person_id)
            if person:
                relationship = "Unknown"
                if relation_value > 80:
                    relationship = "Best Friend"
                elif relation_value > 50:
                    relationship = "Friend"
                elif relation_value > 0:
                    relationship = "Acquaintance"
                elif relation_value > -50:
                    relationship = "Disliked"
                else:
                    relationship = "Enemy"
                    
                print(f"- {person.name} ({person.occupation}): {relationship}")
    
    def save_game(self):
        # Implement game saving
        if not os.path.exists(self.save_directory):
            os.makedirs(self.save_directory)
            
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{self.save_directory}save_{self.player.name}_{timestamp}.json"
        
        # Create save data (would need proper serialization)
        save_data = {
            "player": self.player.__dict__,
            "world": self.world.__dict__,
            "turn": self.turn
        }
        
        print(f"Game saved as: {filename}")
        
    def load_game(self):
        # Implement game loading
        print("Loading game (not fully implemented)")

# Game entry point
if __name__ == "__main__":
    game = Game()
    game.new_game()