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
from kivy.uix.carousel import Carousel
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.logger import Logger
from kivy.graphics import PushMatrix, PopMatrix, Rotate

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


class RotatedTarotImage(Image):
    """A robust rotatable image widget for tarot cards"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._rotation_angle = 0
        self.bind(pos=self._update_rotation, size=self._update_rotation)
        Clock.schedule_once(self._update_rotation, 0.1)
        
    def set_rotation(self, angle):
        """Set the rotation angle for the card"""
        self._rotation_angle = angle
        self._update_rotation()
        
    def _update_rotation(self, *args):
        """Apply rotation transformation to the widget"""
        self.canvas.before.clear()
        self.canvas.after.clear()
        
        if self._rotation_angle != 0:
            with self.canvas.before:
                PushMatrix()
                # Calculate center point for rotation
                center_x = self.center_x
                center_y = self.center_y
                Rotate(angle=self._rotation_angle, origin=(center_x, center_y))
                
            with self.canvas.after:
                PopMatrix()


class TarotApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Logger.info("TarotApp: Initializing")

    def build(self):
        Logger.info("TarotApp: Building app")
        
        # Set the application icon - check multiple possible paths
        icon_paths = [
            'images/AppIcons/playstore.png',
            'images/rider-waite-tarot/CardBacks.jpg',
            'images/CardBacks.jpg',
            'CardBacks.jpg'
        ]

        for path in icon_paths:
            if os.path.exists(path):
                self.icon = path
                Logger.info(f"TarotApp: Using icon: {path}")
                break

        # Use FloatLayout as root to prevent off-screen issues
        self.root_layout = FloatLayout()
        self.main_layout = BoxLayout(
            orientation='vertical', 
            padding=20, 
            spacing=10,
            size_hint=(0.95, 0.95),  # Ensure it stays within screen bounds
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )
        self.root_layout.add_widget(self.main_layout)
        
        self.show_spread_selection()
        return self.root_layout

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

        # Try different file extensions
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
        """Display the spread selection screen with a safer grid layout."""
        Logger.info("TarotApp: Showing spread selection")
        self.main_layout.clear_widgets()

        # Title
        title = Label(
            text="Select a Tarot Spread",
            font_size='24sp',
            size_hint_y=0.15,
            color=(1, 1, 1, 1)
        )
        self.main_layout.add_widget(title)

        # Use a simple grid layout instead of RelativeLayout for better stability
        spreads_layout = GridLayout(
            cols=2, 
            rows=2, 
            spacing=20, 
            padding=20,
            size_hint_y=0.75
        )

        spread_options = [
            ("Single Card", 1, "Focus on one question"),
            ("Three-Card", 3, "Past, Present, Future"),
            ("Five-Card", 5, "Detailed insight"),
            ("Celtic Cross", 10, "Complete reading")
        ]

        for name, cards, description in spread_options:
            # Create a container for each spread option
            spread_container = BoxLayout(orientation='vertical', spacing=5)
            
            # Create the button
            spread_button = Button(
                text=name,
                background_color=(0.3, 0.3, 0.6, 1),
                color=(1, 1, 1, 1),
                font_size='16sp'
            )
            spread_button.bind(on_press=lambda btn, c=cards, n=name: self.draw_and_display_spread(c, n))
            
            # Create description label
            desc_label = Label(
                text=description,
                font_size='12sp',
                color=(0.8, 0.8, 0.8, 1),
                size_hint_y=0.3
            )
            
            spread_container.add_widget(spread_button)
            spread_container.add_widget(desc_label)
            spreads_layout.add_widget(spread_container)

        self.main_layout.add_widget(spreads_layout)

        # Add some bottom spacing
        spacer = Label(text="", size_hint_y=0.1)
        self.main_layout.add_widget(spacer)

    def draw_and_display_spread(self, num_cards, spread_name):
        """Set up the spread display with proper card rotation."""
        Logger.info(f"TarotApp: Drawing spread: {spread_name} with {num_cards} cards")
        self.main_layout.clear_widgets()

        # Title
        title = Label(
            text=f"{spread_name} - Card 1 of {num_cards}",
            font_size='20sp',
            size_hint_y=0.1,
            color=(1, 1, 1, 1)
        )
        self.main_layout.add_widget(title)

        # Store the title for updating
        self.current_title = title
        self.spread_name = spread_name
        self.num_cards = num_cards

        # Create a simple layout for the current card
        card_area = BoxLayout(
            orientation='vertical', 
            spacing=10, 
            padding=20,
            size_hint_y=0.7
        )

        # Initialize card data
        self.cards_to_draw = random.sample(tarot_cards, num_cards)
        self.orientations = [random.choice(["Upright", "Reversed"]) for _ in range(num_cards)]
        self.current_card_index = 0
        self.revealed_cards = [False] * num_cards

        # Create the main card image using our rotatable image
        card_back_path = self.get_card_back_path()
        self.current_card_image = RotatedTarotImage(
            source=card_back_path or '',
            allow_stretch=True,
            keep_ratio=True,
            size_hint=(1, 0.8)
        )
        
        # Card info label
        self.card_info_label = Label(
            text="Tap card to reveal",
            font_size='16sp',
            color=(1, 1, 1, 1),
            size_hint_y=0.2,
            halign='center'
        )
        
        card_area.add_widget(self.current_card_image)
        card_area.add_widget(self.card_info_label)
        self.main_layout.add_widget(card_area)

        # Bind touch event to reveal card
        self.current_card_image.bind(on_touch_down=self.on_card_touch)

        # Navigation and control buttons
        button_layout = BoxLayout(
            orientation='horizontal', 
            spacing=10,
            size_hint_y=0.15
        )

        # Previous card button
        prev_button = Button(
            text="← Previous",
            background_color=(0.4, 0.4, 0.4, 1),
            disabled=True  # Disabled on first card
        )
        prev_button.bind(on_press=self.show_previous_card)
        self.prev_button = prev_button

        # Next card button
        next_button = Button(
            text="Next →",
            background_color=(0.4, 0.4, 0.4, 1),
            disabled=(num_cards == 1)  # Disabled if only one card
        )
        next_button.bind(on_press=self.show_next_card)
        self.next_button = next_button

        # Back to menu button
        back_button = Button(
            text="Back to Menu",
            background_color=(0.6, 0.2, 0.2, 1)
        )
        back_button.bind(on_press=lambda btn: self.show_spread_selection())

        button_layout.add_widget(prev_button)
        button_layout.add_widget(back_button)
        button_layout.add_widget(next_button)
        
        self.main_layout.add_widget(button_layout)

        # Update the display for the current card
        self.update_card_display()

    def update_card_display(self):
        """Update the display for the current card with proper rotation"""
        card_num = self.current_card_index + 1
        self.current_title.text = f"{self.spread_name} - Card {card_num} of {self.num_cards}"
        
        # Update navigation buttons
        self.prev_button.disabled = (self.current_card_index == 0)
        self.next_button.disabled = (self.current_card_index >= self.num_cards - 1)
        
        # Show the appropriate card state
        if self.revealed_cards[self.current_card_index]:
            # Show revealed card
            card_name = self.cards_to_draw[self.current_card_index]
            orientation = self.orientations[self.current_card_index]
            
            image_source, is_missing = self.get_card_image_path(card_name, "Upright")
            if image_source and os.path.exists(image_source):
                self.current_card_image.source = image_source
                
                # Apply rotation after a short delay to ensure image is loaded
                def apply_rotation(dt):
                    if orientation == "Reversed":
                        self.current_card_image.set_rotation(180)
                        Logger.info(f"TarotApp: Applied 180° rotation to {card_name}")
                    else:
                        self.current_card_image.set_rotation(0)
                
                Clock.schedule_once(apply_rotation, 0.2)
            
            # Update label
            orientation_text = "↑ Upright" if orientation == "Upright" else "↓ Reversed"
            self.card_info_label.text = f"{card_name}\n{orientation_text}"
            
        else:
            # Show card back
            card_back_path = self.get_card_back_path()
            if card_back_path:
                self.current_card_image.source = card_back_path
                self.current_card_image.set_rotation(0)  # Always show card backs upright
            self.card_info_label.text = "Tap card to reveal"

    def show_previous_card(self, instance):
        """Navigate to the previous card"""
        if self.current_card_index > 0:
            self.current_card_index -= 1
            self.update_card_display()

    def show_next_card(self, instance):
        """Navigate to the next card"""
        if self.current_card_index < self.num_cards - 1:
            self.current_card_index += 1
            self.update_card_display()

    def on_card_touch(self, instance, touch):
        """Handles the tap on a card image to reveal it with rotation"""
        # Check if the touch is within the widget's bounds
        if not instance.collide_point(*touch.pos):
            return False
        
        # Only reveal if not already revealed
        if not self.revealed_cards[self.current_card_index]:
            Logger.info(f"TarotApp: Revealing card {self.current_card_index}")
            self.revealed_cards[self.current_card_index] = True
            
            # Update display with rotation
            self.update_card_display()
            
        return True  # Consume the touch event


if __name__ == '__main__':
    Logger.info("TarotApp: Starting application")
    TarotApp().run()