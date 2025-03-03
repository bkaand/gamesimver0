import tkinter as tk
from tkinter import ttk, messagebox, font
from PIL import Image, ImageTk
import json
import os
import random
from datetime import datetime
from game_logic import Person, World, Game  # Import game logic classes

class MedievalSimulator:
    def __init__(self, root):
        self.root = root
        self.root.title("Medieval Life Simulator")
        self.root.geometry("1024x768")
        self.root.minsize(800, 600)
        
        # Set up custom fonts
        self.title_font = font.Font(family="Times New Roman", size=20, weight="bold")
        self.header_font = font.Font(family="Times New Roman", size=14, weight="bold")
        self.text_font = font.Font(family="Times New Roman", size=12)
        self.small_font = font.Font(family="Times New Roman", size=10)
        
        # Game data
        self.player = None
        self.world = None
        self.current_location = None
        self.current_year = 1200
        self.current_season = "Spring"
        self.seasons = ["Spring", "Summer", "Autumn", "Winter"]
        self.season_index = 0
        self.turn = 1
        
        # Configure main container
        self.main_container = tk.Frame(self.root, bg="#f0e6d2")
        self.main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Start with the main menu
        self.show_main_menu()
    
    def get_button_style(self, size="medium"):
        """Return consistent button styling based on size"""
        if size == "large":
            return {"font": ("Times New Roman", 14), "bg": "#8b7355", "fg": "black", 
                    "width": 20, "height": 1, "bd": 3, "relief": tk.RAISED}
        elif size == "medium":
            return {"font": self.text_font, "bg": "#8b7355", "fg": "black", 
                    "width": 15, "height": 1, "bd": 2, "relief": tk.RAISED}
        elif size == "small":
            return {"font": self.small_font, "bg": "#8b7355", "fg": "black", 
                    "width": 10, "height": 1, "bd": 2, "relief": tk.RAISED}
        elif size == "action":
            return {"font": self.text_font, "bg": "#8b7355", "fg": "black", 
                    "width": 12, "height": 1, "bd": 2, "relief": tk.RAISED}
    
    def clear_screen(self):
        # Clear the main container
        for widget in self.main_container.winfo_children():
            widget.destroy()
    
    def save_game(self):
        # Create saves directory if it doesn't exist
        save_directory = "saves/"
        if not os.path.exists(save_directory):
            os.makedirs(save_directory)
            
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{save_directory}save_{self.player['name']}_{timestamp}.json"
        
        # Create save data
        save_data = {
            "player": self.player,
            "world": self.world,
            "current_year": self.current_year,
            "current_season": self.current_season,
            "season_index": self.season_index,
            "current_location": self.current_location,
            "turn": self.turn if hasattr(self, 'turn') else 1
        }
        
        # Save to file
        with open(filename, 'w') as f:
            json.dump(save_data, f, indent=4)
        
        messagebox.showinfo("Game Saved", f"Game saved as: {filename}")
    
    def confirm_exit_to_menu(self):
        # Ask user to confirm before exiting to main menu
        if messagebox.askyesno("Return to Main Menu", "Are you sure you want to return to the main menu? Unsaved progress will be lost."):
            self.show_main_menu()
    
    def add_event(self, event_text):
        # Add an event to the player's event log
        timestamp = f"{self.current_season}, Year {self.current_year}"
        event = {"text": event_text, "timestamp": timestamp}
        
        # Add to player's events
        self.player["events"].append(event)
        
        # Update event log if it exists
        if hasattr(self, 'event_log') and self.event_log:
            self.update_event_log()
    
    def update_event_log(self):
        # Clear existing event log
        self.event_log.delete(1.0, tk.END)
        
        # Add events in reverse chronological order (newest first)
        for event in reversed(self.player["events"]):
            self.event_log.insert(tk.END, f"{event['timestamp']}: {event['text']}\n\n")
    
    def show_main_menu(self):
        # Clear the main container
        for widget in self.main_container.winfo_children():
            widget.destroy()
        
        # Title
        title_frame = tk.Frame(self.main_container, bg="#f0e6d2")
        title_frame.pack(pady=50)
        
        title = tk.Label(title_frame, text="Medieval Life Simulator", font=("Times New Roman", 36, "bold"), 
                       bg="#f0e6d2", fg="#5c4425")
        title.pack()
        
        subtitle = tk.Label(title_frame, text="Life in the Middle Ages", font=("Times New Roman", 18), 
                          bg="#f0e6d2", fg="#5c4425")
        subtitle.pack(pady=10)
        
        # Menu buttons
        button_frame = tk.Frame(self.main_container, bg="#f0e6d2")
        button_frame.pack(pady=20)
        
        button_style = self.get_button_style("large")
        
        new_game_btn = tk.Button(button_frame, text="New Game", command=self.start_new_game, **button_style)
        new_game_btn.pack(pady=10)
        
        load_game_btn = tk.Button(button_frame, text="Load Game", command=self.load_game, **button_style)
        load_game_btn.pack(pady=10)
        
        options_btn = tk.Button(button_frame, text="Options", command=self.show_options, **button_style)
        options_btn.pack(pady=10)
        
        exit_btn = tk.Button(button_frame, text="Exit", command=self.root.quit, **button_style)
        exit_btn.pack(pady=10)
        
        # Version info
        version_label = tk.Label(self.main_container, text="Version 0.1 - Alpha", 
                               font=self.small_font, bg="#f0e6d2", fg="#5c4425")
        version_label.pack(side=tk.BOTTOM, pady=10)
    def start_new_game(self):
        """Start a new game by creating a character"""
        # Clear the main container
        for widget in self.main_container.winfo_children():
            widget.destroy()
            
        # Create character creation screen
        self.create_character_form()
    
    def load_game(self):
        """Load a saved game"""
        # For now, just show a message
        messagebox.showinfo("Load Game", "Load game functionality will be implemented in a future update.")
    
    def show_options(self):
        """Show game options"""
        # For now, just show a message
        messagebox.showinfo("Options", "Options menu will be implemented in a future update.")
    
    def get_occupation_description(self, occupation):
        """Return a description of the selected occupation"""
        descriptions = {
            "King": "As a king, you rule over your kingdom with absolute authority. Your decisions shape the lives of thousands of subjects. You have great wealth and power, but also great responsibilities and many who might plot against you.",
            
            "Noble": "As a noble, you are a member of the aristocracy with lands, wealth, and influence. You have responsibilities to both the crown above you and the peasants who work your lands. Your life is one of privilege, but also political intrigue.",
            
            "Knight": "As a knight, you are a warrior sworn to serve your lord and uphold the code of chivalry. You are skilled in combat and may own a small estate. You are expected to fight in wars and tournaments, and to protect the weak.",
            
            "Merchant": "As a merchant, you make your living through trade and commerce. You travel between towns and cities, buying and selling goods for profit. You have freedom and opportunity for wealth, but face risks from bandits and market fluctuations.",
            
            "Tavern Owner": "As a tavern owner, you run an establishment that serves as the social center of the community. You hear all the local gossip and meet travelers from far and wide. Your business provides a steady income and many connections.",
            
            "Farmer": "As a farmer, you work the land to grow crops and raise livestock. Your life follows the rhythm of the seasons, with hard work during planting and harvest. You are the backbone of medieval society, providing food for all.",
            
            "Peasant": "As a peasant, you live a humble life working the land owned by nobles. Your days are filled with hard labor, but you find joy in simple pleasures and community celebrations. Though your means are limited, you have opportunities to improve your station through hard work and clever dealings."
        }
        
        return descriptions.get(occupation, "No description available for this occupation.")
    
    def create_character(self):
        """Create a new character based on form inputs"""
        # Validate inputs
        name = self.name_var.get().strip()
        if not name:
            messagebox.showerror("Error", "Please enter a name.")
            return
        
        gender = self.gender_var.get()
        if not gender:
            messagebox.showerror("Error", "Please select a gender.")
            return
            
        occupation = self.occupation_var.get()
        if not occupation:
            messagebox.showerror("Error", "Please select an occupation.")
            return
            
        # Create player data
        self.player = {
            "name": name,
            "gender": gender.lower(),  # Store gender in lowercase for consistency
            "age": random.randint(18, 30),
            "occupation": occupation,
            "health": 100,
            "wealth": self.get_starting_wealth(occupation),
            "skills": self.generate_skills(occupation),
            "traits": self.generate_traits(),
            "spouse": None,
            "children": [],
            "inventory": [],
            "events": []
        }
        
        # Generate world data
        self.world = {
            "kingdoms": self.generate_kingdoms()
        }
        
        # Set starting location based on occupation
        self.set_starting_location()
        
        # Set initial game state
        self.current_year = 1200
        self.current_season = "Spring"
        self.season_index = 0
        self.current_day = 1
        
        # Add initial event
        self.add_event(f"You begin your life as a {occupation.lower()} in {self.current_location}.")
        
        # Show the main game interface
        self.show_game_interface()
    
    def get_starting_wealth(self, occupation):
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
        return wealth_map.get(occupation, 50)
    
    def generate_skills(self, occupation):
        # Base skills for everyone
        skills = {
            "combat": random.randint(1, 10),
            "diplomacy": random.randint(1, 10),
            "stewardship": random.randint(1, 10),
            "farming": random.randint(1, 10),
            "crafting": random.randint(1, 10),
            "medicine": random.randint(1, 10),
            "trading": random.randint(1, 10)
        }
        
        # Boost occupation-specific skills
        if occupation == "King":
            skills["diplomacy"] += 5
            skills["stewardship"] += 5
        elif occupation == "Noble":
            skills["diplomacy"] += 3
            skills["stewardship"] += 3
        elif occupation == "Knight":
            skills["combat"] += 5
            skills["diplomacy"] += 2
        elif occupation == "Merchant":
            skills["trading"] += 5
            skills["diplomacy"] += 2
        elif occupation == "Farmer":
            skills["farming"] += 5
            skills["crafting"] += 2
        elif occupation == "Craftsman":
            skills["crafting"] += 5
            skills["trading"] += 2
        elif occupation == "Tavern Owner":
            skills["trading"] += 3
            skills["diplomacy"] += 3
        elif occupation == "Beggar":
            skills["trading"] += 2
            
        return skills
    def generate_traits(self):
        # Personality traits that affect gameplay
        all_traits = ["brave", "cowardly", "ambitious", "content", "honest", "deceitful", 
                     "loyal", "treacherous", "kind", "cruel", "pious", "cynical"]
        
        # Each character gets 2-4 traits
        num_traits = random.randint(2, 4)
        return random.sample(all_traits, num_traits)
    
    def generate_kingdoms(self):
        # Create basic kingdom structure
        kingdoms = {
            "Westoria": {
                "ruler": "King Edmund",
                "capital": "Crownhaven",
                "cities": ["Crownhaven", "Eastport", "Northkeep"],
                "villages": ["Millvale", "Riverside", "Oakhill", "Pinedale"],
                "prosperity": 70,
                "stability": 65
            },
            "Eastmark": {
                "ruler": "Queen Elara",
                "capital": "Easthold",
                "cities": ["Easthold", "Southbay"],
                "villages": ["Greenmeadow", "Stonecrest"],
                "prosperity": 60,
                "stability": 80
            }
        }
        
        return kingdoms
    
    def set_starting_location(self):
        # Set starting location based on occupation
        if self.player["occupation"] in ["King", "Noble"]:
            # Royalty starts in a capital
            kingdom = random.choice(list(self.world["kingdoms"].keys()))
            self.current_location = self.world["kingdoms"][kingdom]["capital"]
        elif self.player["occupation"] in ["Knight", "Merchant", "Tavern Owner"]:
            # These occupations typically start in cities
            kingdom = random.choice(list(self.world["kingdoms"].keys()))
            cities = self.world["kingdoms"][kingdom]["cities"]
            self.current_location = random.choice(cities)
        else:
            # Farmers, craftsmen, beggars typically start in villages
            kingdom = random.choice(list(self.world["kingdoms"].keys()))
            villages = self.world["kingdoms"][kingdom]["villages"]
            if villages:
                self.current_location = random.choice(villages)
            else:
                # Fallback to a city if needed
                self.current_location = random.choice(self.world["kingdoms"][kingdom]["cities"])
    
    def show_game_interface(self):
        self.clear_screen()
        
        # Create main game layout
        # Top bar with character info and date
        top_bar = tk.Frame(self.main_container, bg="#8b7355", height=40)
        top_bar.pack(fill=tk.X, pady=(0, 10))
        top_bar.pack_propagate(False)
        
        # Player name and basic info
        player_info = tk.Label(top_bar, text=f"{self.player['name']} - {self.player['occupation']} | Age: {self.player['age']} | Health: {self.player['health']} | Gold: {self.player['wealth']}", 
                              font=self.text_font, bg="#8b7355", fg="black")
        player_info.pack(side=tk.LEFT, padx=10, pady=5)
        
        # Date
        date_info = tk.Label(top_bar, text=f"{self.current_season}, Year {self.current_year}", 
                            font=self.text_font, bg="#8b7355", fg="black")
        date_info.pack(side=tk.RIGHT, padx=10, pady=5)
        
        # Split the main area into sections
        main_area = tk.Frame(self.main_container, bg="#f0e6d2")
        main_area.pack(fill=tk.BOTH, expand=True)
        
        # Left panel - location and map info
        left_panel = tk.Frame(main_area, bg="#e6d8bf", width=200, bd=2, relief=tk.RIDGE)
        left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        left_panel.pack_propagate(False)
        
        location_label = tk.Label(left_panel, text="Location", font=self.header_font, bg="#e6d8bf", fg="#5c4425")
        location_label.pack(pady=(10, 5))
        
        self.location_info = tk.Label(left_panel, text=self.current_location, font=self.text_font, bg="#e6d8bf", fg="#5c4425")
        self.location_info.pack(pady=5)
        
        # Location type (city, village, etc.)
        location_type = self.get_location_type(self.current_location)
        location_type_label = tk.Label(left_panel, text=f"Type: {location_type}", font=self.small_font, bg="#e6d8bf", fg="#5c4425")
        location_type_label.pack(pady=2)
        
        # Kingdom info
        kingdom = self.get_kingdom_for_location(self.current_location)
        kingdom_label = tk.Label(left_panel, text=f"Kingdom: {kingdom}", font=self.small_font, bg="#e6d8bf", fg="#5c4425")
        kingdom_label.pack(pady=2)
        
        # Separator
        ttk.Separator(left_panel, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=10, padx=10)
        # Quick stats
        stats_label = tk.Label(left_panel, text="Skills", font=self.header_font, bg="#e6d8bf", fg="#5c4425")
        stats_label.pack(pady=(10, 5))
        
        # Show main skills based on occupation
        self.display_key_skills(left_panel)
        
        # Travel button
        travel_btn = tk.Button(left_panel, text="Travel", 
                             **self.get_button_style("medium"),
                             command=self.show_travel_options)
        travel_btn.pack(pady=10)
        
        # End Season button
        end_season_btn = tk.Button(left_panel, text="End Season", 
                                 **self.get_button_style("medium"),
                                 command=self.advance_season)
        end_season_btn.pack(pady=10)
        
        # Center panel - main game area
        center_panel = tk.Frame(main_area, bg="#f0e6d2", bd=2, relief=tk.RIDGE)
        center_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        # Location description
        desc_frame = tk.Frame(center_panel, bg="#f0e6d2", padx=15, pady=15)
        desc_frame.pack(fill=tk.X)
        
        desc_title = tk.Label(desc_frame, text=f"{self.current_location}", font=self.header_font, bg="#f0e6d2", fg="#5c4425")
        desc_title.pack(anchor=tk.W)
        
        desc_text = tk.Label(desc_frame, text=self.get_location_description(), 
                           font=self.text_font, bg="#f0e6d2", fg="#5c4425", 
                           wraplength=400, justify=tk.LEFT)
        desc_text.pack(anchor=tk.W, pady=10)
        
        # Action buttons
        action_frame = tk.Frame(center_panel, bg="#f0e6d2", padx=15, pady=15)
        action_frame.pack(fill=tk.X)
        
        action_title = tk.Label(action_frame, text="Actions", font=self.header_font, bg="#f0e6d2", fg="#5c4425")
        action_title.pack(anchor=tk.W, pady=(0, 10))
        
        # Create action buttons based on occupation
        self.create_action_buttons(action_frame)
        
        # Event log
        log_frame = tk.Frame(center_panel, bg="#f0e6d2", padx=15, pady=15)
        log_frame.pack(fill=tk.BOTH, expand=True)
        
        log_title = tk.Label(log_frame, text="Event Log", font=self.header_font, bg="#f0e6d2", fg="#5c4425")
        log_title.pack(anchor=tk.W, pady=(0, 10))
        
        # Create a text widget for the event log
        self.event_log = tk.Text(log_frame, wrap=tk.WORD, width=50, height=10, 
                               font=self.small_font, bg="#e6d8bf", fg="#5c4425")
        self.event_log.pack(fill=tk.BOTH, expand=True)
        self.event_log.config(state=tk.DISABLED)  # Make it read-only
        
        # Right panel - NPCs and interactions
        right_panel = tk.Frame(main_area, bg="#e6d8bf", width=200, bd=2, relief=tk.RIDGE)
        right_panel.pack(side=tk.RIGHT, fill=tk.Y)
        right_panel.pack_propagate(False)
        
        # People in location
        people_label = tk.Label(right_panel, text="People", font=self.header_font, bg="#e6d8bf", fg="#5c4425")
        people_label.pack(pady=(10, 5))
        
        # Interact button
        interact_btn = tk.Button(right_panel, text="Interact with NPCs", 
                               **self.get_button_style("medium"),
                               command=self.show_interaction_menu)
        interact_btn.pack(pady=5)
        
        # Family button
        family_btn = tk.Button(right_panel, text="Family", 
                             **self.get_button_style("medium"),
                             command=self.show_family_screen)
        family_btn.pack(pady=5)
        
        # Spouse button (if married)
        if self.player.get("spouse"):
            # Check if spouse is a string (old format) or a dictionary (new format)
            if isinstance(self.player["spouse"], str):
                # Convert to new format
                self.player["spouse"] = {
                    "name": self.player["spouse"],
                    "age": random.randint(16, 40),
                    "traits": self.generate_traits(),
                    "relationship": 75
                }
                
            spouse_btn = tk.Button(right_panel, text="Interact with Spouse", 
                                 **self.get_button_style("medium"),
                                 command=self.interact_with_spouse)
            spouse_btn.pack(pady=5)
        
        # Market button
        market_btn = tk.Button(right_panel, text="Market", 
                             **self.get_button_style("medium"),
                             command=self.show_market)
        market_btn.pack(pady=5)
        
        # Inventory button
        inventory_btn = tk.Button(right_panel, text="Inventory", 
                                **self.get_button_style("medium"),
                                command=self.show_inventory)
        inventory_btn.pack(pady=5)
        
        # Save button
        save_btn = tk.Button(right_panel, text="Save Game", 
                           **self.get_button_style("medium"),
                           command=self.save_game)
        save_btn.pack(pady=5)
        
        # Exit to menu button
        exit_btn = tk.Button(right_panel, text="Exit to Menu", 
                           **self.get_button_style("medium"),
                           command=self.confirm_exit_to_menu)
        exit_btn.pack(pady=5)
        
        # Update the event log
        self.update_event_log()
    
    def get_location_type(self, location):
        # Determine if location is a city, village, etc.
        for kingdom in self.world["kingdoms"].values():
            if location in kingdom["cities"]:
                return "City"
            elif location in kingdom["villages"]:
                return "Village"
            elif location == kingdom["capital"]:
                return "Capital City"
        return "Unknown"
    
    def get_kingdom_for_location(self, location):
        # Find which kingdom this location belongs to
        for kingdom_name, kingdom in self.world["kingdoms"].items():
            if location in kingdom["cities"] or location in kingdom["villages"] or location == kingdom["capital"]:
                return kingdom_name
        return "Unknown"
    
    def get_location_description(self):
        location_type = self.get_location_type(self.current_location)
        kingdom = self.get_kingdom_for_location(self.current_location)
        
        # Generate description based on location type
        if location_type == "Capital City":
            return f"{self.current_location} is the grand capital of {kingdom}. The streets are bustling with nobles, merchants, and commoners alike. The royal castle dominates the skyline, while markets and guildhalls fill the city with commerce and activity."
        
        elif location_type == "City":
            return f"{self.current_location} is a major city in {kingdom}. Stone buildings line the cobbled streets, and city guards patrol regularly. There are several markets, workshops, and taverns serving the large population."
        
        elif location_type == "Village":
            return f"{self.current_location} is a small village in the countryside of {kingdom}. Thatched cottages surround a village square with a well. Most residents are farmers or craftsmen, and life follows the rhythm of the seasons."
        
        else:
            return f"{self.current_location} is a settlement in {kingdom}."
        
    def display_key_skills(self, parent_frame):
        # Show different skills based on occupation
        relevant_skills = []
        if self.player["occupation"] in ["King", "Noble"]:
            relevant_skills = ["diplomacy", "stewardship"]
        elif self.player["occupation"] == "Knight":
            relevant_skills = ["combat", "diplomacy"]
        elif self.player["occupation"] == "Farmer":
            relevant_skills = ["farming", "crafting"]
        elif self.player["occupation"] in ["Merchant", "Tavern Owner"]:
            relevant_skills = ["trading", "diplomacy"]
        elif self.player["occupation"] == "Craftsman":
            relevant_skills = ["crafting", "trading"]
        elif self.player["occupation"] == "Beggar":
            relevant_skills = ["trading", "medicine"]
        
        # Show the selected skills with bars representing level
        for skill in relevant_skills:
            skill_frame = tk.Frame(parent_frame, bg="#e6d8bf")
            skill_frame.pack(fill=tk.X, padx=10, pady=2)
            
            skill_name = tk.Label(skill_frame, text=f"{skill.capitalize()}:", font=self.small_font, 
                               bg="#e6d8bf", fg="#5c4425", width=10, anchor="w")
            skill_name.pack(side=tk.LEFT)
            
            skill_value = self.player["skills"][skill]
            skill_bar = tk.Canvas(skill_frame, width=100, height=15, bg="#d9c9a3", highlightthickness=0)
            skill_bar.pack(side=tk.LEFT, padx=5)
            
            # Draw skill level bar
            bar_width = int(skill_value * 10)  # Scale to fit (skills are 1-10)
            skill_bar.create_rectangle(0, 0, bar_width, 15, fill="#8b7355", outline="")
            
            skill_text = tk.Label(skill_frame, text=str(skill_value), font=self.small_font, 
                               bg="#e6d8bf", fg="#5c4425", width=2)
            skill_text.pack(side=tk.LEFT)
    
    def create_action_buttons(self, parent_frame):
        """Create occupation-specific action buttons"""
        occupation = self.player["occupation"]
        
        if occupation == "King":
            actions = ["Hold Court", "Collect Taxes", "Make Laws", "Diplomacy"]
        elif occupation == "Noble":
            actions = ["Manage Estate", "Host Event", "Collect Taxes", "Patronage"]
        elif occupation == "Knight":
            actions = ["Train", "Quest", "Tournament", "Patrol"]
        elif occupation == "Merchant":
            actions = ["Trade", "Invest", "Negotiate", "Travel"]
        elif occupation == "Farmer":
            actions = ["Plant Crops", "Harvest", "Tend Animals", "Improve Farm"]
        elif occupation == "Craftsman":
            actions = ["Create Goods", "Sell Wares", "Improve Skills", "Take Orders"]
        elif occupation == "Tavern Owner":
            actions = ["Serve Guests", "Hire Staff", "Special Event", "Renovate"]
        elif occupation == "Beggar":
            actions = ["Beg", "Scavenge", "Perform", "Listen for Rumors"]
        else:
            actions = ["Work", "Rest", "Socialize", "Learn"]
        
        # Create buttons for each action
        for action in actions:
            action_btn = tk.Button(parent_frame, text=action, 
                                 command=lambda a=action: self.perform_action(a),
                                 **self.get_button_style("action"))
            action_btn.pack(side=tk.LEFT, padx=5)
    
    def perform_action(self, action):
        """Handle player actions based on their occupation"""
        # Add event to event log
        self.add_event(f"You decided to {action.lower()}.")
        
        # Handle different actions
        if action == "Hold Court":
            self.show_dialog("Royal Court", 
                           "You hold court, listening to the petitions and disputes of your subjects.\n\n"
                           "A peasant claims his neighbor stole his cow. A merchant seeks lower taxes. "
                           "A noble requests permission to build a new mill on his land.")
        elif action == "Collect Taxes":
            tax_amount = random.randint(20, 100)
            self.player["wealth"] += tax_amount
            self.add_event(f"You collected {tax_amount} gold in taxes.")
            self.update_player_info()
        elif action == "Train":
            skill_increase = random.randint(1, 3)
            self.player["skills"]["combat"] += skill_increase
            self.add_event(f"Your combat skill increased by {skill_increase}!")
        elif action == "Plant Crops":
            if self.current_season == "Spring":
                self.add_event("You plant your fields for the coming season. With good weather, you expect a bountiful harvest.")
            else:
                self.add_event("It's not the right season for planting. You should wait until spring.")
        elif action == "Harvest":
            if self.current_season == "Autumn":
                harvest_amount = random.randint(10, 30)
                self.player["wealth"] += harvest_amount
                self.add_event(f"You harvest your crops, earning {harvest_amount} gold at the market.")
                self.update_player_info()
            else:
                self.add_event("Your crops aren't ready for harvest yet. Be patient.")
        
        elif action == "Trade":
            trade_result = random.randint(-10, 30)
            if trade_result > 0:
                self.player["wealth"] += trade_result
                self.add_event(f"Your trading was successful! You earned {trade_result} gold.")
            elif trade_result < 0:
                self.player["wealth"] += trade_result
                self.add_event(f"Your trading went poorly. You lost {abs(trade_result)} gold.")
            else:
                self.add_event("You broke even on your trades today.")
            self.update_player_info()
        elif action == "Beg":
            amount = random.randint(0, 5)
            self.player["wealth"] += amount
            self.add_event(f"You spend the day begging. You collect {amount} gold coins.")
            self.update_player_info()
        else:
            # Generic handling for other actions
            self.add_event(f"You spend the day {action.lower()}ing.")
    
    def show_interaction_menu(self):
        """Show options for interacting with NPCs"""
        # Create a dialog window
        dialog = tk.Toplevel(self.root)
        dialog.title("Interactions")
        dialog.geometry("400x500")
        dialog.configure(bg="#f0e6d2")
        
        # Make dialog modal
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Title
        title = tk.Label(dialog, text="Who would you like to interact with?", 
                       font=self.header_font, bg="#f0e6d2", fg="#5c4425")
        title.pack(pady=20)
        
        # Create a frame for the NPC list
        list_frame = tk.Frame(dialog, bg="#f0e6d2")
        list_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Add scrollbar for NPC list
        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Create a canvas with scrollbar
        canvas = tk.Canvas(list_frame, bg="#f0e6d2", yscrollcommand=scrollbar.set)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Configure the scrollbar to work with the canvas
        scrollbar.config(command=canvas.yview)
        
        # Create a frame inside the canvas to hold the NPC buttons
        npc_frame = tk.Frame(canvas, bg="#f0e6d2")
        canvas.create_window((0, 0), window=npc_frame, anchor="nw")
        
        # Sample NPCs based on location type
        npcs = self.get_location_npcs()
        
        # Create buttons for each NPC
        for npc in npcs:
            npc_btn = tk.Button(npc_frame, text=f"{npc['name']} - {npc['occupation']}", 
                              command=lambda n=npc: self.interact_with_npc(n, dialog),
                              font=self.text_font, bg="#e6d8bf", fg="#5c4425", 
                              width=30, height=2, anchor="w", justify=tk.LEFT)
            npc_btn.pack(fill=tk.X, pady=5)
        
        # Update the canvas scroll region when the frame changes size
        npc_frame.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))
        
        # Close button
        close_btn = tk.Button(dialog, text="Close", command=dialog.destroy, 
                            **self.get_button_style("medium"))
        close_btn.pack(pady=20)
    
    def get_location_npcs(self):
        """Generate NPCs based on current location"""
        location_type = self.get_location_type(self.current_location)
        npcs = []
        
        # Generate different NPCs based on location type
        if location_type == "Capital City":
            npcs = [
                {"name": "Lord Harrington", "occupation": "Noble", "attitude": "formal"},
                {"name": "Master Thomas", "occupation": "Royal Blacksmith", "attitude": "respectful"},
                {"name": "Lady Elaine", "occupation": "Court Advisor", "attitude": "cautious"},
                {"name": "Brother Michael", "occupation": "Cathedral Priest", "attitude": "kind"},
                {"name": "Galen", "occupation": "Royal Guard Captain", "attitude": "stern"}
            ]
        elif location_type == "City":
            npcs = [
                {"name": "Alderman William", "occupation": "City Official", "attitude": "busy"},
                {"name": "Goodwife Martha", "occupation": "Tavern Owner", "attitude": "friendly"},
                {"name": "Master Edwin", "occupation": "Guild Master", "attitude": "proud"},
                {"name": "Father Thomas", "occupation": "Priest", "attitude": "humble"},
                {"name": "Sergeant Roderick", "occupation": "City Guard", "attitude": "suspicious"}
            ]
        elif location_type == "Village":
            npcs = [
                {"name": "Elder Tomas", "occupation": "Village Elder", "attitude": "wise"},
                {"name": "Goodman John", "occupation": "Farmer", "attitude": "hardworking"},
                {"name": "Goodwife Emma", "occupation": "Herbalist", "attitude": "caring"},
                {"name": "Blacksmith Gareth", "occupation": "Blacksmith", "attitude": "strong"},
                {"name": "Miller's Son Adam", "occupation": "Miller", "attitude": "cheerful"}
            ]
        
        return npcs
    def interact_with_npc(self, npc, parent_dialog):
        """Handle interaction with an NPC"""
        # Close the NPC list dialog
        parent_dialog.destroy()
        
        # Create a new dialog for the interaction
        dialog = tk.Toplevel(self.root)
        dialog.title(f"Speaking with {npc['name']}")
        dialog.geometry("500x400")
        dialog.configure(bg="#f0e6d2")
        
        # Make dialog modal
        dialog.transient(self.root)
        dialog.grab_set()
        
        # NPC info at the top
        npc_frame = tk.Frame(dialog, bg="#e6d8bf", bd=2, relief=tk.GROOVE)
        npc_frame.pack(fill=tk.X, padx=20, pady=10)
        
        npc_name = tk.Label(npc_frame, text=npc["name"], font=self.header_font, 
                          bg="#e6d8bf", fg="#5c4425")
        npc_name.pack(pady=(10, 0))
        
        npc_occupation = tk.Label(npc_frame, text=npc["occupation"], font=self.text_font, 
                                bg="#e6d8bf", fg="#5c4425")
        npc_occupation.pack(pady=(0, 5))
        
        # Initial dialogue
        dialogue_frame = tk.Frame(dialog, bg="#f5f0e6", bd=2, relief=tk.GROOVE)
        dialogue_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # NPC greeting based on their attitude
        greeting = self.get_npc_greeting(npc)
        
        dialogue_text = tk.Label(dialogue_frame, text=greeting, font=self.text_font, 
                               bg="#f5f0e6", fg="#5c4425", wraplength=440, justify=tk.LEFT)
        dialogue_text.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        
        # Options frame at the bottom
        options_frame = tk.Frame(dialog, bg="#f0e6d2")
        options_frame.pack(fill=tk.X, padx=20, pady=10)
        
        # Generate dialogue options based on player occupation and NPC
        options = self.get_dialogue_options(npc)
        
        # Create buttons for dialogue options
        for option_text, response in options:
            option_btn = tk.Button(options_frame, text=option_text, 
                                 command=lambda r=response: self.show_dialogue_response(dialogue_text, r, options_frame),
                                 font=self.text_font, bg="#e6d8bf", fg="#5c4425", 
                                 wraplength=400, justify=tk.LEFT)
            option_btn.pack(fill=tk.X, pady=5)
        
        # Close button
        close_btn = tk.Button(dialog, text="End Conversation", command=dialog.destroy, 
                            **self.get_button_style("medium"))
        close_btn.pack(pady=20)
    
    def get_npc_greeting(self, npc):
        """Generate appropriate greeting based on NPC attitude and player status"""
        attitude = npc["attitude"]
        player_occupation = self.player["occupation"]
        
        # Different greetings based on attitude and player status
        if attitude == "formal":
            if player_occupation in ["King", "Noble"]:
                return f'"Greetings, my {player_occupation}. It is an honor to speak with you today. How may I be of service?"'
            else:
                return f'"Well met. What business brings you to see me today?"'
        
        elif attitude == "friendly":
            return f'"Hello there! It\'s good to see a new face. What can I do for you today?"'
        
        elif attitude == "suspicious":
            if player_occupation in ["Beggar", "Farmer"]:
                return f'"What do you want? Make it quick, I\'m watching you."'
            else:
                return f'"State your business. I don\'t have all day."'
        
        elif attitude == "respectful":
            return f'"Good day to you. How may I assist you?"'
        
        else:
            return f'"Hello there. What brings you to me today?"'
    
    def get_dialogue_options(self, npc):
        """Generate dialogue options based on NPC and player"""
        npc_occupation = npc["occupation"]
        player_occupation = self.player["occupation"]
        
        # Base options available to all player types
        options = [
            ("Ask about local news", f'"Well, the weather has been {random.choice(["fair", "poor", "excellent"])} for the season. ' + 
                                  f'The {random.choice(["harvest", "hunting", "fishing"])} has been ' + 
                                  f'{random.choice(["good", "bad", "average"])} this year."'),
            
            ("Introduce yourself", f'"A {player_occupation}? Interesting. We don\'t get many of your kind around here."')
        ]

        # Add occupation-specific options
        if "Guard" in npc_occupation:
            options.append(("Ask about safety in the area", 
                         f'"It\'s been {random.choice(["quiet", "troubled", "peaceful"])} lately. ' + 
                         f'A few reports of {random.choice(["bandits", "wolves", "thieves"])} to the ' + 
                         f'{random.choice(["north", "south", "east", "west"])}, but nothing too concerning."'))
        
        elif "Merchant" in npc_occupation or "Blacksmith" in npc_occupation or npc_occupation == "Tavern Owner":
            options.append(("Ask about goods for sale", 
                         f'"I have the finest {random.choice(["goods", "wares", "merchandise"])} in the area. ' + 
                         f'My prices are {random.choice(["fair", "reasonable", "the best you will find"])}, ' + 
                         f'I assure you."'))
        
        elif "Priest" in npc_occupation:
            options.append(("Ask for a blessing", 
                         f'"May the heavens smile upon you and guide your path. ' + 
                         f'These are {random.choice(["challenging", "blessed", "interesting"])} times we live in."'))
        
        # Add special options based on player occupation
        if player_occupation == "King" or player_occupation == "Noble":
            options.append(("Request service or information", 
                          f'"Of course, my {player_occupation}! I am at your service. What would you like to know?"'))
        
        elif player_occupation == "Knight":
            options.append(("Ask about quests or missions", 
                          f'"A knight seeking glory? Well, there have been reports of ' + 
                          f'{random.choice(["bandits", "a monster", "raiders"])} near the ' + 
                          f'{random.choice(["forest", "hills", "old bridge"])}."'))
        
        return options
    
    def show_dialogue_response(self, dialogue_label, response, options_frame):
        """Show NPC response to dialogue option"""
        dialogue_label.config(text=response)
        
        # Clear previous options
        for widget in options_frame.winfo_children():
            widget.destroy()
        
        # Add new options based on the conversation progress
        continue_btn = tk.Button(options_frame, text="Continue conversation", 
                               command=lambda: self.add_event("You had a pleasant conversation."),
                               font=self.text_font, bg="#e6d8bf", fg="#5c4425")
        continue_btn.pack(fill=tk.X, pady=5)
    
    def show_family_screen(self):
        """Show the player's family information"""
        # Create dialog for family screen
        dialog = tk.Toplevel(self.root)
        dialog.title("Family")
        dialog.geometry("600x500")
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Make the dialog modal
        dialog.focus_set()
        
        # Add some padding
        frame = tk.Frame(dialog, padx=20, pady=20, bg="#f0e6d2")
        frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = tk.Label(frame, text="Your Family", font=self.header_font, bg="#f0e6d2", fg="#5c4425")
        title_label.pack(pady=(0, 20))
        
        # Spouse section
        spouse_frame = tk.Frame(frame, bg="#e6d8bf", bd=2, relief=tk.RIDGE, padx=10, pady=10)
        spouse_frame.pack(fill=tk.X, pady=10)
        
        spouse_title = tk.Label(spouse_frame, text="Spouse", font=self.header_font, bg="#e6d8bf", fg="#5c4425")
        spouse_title.pack(anchor=tk.W)
        
        if self.player.get("spouse"):
            spouse = self.player["spouse"]
            # Check if spouse is a string (old format) or a dictionary (new format)
            if isinstance(spouse, str):
                # Convert to new format
                self.player["spouse"] = {
                    "name": spouse,
                    "age": random.randint(16, 40),
                    "traits": self.generate_traits(),
                    "relationship": 75
                }
                spouse = self.player["spouse"]
                
            spouse_info = tk.Label(spouse_frame, 
                                 text=f"{spouse['name']} - Age: {spouse.get('age', 'Unknown')}", 
                                 font=self.text_font, bg="#e6d8bf", fg="#5c4425")
            spouse_info.pack(anchor=tk.W, pady=5)
            
            # Traits
            if spouse.get("traits"):
                traits_text = ", ".join(spouse["traits"])
                traits_label = tk.Label(spouse_frame, text=f"Traits: {traits_text}", 
                                      font=self.small_font, bg="#e6d8bf", fg="#5c4425")
                traits_label.pack(anchor=tk.W)
            
            # Relationship status
            relationship = spouse.get("relationship", 50)
            relationship_text = "Loving" if relationship > 75 else "Good" if relationship > 50 else "Neutral" if relationship > 25 else "Poor"
            relationship_label = tk.Label(spouse_frame, text=f"Relationship: {relationship_text}", 
                                        font=self.small_font, bg="#e6d8bf", fg="#5c4425")
            relationship_label.pack(anchor=tk.W)
            
            # Interact button
            interact_btn = tk.Button(spouse_frame, text="Interact with Spouse", 
                                   **self.get_button_style("medium"),
                                   command=lambda: self.interact_with_spouse_from_family(dialog))
            interact_btn.pack(anchor=tk.E, pady=10)
        else:
            no_spouse = tk.Label(spouse_frame, text="You are not married.", font=self.text_font, bg="#e6d8bf", fg="#5c4425")
            no_spouse.pack(anchor=tk.W, pady=5)
            
            find_spouse_btn = tk.Button(spouse_frame, text="Find a Spouse", 
                                      **self.get_button_style("medium"),
                                      command=lambda: self.find_spouse_from_family(dialog))
            find_spouse_btn.pack(anchor=tk.E, pady=10)
        
        # Children section
        children_frame = tk.Frame(frame, bg="#e6d8bf", bd=2, relief=tk.RIDGE, padx=10, pady=10)
        children_frame.pack(fill=tk.X, pady=10, expand=True)
        
        children_title = tk.Label(children_frame, text="Children", font=self.header_font, bg="#e6d8bf", fg="#5c4425")
        children_title.pack(anchor=tk.W)
        
        if self.player.get("children") and len(self.player["children"]) > 0:
            children_list_frame = tk.Frame(children_frame, bg="#e6d8bf")
            children_list_frame.pack(fill=tk.BOTH, expand=True, pady=5)
            
            for child in self.player["children"]:
                # Check if child is a string (old format) or a dictionary (new format)
                if isinstance(child, str):
                    # Convert to new format
                    child = {
                        "name": child,
                        "gender": random.choice(["male", "female"]),
                        "age": random.randint(0, 10),
                        "traits": self.generate_traits(),
                        "relationship": 100
                    }
                    
                child_frame = tk.Frame(children_list_frame, bg="#e6d8bf", bd=1, relief=tk.GROOVE, padx=5, pady=5)
                child_frame.pack(fill=tk.X, pady=2)
                
                gender_text = "Son" if child.get("gender", "male") == "male" else "Daughter"
                child_info = tk.Label(child_frame, 
                                    text=f"{child['name']} - {gender_text}, Age: {child.get('age', 0)}", 
                                   font=self.text_font, bg="#e6d8bf", fg="#5c4425")
                child_info.pack(anchor=tk.W)
                
                # Traits if any
                if child.get("traits"):
                    traits_text = ", ".join(child["traits"])
                    traits_label = tk.Label(child_frame, text=f"Traits: {traits_text}", 
                                          font=self.small_font, bg="#e6d8bf", fg="#5c4425")
                    traits_label.pack(anchor=tk.W)
        else:
            no_children = tk.Label(children_frame, text="You have no children.", font=self.text_font, bg="#e6d8bf", fg="#5c4425")
            no_children.pack(anchor=tk.W, pady=5)
        
        # Close button
        close_button = tk.Button(frame, text="Close", **self.get_button_style("medium"), command=dialog.destroy)
        close_button.pack(pady=10)
    
    def interact_with_spouse_from_family(self, family_dialog):
        """Open spouse interaction screen from family screen"""
        family_dialog.destroy()
        self.interact_with_spouse()
    
    def find_spouse_from_family(self, family_dialog):
        """Find a spouse from the family screen"""
        family_dialog.destroy()
        self.find_spouse()
    
    def find_spouse(self):
        """Find potential spouses based on player's status and location"""
        # Check if already married
        if self.player.get("spouse"):
            self.show_dialog("Marriage", "You are already married.")
            return
            
        # Generate potential spouses based on player's status
        potential_spouses = []
        
        # Number of potential spouses based on location type
        location_type = self.get_location_type(self.current_location)
        if location_type == "City":
            num_spouses = random.randint(3, 5)
        elif location_type == "Town":
            num_spouses = random.randint(2, 4)
        else:  # Village
            num_spouses = random.randint(1, 3)
            
        # Get player's gender (ensure it's lowercase for consistency)
        player_gender = self.player["gender"].lower() if isinstance(self.player["gender"], str) else "male"
        
        # Generate spouses
        for _ in range(num_spouses):
            # Determine gender (opposite of player's gender)
            gender = "female" if player_gender == "male" else "male"
            
            # Generate name based on gender
            name = self.generate_name(gender)
            
            # Age range (slightly younger for female spouses in medieval times)
            if gender == "female":
                age = random.randint(16, self.player["age"])
        else:
                age = random.randint(self.player["age"] - 5, self.player["age"] + 10)
                
            # Cap age
            age = max(16, min(age, 45))
            
            # Generate traits
            traits = self.generate_traits()
            
            # Wealth based on traits and random factors
            base_wealth = random.randint(10, 50)
            if "wealthy" in traits:
                base_wealth *= 3
            elif "poor" in traits:
                base_wealth = max(5, base_wealth // 2)
                
            # Create spouse data
            spouse = {
                "name": name,
                "age": age,
                "gender": gender,
                "traits": traits,
                "wealth": base_wealth,
                "dowry": base_wealth * 2,  # Dowry is twice the base wealth
                "relationship": 50  # Neutral starting relationship
            }
            
            potential_spouses.append(spouse)
            
        # Show spouse selection screen
        self.show_spouse_selection(potential_spouses)
    
    def show_spouse_selection(self, potential_spouses):
        """Show a dialog with potential spouses to choose from"""
        # Create dialog
        dialog = tk.Toplevel(self.root)
        dialog.title("Find a Spouse")
        dialog.geometry("600x500")
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Make the dialog modal
        dialog.focus_set()
        
        # Add some padding
        frame = tk.Frame(dialog, padx=20, pady=20, bg="#f0e6d2")
        frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = tk.Label(frame, text="Potential Spouses", font=self.header_font, bg="#f0e6d2", fg="#5c4425")
        title_label.pack(pady=(0, 20))
        
        # Description
        desc_text = "Choose a spouse to marry. Marriage will bring companionship and potentially children."
        desc_label = tk.Label(frame, text=desc_text, font=self.text_font, bg="#f0e6d2", fg="#5c4425", wraplength=500)
        desc_label.pack(pady=(0, 20))
        
        # Spouse options
        spouse_frame = tk.Frame(frame, bg="#f0e6d2")
        spouse_frame.pack(fill=tk.BOTH, expand=True)
        
        for spouse in potential_spouses:
            # Create a frame for each spouse
            option_frame = tk.Frame(spouse_frame, bg="#e6d8bf", bd=2, relief=tk.RIDGE, padx=10, pady=10)
            option_frame.pack(fill=tk.X, pady=10)
            
            # Spouse name and age
            gender_text = "woman" if spouse["gender"] == "female" else "man"
            name_label = tk.Label(option_frame, text=f"{spouse['name']}, a {spouse['age']} year old {gender_text}", 
                                font=self.header_font, bg="#e6d8bf", fg="#5c4425")
            name_label.pack(anchor=tk.W)
            
            # Traits
            traits_text = ", ".join(spouse["traits"])
            traits_label = tk.Label(option_frame, text=f"Traits: {traits_text}", 
                               font=self.text_font, bg="#e6d8bf", fg="#5c4425")
            traits_label.pack(anchor=tk.W, pady=5)
            
            # Dowry
            dowry_label = tk.Label(option_frame, text=f"Dowry: {spouse['dowry']} gold", 
                                  font=self.text_font, bg="#e6d8bf", fg="#5c4425")
            dowry_label.pack(anchor=tk.W, pady=5)
            
            # Marry button
            marry_btn = tk.Button(option_frame, text="Marry", 
                                **self.get_button_style("medium"),
                                command=lambda s=spouse: self.marry_spouse(s, dialog))
            marry_btn.pack(anchor=tk.E, pady=5)
        
        # Close button
        close_button = tk.Button(frame, text="Cancel", **self.get_button_style("medium"), command=dialog.destroy)
        close_button.pack(pady=10)
    
    def marry_spouse(self, spouse, dialog):
        """Handle marriage to selected spouse"""
        dialog.destroy()
        
        # Create spouse data structure
        spouse_data = {
            "name": spouse["name"],
            "age": spouse["age"],
            "gender": spouse["gender"],
            "traits": spouse.get("traits", self.generate_traits()),
            "relationship": 75  # Start with a good relationship
        }
        
        # Set spouse
        self.player["spouse"] = spouse_data
        
        # Show marriage dialog
        self.show_dialog("Marriage", 
                       f"Congratulations on your marriage to {spouse['name']}!\n\n"
                       f"You have a lovely ceremony, and your new spouse moves into your home in {self.current_location}.")
        
        # Add event
        self.add_event(f"You married {spouse['name']}.")
        
        # Update UI
        self.update_player_info()
    
    def show_market(self):
        """Show market screen with goods to buy/sell"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Market")
        dialog.geometry("600x500")
        dialog.configure(bg="#f0e6d2")
        
        # Make dialog modal
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Title
        title = tk.Label(dialog, text="Market", font=self.header_font, bg="#f0e6d2", fg="#5c4425")
        title.pack(pady=20)
        
        # Player gold info
        gold_frame = tk.Frame(dialog, bg="#e6d8bf", bd=2, relief=tk.GROOVE)
        gold_frame.pack(fill=tk.X, padx=20, pady=10)
        
        gold_label = tk.Label(gold_frame, text=f"Your Gold: {self.player['wealth']}", 
                            font=self.text_font, bg="#e6d8bf", fg="#5c4425")
        gold_label.pack(pady=10)

        # Market tabs
        tab_control = ttk.Notebook(dialog)
        tab_control.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Buy tab
        buy_tab = tk.Frame(tab_control, bg="#f0e6d2")
        tab_control.add(buy_tab, text="Buy")
        
        # Sell tab
        sell_tab = tk.Frame(tab_control, bg="#f0e6d2")
        tab_control.add(sell_tab, text="Sell")
        
        # Generate items to buy based on location
        location_type = self.get_location_type(self.current_location)
        items_to_buy = self.get_market_items(location_type)
        
        # Create scrollable frame for buy items
        buy_canvas = tk.Canvas(buy_tab, bg="#f0e6d2", highlightthickness=0)
        buy_scrollbar = ttk.Scrollbar(buy_tab, orient="vertical", command=buy_canvas.yview)
        buy_scrollable_frame = tk.Frame(buy_canvas, bg="#f0e6d2")
        
        buy_scrollable_frame.bind(
            "<Configure>",
            lambda e: buy_canvas.configure(scrollregion=buy_canvas.bbox("all"))
        )
        
        buy_canvas.create_window((0, 0), window=buy_scrollable_frame, anchor="nw")
        buy_canvas.configure(yscrollcommand=buy_scrollbar.set)
        
        buy_canvas.pack(side="left", fill="both", expand=True)
        buy_scrollbar.pack(side="right", fill="y")
        
        # Add buy items to scrollable frame
        for item in items_to_buy:
            item_frame = tk.Frame(buy_scrollable_frame, bg="#e6d8bf", bd=2, relief=tk.GROOVE)
            item_frame.pack(fill=tk.X, pady=5, padx=5)
            
            item_name = tk.Label(item_frame, text=item["name"], 
                               font=self.text_font, bg="#e6d8bf", fg="#5c4425", width=20, anchor="w")
            item_name.pack(side=tk.LEFT, padx=5, pady=5)
            
            item_price = tk.Label(item_frame, text=f"Price: {item['price']} gold", 
                                font=self.small_font, bg="#e6d8bf", fg="#5c4425", width=15)
            item_price.pack(side=tk.LEFT, padx=5, pady=5)
            
            buy_btn = tk.Button(item_frame, text="Buy", 
                              command=lambda i=item: self.buy_item(i, gold_label),
                              **self.get_button_style("small"))
            buy_btn.pack(side=tk.RIGHT, padx=5, pady=5)
        
        # Create player inventory items to sell
        # For now, we'll just create some sample items the player can sell
        player_items = [
            {"name": "Old Sword", "price": 25, "quantity": 1},
            {"name": "Herbs", "price": 5, "quantity": 10},
            {"name": "Wheat", "price": 2, "quantity": 20},
            {"name": "Leather", "price": 8, "quantity": 5}
        ]
        
        # Create scrollable frame for sell items
        sell_canvas = tk.Canvas(sell_tab, bg="#f0e6d2", highlightthickness=0)
        sell_scrollbar = ttk.Scrollbar(sell_tab, orient="vertical", command=sell_canvas.yview)
        sell_scrollable_frame = tk.Frame(sell_canvas, bg="#f0e6d2")
        
        sell_scrollable_frame.bind(
            "<Configure>",
            lambda e: sell_canvas.configure(scrollregion=sell_canvas.bbox("all"))
        )
        
        sell_canvas.create_window((0, 0), window=sell_scrollable_frame, anchor="nw")
        sell_canvas.configure(yscrollcommand=sell_scrollbar.set)
        
        sell_canvas.pack(side="left", fill="both", expand=True)
        sell_scrollbar.pack(side="right", fill="y")
        
        # Add sell items to scrollable frame
        for item in player_items:
            item_frame = tk.Frame(sell_scrollable_frame, bg="#e6d8bf", bd=2, relief=tk.GROOVE)
            item_frame.pack(fill=tk.X, pady=5, padx=5)
            
            item_name = tk.Label(item_frame, text=f"{item['name']} (x{item['quantity']})", 
                               font=self.text_font, bg="#e6d8bf", fg="#5c4425", width=20, anchor="w")
            item_name.pack(side=tk.LEFT, padx=5, pady=5)
            
            item_price = tk.Label(item_frame, text=f"Value: {item['price']} gold", 
                                font=self.small_font, bg="#e6d8bf", fg="#5c4425", width=15)
            item_price.pack(side=tk.LEFT, padx=5, pady=5)
            
            sell_btn = tk.Button(item_frame, text="Sell", 
                               command=lambda i=item: self.sell_item(i, gold_label),
                               **self.get_button_style("small"))
            sell_btn.pack(side=tk.RIGHT, padx=5, pady=5)

        # Close button
        close_btn = tk.Button(dialog, text="Close", command=dialog.destroy, 
                            **self.get_button_style("medium"))
        close_btn.pack(pady=20)
    
    def get_market_items(self, location_type):
        """Generate market items based on location type"""
        # Base items available everywhere
        items = [
            {"name": "Bread", "price": 2, "type": "food"},
            {"name": "Ale", "price": 3, "type": "food"},
            {"name": "Cheese", "price": 5, "type": "food"}
        ]
        
        # Add location-specific items
        if location_type == "Capital City":
            items.extend([
                {"name": "Fine Clothing", "price": 50, "type": "clothing"},
                {"name": "Silver Goblet", "price": 80, "type": "luxury"},
                {"name": "Quality Sword", "price": 120, "type": "weapon"},
                {"name": "Books", "price": 60, "type": "luxury"},
                {"name": "Spices", "price": 40, "type": "food"},
                {"name": "Fine Horse", "price": 200, "type": "animal"}
            ])
        elif location_type == "City":
            items.extend([
                {"name": "Clothing", "price": 25, "type": "clothing"},
                {"name": "Basic Sword", "price": 60, "type": "weapon"},
                {"name": "Shield", "price": 40, "type": "weapon"},
                {"name": "Wine", "price": 15, "type": "food"},
                {"name": "Horse", "price": 100, "type": "animal"}
            ])
        elif location_type == "Village":
            items.extend([
                {"name": "Simple Clothing", "price": 15, "type": "clothing"},
                {"name": "Knife", "price": 20, "type": "tool"},
                {"name": "Chicken", "price": 8, "type": "animal"},
                {"name": "Seeds", "price": 5, "type": "farming"},
                {"name": "Tools", "price": 25, "type": "tool"}
            ])
        
        return items
    
    def buy_item(self, item, gold_label):
        """Handle buying an item"""
        # Check if player has enough gold
        if self.player["wealth"] >= item["price"]:
            # Deduct cost
            self.player["wealth"] -= item["price"]
            
            # Update gold display
            gold_label.config(text=f"Your Gold: {self.player['wealth']}")
            
            # Add item to inventory (not implemented yet)
            self.add_event(f"You purchased {item['name']} for {item['price']} gold.")
            
            # Update main screen player info
            self.update_player_info()
        else:
            # Show error message
            messagebox.showerror("Cannot Buy", "You don't have enough gold for this item.")
    
    def sell_item(self, item, gold_label):
        """Handle selling an item"""
        # Add value to player's gold
        sell_value = item["price"]
        self.player["wealth"] += sell_value
        
        # Update gold display
        gold_label.config(text=f"Your Gold: {self.player['wealth']}")
        
        # Remove one from quantity
        item["quantity"] -= 1
        
        # If quantity is zero, remove item (would need to update the UI)
        if item["quantity"] <= 0:
            # Remove item from list (not implemented yet)
            pass
        
        # Add event
        self.add_event(f"You sold {item['name']} for {sell_value} gold.")
        
        # Update main screen player info
        self.update_player_info()
    
    def show_inventory(self):
        """Show player inventory"""
        # For future implementation
        self.show_dialog("Inventory", "Inventory system not yet implemented.")

    def show_travel_options(self):
        """Show options for traveling to different locations"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Travel")
        dialog.geometry("500x400")
        dialog.configure(bg="#f0e6d2")
        
        # Make dialog modal
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Title
        title = tk.Label(dialog, text="Travel", font=self.header_font, bg="#f0e6d2", fg="#5c4425")
        title.pack(pady=20)
        
        # Current location
        current = tk.Label(dialog, text=f"Current Location: {self.current_location}", 
                         font=self.text_font, bg="#f0e6d2", fg="#5c4425")
        current.pack(pady=10)
        
        # Get available locations to travel to
        available_locations = self.get_available_travel_locations()
        
        # Create a frame for the location list
        locations_frame = tk.Frame(dialog, bg="#f0e6d2")
        locations_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Add each location as a button
        for location, travel_time in available_locations:
            loc_frame = tk.Frame(locations_frame, bg="#e6d8bf", bd=2, relief=tk.GROOVE)
            loc_frame.pack(fill=tk.X, pady=5)
            
            loc_name = tk.Label(loc_frame, text=location, 
                              font=self.text_font, bg="#e6d8bf", fg="#5c4425", width=20, anchor="w")
            loc_name.pack(side=tk.LEFT, padx=10, pady=10)
            
            loc_time = tk.Label(loc_frame, text=f"Travel Time: {travel_time} days", 
                              font=self.small_font, bg="#e6d8bf", fg="#5c4425")
            loc_time.pack(side=tk.LEFT, padx=10, pady=10)
            
            travel_btn = tk.Button(loc_frame, text="Travel", 
                                 command=lambda l=location, t=travel_time: self.travel_to(l, t, dialog),
                                 font=self.text_font, bg="#8b7355", fg="black", width=8)
            travel_btn.pack(side=tk.RIGHT, padx=10, pady=10)
        
        # Close button
        close_btn = tk.Button(dialog, text="Cancel", command=dialog.destroy, 
                            **self.get_button_style("medium"))
        close_btn.pack(pady=20)
    
    def get_available_travel_locations(self):
        """Get available locations to travel to based on current location"""
        current_kingdom = self.get_kingdom_for_location(self.current_location)
        locations = []
        
        # Add all cities and villages in the current kingdom except current location
        if current_kingdom != "Unknown":
            kingdom_data = self.world["kingdoms"][current_kingdom]
            
            for city in kingdom_data["cities"]:
                if city != self.current_location:
                    # Cities are 1-3 days travel time
                    travel_time = random.randint(1, 3)
                    locations.append((city, travel_time))
            
            for village in kingdom_data["villages"]:
                if village != self.current_location:
                    # Villages are 1-2 days travel time
                    travel_time = random.randint(1, 2)
                    locations.append((village, travel_time))
        
        # Add capitals of other kingdoms (longer travel time)
        for k_name, kingdom in self.world["kingdoms"].items():
            if k_name != current_kingdom:
                capital = kingdom["capital"]
                # Traveling to another kingdom takes 3-7 days
                travel_time = random.randint(3, 7)
                locations.append((capital, travel_time))
        
        return locations
    def travel_to(self, location, travel_time, dialog):
        """Handle traveling to a new location"""
        dialog.destroy()
        
        # Check if any random events during travel
        travel_event = self.generate_travel_event()
        
        if travel_event:
            # Show travel event dialog
            self.show_dialog("Travel Event", travel_event["description"])
            
            # Apply any effects from the event
            if "wealth_change" in travel_event:
                self.player["wealth"] += travel_event["wealth_change"]
                if travel_event["wealth_change"] > 0:
                    self.add_event(f"You gained {travel_event['wealth_change']} gold during your journey.")
                else:
                    self.add_event(f"You lost {abs(travel_event['wealth_change'])} gold during your journey.")
            
            if "health_change" in travel_event:
                self.player["health"] += travel_event["health_change"]
                self.player["health"] = max(0, min(100, self.player["health"]))  # Ensure health stays 0-100
                
                if travel_event["health_change"] > 0:
                    self.add_event(f"Your health improved by {travel_event['health_change']} during your journey.")
                else:
                    self.add_event(f"You were injured during your journey, losing {abs(travel_event['health_change'])} health.")
        
        # Update current location
        self.current_location = location
        self.location_info.config(text=location)
        
        # Add travel log
        self.add_event(f"You traveled to {location}. The journey took {travel_time} days.")
        
        # Advance time based on travel days
        for _ in range(travel_time):
            self.advance_day()
        
        # Update player info
        self.update_player_info()
    
    def generate_travel_event(self):
        """Generate a random travel event"""
        # 30% chance of an event during travel
        if random.random() < 0.3:
            events = [
                {
                    "description": "You encounter bandits on the road! They demand payment to let you pass safely.",
                    "wealth_change": -random.randint(5, 20)
                },
                {
                    "description": "You find a wounded traveler on the road. After helping them, they reward you for your kindness.",
                    "wealth_change": random.randint(5, 15)
                },
                {
                    "description": "Bad weather makes the journey difficult. You slip and fall, injuring yourself.",
                    "health_change": -random.randint(5, 15)
                },
                {
                    "description": "You come across an abandoned cart with some valuable goods inside.",
                    "wealth_change": random.randint(10, 30)
                },
                {
                    "description": "You meet a traveling merchant and trade stories. They give you advice about the local markets.",
                    "effect": "trading_knowledge"
                }
            ]
            return random.choice(events)
        return None
    
    def advance_season(self):
        """Advance the game by one season"""
        # Update season
        self.season_index = (self.season_index + 1) % 4
        self.current_season = self.seasons[self.season_index]
        
        # If we've gone through all seasons, advance the year
        if self.season_index == 0:
            self.current_year += 1
        
        # Add event to log
        self.add_event(f"The season has changed to {self.current_season}.")
        if self.season_index == 0:
            self.add_event(f"A new year has begun! It is now the year {self.current_year}.")
        
        # Age character
        self.player["age"] += 0.25  # Add quarter of a year
        
        # Age spouse and children
        if self.player.get("spouse") and isinstance(self.player["spouse"], dict):
            self.player["spouse"]["age"] += 0.25
            
        if self.player.get("children"):
            for i, child in enumerate(self.player["children"]):
                if isinstance(child, dict):
                    self.player["children"][i]["age"] += 0.25
        
        # Generate seasonal events
        self.generate_seasonal_events()
        
        # Random wealth changes based on occupation and season
        self.apply_seasonal_income()
        
        # Update UI
        self.update_status_bar()
        
        # Show a summary dialog
        self.show_season_summary()
    
    def apply_seasonal_income(self):
        """Apply seasonal income based on occupation"""
        occupation = self.player["occupation"]
        base_income = 0
        
        # Base income by occupation
        if occupation == "King":
            base_income = random.randint(100, 200)
        elif occupation == "Noble":
            base_income = random.randint(50, 100)
        elif occupation == "Knight":
            base_income = random.randint(30, 60)
        elif occupation == "Merchant":
            base_income = random.randint(20, 80)
        elif occupation == "Tavern Owner":
            base_income = random.randint(15, 40)
        elif occupation == "Farmer":
            base_income = random.randint(5, 20)
        else:  # Default
            base_income = random.randint(5, 15)
        
        # Seasonal modifiers
        season_modifier = 1.0
        if occupation == "Farmer":
            if self.current_season == "Spring":
                season_modifier = 0.5  # Planting season, less income
            elif self.current_season == "Summer":
                season_modifier = 0.8  # Growing season, some income
            elif self.current_season == "Autumn":
                season_modifier = 2.0  # Harvest season, more income
            elif self.current_season == "Winter":
                season_modifier = 0.3  # Winter, very little income
        elif occupation == "Merchant" or occupation == "Tavern Owner":
            if self.current_season == "Winter":
                season_modifier = 0.7  # Less trade in winter
            elif self.current_season == "Summer":
                season_modifier = 1.3  # More trade in summer
        
        # Calculate final income
        income = int(base_income * season_modifier)
        
        # Apply income
        self.player["wealth"] += income
        
        # Add event
        self.add_event(f"You earned {income} gold this season from your occupation.")
    
    def show_season_summary(self):
        """Show a summary of the season's events"""
        # Create summary message
        summary = f"Season Summary: {self.current_season}, Year {self.current_year}\n\n"
        
        # Add age update
        summary += f"You are now {int(self.player['age'])} years"
        months = int((self.player['age'] % 1) * 12)
        if months > 0:
            summary += f" and {months} months"
        summary += " old.\n\n"
        
        # Add wealth update
        summary += f"Your current wealth: {self.player['wealth']} gold\n\n"
        
        # Add family update if applicable
        if self.player.get("spouse"):
            spouse = self.player["spouse"]
            spouse_name = spouse["name"] if isinstance(spouse, dict) else spouse
            summary += f"Your spouse {spouse_name} is by your side.\n"
            
        if self.player.get("children") and len(self.player["children"]) > 0:
            summary += f"You have {len(self.player['children'])} children.\n"
        
        # Show dialog
        self.show_dialog(f"{self.current_season} Summary", summary)
    
    def advance_day(self):
        """Advance the game by one day"""
        # Update game state for a new day
        self.current_day += 1
        
        # Check for season change (every 30 days)
        if self.current_day % 30 == 0:
            self.advance_season()
            
        # Update UI elements
        self.update_status_bar()
        
        # Random events
        if random.random() < 0.2:  # 20% chance of an event each day
            self.generate_travel_event()
    
    def create_character_form(self):
        """Create the character creation form"""
        self.clear_screen()
        
        # Set up variables for form inputs
        self.name_var = tk.StringVar()
        self.gender_var = tk.StringVar()
        self.occupation_var = tk.StringVar()
        
        # Title
        title_label = tk.Label(self.main_container, text="Create Your Character", 
                              font=self.title_font, bg="#f0e6d2", fg="#5c4425")
        title_label.pack(pady=20)
        
        # Main form container
        form_frame = tk.Frame(self.main_container, bg="#f0e6d2", padx=20, pady=20)
        form_frame.pack(fill=tk.BOTH, expand=True)
        
        # Left side - character info inputs
        left_frame = tk.Frame(form_frame, bg="#f0e6d2")
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        # Name input
        name_frame = tk.Frame(left_frame, bg="#f0e6d2")
        name_frame.pack(fill=tk.X, pady=10)
        
        name_label = tk.Label(name_frame, text="Name:", font=self.header_font, bg="#f0e6d2", fg="#5c4425")
        name_label.pack(anchor=tk.W)
        
        name_entry = tk.Entry(name_frame, textvariable=self.name_var, font=self.text_font, width=30)
        name_entry.pack(fill=tk.X, pady=5)
        
        # Gender selection
        gender_frame = tk.Frame(left_frame, bg="#f0e6d2")
        gender_frame.pack(fill=tk.X, pady=10)
        
        gender_label = tk.Label(gender_frame, text="Gender:", font=self.header_font, bg="#f0e6d2", fg="#5c4425")
        gender_label.pack(anchor=tk.W)
        
        gender_options = ["Male", "Female"]
        for option in gender_options:
            rb = tk.Radiobutton(gender_frame, text=option, variable=self.gender_var, value=option,
                              font=self.text_font, bg="#f0e6d2", fg="#5c4425")
            rb.pack(anchor=tk.W)
        
        # Occupation selection
        occupation_frame = tk.Frame(left_frame, bg="#f0e6d2")
        occupation_frame.pack(fill=tk.X, pady=10)
        
        occupation_label = tk.Label(occupation_frame, text="Occupation:", font=self.header_font, bg="#f0e6d2", fg="#5c4425")
        occupation_label.pack(anchor=tk.W)
        
        occupations = ["King", "Noble", "Knight", "Merchant", "Tavern Owner", "Farmer", "Peasant"]
        for occupation in occupations:
            rb = tk.Radiobutton(occupation_frame, text=occupation, variable=self.occupation_var, value=occupation,
                              font=self.text_font, bg="#f0e6d2", fg="#5c4425",
                              command=lambda o=occupation: update_description(o))
            rb.pack(anchor=tk.W)
        
        # Right side - description and start button
        right_frame = tk.Frame(form_frame, bg="#e6d8bf", bd=2, relief=tk.RIDGE, padx=15, pady=15)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))
        
        # Description title
        desc_title = tk.Label(right_frame, text="Occupation Description", font=self.header_font, bg="#e6d8bf", fg="#5c4425")
        desc_title.pack(anchor=tk.W, pady=(0, 10))
        
        # Description text
        self.desc_text = tk.Text(right_frame, wrap=tk.WORD, width=40, height=15, 
                               font=self.text_font, bg="#e6d8bf", fg="#5c4425", bd=0)
        self.desc_text.pack(fill=tk.BOTH, expand=True)
        self.desc_text.insert(tk.END, "Select an occupation to see its description.")
        self.desc_text.config(state=tk.DISABLED)
        
        # Start button
        start_frame = tk.Frame(self.main_container, bg="#f0e6d2", pady=20)
        start_frame.pack(fill=tk.X)
        
        start_btn = tk.Button(start_frame, text="Start Your Journey", 
                            command=self.create_character,
                            **self.get_button_style("large"))
        start_btn.pack()
        
        # Back button
        back_btn = tk.Button(start_frame, text="Back to Menu", 
                           command=self.show_main_menu,
                           **self.get_button_style("medium"))
        start_btn.pack(side=tk.LEFT, padx=10)
        back_btn.pack(side=tk.RIGHT, padx=10)
        
        def update_description(*args):
            """Update the description text when an occupation is selected"""
            occupation = self.occupation_var.get()
            if occupation:
                description = self.get_occupation_description(occupation)
                self.desc_text.config(state=tk.NORMAL)
                self.desc_text.delete(1.0, tk.END)
                self.desc_text.insert(tk.END, description)
                self.desc_text.config(state=tk.DISABLED)
    
    def update_player_info(self):
        """Update the player information display in the top bar"""
        # Find the player info label in the top bar
        for widget in self.main_container.winfo_children():
            if isinstance(widget, tk.Frame) and widget.winfo_height() == 40:  # This is likely the top bar
                for child in widget.winfo_children():
                    if isinstance(child, tk.Label) and child.winfo_x() < 100:  # This is likely the player info label (on the left)
                        # Update the label text with current player info
                        child.config(text=f"{self.player['name']} - {self.player['occupation']} | Age: {self.player['age']} | Health: {self.player['health']} | Gold: {self.player['wealth']}")
                        break
                break
    
    def show_dialog(self, title, message):
        """Show a dialog box with a title and message"""
        dialog = tk.Toplevel(self.root)
        dialog.title(title)
        dialog.geometry("400x300")
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Make the dialog modal
        dialog.focus_set()
        
        # Add some padding
        frame = tk.Frame(dialog, padx=20, pady=20, bg="#f0e6d2")
        frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = tk.Label(frame, text=title, font=self.header_font, bg="#f0e6d2", fg="#5c4425")
        title_label.pack(pady=(0, 10))
        
        # Message
        message_text = tk.Text(frame, wrap=tk.WORD, width=40, height=10, font=self.text_font, bg="#f0e6d2", fg="#5c4425", bd=0)
        message_text.insert(tk.END, message)
        message_text.config(state=tk.DISABLED)
        message_text.pack(pady=10)
        
        # Close button
        close_button = tk.Button(frame, text="Close", **self.get_button_style("medium"), command=dialog.destroy)
        close_button.pack(pady=10)
        
        # Center the dialog on the parent window
        dialog.update_idletasks()
        width = dialog.winfo_width()
        height = dialog.winfo_height()
        x = self.root.winfo_x() + (self.root.winfo_width() // 2) - (width // 2)
        y = self.root.winfo_y() + (self.root.winfo_height() // 2) - (height // 2)
        dialog.geometry(f"{width}x{height}+{x}+{y}")
        
        return dialog
    
    def generate_seasonal_events(self):
        """Generate random events based on the current season"""
        # Define possible events for each season
        seasonal_events = {
            "Spring": [
                "The flowers are blooming and the fields are green.",
                "Spring rains have made the roads muddy and difficult to travel.",
                "A traveling fair has arrived in the area.",
                "Local farmers are busy planting their crops."
            ],
            "Summer": [
                "The summer heat is intense this year.",
                "A drought has affected local crops.",
                "The summer festival is being prepared in nearby towns.",
                "Merchants from distant lands have arrived with exotic goods."
            ],
            "Autumn": [
                "The harvest season is in full swing.",
                "The leaves are changing color, painting the landscape in gold and red.",
                "Preparations for winter have begun.",
                "A bountiful harvest has led to celebrations in the region."
            ],
            "Winter": [
                "Snow blankets the landscape, making travel difficult.",
                "The winter is harsh, and food supplies are dwindling.",
                "Winter festivities are being held to lift spirits during the cold months.",
                "A blizzard has struck the region, forcing people to stay indoors."
            ]
        }
        
        # Randomly decide if an event should occur (50% chance)
        if random.random() < 0.5:
            # Select a random event for the current season
            event = random.choice(seasonal_events[self.current_season])
            self.add_event(event)
            
            # For significant events, show a dialog (20% chance)
            if random.random() < 0.2:
                self.show_dialog(f"{self.current_season} Event", event)
    
    def update_date_display(self):
        """Update the date display in the top bar"""
        # Find the date info label in the top bar
        for widget in self.main_container.winfo_children():
            if isinstance(widget, tk.Frame) and widget.winfo_height() == 40:  # This is likely the top bar
                for child in widget.winfo_children():
                    if isinstance(child, tk.Label) and child.winfo_x() > 100:  # This is likely the date info label (on the right)
                        # Update the label text with current date
                        child.config(text=f"{self.current_season}, Year {self.current_year}")
                        break
                break
    
    def update_status_bar(self):
        """Update both player info and date display in the top bar"""
        self.update_player_info()
        self.update_date_display()
    
    def interact_with_spouse(self):
        """Interact with your spouse with various options"""
        if not self.player.get("spouse"):
            self.show_dialog("Family", "You are not married. Perhaps you should find a spouse first?")
            return
            
        spouse = self.player["spouse"]
        
        # Create dialog for spouse interaction
        dialog = tk.Toplevel(self.root)
        dialog.title(f"Interact with {spouse['name']}")
        dialog.geometry("500x400")
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Make the dialog modal
        dialog.focus_set()
        
        # Add some padding
        frame = tk.Frame(dialog, padx=20, pady=20, bg="#f0e6d2")
        frame.pack(fill=tk.BOTH, expand=True)
        
        # Spouse info
        title_label = tk.Label(frame, text=f"Your Spouse: {spouse['name']}", font=self.header_font, bg="#f0e6d2", fg="#5c4425")
        title_label.pack(pady=(0, 10))
        
        # Relationship status
        relationship = spouse.get("relationship", 50)
        relationship_text = "Loving" if relationship > 75 else "Good" if relationship > 50 else "Neutral" if relationship > 25 else "Poor"
        relationship_label = tk.Label(frame, text=f"Relationship: {relationship_text} ({relationship}/100)", font=self.text_font, bg="#f0e6d2", fg="#5c4425")
        relationship_label.pack(pady=5)
        
        # Spouse traits
        traits_text = ", ".join(spouse.get("traits", []))
        traits_label = tk.Label(frame, text=f"Traits: {traits_text}", font=self.text_font, bg="#f0e6d2", fg="#5c4425")
        traits_label.pack(pady=5)
        
        # Interaction options
        options_frame = tk.Frame(frame, bg="#f0e6d2")
        options_frame.pack(pady=20, fill=tk.X)
        
        # Conversation button
        converse_btn = tk.Button(options_frame, text="Have a Conversation", 
                               **self.get_button_style("medium"),
                               command=lambda: self.spouse_conversation(spouse, dialog))
        converse_btn.pack(pady=5, fill=tk.X)
        
        # Gift button
        gift_btn = tk.Button(options_frame, text="Give a Gift", 
                           **self.get_button_style("medium"),
                           command=lambda: self.give_spouse_gift(spouse, dialog))
        gift_btn.pack(pady=5, fill=tk.X)
        
        # Go on outing button
        outing_btn = tk.Button(options_frame, text="Go on an Outing", 
                             **self.get_button_style("medium"),
                             command=lambda: self.spouse_outing(spouse, dialog))
        outing_btn.pack(pady=5, fill=tk.X)
        
        # Have child button (if no children or less than 5)
        if len(self.player.get("children", [])) < 5:
            child_btn = tk.Button(options_frame, text="Try for a Child", 
                                **self.get_button_style("medium"),
                                command=lambda: self.try_for_child(spouse, dialog))
            child_btn.pack(pady=5, fill=tk.X)
        
        # Close button
        close_button = tk.Button(frame, text="Back", **self.get_button_style("medium"), command=dialog.destroy)
        close_button.pack(pady=10)
    
    def spouse_conversation(self, spouse, parent_dialog):
        """Have a conversation with your spouse"""
        # Topics based on spouse traits
        topics = [
            "Discuss the future",
            "Talk about the kingdom",
            "Share stories from your past",
            "Discuss local gossip",
            "Talk about your feelings"
        ]
        
        # Add trait-specific topics
        if "ambitious" in spouse.get("traits", []):
            topics.append("Discuss plans for advancement")
        if "pious" in spouse.get("traits", []):
            topics.append("Discuss religious matters")
        if "kind" in spouse.get("traits", []):
            topics.append("Talk about helping others")
        
        # Create dialog for conversation
        dialog = tk.Toplevel(parent_dialog)
        dialog.title(f"Conversation with {spouse['name']}")
        dialog.geometry("450x350")
        dialog.transient(parent_dialog)
        dialog.grab_set()
        
        # Make the dialog modal
        dialog.focus_set()
        
        # Add some padding
        frame = tk.Frame(dialog, padx=20, pady=20, bg="#f0e6d2")
        frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = tk.Label(frame, text="Choose a Conversation Topic", font=self.header_font, bg="#f0e6d2", fg="#5c4425")
        title_label.pack(pady=(0, 20))
        
        # Topic buttons
        for topic in topics:
            topic_btn = tk.Button(frame, text=topic, 
                                **self.get_button_style("medium"),
                                command=lambda t=topic: self.handle_spouse_conversation(spouse, t, dialog))
            topic_btn.pack(pady=5, fill=tk.X)
        
        # Close button
        close_button = tk.Button(frame, text="Back", **self.get_button_style("medium"), command=dialog.destroy)
        close_button.pack(pady=10)
    
    def handle_spouse_conversation(self, spouse, topic, dialog):
        """Handle the outcome of a conversation with spouse"""
        dialog.destroy()
        
        # Get spouse traits for personalized responses
        traits = spouse.get("traits", [])
        
        # Responses based on topic and traits
        responses = {
            "Discuss the future": {
                "ambitious": "Your spouse excitedly shares their grand plans for your future together.",
                "content": "Your spouse seems happy with your current life, but is open to small changes.",
                "default": "You and your spouse discuss your hopes and dreams for the future."
            },
            "Talk about the kingdom": {
                "loyal": "Your spouse speaks highly of the current ruler and their policies.",
                "treacherous": "Your spouse whispers about the weaknesses of the current leadership.",
                "default": "You and your spouse discuss recent events in the kingdom."
            },
            "Share stories from your past": {
                "brave": "Your spouse tells exciting tales of adventure from their youth.",
                "default": "You and your spouse reminisce about your lives before you met."
            },
            "Discuss local gossip": {
                "deceitful": "Your spouse seems to know all the scandalous secrets of the local nobility.",
                "honest": "Your spouse seems uncomfortable discussing rumors about others.",
                "default": "You and your spouse share interesting tidbits you've heard around town."
            },
            "Talk about your feelings": {
                "kind": "Your spouse listens attentively and offers comforting words.",
                "cruel": "Your spouse seems disinterested in your emotional state.",
                "default": "You and your spouse have a heart-to-heart conversation."
            },
            "Discuss plans for advancement": {
                "default": "Your spouse shares ambitious ideas about how you could improve your standing."
            },
            "Discuss religious matters": {
                "default": "You and your spouse discuss matters of faith and spirituality."
            },
            "Talk about helping others": {
                "default": "Your spouse suggests ways you could help those less fortunate in your community."
            }
        }
        
        # Get appropriate response
        response = "You have a pleasant conversation with your spouse."
        for trait in traits:
            if trait in responses.get(topic, {}) and random.random() < 0.7:
                response = responses[topic][trait]
                break
        else:
            if "default" in responses.get(topic, {}):
                response = responses[topic]["default"]
        
        # Relationship change based on compatibility of topic and traits
        relationship_change = 0
        if topic == "Discuss plans for advancement" and "ambitious" in traits:
            relationship_change = random.randint(5, 10)
        elif topic == "Discuss religious matters" and "pious" in traits:
            relationship_change = random.randint(5, 10)
        elif topic == "Talk about helping others" and "kind" in traits:
            relationship_change = random.randint(5, 10)
        elif topic == "Talk about your feelings" and "cruel" in traits:
            relationship_change = random.randint(-5, -2)
        else:
            relationship_change = random.randint(1, 5)
        
        # Update relationship
        spouse["relationship"] = min(100, max(0, spouse.get("relationship", 50) + relationship_change))
        
        # Show result
        result_message = f"{response}\n\n"
        if relationship_change > 0:
            result_message += f"Your relationship with {spouse['name']} has improved."
        elif relationship_change < 0:
            result_message += f"Your relationship with {spouse['name']} has slightly deteriorated."
        else:
            result_message += f"Your relationship with {spouse['name']} remains unchanged."
        
        self.add_event(f"You had a conversation with your spouse about {topic.lower()}.")
        self.show_dialog("Conversation Result", result_message)
    
    def give_spouse_gift(self, spouse, parent_dialog):
        """Give a gift to your spouse"""
        # Check if player has enough money
        if self.player["wealth"] < 5:
            self.show_dialog("Gift", "You don't have enough money to buy a gift.")
            return
            
        # Create gift options based on price
        gifts = [
            {"name": "Flowers", "cost": 5, "value": 5},
            {"name": "Sweets", "cost": 10, "value": 10},
            {"name": "Book", "cost": 20, "value": 15},
            {"name": "Jewelry", "cost": 50, "value": 25},
            {"name": "Fine Clothing", "cost": 100, "value": 40}
        ]
        
        # Filter gifts based on player's wealth
        affordable_gifts = [gift for gift in gifts if gift["cost"] <= self.player["wealth"]]
        
        # Create dialog for gift selection
        dialog = tk.Toplevel(parent_dialog)
        dialog.title("Give a Gift")
        dialog.geometry("450x400")
        dialog.transient(parent_dialog)
        dialog.grab_set()
        
        # Make the dialog modal
        dialog.focus_set()
        
        # Add some padding
        frame = tk.Frame(dialog, padx=20, pady=20, bg="#f0e6d2")
        frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = tk.Label(frame, text="Choose a Gift", font=self.header_font, bg="#f0e6d2", fg="#5c4425")
        title_label.pack(pady=(0, 10))
        
        # Player's wealth
        wealth_label = tk.Label(frame, text=f"Your Gold: {self.player['wealth']}", font=self.text_font, bg="#f0e6d2", fg="#5c4425")
        wealth_label.pack(pady=(0, 20))
        
        # Gift options
        for gift in affordable_gifts:
            gift_frame = tk.Frame(frame, bg="#e6d8bf", bd=1, relief=tk.RIDGE)
            gift_frame.pack(fill=tk.X, pady=5)
            
            gift_name = tk.Label(gift_frame, text=gift["name"], font=self.text_font, bg="#e6d8bf", fg="#5c4425")
            gift_name.pack(side=tk.LEFT, padx=10, pady=5)
            
            gift_cost = tk.Label(gift_frame, text=f"Cost: {gift['cost']} gold", font=self.small_font, bg="#e6d8bf", fg="#5c4425")
            gift_cost.pack(side=tk.LEFT, padx=10, pady=5)
            
            buy_btn = tk.Button(gift_frame, text="Give", 
                              **self.get_button_style("small"),
                              command=lambda g=gift: self.handle_gift_giving(spouse, g, dialog))
            buy_btn.pack(side=tk.RIGHT, padx=10, pady=5)
        
        # Close button
        close_button = tk.Button(frame, text="Back", **self.get_button_style("medium"), command=dialog.destroy)
        close_button.pack(pady=10)
    
    def handle_gift_giving(self, spouse, gift, dialog):
        """Handle the outcome of giving a gift"""
        dialog.destroy()
        
        # Deduct cost
        self.player["wealth"] -= gift["cost"]
        
        # Get spouse traits for personalized responses
        traits = spouse.get("traits", [])
        
        # Base relationship increase
        relationship_increase = gift["value"]
        
        # Adjust based on traits
        if "content" in traits and gift["name"] in ["Flowers", "Sweets"]:
            relationship_increase += 5
            response = f"{spouse['name']} is delighted with the simple but thoughtful gift."
        elif "ambitious" in traits and gift["name"] in ["Jewelry", "Fine Clothing"]:
            relationship_increase += 10
            response = f"{spouse['name']} is impressed by your generous and luxurious gift."
        elif "pious" in traits and gift["name"] == "Book":
            relationship_increase += 5
            response = f"{spouse['name']} appreciates the gift of knowledge and wisdom."
        else:
            response = f"{spouse['name']} thanks you for the {gift['name'].lower()}."
        
        # Update relationship
        spouse["relationship"] = min(100, max(0, spouse.get("relationship", 50) + relationship_increase))
        
        # Show result
        result_message = f"{response}\n\n"
        result_message += f"Your relationship with {spouse['name']} has improved."
        
        self.add_event(f"You gave {spouse['name']} a gift of {gift['name'].lower()}.")
        self.show_dialog("Gift Result", result_message)
        self.update_player_info()  # Update gold display
    
    def spouse_outing(self, spouse, parent_dialog):
        """Go on an outing with your spouse"""
        # Check if player has enough money
        if self.player["wealth"] < 10:
            self.show_dialog("Outing", "You don't have enough money to go on an outing.")
            return
            
        # Create outing options
        outings = [
            {"name": "Walk in the countryside", "cost": 0, "value": 5},
            {"name": "Visit the local market", "cost": 10, "value": 10},
            {"name": "Attend a festival", "cost": 25, "value": 15},
            {"name": "Dine at a tavern", "cost": 40, "value": 20},
            {"name": "Attend a royal tournament", "cost": 75, "value": 30}
        ]
        
        # Filter outings based on player's wealth
        affordable_outings = [outing for outing in outings if outing["cost"] <= self.player["wealth"]]
        
        # Create dialog for outing selection
        dialog = tk.Toplevel(parent_dialog)
        dialog.title("Go on an Outing")
        dialog.geometry("450x400")
        dialog.transient(parent_dialog)
        dialog.grab_set()
        
        # Make the dialog modal
        dialog.focus_set()
        
        # Add some padding
        frame = tk.Frame(dialog, padx=20, pady=20, bg="#f0e6d2")
        frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = tk.Label(frame, text="Choose an Outing", font=self.header_font, bg="#f0e6d2", fg="#5c4425")
        title_label.pack(pady=(0, 10))
        
        # Player's wealth
        wealth_label = tk.Label(frame, text=f"Your Gold: {self.player['wealth']}", font=self.text_font, bg="#f0e6d2", fg="#5c4425")
        wealth_label.pack(pady=(0, 20))
        
        # Outing options
        for outing in affordable_outings:
            outing_frame = tk.Frame(frame, bg="#e6d8bf", bd=1, relief=tk.RIDGE)
            outing_frame.pack(fill=tk.X, pady=5)
            
            outing_name = tk.Label(outing_frame, text=outing["name"], font=self.text_font, bg="#e6d8bf", fg="#5c4425")
            outing_name.pack(side=tk.LEFT, padx=10, pady=5)
            
            outing_cost = tk.Label(outing_frame, text=f"Cost: {outing['cost']} gold", font=self.small_font, bg="#e6d8bf", fg="#5c4425")
            outing_cost.pack(side=tk.LEFT, padx=10, pady=5)
            
            select_btn = tk.Button(outing_frame, text="Select", 
                                 **self.get_button_style("small"),
                                 command=lambda o=outing: self.handle_spouse_outing(spouse, o, dialog))
            select_btn.pack(side=tk.RIGHT, padx=10, pady=5)
        
        # Close button
        close_button = tk.Button(frame, text="Back", **self.get_button_style("medium"), command=dialog.destroy)
        close_button.pack(pady=10)
    
    def handle_spouse_outing(self, spouse, outing, dialog):
        """Handle the outcome of going on an outing with spouse"""
        dialog.destroy()
        
        # Deduct cost
        self.player["wealth"] -= outing["cost"]
        
        # Get spouse traits for personalized responses
        traits = spouse.get("traits", [])
        
        # Base relationship increase
        relationship_increase = outing["value"]
        
        # Possible events during outing
        outing_events = [
            {"description": "You have a wonderful time together.", "rel_mod": 2},
            {"description": "The weather is perfect for your outing.", "rel_mod": 1},
            {"description": "You encounter some interesting people during your outing.", "rel_mod": 0},
            {"description": "A small mishap occurs, but you laugh it off together.", "rel_mod": -1},
            {"description": "The outing doesn't go quite as planned, but you make the best of it.", "rel_mod": -2}
        ]
        
        # Select a random event
        event = random.choice(outing_events)
        
        # Adjust based on traits and outing type
        if "brave" in traits and outing["name"] == "Attend a royal tournament":
            relationship_increase += 5
            response = f"{spouse['name']} is thrilled by the excitement of the tournament."
        elif "kind" in traits and outing["name"] == "Walk in the countryside":
            relationship_increase += 5
            response = f"{spouse['name']} enjoys the peaceful time spent in nature with you."
        elif "ambitious" in traits and outing["name"] in ["Attend a royal tournament", "Dine at a tavern"]:
            relationship_increase += 5
            response = f"{spouse['name']} appreciates the opportunity to be seen in society."
        else:
            response = f"You and {spouse['name']} enjoy your time {outing['name'].lower()}."
        
        # Apply event modifier
        relationship_increase += event["rel_mod"]
        
        # Update relationship
        spouse["relationship"] = min(100, max(0, spouse.get("relationship", 50) + relationship_increase))
        
        # Show result
        result_message = f"{response}\n\n{event['description']}\n\n"
        if relationship_increase > 0:
            result_message += f"Your relationship with {spouse['name']} has improved."
        elif relationship_increase < 0:
            result_message += f"Your relationship with {spouse['name']} has slightly deteriorated."
        else:
            result_message += f"Your relationship with {spouse['name']} remains unchanged."
        
        self.add_event(f"You went on an outing with {spouse['name']} to {outing['name'].lower()}.")
        self.show_dialog("Outing Result", result_message)
        self.update_player_info()  # Update gold display
    
    def try_for_child(self, spouse, parent_dialog):
        """Try to have a child with your spouse"""
        parent_dialog.destroy()
        
        # Check relationship level - better relationship means higher chance
        relationship = spouse.get("relationship", 50)
        base_chance = 0.3  # 30% base chance
        relationship_bonus = relationship / 200  # Up to +25% for 100 relationship
        
        # Calculate success chance
        success_chance = min(0.8, base_chance + relationship_bonus)  # Cap at 80%
        
        # Determine outcome
        if random.random() < success_chance:
            # Success! Create a child
            child_gender = random.choice(["male", "female"])
            child_name = self.generate_name(child_gender)
            
            # Create child data
            child = {
                "name": child_name,
                "gender": child_gender,
                "age": 0,
                "traits": self.generate_traits(),  # Inherit some traits
                "relationship": 100  # Children start with max relationship
            }
            
            # Add child to player's children
            if "children" not in self.player:
                self.player["children"] = []
            
            self.player["children"].append(child)
            
            # Create success message
            if child_gender == "male":
                message = f"Congratulations! Your wife has given birth to a healthy baby boy named {child_name}."
            else:
                message = f"Congratulations! Your wife has given birth to a healthy baby girl named {child_name}."
                
            # Add event
            self.add_event(f"Your child {child_name} was born.")
            
            # Improve relationship with spouse
            spouse["relationship"] = min(100, spouse.get("relationship", 50) + 10)
            
            # Show dialog
            self.show_dialog("New Child", message)
        else:
            # No child this time
            message = "Despite your efforts, your wife does not become pregnant at this time."
            self.show_dialog("Family Planning", message)
    
    def generate_name(self, gender):
        """Generate a random medieval name based on gender"""
        male_names = [
            "William", "Robert", "John", "Richard", "Thomas", "Henry", "Edward", "Walter",
            "Hugh", "Simon", "Geoffrey", "Adam", "Stephen", "Peter", "Nicholas", "Roger",
            "Bartholomew", "Gilbert", "Martin", "Ralph", "Edmund", "Philip", "Gregory"
        ]
        
        female_names = [
            "Alice", "Agnes", "Matilda", "Margaret", "Joan", "Isabella", "Emma", "Cecilia",
            "Eleanor", "Beatrice", "Juliana", "Katherine", "Margery", "Edith", "Mabel",
            "Constance", "Avice", "Johanna", "Elizabeth", "Amice", "Eloise", "Philippa"
        ]
        
        if gender == "male":
            return random.choice(male_names)
        else:
            return random.choice(female_names)
    
    