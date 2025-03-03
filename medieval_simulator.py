import tkinter as tk
from tkinter import ttk, messagebox, font, simpledialog
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
        
        # UI colors
        self.bg_color = "#f0e6d2"  # Original light beige background
        self.text_color = "#5c4425"  # Original brown text
        self.root.configure(bg=self.bg_color)
        
        # Game data
        self.player = None
        self.world = None
        self.current_location = None
        self.current_year = 1200
        self.current_season = "Spring"
        self.seasons = ["Spring", "Summer", "Autumn", "Winter"]
        self.season_index = 0
        self.current_day = 1
        self.event_log = []
        
        # Create a main container for all screens
        self.main_container = tk.Frame(self.root, bg=self.bg_color)
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
        elif size == "family":
            return {"font": ("Times New Roman", 14, "bold"), "bg": "#8b4513", "fg": "white", 
                    "width": 15, "height": 1, "bd": 3, "relief": tk.RAISED}
    
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
        """Update the event log display with all events"""
        # Check if event_log widget exists
        if not hasattr(self, 'event_log'):
            return
            
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
        """Return a description for the selected occupation"""
        descriptions = {
            "King": "As King, you rule over your own kingdom with absolute authority. Your wealth is unmatched, but the responsibilities are heavy. You must manage relations with nobles, defend against rival kingdoms, and ensure your subjects remain loyal. Your decisions will shape the fate of thousands.\n\nStarting wealth: Very High\nKey skills: Leadership, Politics, Warfare",
            
            "Noble": "Born into privilege as a Noble, you own vast lands and command respect wherever you go. You have significant influence in court politics and can leverage your family connections. However, you must maintain your status through strategic marriages and alliances.\n\nStarting wealth: High\nKey skills: Etiquette, Politics, Management",
            
            "Knight": "As a Knight, you've sworn oaths of loyalty and chivalry. You're skilled in combat and respected for your honor. You may serve a lord directly or be a wandering knight seeking glory in tournaments and battle. Your martial prowess is your greatest asset.\n\nStarting wealth: Medium\nKey skills: Combat, Riding, Leadership",
            
            "Merchant": "The life of a Merchant is one of opportunity and risk. You travel between towns and cities, buying low and selling high. With shrewd deals and careful investment, you could amass a fortune to rival the nobility. Your network of contacts is as valuable as your coin.\n\nStarting wealth: Medium-High\nKey skills: Bargaining, Mathematics, Persuasion",
            
            "Tavern Owner": "As a Tavern Owner, you're at the heart of the community. Your establishment is where people gather to drink, gossip, and find respite from their daily toils. You hear all the local news and rumors, making you surprisingly well-informed about the goings-on in your area.\n\nStarting wealth: Medium\nKey skills: Brewing, Cooking, Socializing",
            
            "Farmer": "The honest life of a Farmer is one of hard work and connection to the land. You grow crops and raise animals to feed yourself and sell at market. While not wealthy, you have independence and the satisfaction of living by the fruits of your labor. Your fortunes rise and fall with the seasons.\n\nStarting wealth: Low-Medium\nKey skills: Agriculture, Animal Husbandry, Crafting",
            
            "Peasant": "As a humble Peasant, you begin with little but your determination. You work the land owned by others and struggle to make ends meet. However, your simple origins mean you're resourceful and hardy. With cunning and perseverance, you might rise above your station.\n\nStarting wealth: Low\nKey skills: Survival, Labor, Foraging"
        }
        
        return descriptions.get(occupation, "Select an occupation to see its description.")
    
    def create_character(self):
        """Create a new character based on form inputs"""
        # Get form values
        name = self.name_var.get().strip()
        gender = self.gender_var.get()
        occupation = self.occupation_var.get()
        
        # Validate inputs
        if not name:
            messagebox.showerror("Error", "Please enter a name for your character.")
            return
            
        if not gender:
            messagebox.showerror("Error", "Please select a gender for your character.")
            return
            
        if not occupation:
            messagebox.showerror("Error", "Please select an occupation for your character.")
            return
        
        # Create player data
        self.player = {
            "name": name,
            "gender": gender.lower(),
            "occupation": occupation,
            "age": random.randint(18, 30),
            "health": 100,
            "wealth": self.get_starting_wealth(occupation),
            "skills": self.generate_skills(occupation),
            "traits": self.generate_traits(),
            "inventory": [],
            "equipment": {},
            "spouse": None,
            "children": [],
            "events": []  # Initialize events list
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
        initial_message = f"You begin your life as a {occupation} in {self.current_location}."
        self.add_event(initial_message)
        
        # Show game interface
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
        
        # Location info
        location_label = tk.Label(left_panel, text="Location", font=self.header_font, bg="#e6d8bf", fg="#5c4425")
        location_label.pack(pady=(10, 5))
        
        location_type = self.get_location_type(self.current_location)
        kingdom = self.get_kingdom_for_location(self.current_location)
        
        location_info = tk.Label(left_panel, text=f"{self.current_location}\n{location_type} in {kingdom}", 
                               font=self.small_font, bg="#e6d8bf", fg="#5c4425", justify=tk.LEFT)
        location_info.pack(pady=(0, 10))
        
        # Separator
        ttk.Separator(left_panel, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=10, padx=10)
        
        # Quick stats
        stats_label = tk.Label(left_panel, text="Skills", font=self.header_font, bg="#e6d8bf", fg="#5c4425")
        stats_label.pack(pady=(10, 5))
        
        # Show main skills based on occupation
        self.display_key_skills(left_panel)
        
        # Action buttons
        actions_label = tk.Label(left_panel, text="Actions", font=self.header_font, bg="#e6d8bf", fg="#5c4425")
        actions_label.pack(pady=(20, 5))
        
        # Travel button
        travel_btn = tk.Button(left_panel, text="Travel", 
                             **self.get_button_style("medium"),
                             command=self.show_travel_options)
        travel_btn.pack(pady=5)
        
        # Market button
        market_btn = tk.Button(left_panel, text="Visit Market", 
                             **self.get_button_style("medium"),
                             command=self.show_market)
        market_btn.pack(pady=5)
        
        # End Season button
        end_season_btn = tk.Button(left_panel, text="End Season", 
                                 **self.get_button_style("medium"),
                                 command=self.advance_season)
        end_season_btn.pack(pady=5)
        
        # Center panel - main game area
        center_panel = tk.Frame(main_area, bg="#f0e6d2", bd=2, relief=tk.RIDGE)
        center_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        # Location description
        desc_frame = tk.Frame(center_panel, bg="#f0e6d2", padx=15, pady=15)
        desc_frame.pack(fill=tk.X)
        
        desc_title = tk.Label(desc_frame, text=f"{self.current_location}", font=self.header_font, bg="#f0e6d2", fg="#5c4425")
        desc_title.pack(anchor=tk.W)
        
        location_desc = self.get_location_description()
        desc_text = tk.Label(desc_frame, text=location_desc, font=self.text_font, bg="#f0e6d2", fg="#5c4425", 
                           justify=tk.LEFT, wraplength=500)
        desc_text.pack(fill=tk.X, pady=(10, 0))
        
        # Action buttons
        action_frame = tk.Frame(center_panel, bg="#f0e6d2", padx=15, pady=15)
        action_frame.pack(fill=tk.X)
        
        action_title = tk.Label(action_frame, text="Available Actions", font=self.header_font, bg="#f0e6d2", fg="#5c4425")
        action_title.pack(anchor=tk.W, pady=(0, 10))
        
        # Create action buttons based on location and occupation
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
        """Create action buttons based on location and occupation"""
        # Common actions for all occupations
        common_actions = ["Rest", "Explore"]
        
        # Occupation-specific actions
        occupation_actions = {
            "King": ["Hold Court", "Collect Taxes", "Make Decree"],
            "Noble": ["Collect Rent", "Host Feast", "Attend Court"],
            "Knight": ["Train", "Patrol", "Enter Tournament"],
            "Merchant": ["Trade", "Negotiate", "Invest"],
            "Tavern Owner": ["Serve Drinks", "Hire Bard", "Listen to Gossip"],
            "Farmer": ["Tend Crops", "Harvest", "Sell Produce"],
            "Peasant": ["Work", "Forage", "Beg"]
        }
        
        # Get actions for current occupation
        occupation = self.player["occupation"]
        actions = common_actions + occupation_actions.get(occupation, [])
        
        # Create a frame for the buttons
        buttons_frame = tk.Frame(parent_frame, bg="#f0e6d2")
        buttons_frame.pack(fill=tk.X)
        
        # Create buttons in a grid layout
        row, col = 0, 0
        for action in actions:
            btn = tk.Button(buttons_frame, text=action, 
                          **self.get_button_style("small"),
                          command=lambda a=action: self.perform_action(a))
            btn.grid(row=row, column=col, padx=5, pady=5, sticky="w")
            
            # Update row and column for next button
            col += 1
            if col > 2:  # 3 buttons per row
                col = 0
                row += 1
    
    def perform_action(self, action):
        """Handle player actions"""
        # Common actions
        if action == "Rest":
            self.add_event("You take some time to rest and recover.")
            self.player["health"] = min(100, self.player["health"] + 10)
            messagebox.showinfo("Rest", "You feel refreshed. Health increased by 10 points.")
            
        elif action == "Explore":
            self.add_event(f"You explore the area around {self.current_location}.")
            # Random chance to find something
            if random.random() < 0.3:  # 30% chance
                gold_found = random.randint(5, 20)
                self.player["wealth"] += gold_found
                self.add_event(f"You found {gold_found} gold while exploring!")
                messagebox.showinfo("Exploration", f"You explored the area and found {gold_found} gold!")
            else:
                messagebox.showinfo("Exploration", "You explored the area but found nothing of interest.")
        
        # King actions
        elif action == "Hold Court":
            self.add_event("You held court, listening to petitions from your subjects.")
            messagebox.showinfo("Hold Court", "You held court and made several important decisions.")
            
        elif action == "Collect Taxes":
            tax_amount = random.randint(100, 300)
            self.player["wealth"] += tax_amount
            self.add_event(f"You collected {tax_amount} gold in taxes.")
            messagebox.showinfo("Taxes", f"You collected {tax_amount} gold in taxes from your kingdom.")
            
        elif action == "Make Decree":
            self.add_event("You issued a royal decree.")
            messagebox.showinfo("Decree", "Your decree has been announced throughout the kingdom.")
        
        # Noble actions
        elif action == "Collect Rent":
            rent_amount = random.randint(50, 150)
            self.player["wealth"] += rent_amount
            self.add_event(f"You collected {rent_amount} gold in rent from your lands.")
            messagebox.showinfo("Rent", f"You collected {rent_amount} gold in rent from your tenants.")
            
        elif action == "Host Feast":
            cost = random.randint(30, 80)
            if self.player["wealth"] >= cost:
                self.player["wealth"] -= cost
                self.add_event(f"You hosted a feast for {cost} gold. Your reputation has improved.")
                messagebox.showinfo("Feast", "Your feast was a success! Your reputation has improved.")
            else:
                messagebox.showerror("Insufficient Funds", "You don't have enough gold to host a feast.")
                
        elif action == "Attend Court":
            self.add_event("You attended court at the royal palace.")
            messagebox.showinfo("Court", "You attended court and made valuable connections.")
        
        # Knight actions
        elif action == "Train":
            self.add_event("You spent time training your combat skills.")
            if "Combat" in self.player["skills"]:
                self.player["skills"]["Combat"] += 1
            messagebox.showinfo("Training", "Your combat skills have improved.")
            
        elif action == "Patrol":
            self.add_event("You patrolled the area, keeping it safe.")
            patrol_pay = random.randint(10, 30)
            self.player["wealth"] += patrol_pay
            messagebox.showinfo("Patrol", f"You completed your patrol and earned {patrol_pay} gold.")
            
        elif action == "Enter Tournament":
            tournament_fee = 50
            if self.player["wealth"] >= tournament_fee:
                self.player["wealth"] -= tournament_fee
                self.add_event(f"You entered a tournament for {tournament_fee} gold.")
                
                # Determine outcome based on Combat skill
                combat_skill = self.player["skills"].get("Combat", 0)
                success_chance = 0.3 + (combat_skill * 0.05)  # Base 30% + 5% per skill level
                
                if random.random() < success_chance:
                    prize = random.randint(80, 200)
                    self.player["wealth"] += prize
                    self.add_event(f"You won the tournament and earned {prize} gold!")
                    messagebox.showinfo("Tournament Victory", f"You won the tournament and earned {prize} gold!")
                else:
                    self.add_event("You were defeated in the tournament.")
                    messagebox.showinfo("Tournament Defeat", "You fought well but were defeated in the tournament.")
            else:
                messagebox.showerror("Insufficient Funds", "You don't have enough gold to enter the tournament.")
        
        # Merchant actions
        elif action == "Trade":
            trade_profit = random.randint(20, 60)
            self.player["wealth"] += trade_profit
            self.add_event(f"You conducted trade and earned {trade_profit} gold.")
            messagebox.showinfo("Trade", f"Your trading was successful. You earned {trade_profit} gold.")
            
        elif action == "Negotiate":
            self.add_event("You negotiated better prices for your goods.")
            if "Bargaining" in self.player["skills"]:
                self.player["skills"]["Bargaining"] += 1
            messagebox.showinfo("Negotiation", "Your bargaining skills have improved.")
            
        elif action == "Invest":
            investment_amount = simpledialog.askinteger("Investment", "How much gold would you like to invest?", 
                                                      minvalue=10, maxvalue=self.player["wealth"])
            if investment_amount:
                if self.player["wealth"] >= investment_amount:
                    self.player["wealth"] -= investment_amount
                    self.add_event(f"You invested {investment_amount} gold in a business venture.")
                    messagebox.showinfo("Investment", "Your investment will yield returns in the future.")
                else:
                    messagebox.showerror("Insufficient Funds", "You don't have enough gold for this investment.")
        
        # Tavern Owner actions
        elif action == "Serve Drinks":
            earnings = random.randint(15, 40)
            self.player["wealth"] += earnings
            self.add_event(f"You served drinks at your tavern and earned {earnings} gold.")
            messagebox.showinfo("Tavern Business", f"You earned {earnings} gold from serving drinks.")
            
        elif action == "Hire Bard":
            bard_cost = 30
            if self.player["wealth"] >= bard_cost:
                self.player["wealth"] -= bard_cost
                self.add_event(f"You hired a bard for {bard_cost} gold to entertain your customers.")
                
                # Chance for increased business
                if random.random() < 0.7:  # 70% chance
                    bonus = random.randint(40, 70)
                    self.player["wealth"] += bonus
                    self.add_event(f"The bard attracted more customers, earning you an extra {bonus} gold!")
                    messagebox.showinfo("Bard Performance", f"The bard's performance was a hit! You earned an extra {bonus} gold.")
                else:
                    messagebox.showinfo("Bard Performance", "The bard's performance was average. Your customers were entertained.")
            else:
                messagebox.showerror("Insufficient Funds", "You don't have enough gold to hire a bard.")
                
        elif action == "Listen to Gossip":
            self.add_event("You listened to gossip from your tavern patrons.")
            messagebox.showinfo("Gossip", "You overheard interesting rumors and gossip from your patrons.")
        
        # Farmer actions
        elif action == "Tend Crops":
            self.add_event("You spent time tending to your crops.")
            if "Agriculture" in self.player["skills"]:
                self.player["skills"]["Agriculture"] += 1
            messagebox.showinfo("Farming", "Your agricultural skills have improved.")
            
        elif action == "Harvest":
            if self.current_season in ["Summer", "Fall"]:
                harvest_amount = random.randint(20, 50)
                self.player["wealth"] += harvest_amount
                self.add_event(f"You harvested your crops and earned {harvest_amount} gold at the market.")
                messagebox.showinfo("Harvest", f"Your harvest was successful! You earned {harvest_amount} gold.")
            else:
                self.add_event("It's not the right season for harvesting.")
                messagebox.showinfo("Harvest", "It's not the right season for harvesting. Try again in Summer or Fall.")
                
        elif action == "Sell Produce":
            earnings = random.randint(10, 30)
            self.player["wealth"] += earnings
            self.add_event(f"You sold some of your produce at the market for {earnings} gold.")
            messagebox.showinfo("Market", f"You sold your produce and earned {earnings} gold.")
        
        # Peasant actions
        elif action == "Work":
            earnings = random.randint(5, 15)
            self.player["wealth"] += earnings
            self.add_event(f"You worked hard and earned {earnings} gold.")
            messagebox.showinfo("Work", f"You worked hard and earned {earnings} gold.")
            
        elif action == "Forage":
            self.add_event("You foraged in the nearby woods for food and resources.")
            if random.random() < 0.4:  # 40% chance
                forage_amount = random.randint(3, 10)
                self.player["wealth"] += forage_amount
                self.add_event(f"You found items worth {forage_amount} gold while foraging!")
                messagebox.showinfo("Foraging", f"You found valuable herbs and mushrooms worth {forage_amount} gold!")
            else:
                messagebox.showinfo("Foraging", "You found some food for yourself, but nothing of significant value.")
                
        elif action == "Beg":
            earnings = random.randint(1, 8)
            self.player["wealth"] += earnings
            self.add_event(f"You begged on the streets and received {earnings} gold in charity.")
            messagebox.showinfo("Begging", f"You received {earnings} gold in charity.")
        
        # Default case
        else:
            self.add_event(f"You performed the action: {action}")
            messagebox.showinfo("Action", f"You performed: {action}")
        
        # Update player info display
        self.update_player_info()
    
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
            
            # Buttons frame
            spouse_buttons_frame = tk.Frame(spouse_frame, bg="#e6d8bf")
            spouse_buttons_frame.pack(fill=tk.X, pady=5)
            
            # Interact button
            interact_btn = tk.Button(spouse_buttons_frame, text="Interact with Spouse", 
                                   **self.get_button_style("medium"),
                                   command=lambda: self.interact_with_spouse_from_family(dialog))
            interact_btn.pack(side=tk.LEFT, padx=5)
            
            # Try for child button - direct access
            try_child_btn = tk.Button(spouse_buttons_frame, text="Try for Child", 
                                    **self.get_button_style("family"),
                                    command=lambda: self.try_for_child_from_family(dialog))
            try_child_btn.pack(side=tk.LEFT, padx=5)
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
            
            for i, child in enumerate(self.player["children"]):
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
                    # Update the child in the player's children list
                    self.player["children"][i] = child
                    
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
                
                # Relationship status
                relationship = child.get("relationship", 100)
                relationship_text = "Loving" if relationship > 75 else "Good" if relationship > 50 else "Neutral" if relationship > 25 else "Poor"
                relationship_label = tk.Label(child_frame, text=f"Relationship: {relationship_text}", 
                                            font=self.small_font, bg="#e6d8bf", fg="#5c4425")
                relationship_label.pack(anchor=tk.W)
                
                # Interact button
                interact_btn = tk.Button(child_frame, text="Interact", 
                                       **self.get_button_style("small"),
                                       command=lambda c=child: self.interact_with_child(c, dialog))
                interact_btn.pack(anchor=tk.E, pady=5)
        else:
            no_children = tk.Label(children_frame, text="You have no children.", font=self.text_font, bg="#e6d8bf", fg="#5c4425")
            no_children.pack(anchor=tk.W, pady=5)
        
        # Close button
        close_button = tk.Button(frame, text="Close", **self.get_button_style("medium"), command=dialog.destroy)
        close_button.pack(pady=10)
        
    def try_for_child_from_family(self, family_dialog):
        """Try for a child from the family screen"""
        family_dialog.destroy()
        self.try_for_child(None)
    
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
        if location_type == "City" or location_type == "Capital City":
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
                
            # Calculate dowry based on wealth
            dowry = base_wealth * random.randint(1, 3)
            
            # Create spouse data
            spouse = {
                "name": name,
                "age": age,
                "gender": gender,
                "traits": traits,
                "wealth": base_wealth,
                "dowry": dowry,  # Add dowry field
                "relationship": random.randint(30, 70)  # Initial relationship score
            }
            
            potential_spouses.append(spouse)
            
        # Show spouse selection screen
        if potential_spouses:
            self.show_spouse_selection(potential_spouses)
        else:
            self.show_dialog("No Matches", "There are no suitable marriage prospects in this location.")
    
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
        
        # Create a canvas with scrollbar for many spouse options
        canvas = tk.Canvas(frame, bg="#f0e6d2", highlightthickness=0)
        scrollbar = tk.Scrollbar(frame, orient="vertical", command=canvas.yview)
        spouse_frame = tk.Frame(canvas, bg="#f0e6d2")
        
        # Configure the canvas
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Create a window inside the canvas for the spouse frame
        canvas_window = canvas.create_window((0, 0), window=spouse_frame, anchor="nw")
        
        # Function to update the scrollregion when the frame size changes
        def configure_scroll_region(event):
            canvas.configure(scrollregion=canvas.bbox("all"))
        
        spouse_frame.bind("<Configure>", configure_scroll_region)
        
        # Function to handle mouse wheel scrolling
        def on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        # Bind the mousewheel event
        canvas.bind_all("<MouseWheel>", on_mousewheel)
        
        # Function to unbind the mousewheel event when the dialog is closed
        def on_dialog_close():
            canvas.unbind_all("<MouseWheel>")
            dialog.destroy()
        
        for i, spouse in enumerate(potential_spouses):
            # Create a frame for each spouse
            option_frame = tk.Frame(spouse_frame, bg="#e6d8bf", bd=2, relief=tk.RIDGE, padx=10, pady=10, width=550)
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
            
            # Marry button - Fix the lambda function to properly capture the spouse
            marry_btn = tk.Button(option_frame, text="Marry", 
                                **self.get_button_style("medium"),
                                command=lambda s=spouse: self.marry_spouse(s, dialog))
            marry_btn.pack(anchor=tk.E, pady=5)
        
        # Update the canvas scroll region
        spouse_frame.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))
        
        # Close button
        close_button = tk.Button(frame, text="Close", **self.get_button_style("medium"), command=on_dialog_close)
        close_button.pack(pady=10)
        
        # Bind the dialog close event
        dialog.protocol("WM_DELETE_WINDOW", on_dialog_close)
    
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
        """Show the market interface"""
        # Create a dialog for the market
        dialog = tk.Toplevel(self.root)
        dialog.title("Market")
        dialog.geometry("800x600")
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Make the dialog modal
        dialog.focus_set()
        
        # Create a frame for the market
        market_frame = tk.Frame(dialog, padx=20, pady=20, bg="#f0e6d2")
        market_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = tk.Label(market_frame, text="Market", font=self.header_font, bg="#f0e6d2", fg="#5c4425")
        title_label.pack(pady=(0, 20))
        
        # Player's gold
        gold_frame = tk.Frame(market_frame, bg="#f0e6d2")
        gold_frame.pack(fill=tk.X, pady=(0, 20))
        
        gold_label = tk.Label(gold_frame, text=f"Your Gold: {self.player['wealth']}", 
                            font=self.text_font, bg="#f0e6d2", fg="#5c4425")
        gold_label.pack(side=tk.LEFT)
        
        # Inventory button
        inventory_btn = tk.Button(gold_frame, text="View Inventory", 
                                **self.get_button_style(),
                                command=lambda: self.show_inventory_from_market(dialog))
        inventory_btn.pack(side=tk.RIGHT)
        
        # Create a frame for the items
        items_frame = tk.Frame(market_frame, bg="#f0e6d2")
        items_frame.pack(fill=tk.BOTH, expand=True)
        
        # Generate market items
        market_items = self.generate_market_items()
        
        # Column headers
        headers_frame = tk.Frame(items_frame, bg="#e6d8bf")
        headers_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Define column widths
        widths = [200, 100, 80, 300, 80]
        
        # Headers
        headers = ["Item", "Type", "Price", "Description", "Action"]
        for i, header in enumerate(headers):
            header_label = tk.Label(headers_frame, text=header, font=self.header_font, 
                                  bg="#e6d8bf", fg="#5c4425", width=widths[i]//10)
            header_label.grid(row=0, column=i, padx=5, pady=5)
        
        # Create a canvas and scrollbar for the items
        canvas = tk.Canvas(items_frame, bg="#f0e6d2", highlightthickness=0)
        scrollbar = tk.Scrollbar(items_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#f0e6d2")
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Add items to the scrollable frame
        for i, item in enumerate(market_items):
            item_frame = tk.Frame(scrollable_frame, bg="#f0e6d2", pady=5)
            item_frame.pack(fill=tk.X)
            
            # Item name
            name_label = tk.Label(item_frame, text=item["name"], font=self.text_font,
                                bg="#f0e6d2", fg="#5c4425", width=widths[0]//10, anchor="w")
            name_label.grid(row=0, column=0, padx=5)
            
            # Item type
            type_label = tk.Label(item_frame, text=item["type"], font=self.text_font,
                                bg="#f0e6d2", fg="#5c4425", width=widths[1]//10)
            type_label.grid(row=0, column=1, padx=5)
            
            # Item price
            price_label = tk.Label(item_frame, text=str(item["price"]), font=self.text_font,
                                 bg="#f0e6d2", fg="#5c4425", width=widths[2]//10)
            price_label.grid(row=0, column=2, padx=5)
            
            # Item description
            description = item.get("description", "")
            if not description:
                if item["type"] == "Food":
                    description = f"Restores {item.get('health_value', 10)} health"
                elif item["type"] == "Potion":
                    effect = item.get("effect", "health")
                    if effect == "health":
                        description = f"Restores {item.get('health_value', 20)} health"
                    else:
                        description = f"Improves {item.get('skill', 'combat')} by {item.get('skill_value', 1)}"
                elif item["type"] == "Book":
                    description = f"Teaches {item.get('skill', 'diplomacy')} +{item.get('skill_value', 2)}"
                elif item["type"] == "Weapon":
                    description = f"Damage: {item.get('damage', 5)}"
                elif item["type"] == "Armor":
                    description = f"Protection: {item.get('protection', 5)}"
            
            desc_label = tk.Label(item_frame, text=description, font=self.text_font,
                                bg="#f0e6d2", fg="#5c4425", width=widths[3]//10, anchor="w")
            desc_label.grid(row=0, column=3, padx=5)
            
            # Buy button
            buy_button = tk.Button(
                item_frame, 
                text="Buy", 
                command=lambda item=item: self.buy_item(item, gold_label),
                **self.get_button_style("small")
            )
            buy_button.grid(row=0, column=4, padx=5)
            
            # Alternate row colors for better readability
            if i % 2 == 1:
                item_frame.configure(bg="#e6d8bf")
                name_label.configure(bg="#e6d8bf")
                type_label.configure(bg="#e6d8bf")
                price_label.configure(bg="#e6d8bf")
                desc_label.configure(bg="#e6d8bf")
        
        # Back button
        back_button = tk.Button(
            market_frame, 
            text="Back to Town", 
            command=dialog.destroy,
            **self.get_button_style()
        )
        back_button.pack(pady=20)
    
    def generate_market_items(self):
        """Generate items for the market"""
        # Create a list of market items
        market_items = []
        
        # Food items
        food_items = [
            {"name": "Bread", "type": "Food", "price": 5, "health_value": 10, "value": 5},
            {"name": "Cheese", "type": "Food", "price": 8, "health_value": 15, "value": 8},
            {"name": "Meat", "type": "Food", "price": 12, "health_value": 25, "value": 12},
            {"name": "Fruit", "type": "Food", "price": 7, "health_value": 12, "value": 7},
            {"name": "Wine", "type": "Food", "price": 15, "health_value": 8, "value": 15}
        ]
        
        # Potion items
        potion_items = [
            {"name": "Health Potion", "type": "Potion", "price": 25, "health_value": 50, "effect": "health", "value": 25},
            {"name": "Strength Potion", "type": "Potion", "price": 40, "skill": "Combat", "skill_value": 2, "effect": "skill", "value": 40},
            {"name": "Intelligence Potion", "type": "Potion", "price": 45, "skill": "Intelligence", "skill_value": 2, "effect": "skill", "value": 45}
        ]
        
        # Book items
        book_items = [
            {"name": "Book of Combat", "type": "Book", "price": 60, "skill": "Combat", "skill_value": 3, "value": 60},
            {"name": "Book of Trade", "type": "Book", "price": 55, "skill": "Bargaining", "skill_value": 3, "value": 55},
            {"name": "Book of Diplomacy", "type": "Book", "price": 65, "skill": "Diplomacy", "skill_value": 3, "value": 65}
        ]
        
        # Weapon items
        weapon_items = [
            {"name": "Dagger", "type": "Weapon", "price": 30, "damage": 5, "value": 30},
            {"name": "Sword", "type": "Weapon", "price": 80, "damage": 10, "value": 80},
            {"name": "Axe", "type": "Weapon", "price": 70, "damage": 12, "value": 70},
            {"name": "Bow", "type": "Weapon", "price": 75, "damage": 8, "value": 75}
        ]
        
        # Armor items
        armor_items = [
            {"name": "Leather Armor", "type": "Armor", "price": 50, "protection": 5, "value": 50},
            {"name": "Chain Mail", "type": "Armor", "price": 120, "protection": 10, "value": 120},
            {"name": "Plate Armor", "type": "Armor", "price": 200, "protection": 15, "value": 200}
        ]
        
        # Add some random items from each category
        market_items.extend(random.sample(food_items, min(3, len(food_items))))
        market_items.extend(random.sample(potion_items, min(2, len(potion_items))))
        market_items.extend(random.sample(book_items, min(1, len(book_items))))
        market_items.extend(random.sample(weapon_items, min(2, len(weapon_items))))
        market_items.extend(random.sample(armor_items, min(1, len(armor_items))))
        
        # Shuffle the items
        random.shuffle(market_items)
        
        return market_items
    
    def buy_item(self, item, gold_label):
        """Buy an item from the market"""
        # Check if player has enough gold
        if self.player["wealth"] < item["price"]:
            messagebox.showerror("Insufficient Funds", 
                               f"You don't have enough gold to buy {item['name']}.")
            return
            
        # Confirm purchase
        confirm = messagebox.askyesno("Confirm Purchase", 
                                    f"Are you sure you want to buy {item['name']} for {item['price']} gold?")
        
        if confirm:
            # Deduct cost
            self.player["wealth"] -= item["price"]
            
            # Add to inventory
            if "inventory" not in self.player:
                self.player["inventory"] = []
                
            # Create inventory item (slightly different structure than market item)
            inventory_item = {
                "name": item["name"],
                "type": item["type"],
                "value": item["price"],  # Store original price as value
                "description": item.get("description", ""),
                "usable": item.get("usable", False)
            }
            
            # Add specific properties based on item type
            if item["type"] == "Food":
                inventory_item["health_value"] = item.get("health_value", 10)
            elif item["type"] == "Potion":
                inventory_item["effect"] = item.get("effect", "health")
                inventory_item["health_value"] = item.get("health_value", 20)
                inventory_item["skill"] = item.get("skill", "combat")
                inventory_item["skill_value"] = item.get("skill_value", 1)
            elif item["type"] == "Book":
                inventory_item["skill"] = item.get("skill", "diplomacy")
                inventory_item["skill_value"] = item.get("skill_value", 2)
            elif item["type"] == "Weapon":
                inventory_item["damage"] = item.get("damage", 5)
            elif item["type"] == "Armor":
                inventory_item["protection"] = item.get("protection", 5)
                
            self.player["inventory"].append(inventory_item)
            
            # Update gold display
            gold_label.config(text=f"Your Gold: {self.player['wealth']}")
            
            # Add event
            self.add_event(f"You purchased {item['name']} for {item['price']} gold.")
            
            # Update player info in main screen
            self.update_player_info()
    
    def sell_item(self, item, gold_label):
        """Sell an item from the player's inventory"""
        # Calculate sell value (usually less than buy price)
        sell_value = int(item["value"] * 0.7)  # 70% of original value
        
        # Confirm sale
        confirm = messagebox.askyesno("Confirm Sale", 
                                    f"Are you sure you want to sell {item['name']} for {sell_value} gold?")
        
        if confirm:
            # Add gold to player
            self.player["wealth"] += sell_value
            
            # Remove item from inventory
            self.player["inventory"].remove(item)
            
            # Update gold display if provided
            if gold_label:
                gold_label.config(text=f"Your Gold: {self.player['wealth']}")
            
            # Add event
            self.add_event(f"You sold {item['name']} for {sell_value} gold.")
            
            # Update player info
            self.update_player_info()
            
            return True
        
        return False
    
    def show_inventory(self):
        """Show the player's inventory"""
        # Create a dialog for the inventory
        dialog = tk.Toplevel(self.root)
        dialog.title("Inventory")
        dialog.geometry("800x600")
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Make the dialog modal
        dialog.focus_set()
        
        # Create a frame for the inventory
        frame = tk.Frame(dialog, padx=20, pady=20, bg="#f0e6d2")
        frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = tk.Label(frame, text="Your Inventory", font=self.header_font, bg="#f0e6d2", fg="#5c4425")
        title_label.pack(pady=(0, 20))
        
        # Player's wealth
        wealth_label = tk.Label(frame, text=f"Your Gold: {self.player['wealth']}", 
                              font=self.text_font, bg="#f0e6d2", fg="#5c4425")
        wealth_label.pack(pady=(0, 20))
        
        # Create a frame for the items
        items_frame = tk.Frame(frame, bg="#f0e6d2")
        items_frame.pack(fill=tk.BOTH, expand=True)
        
        # Check if inventory is empty
        if not self.player["inventory"]:
            empty_label = tk.Label(items_frame, text="Your inventory is empty.", 
                                 font=self.text_font, bg="#f0e6d2", fg="#5c4425")
            empty_label.pack(pady=50)
        else:
            # Column headers
            headers_frame = tk.Frame(items_frame, bg="#e6d8bf")
            headers_frame.pack(fill=tk.X, pady=(0, 10))
            
            # Define column widths
            widths = [200, 100, 80, 300, 100]
            
            # Headers
            headers = ["Item", "Type", "Value", "Description", "Actions"]
            for i, header in enumerate(headers):
                header_label = tk.Label(headers_frame, text=header, font=self.header_font, 
                                      bg="#e6d8bf", fg="#5c4425", width=widths[i]//10)
                header_label.grid(row=0, column=i, padx=5, pady=5)
            
            # Create a canvas and scrollbar for the items
            canvas = tk.Canvas(items_frame, bg="#f0e6d2", highlightthickness=0)
            scrollbar = tk.Scrollbar(items_frame, orient="vertical", command=canvas.yview)
            scrollable_frame = tk.Frame(canvas, bg="#f0e6d2")
            
            scrollable_frame.bind(
                "<Configure>",
                lambda e: canvas.configure(
                    scrollregion=canvas.bbox("all")
                )
            )
            
            canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)
            
            canvas.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")
            
            # Add items to the scrollable frame
            for i, item in enumerate(self.player["inventory"]):
                item_frame = tk.Frame(scrollable_frame, bg="#f0e6d2", pady=5)
                item_frame.pack(fill=tk.X)
                
                # Item name
                name_label = tk.Label(item_frame, text=item["name"], font=self.text_font,
                                    bg="#f0e6d2", fg="#5c4425", width=widths[0]//10, anchor="w")
                name_label.grid(row=0, column=0, padx=5)
                
                # Item type
                type_label = tk.Label(item_frame, text=item["type"], font=self.text_font,
                                    bg="#f0e6d2", fg="#5c4425", width=widths[1]//10)
                type_label.grid(row=0, column=1, padx=5)
                
                # Item value
                value_label = tk.Label(item_frame, text=str(item["value"]), font=self.text_font,
                                     bg="#f0e6d2", fg="#5c4425", width=widths[2]//10)
                value_label.grid(row=0, column=2, padx=5)
                
                # Item description
                description = item.get("description", "")
                if not description:
                    if item["type"] == "Food":
                        description = f"Restores {item.get('health_value', 10)} health"
                    elif item["type"] == "Potion":
                        effect = item.get("effect", "health")
                        if effect == "health":
                            description = f"Restores {item.get('health_value', 20)} health"
                        else:
                            description = f"Improves {item.get('skill', 'combat')} by {item.get('skill_value', 1)}"
                    elif item["type"] == "Book":
                        description = f"Teaches {item.get('skill', 'diplomacy')} +{item.get('skill_value', 2)}"
                    elif item["type"] == "Weapon":
                        description = f"Damage: {item.get('damage', 5)}"
                    elif item["type"] == "Armor":
                        description = f"Protection: {item.get('protection', 5)}"
                
                desc_label = tk.Label(item_frame, text=description, font=self.text_font,
                                    bg="#f0e6d2", fg="#5c4425", width=widths[3]//10, anchor="w")
                desc_label.grid(row=0, column=3, padx=5)
                
                # Action buttons
                action_frame = tk.Frame(item_frame, bg="#f0e6d2")
                action_frame.grid(row=0, column=4, padx=5)
                
                # Use button
                use_button = tk.Button(
                    action_frame, 
                    text="Use", 
                    command=lambda item=item: self.use_item(item, dialog),
                    **self.get_button_style("small")
                )
                use_button.pack(side=tk.LEFT, padx=2)
                
                # Sell button
                sell_button = tk.Button(
                    action_frame, 
                    text="Sell", 
                    command=lambda item=item: self.sell_item_from_inventory(item, wealth_label, dialog),
                    **self.get_button_style("small")
                )
                sell_button.pack(side=tk.LEFT, padx=2)
                
                # Alternate row colors for better readability
                if i % 2 == 1:
                    item_frame.configure(bg="#2a2a2a")
                    name_label.configure(bg="#2a2a2a")
                    type_label.configure(bg="#2a2a2a")
                    value_label.configure(bg="#2a2a2a")
                    desc_label.configure(bg="#2a2a2a")
                    action_frame.configure(bg="#2a2a2a")
        
        # Close button
        close_button = tk.Button(
            frame, 
            text="Close", 
            font=("Arial", 14),
            **self.get_button_style(),
            command=dialog.destroy
        )
        close_button.pack(pady=20)
        
    def sell_item_from_inventory(self, item, wealth_label, dialog):
        """Sell an item from the inventory"""
        # Calculate sell price (usually less than buy price)
        sell_price = int(item["value"] * 0.7)  # 70% of original value
        
        # Confirm sale
        confirm = messagebox.askyesno("Confirm Sale", 
                                     f"Are you sure you want to sell {item['name']} for {sell_price} gold?",
                                     parent=dialog)
        
        if confirm:
            # Remove item from inventory
            self.player["inventory"].remove(item)
            
            # Add gold to player's wealth
            self.player["wealth"] += sell_price
            
            # Update wealth display
            wealth_label.config(text=f"Gold: {self.player['wealth']}")
            
            # Add event
            self.add_event(f"You sold {item['name']} for {sell_price} gold.")
            
            # Update player info in main screen
            self.update_player_info()
            
            # Refresh inventory display
            dialog.destroy()
            self.show_inventory()
            
    def use_item(self, item, dialog):
        """Use an item from the inventory"""
        # Different effects based on item type
        if item["type"] == "Food":
            # Food items restore health
            health_gain = item.get("health_value", 10)
            self.player["health"] = min(100, self.player["health"] + health_gain)
            message = f"You consumed {item['name']} and gained {health_gain} health."
            
        elif item["type"] == "Potion":
            # Potions have special effects
            effect = item.get("effect", "health")
            if effect == "health":
                health_gain = item.get("health_value", 20)
                self.player["health"] = min(100, self.player["health"] + health_gain)
                message = f"You drank {item['name']} and gained {health_gain} health."
            elif effect == "skill":
                skill = item.get("skill", "combat")
                skill_gain = item.get("skill_value", 1)
                
                # Initialize skills if not present
                if "skills" not in self.player:
                    self.player["skills"] = {}
                
                # Initialize specific skill if not present
                if skill not in self.player["skills"]:
                    self.player["skills"][skill] = 0
                    
                self.player["skills"][skill] += skill_gain
                message = f"You drank {item['name']} and gained {skill_gain} {skill} skill."
                
        elif item["type"] == "Book":
            # Books improve skills
            skill = item.get("skill", "diplomacy")
            skill_gain = item.get("skill_value", 2)
            
            # Initialize skills if not present
            if "skills" not in self.player:
                self.player["skills"] = {}
            
            # Initialize specific skill if not present
            if skill not in self.player["skills"]:
                self.player["skills"][skill] = 0
                
            self.player["skills"][skill] += skill_gain
            message = f"You read {item['name']} and gained {skill_gain} {skill} skill."
            
        else:
            # Generic usable item
            message = f"You used {item['name']}."
        
        # Remove item from inventory
        self.player["inventory"].remove(item)
        
        # Add event
        self.add_event(message)
        
        # Show result
        self.show_dialog("Item Used", message)
        
        # Update player info
        self.update_player_info()
    
        # Refresh inventory display
        dialog.destroy()
        self.show_inventory()
    
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
    
    def equip_item(self, item, dialog=None):
        """Equip a weapon or armor item"""
        if item["type"] not in ["Weapon", "Armor"]:
            messagebox.showinfo("Cannot Equip", f"{item['name']} cannot be equipped.")
            return
            
        # Initialize equipment if not present
        if "equipment" not in self.player:
            self.player["equipment"] = {}
            
        # Check if an item is already equipped in this slot
        slot = item["type"].lower()
        old_item = self.player["equipment"].get(slot)
        
        # Equip the new item
        self.player["equipment"][slot] = item
        
        # Add event
        message = f"You equipped {item['name']}."
        self.add_event(message)
        
        # Show result
        self.show_dialog("Item Equipped", message)
        
        # Update player info
        self.update_player_info()
    
        # Refresh inventory display if dialog is provided
        if dialog and dialog.winfo_exists():
            dialog.destroy()
            self.show_inventory()
            
            
    def is_item_equipped(self, item):
        """Check if an item is currently equipped"""
        if "equipment" not in self.player:
            return False
            
        slot = item["type"].lower()
        equipped_item = self.player["equipment"].get(slot)
        
        if not equipped_item:
            return False
            
        # Compare items (name should be unique enough)
        return equipped_item["name"] == item["name"]
    
    def unequip_item(self, slot, dialog=None):
        """Unequip an item from the specified slot"""
        if "equipment" not in self.player or slot not in self.player["equipment"]:
            return
            
        # Get the item being unequipped
        item = self.player["equipment"][slot]
        
        # Remove from equipment
        del self.player["equipment"][slot]
        
        # Add event
        message = f"You unequipped {item['name']}."
        self.add_event(message)
        
        # Show result
        self.show_dialog("Item Unequipped", message)
        
        # Update player info
        self.update_player_info()
        
        # Refresh inventory display if dialog is provided
        if dialog and dialog.winfo_exists():
            dialog.destroy()
            self.show_inventory()
    
    def update_player_info(self):
        """Update the player information display in the top bar"""
        # Find the player info label in the top bar
        for widget in self.main_container.winfo_children():
            if isinstance(widget, tk.Frame) and widget.winfo_height() == 40:  # This is the top bar
                for child in widget.winfo_children():
                    if isinstance(child, tk.Label) and child.winfo_x() < 100:  # This is the player info label on the left
                        # Update the label text
                        child.config(text=f"{self.player['name']} - {self.player['occupation']} | Age: {self.player['age']} | Health: {self.player['health']} | Gold: {self.player['wealth']}")
                        break
    
    def create_character_form(self):
        """Display the character creation form"""
        self.clear_screen()
        
        # Create variables for form inputs
        self.name_var = tk.StringVar()
        self.gender_var = tk.StringVar()
        self.occupation_var = tk.StringVar()
        
        # Create title
        title_label = tk.Label(self.main_container, text="Create Your Character", 
                              font=("Times New Roman", 24, "bold"), fg="#8B4513")
        title_label.pack(pady=(20, 30))
        
        # Create main form container with two columns
        form_container = tk.Frame(self.main_container)
        form_container.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Left column - inputs
        left_frame = tk.Frame(form_container, width=400)
        left_frame.pack(side="left", fill="both", padx=(0, 10))
        
        # Right column - description and buttons
        right_frame = tk.Frame(form_container, width=400)
        right_frame.pack(side="right", fill="both", padx=(10, 0))
        
        # Name input
        name_frame = tk.Frame(left_frame)
        name_frame.pack(fill="x", pady=10)
        
        name_label = tk.Label(name_frame, text="Name:", font=("Times New Roman", 14))
        name_label.pack(side="left", padx=(0, 10))
        
        name_entry = tk.Entry(name_frame, textvariable=self.name_var, font=("Times New Roman", 14), width=20)
        name_entry.pack(side="left", fill="x", expand=True)
        
        # Gender selection
        gender_frame = tk.Frame(left_frame)
        gender_frame.pack(fill="x", pady=10)
        
        gender_label = tk.Label(gender_frame, text="Gender:", font=("Times New Roman", 14))
        gender_label.pack(side="left", padx=(0, 10))
        
        gender_options_frame = tk.Frame(gender_frame)
        gender_options_frame.pack(side="left", fill="x")
        
        male_radio = tk.Radiobutton(gender_options_frame, text="Male", variable=self.gender_var, 
                                   value="Male", font=("Times New Roman", 12))
        male_radio.pack(side="left", padx=10)
        
        female_radio = tk.Radiobutton(gender_options_frame, text="Female", variable=self.gender_var, 
                                     value="Female", font=("Times New Roman", 12))
        female_radio.pack(side="left", padx=10)
        
        # Occupation selection with scrollable frame
        occupation_label = tk.Label(left_frame, text="Choose Your Occupation:", 
                                   font=("Times New Roman", 14, "bold"))
        occupation_label.pack(anchor="w", pady=(20, 10))
        
        occupations_frame = tk.Frame(left_frame)
        occupations_frame.pack(fill="both", expand=True)
        
        occupations = [
            "King", "Noble", "Knight", "Merchant", 
            "Tavern Owner", "Farmer", "Peasant"
        ]
        
        # Create radio buttons for each occupation
        for occupation in occupations:
            occupation_radio = tk.Radiobutton(
                occupations_frame, 
                text=occupation,
                variable=self.occupation_var,
                value=occupation,
                font=("Times New Roman", 12),
                command=self.update_occupation_description
            )
            occupation_radio.pack(anchor="w", pady=5)
        
        # Right side - occupation description
        description_label = tk.Label(right_frame, text="Occupation Description:", 
                                    font=("Times New Roman", 14, "bold"))
        description_label.pack(anchor="w", pady=(0, 10))
        
        # Create a text widget for the description
        self.description_text = tk.Text(right_frame, height=12, width=40, 
                                      font=("Times New Roman", 12),
                                      wrap="word", bg="#F5F5DC", bd=2)
        self.description_text.pack(fill="both", expand=True, pady=(0, 20))
        self.description_text.config(state="disabled")
        
        # Buttons
        buttons_frame = tk.Frame(right_frame)
        buttons_frame.pack(fill="x", pady=20)
        
        back_btn = tk.Button(buttons_frame, text="Back to Menu", 
                           **self.get_button_style(),
                           command=self.show_main_menu)
        back_btn.pack(side="left", padx=10)
        
        start_btn = tk.Button(buttons_frame, text="Begin Your Journey", 
                            **self.get_button_style(),
                            command=self.create_character)
        start_btn.pack(side="right", padx=10)
        
        # Set focus to name entry
        name_entry.focus_set()
    
    def update_occupation_description(self):
        """Update the occupation description based on selected occupation"""
        occupation = self.occupation_var.get()
        
        # Enable text widget for editing
        self.description_text.config(state="normal")
        
        # Clear current text
        self.description_text.delete(1.0, tk.END)
        
        # Get and insert description
        description = self.get_occupation_description(occupation)
        self.description_text.insert(tk.END, description)
        
        # Disable text widget again
        self.description_text.config(state="disabled")
    
    def show_travel_options(self):
        """Show available travel destinations"""
        messagebox.showinfo("Travel", "Travel options will be implemented in a future update.")
        # TODO: Implement travel functionality
    
    def advance_season(self):
        """Advance the game by one season"""
        seasons = ["Spring", "Summer", "Fall", "Winter"]
        
        # Update season
        self.season_index = (self.season_index + 1) % 4
        self.current_season = seasons[self.season_index]
        
        # If we've completed a year cycle, increase age
        if self.season_index == 0:  # Back to Spring
            self.current_year += 1
            self.player["age"] += 1
            self.add_event(f"You are now {self.player['age']} years old.")
        
        # Add season change event
        self.add_event(f"The season has changed to {self.current_season}.")
        
        # Update the game interface
        self.show_game_interface()
        
        # Show a summary message
        messagebox.showinfo("Season Change", f"The season has changed to {self.current_season}.\nCurrent year: {self.current_year}")
    
    def show_inventory_from_market(self, market_dialog):
        """Show inventory from the market dialog"""
        # Hide market dialog temporarily
        market_dialog.withdraw()
        
        # Show inventory
        self.show_inventory()
        
        # Restore market dialog
        market_dialog.deiconify()
    
    def show_dialog(self, title, message):
        """Show a simple dialog with a message"""
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
        
        # Message
        message_label = tk.Label(frame, text=message, font=self.text_font, 
                               bg="#f0e6d2", fg="#5c4425", wraplength=350, justify=tk.LEFT)
        message_label.pack(pady=(0, 20))
        
        # OK button
        ok_button = tk.Button(frame, text="OK", **self.get_button_style(), command=dialog.destroy)
        ok_button.pack()
    
    def interact_with_spouse(self):
        """Interact with the player's spouse"""
        # Check if player has a spouse
        if not self.player.get("spouse"):
            self.show_dialog("No Spouse", "You are not married.")
            return
            
        # Create dialog for spouse interaction
        dialog = tk.Toplevel(self.root)
        dialog.title(f"Interact with {self.player['spouse']['name']}")
        dialog.geometry("500x450")
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Make the dialog modal
        dialog.focus_set()
        
        # Add some padding
        frame = tk.Frame(dialog, padx=20, pady=20, bg="#f0e6d2")
        frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = tk.Label(frame, text=f"Interact with {self.player['spouse']['name']}", 
                             font=self.header_font, bg="#f0e6d2", fg="#5c4425")
        title_label.pack(pady=(0, 20))
        
        # Spouse info
        spouse = self.player["spouse"]
        
        info_text = f"Age: {spouse['age']}\n"
        if "traits" in spouse:
            info_text += f"Traits: {', '.join(spouse['traits'])}\n"
        if "relationship" in spouse:
            info_text += f"Relationship: {spouse['relationship']}/100\n"
            
        info_label = tk.Label(frame, text=info_text, font=self.text_font, 
                            bg="#f0e6d2", fg="#5c4425", justify=tk.LEFT)
        info_label.pack(anchor=tk.W, pady=(0, 20))
        
        # Interaction buttons
        buttons_frame = tk.Frame(frame, bg="#f0e6d2")
        buttons_frame.pack(fill=tk.X, pady=10)
        
        # Talk button
        talk_btn = tk.Button(buttons_frame, text="Talk", 
                           **self.get_button_style(),
                           command=lambda: self.talk_to_spouse(dialog))
        talk_btn.pack(side=tk.LEFT, padx=10)
        
        # Gift button
        gift_btn = tk.Button(buttons_frame, text="Give Gift", 
                           **self.get_button_style(),
                           command=lambda: self.give_gift_to_spouse(dialog))
        gift_btn.pack(side=tk.LEFT, padx=10)
        
        # Outing button
        outing_btn = tk.Button(buttons_frame, text="Go on Outing", 
                             **self.get_button_style(),
                             command=lambda: self.go_on_outing_with_spouse(dialog))
        outing_btn.pack(side=tk.LEFT, padx=10)
        
        # Try for child section - Make it more prominent
        child_frame = tk.Frame(frame, bg="#e6d8bf", bd=2, relief=tk.RIDGE, padx=15, pady=15)
        child_frame.pack(fill=tk.X, pady=20)
        
        child_title = tk.Label(child_frame, text="Family Planning", 
                             font=self.header_font, bg="#e6d8bf", fg="#5c4425")
        child_title.pack(anchor=tk.W)
        
        child_desc = tk.Label(child_frame, 
                            text="You can try to have a child with your spouse. A good relationship (70+) is required.",
                            font=self.text_font, bg="#e6d8bf", fg="#5c4425", wraplength=400, justify=tk.LEFT)
        child_desc.pack(anchor=tk.W, pady=5)
        
        # Try for child button - larger and more prominent
        child_btn = tk.Button(child_frame, text="Try for Child", 
                            **self.get_button_style("family"),
                            command=lambda: self.try_for_child(dialog))
        child_btn.pack(anchor=tk.CENTER, pady=10)
        
        # Close button
        close_btn = tk.Button(frame, text="Close", 
                            **self.get_button_style(),
                            command=dialog.destroy)
        close_btn.pack(pady=20)
    
    def talk_to_spouse(self, parent_dialog):
        """Talk to spouse to improve relationship"""
        spouse = self.player["spouse"]
        relationship_increase = random.randint(1, 5)
        spouse["relationship"] = min(100, spouse["relationship"] + relationship_increase)
        
        self.add_event(f"You had a pleasant conversation with your spouse, {spouse['name']}.")
        messagebox.showinfo("Talk", f"You had a nice conversation with {spouse['name']}. Relationship improved by {relationship_increase} points.", parent=parent_dialog)
        
        # Refresh the dialog
        parent_dialog.destroy()
        self.interact_with_spouse()
    
    def give_gift_to_spouse(self, parent_dialog):
        """Give a gift to spouse to improve relationship"""
        # Check if player has any items to give
        if not self.player["inventory"]:
            messagebox.showinfo("No Items", "You don't have any items to give as a gift.", parent=parent_dialog)
            return
            
        # Create dialog for gift selection
        gift_dialog = tk.Toplevel(parent_dialog)
        gift_dialog.title("Select Gift")
        gift_dialog.geometry("400x300")
        gift_dialog.transient(parent_dialog)
        gift_dialog.grab_set()
        
        # Make the dialog modal
        gift_dialog.focus_set()
        
        # Add some padding
        frame = tk.Frame(gift_dialog, padx=20, pady=20, bg="#f0e6d2")
        frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = tk.Label(frame, text="Select a Gift", font=self.header_font, bg="#f0e6d2", fg="#5c4425")
        title_label.pack(pady=(0, 20))
        
        # Create a listbox for items
        items_frame = tk.Frame(frame, bg="#f0e6d2")
        items_frame.pack(fill=tk.BOTH, expand=True)
        
        items_listbox = tk.Listbox(items_frame, font=self.text_font, height=10)
        items_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Add scrollbar
        scrollbar = tk.Scrollbar(items_frame, orient=tk.VERTICAL, command=items_listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        items_listbox.config(yscrollcommand=scrollbar.set)
        
        # Add items to listbox
        for item in self.player["inventory"]:
            items_listbox.insert(tk.END, f"{item['name']} ({item['type']})")
        
        # Buttons
        buttons_frame = tk.Frame(frame, bg="#f0e6d2")
        buttons_frame.pack(fill=tk.X, pady=10)
        
        # Give button
        give_btn = tk.Button(buttons_frame, text="Give Gift", 
                           **self.get_button_style(),
                           command=lambda: self.process_gift(items_listbox.curselection(), parent_dialog, gift_dialog))
        give_btn.pack(side=tk.LEFT, padx=10)
        
        # Cancel button
        cancel_btn = tk.Button(buttons_frame, text="Cancel", 
                             **self.get_button_style(),
                             command=gift_dialog.destroy)
        cancel_btn.pack(side=tk.RIGHT, padx=10)
    
    def process_gift(self, selection, parent_dialog, gift_dialog):
        """Process the selected gift"""
        if not selection:
            messagebox.showinfo("No Selection", "Please select an item to give.", parent=gift_dialog)
            return
            
        # Get the selected item
        item_index = selection[0]
        item = self.player["inventory"][item_index]
        
        # Remove the item from inventory
        self.player["inventory"].pop(item_index)
        
        # Calculate relationship increase based on item value
        relationship_increase = max(5, min(20, item["value"] // 5))
        
        # Update spouse relationship
        spouse = self.player["spouse"]
        spouse["relationship"] = min(100, spouse["relationship"] + relationship_increase)
        
        # Add event
        self.add_event(f"You gave {item['name']} as a gift to your spouse, {spouse['name']}.")
        
        # Show message
        messagebox.showinfo("Gift Given", 
                          f"You gave {item['name']} to {spouse['name']}. They appreciated your gift!\n\n"
                          f"Relationship improved by {relationship_increase} points.", 
                          parent=gift_dialog)
        
        # Close dialogs and refresh
        gift_dialog.destroy()
        parent_dialog.destroy()
        self.interact_with_spouse()
    
    def go_on_outing_with_spouse(self, parent_dialog):
        """Go on an outing with spouse to improve relationship"""
        # Check if player has enough gold
        outing_cost = random.randint(10, 30)
        if self.player["wealth"] < outing_cost:
            messagebox.showinfo("Insufficient Funds", 
                              f"You need {outing_cost} gold to go on an outing.", 
                              parent=parent_dialog)
            return
            
        # Deduct cost
        self.player["wealth"] -= outing_cost
        
        # Calculate relationship increase
        relationship_increase = random.randint(5, 15)
        
        # Update spouse relationship
        spouse = self.player["spouse"]
        spouse["relationship"] = min(100, spouse["relationship"] + relationship_increase)
        
        # Generate outing description
        outings = [
            f"a romantic walk through {self.current_location}",
            f"dinner at a local tavern",
            f"a trip to the market",
            f"a visit to a nearby village",
            f"a picnic in the countryside"
        ]
        outing = random.choice(outings)
        
        # Add event
        self.add_event(f"You took your spouse, {spouse['name']}, on {outing}.")
        
        # Show message
        messagebox.showinfo("Outing", 
                          f"You spent {outing_cost} gold to take {spouse['name']} on {outing}.\n\n"
                          f"You both had a wonderful time!\n\n"
                          f"Relationship improved by {relationship_increase} points.", 
                          parent=parent_dialog)
        
        # Update player info
        self.update_player_info()
        
        # Refresh dialog
        parent_dialog.destroy()
        self.interact_with_spouse()
    
    def try_for_child(self, parent_dialog):
        """Try to have a child with spouse"""
        spouse = self.player["spouse"]
        
        # Check if relationship is good enough
        if spouse.get("relationship", 0) < 70:
            messagebox.showinfo("Relationship Too Low", 
                              f"Your relationship with {spouse['name']} needs to be at least 70 to try for a child.\n\n"
                              f"Current relationship: {spouse['relationship']}")
            return
            
        # Check if spouse is too old
        if spouse["age"] > 45:
            messagebox.showinfo("Age Issue", 
                              f"{spouse['name']} is too old to have children.")
            return
            
        # Calculate success chance
        success_chance = 0.3  # 30% base chance
        
        # Modify based on relationship
        success_chance += (spouse["relationship"] - 70) / 100
        
        # Try for child
        if random.random() < success_chance:
            # Success! Create child
            child_gender = random.choice(["male", "female"])
            child_name = self.generate_name(child_gender)
            
            # Create child data
            child = {
                "name": child_name,
                "gender": child_gender,
                "age": 0,
                "traits": self.generate_traits(),
                "relationship": 100
            }
            
            # Add child to player's children
            if "children" not in self.player:
                self.player["children"] = []
                
            self.player["children"].append(child)
            
            # Add event
            self.add_event(f"Your spouse, {spouse['name']}, gave birth to a {child_gender} child named {child_name}.")
            
            # Show message
            messagebox.showinfo("Child Born", 
                              f"Congratulations! Your spouse, {spouse['name']}, gave birth to a {child_gender} child.\n\n"
                              f"You named the child {child_name}.")
        else:
            # Failure
            messagebox.showinfo("No Child", 
                              f"You and {spouse['name']} tried for a child, but were unsuccessful this time.\n\n"
                              f"You can try again later.")
        
        # Refresh dialog
        if parent_dialog:
            parent_dialog.destroy()
            self.interact_with_spouse()
    
    def interact_with_child(self, child, parent_dialog=None):
        """Interact with a child"""
        # Create dialog
        dialog = tk.Toplevel(self.root)
        dialog.title(f"Interact with {child['name']}")
        dialog.geometry("500x400")
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Make the dialog modal
        dialog.focus_set()
        
        # Add some padding
        frame = tk.Frame(dialog, padx=20, pady=20, bg="#f0e6d2")
        frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = tk.Label(frame, text=f"Interact with {child['name']}", font=self.header_font, bg="#f0e6d2", fg="#5c4425")
        title_label.pack(pady=(0, 20))
        
        # Child info
        gender_text = "Son" if child.get("gender", "male") == "male" else "Daughter"
        info_text = f"Your {gender_text}, {child['name']}, is {child.get('age', 0)} years old."
        info_label = tk.Label(frame, text=info_text, font=self.text_font, bg="#f0e6d2", fg="#5c4425", wraplength=450)
        info_label.pack(pady=(0, 20))
        
        # Traits
        if child.get("traits"):
            traits_text = f"Traits: {', '.join(child['traits'])}"
            traits_label = tk.Label(frame, text=traits_text, font=self.text_font, bg="#f0e6d2", fg="#5c4425", wraplength=450)
            traits_label.pack(pady=(0, 20))
        
        # Interaction options
        options_frame = tk.Frame(frame, bg="#f0e6d2")
        options_frame.pack(fill=tk.BOTH, expand=True)
        
        # Talk to child
        talk_btn = tk.Button(options_frame, text="Talk to Child", 
                           **self.get_button_style("medium"),
                           command=lambda: self.talk_to_child(child, dialog))
        talk_btn.pack(fill=tk.X, pady=5)
        
        # Play with child
        play_btn = tk.Button(options_frame, text="Play with Child", 
                           **self.get_button_style("medium"),
                           command=lambda: self.play_with_child(child, dialog))
        play_btn.pack(fill=tk.X, pady=5)
        
        # Teach child
        if child.get("age", 0) >= 5:
            teach_btn = tk.Button(options_frame, text="Teach Child", 
                               **self.get_button_style("medium"),
                               command=lambda: self.teach_child(child, dialog))
            teach_btn.pack(fill=tk.X, pady=5)
        
        # Close button
        close_button = tk.Button(frame, text="Close", **self.get_button_style("medium"), 
                               command=lambda: self.close_child_interaction(dialog, parent_dialog))
        close_button.pack(pady=10)
    
    def close_child_interaction(self, dialog, parent_dialog=None):
        """Close the child interaction dialog and refresh the parent dialog if needed"""
        dialog.destroy()
        if parent_dialog:
            parent_dialog.destroy()
            self.show_family_screen()
    
    def talk_to_child(self, child, parent_dialog):
        """Talk to a child to improve relationship"""
        # Increase relationship
        relationship_increase = random.randint(3, 10)
        child["relationship"] = min(100, child.get("relationship", 0) + relationship_increase)
        
        # Generate random conversation topics based on child's age
        age = child.get("age", 0)
        topics = []
        
        if age < 3:
            topics = ["simple words", "colors", "animals", "family members"]
        elif age < 8:
            topics = ["favorite toys", "friends", "games", "stories", "dreams"]
        elif age < 13:
            topics = ["school", "friends", "hobbies", "future plans", "adventures"]
        else:
            topics = ["future plans", "interests", "friends", "life philosophy", "ambitions"]
        
        topic = random.choice(topics)
        
        # Add event
        self.add_event(f"You had a nice conversation with your child {child['name']} about {topic}.")
        
        # Show message
        messagebox.showinfo("Talk with Child", 
                          f"You had a nice conversation with {child['name']} about {topic}.\n\n"
                          f"Your relationship has improved.", 
                          parent=parent_dialog)
        
        # Refresh dialog
        parent_dialog.destroy()
        self.interact_with_child(child)
    
    def play_with_child(self, child, parent_dialog):
        """Play with a child to improve relationship"""
        # Increase relationship
        relationship_increase = random.randint(5, 15)
        child["relationship"] = min(100, child.get("relationship", 0) + relationship_increase)
        
        # Generate random play activities based on child's age
        age = child.get("age", 0)
        activities = []
        
        if age < 3:
            activities = ["peek-a-boo", "rolling a ball", "stacking blocks", "simple songs"]
        elif age < 8:
            activities = ["hide and seek", "tag", "make-believe", "drawing", "singing songs"]
        elif age < 13:
            activities = ["board games", "outdoor games", "storytelling", "crafts", "exploring"]
        else:
            activities = ["chess", "sports", "music", "hunting practice", "riding"]
        
        activity = random.choice(activities)
        
        # Add event
        self.add_event(f"You spent time playing {activity} with your child {child['name']}.")
        
        # Show message
        messagebox.showinfo("Play with Child", 
                          f"You spent time playing {activity} with {child['name']}.\n\n"
                          f"You both had a wonderful time and your relationship has improved significantly.", 
                          parent=parent_dialog)
        
        # Refresh dialog
        parent_dialog.destroy()
        self.interact_with_child(child)
    
    def teach_child(self, child, parent_dialog):
        """Teach a child to improve their skills"""
        # Only for children 5 and older
        if child.get("age", 0) < 5:
            messagebox.showinfo("Too Young", 
                              f"{child['name']} is too young to learn complex skills.", 
                              parent=parent_dialog)
            return
        
        # Increase relationship slightly
        relationship_increase = random.randint(1, 5)
        child["relationship"] = min(100, child.get("relationship", 0) + relationship_increase)
        
        # Generate random skills to teach based on child's age
        age = child.get("age", 0)
        skills = []
        
        if age < 8:
            skills = ["reading", "writing", "counting", "manners", "simple crafts"]
        elif age < 13:
            skills = ["history", "mathematics", "literature", "craftsmanship", "etiquette"]
        else:
            skills = ["philosophy", "strategy", "economics", "leadership", "combat"]
        
        skill = random.choice(skills)
        
        # Initialize skills if not present
        if "skills" not in child:
            child["skills"] = {}
        
        # Improve or add the skill
        skill_increase = random.randint(1, 5)
        child["skills"][skill] = child["skills"].get(skill, 0) + skill_increase
        
        # Add event
        self.add_event(f"You taught {child['name']} about {skill}.")
        
        # Show message
        messagebox.showinfo("Teach Child", 
                          f"You spent time teaching {child['name']} about {skill}.\n\n"
                          f"{child['name']}'s knowledge of {skill} has improved.", 
                          parent=parent_dialog)
        
        # Refresh dialog
        parent_dialog.destroy()
        self.interact_with_child(child)
    
    