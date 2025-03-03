import tkinter as tk
from medieval_simulator import MedievalSimulator

def main():
    """Main entry point for the Medieval Life Simulator"""
    print("Starting Medieval Life Simulator...")
    # Create the root window
    root = tk.Tk()
    root.title("Medieval Life Simulator")
    
    # Set the window icon (if available)
    try:
        # You would need to create this icon file
        root.iconbitmap("assets/icon.ico")
    except Exception as e:
        print(f"Icon not loaded: {e}")
    
    # Initialize the game
    print("Initializing game...")
    app = MedievalSimulator(root)
    
    # Start the main loop
    print("Starting main loop...")
    root.mainloop()
    print("Game closed.")

if __name__ == "__main__":
    main()