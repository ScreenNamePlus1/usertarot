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
from kivy.uix.floatlayout import FloatLayout
from kivy.logger import Logger
from kivy.graphics import PushMatrix, PopMatrix, Rotate
from kivy.uix.behaviors import ButtonBehavior

# Force portrait orientation and set black background
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


class TarotCardImage(ButtonBehavior, Image):
    """A tarot card that acts as a button with immediate rotation"""
    def __init__(self, card_name, orientation, **kwargs):
        super().__init__(**kwargs)
        self.card_name = card_name
        self.orientation = orientation
        self.is_revealed = False
        
        # Apply rotation immediately if reversed
        if orientation == "Reversed":
            self._apply_rotation()
    
    def _apply_rotation(self):
        """Apply 180-degree rotation immediately"""
        self.canvas.before.clear()
        self.canvas.after.clear()
        
        with self.canvas.before:
            PushMatrix()
            # Rotate around center
            Rotate(angle=180, origin=(self.center_x, self.center_y))
            
        with self.canvas.after:
            PopMatrix()
            
        # Rebind to update rotation when position changes
        self.bind(pos=self._update_rotation, size=self._update_rotation)
    
    def _update_rotation(self, *args):
        """Update rotation center when position/size changes"""
        if self.orientation == "Reversed":
            self.canvas.before.clear()
            self.canvas.after.clear()
            
            with self.canvas.before:
                PushMatrix()
                Rotate(angle=180, origin=(self.center_x, self.center_y))
                
            with self.canvas.after:
                PopMatrix()


class CardButton(ButtonBehavior, FloatLayout):
    """A card-shaped button for the menu"""
    def __init__(self, card_image_path, title_text, subtitle_text, **kwargs):
        super().__init__(**kwargs)
        
        # Card background image
        card_bg = Image(
            source=card_image_path,
            allow_stretch=True,
            keep_ratio=True,
            size_hint=(1, 1),
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )
        self.add_widget(card_bg)
        
        # Semi-transparent overlay for text readability
        overlay = FloatLayout(
            size_hint=(1, 1),
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )
        
        # Title
        title = Label(
            text=title_text,
            font_size='18sp',
            bold=True,
            color=(1, 1, 1, 1),
            outline_color=(0, 0, 0, 1),
            outline_width=2,
            size_hint=(1, 0.3),
            pos_hint={'center_x': 0.5, 'center_y': 0.7},
            halign='center',
            valign='middle'
        )
        title.bind(size=title.setter('text_size'))
        
        # Subtitle
        subtitle = Label(
            text=subtitle_text,
            font_size='14sp',
            color=(0.9, 0.9, 0.9, 1),
            outline_color=(0, 0, 0, 1),
            outline_width=1,
            size_hint=(1, 0.2),
            pos_hint={'center_x': 0.5, 'center_y': 0.3},
            halign='center',
            valign='middle'
        )
        subtitle.bind(size=subtitle.setter('text_size'))
        
        overlay.add_widget(title)
        overlay.add_widget(subtitle)
        self.add_widget(overlay)


class TarotApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Logger.info("TarotApp: Initializing")

    def build(self):
        Logger.info("TarotApp: Building app")
        
        # Set the application icon
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

        # Main container - always portrait
        self.main_layout = FloatLayout()
        self.show_card_menu()
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
        return 'images/'

    def get_card_image_path(self, card_name):
        """Get the correct image path for a card"""
        base_path = self.get_image_base_path()

        # Format the card name for file lookup
        formatted_name = card_name.replace(" ", "_")
        if card_name.startswith("The "):
            formatted_name = card_name.replace(" ", "_")

        # Handle card back as special case
        if formatted_name == "CardBacks" or card_name == "CardBacks":
            for ext in ['.png', '.jpg', '.jpeg']:
                path = f'{base_path}CardBacks{ext}'
                if os.path.exists(path):
                    return path
            return None

        # Try different file extensions
        for ext in ['.png', '.jpg', '.jpeg']:
            image_path = f'{base_path}{formatted_name}{ext}'
            if os.path.exists(image_path):
                return image_path

        # Fallback to card back
        return self.get_card_back_path()

    def get_card_back_path(self):
        """Get the path to the card back image"""
        base_path = self.get_image_base_path()
        for ext in ['.png', '.jpg', '.jpeg']:
            path = f'{base_path}CardBacks{ext}'
            if os.path.exists(path):
                return path
        return None

    def show_card_menu(self):
        """Display the main menu with card-shaped buttons"""
        Logger.info("TarotApp: Showing card menu")
        self.main_layout.clear_widgets()

        # Background container
        container = BoxLayout(
            orientation='vertical',
            padding=30,
            spacing=20,
            size_hint=(0.9, 0.9),
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )

        # Title
        title = Label(
            text="Choose Your Reading",
            font_size='28sp',
            bold=True,
            color=(1, 1, 1, 1),
            size_hint_y=0.15,
            halign='center'
        )
        container.add_widget(title)

        # Card grid - 2x2 layout
        cards_grid = GridLayout(
            cols=2,
            rows=2,
            spacing=15,
            size_hint_y=0.85
        )

        # Get card back image for buttons
        card_back_path = self.get_card_back_path()

        # Spread options with card-like buttons
        spread_options = [
            ("Single Card", 1, "One card for focus"),
            ("Three-Card", 3, "Past • Present • Future"),
            ("Five-Card", 5, "Deeper insight"),
            ("Celtic Cross", 10, "Complete reading")
        ]

        for name, cards, description in spread_options:
            card_button = CardButton(
                card_image_path=card_back_path or '',
                title_text=name,
                subtitle_text=description
            )
            card_button.bind(on_press=lambda btn, c=cards, n=name: self.start_reading(c, n))
            cards_grid.add_widget(card_button)

        container.add_widget(cards_grid)
        self.main_layout.add_widget(container)

    def start_reading(self, num_cards, spread_name):
        """Start a tarot reading"""
        Logger.info(f"TarotApp: Starting {spread_name} reading with {num_cards} cards")
        
        # Draw cards and orientations
        self.current_cards = random.sample(tarot_cards, num_cards)
        self.current_orientations = [random.choice(["Upright", "Reversed"]) for _ in range(num_cards)]
        self.current_spread_name = spread_name
        self.card_index = 0
        
        self.show_card()

    def show_card(self):
        """Display the current card cleanly"""
        self.main_layout.clear_widgets()
        
        # Get current card info
        card_name = self.current_cards[self.card_index]
        orientation = self.current_orientations[self.card_index]
        
        # Main container
        container = BoxLayout(
            orientation='vertical',
            padding=40,
            spacing=20,
            size_hint=(0.95, 0.95),
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )

        # Spread info (small, at top)
        info_text = f"{self.current_spread_name} • Card {self.card_index + 1} of {len(self.current_cards)}"
        info_label = Label(
            text=info_text,
            font_size='14sp',
            color=(0.7, 0.7, 0.7, 1),
            size_hint_y=0.08,
            halign='center'
        )
        container.add_widget(info_label)

        # Get card image path
        card_back_path = self.get_card_back_path()
        
        # Create the tarot card (this will be the main button)
        self.current_card_widget = TarotCardImage(
            card_name=card_name,
            orientation=orientation,
            source=card_back_path,
            allow_stretch=True,
            keep_ratio=True,
            size_hint=(1, 0.84)
        )
        
        # Bind the card tap
        self.current_card_widget.bind(on_press=self.reveal_card)
        
        container.add_widget(self.current_card_widget)

        # Instructions (small, at bottom)
        instruction_label = Label(
            text="Tap the card to reveal",
            font_size='16sp',
            color=(0.8, 0.8, 0.8, 1),
            size_hint_y=0.08,
            halign='center'
        )
        container.add_widget(instruction_label)

        self.main_layout.add_widget(container)

    def reveal_card(self, instance):
        """Reveal the current card"""
        if instance.is_revealed:
            # If already revealed, go to next card or back to menu
            self.next_card_or_menu()
            return
            
        Logger.info(f"TarotApp: Revealing {instance.card_name} ({instance.orientation})")
        
        # Get the actual card image
        card_image_path = self.get_card_image_path(instance.card_name)
        
        if card_image_path and os.path.exists(card_image_path):
            instance.source = card_image_path
            instance.is_revealed = True
            
            # Update instruction text
            for child in self.main_layout.children:
                if isinstance(child, BoxLayout):
                    for subchild in child.children:
                        if isinstance(subchild, Label) and "Tap the card" in subchild.text:
                            card_text = f"{instance.card_name}"
                            orientation_text = f"({instance.orientation})"
                            if self.card_index + 1 < len(self.current_cards):
                                next_text = "Tap for next card"
                            else:
                                next_text = "Tap to return to menu"
                            subchild.text = f"{card_text}\n{orientation_text}\n\n{next_text}"
                            break

    def next_card_or_menu(self):
        """Move to next card or return to menu"""
        self.card_index += 1
        
        if self.card_index >= len(self.current_cards):
            # All cards shown, return to menu
            self.show_card_menu()
        else:
            # Show next card
            self.show_card()


if __name__ == '__main__':
    Logger.info("TarotApp: Starting application")
    TarotApp().run()