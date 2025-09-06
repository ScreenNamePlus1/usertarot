import random
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.core.window import Window
import os
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.clock import Clock

# Set the window background color to black
Window.clearcolor = (0, 0, 0, 1)

# Define the suits and ranks of the tarot cards
suits = ["Wands", "Cups", "Swords", "Pentacles"]
ranks = ["Ace", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine", "Ten", "Page", "Knight", "Queen", "King"]
major_arcana = ["The Fool", "The Magician", "The High Priestess", "The Empress", "The Emperor", "The Hierophant", "The Lovers", 
                "The Chariot", "Strength", "The Hermit", "Wheel of Fortune", "Justice", "The Hanged Man", "Death", 
                "Temperance", "The Devil", "The Tower", "The Star", "The Moon", "The Sun", "Judgement", "The World"]

# Create a list of all the tarot cards
tarot_cards = []
for suit in suits:
    for rank in ranks:
        tarot_cards.append(f"{rank} of {suit}")
tarot_cards.extend(major_arcana)

class TarotApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
    def build(self):
        # Set the application icon - check multiple possible paths
        icon_paths = [
            'images/rider-waite-tarot/CardBacks.jpg',
            'images/CardBacks.jpg',
            'CardBacks.jpg'
        ]
        
        for path in icon_paths:
            if os.path.exists(path):
                self.icon = path
                break

        self.main_layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        self.show_spread_selection()
        return self.main_layout

    def get_image_base_path(self):
        """Determine the correct base path for images"""
        possible_paths = [
            'images/rider-waite-tarot/',
            'images/',
            ''
        ]
        
        for path in possible_paths:
            test_files = ['CardBacks.png', 'CardBacks.jpg', 'The_Fool.png', 'The_Fool.jpg']
            for test_file in test_files:
                if os.path.exists(f"{path}{test_file}"):
                    return path
        return 'images/'  # Default fallback

    def get_card_image_path(self, card_name, orientation="Upright"):
        """Get the correct image path for a card with simplified handling"""
        base_path = self.get_image_base_path()
        
        # Format the card name for file lookup
        formatted_name = card_name.replace(" ", "_")
        if card_name.startswith("The "):
            formatted_name = card_name.replace(" ", "_")
        else:
            formatted_name = card_name.replace(" ", "_").replace("The_", "")

        # Handle card back as special case
        if formatted_name == "CardBacks" or card_name == "CardBacks":
            for ext in ['.png', '.jpg', '.jpeg']:
                path = f'{base_path}CardBacks{ext}'
                if os.path.exists(path):
                    return path, False
            return None, True

        # Try different file extensions - no rotation, just show upright
        # (We'll indicate reversed in text only to avoid PIL dependency)
        for ext in ['.png', '.jpg', '.jpeg']:
            image_path = f'{base_path}{formatted_name}{ext}'
            if os.path.exists(image_path):
                return image_path, False
        
        # Fallback to card back
        return self.get_card_image_path("CardBacks", "Upright")

    def get_card_back_path(self):
        """Get the path to the card back image"""
        base_path = self.get_image_base_path()
        for ext in ['.png', '.jpg', '.jpeg']:
            path = f'{base_path}CardBacks{ext}'
            if os.path.exists(path):
                return path
        return None

    def show_spread_selection(self):
        """Display the spread selection screen"""
        self.main_layout.clear_widgets()
        
        # Title
        title = Label(
            text="Select a Tarot Spread", 
            font_size='24sp', 
            size_hint_y=0.15,
            color=(1, 1, 1, 1)
        )
        self.main_layout.add_widget(title)

        # Spreads grid
        spreads_grid = GridLayout(cols=2, spacing=15, size_hint_y=0.85)

        spread_options = {
            "Single Card": {"cards": 1, "description": "Focus on one question"},
            "Three-Card": {"cards": 3, "description": "Past, Present, Future"},
            "Five-Card": {"cards": 5, "description": "Detailed insight"},
            "Celtic Cross": {"cards": 10, "description": "Complete reading"}
        }

        card_back_path = self.get_card_back_path()

        for name, info in spread_options.items():
            spread_container = BoxLayout(orientation='vertical', spacing=5)

            # Card image button
            card_button = Button(
                background_normal=card_back_path or '',
                background_down=card_back_path or '',
                background_color=(1, 1, 1, 1),
                border=(0, 0, 0, 0),
                size_hint_y=0.7
            )
            card_button.bind(on_press=lambda btn, c=info["cards"], n=name: self.draw_and_display_spread(c, n))

            # Spread name
            name_label = Label(
                text=name, 
                font_size='16sp', 
                halign='center',
                color=(1, 1, 1, 1),
                size_hint_y=0.2
            )

            # Description
            desc_label = Label(
                text=info["description"], 
                font_size='12sp', 
                halign='center',
                color=(0.8, 0.8, 0.8, 1),
                size_hint_y=0.1
