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
        base_path = self.get_image_base_path(

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
        self.main_layout.clear_widgets(

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
            )

            spread_container.add_widget(card_button)
            spread_container.add_widget(name_label)
            spread_container.add_widget(desc_label)
            spreads_grid.add_widget(spread_container)

        self.main_layout.add_widget(spreads_grid)

    def draw_and_display_spread(self, num_cards, spread_name):
        """Set up the spread display and draw cards"""
        self.main_layout.clear_widgets()

        # Title
        title = Label(
            text=spread_name, 
            font_size='24sp', 
            size_hint_y=0.1,
            color=(1, 1, 1, 1)
        )
        self.main_layout.add_widget(title)

        # Card container
        card_container = BoxLayout(orientation='vertical', size_hint_y=0.8, spacing=10)

        # Draw button
        draw_button = Button(
            text="Draw Cards", 
            size_hint=(1, 0.15),
            background_color=(0.2, 0.6, 0.8, 1),
            color=(1, 1, 1, 1),
            font_size='18sp'
        )
        draw_button.bind(on_press=lambda btn: self.reveal_cards(num_cards))
        card_container.add_widget(draw_button)

        # Card layout - adjust based on spread type
        if spread_name == "Celtic Cross":
            self.card_layout = GridLayout(cols=4, spacing=5, size_hint_y=0.85)
        elif num_cards <= 3:
            self.card_layout = BoxLayout(orientation='horizontal', spacing=10, size_hint_y=0.85)
        else:
            # For larger spreads, use a grid
            cols = 3 if num_cards > 5 else 2
            self.card_layout = GridLayout(cols=cols, spacing=5, size_hint_y=0.85)

        self.card_images = []
        self.cards_to_draw = random.sample(tarot_cards, num_cards)
        self.orientations = [random.choice(["Upright", "Reversed"]) for _ in range(num_cards)]

        card_back_path = self.get_card_back_path()

        for i in range(num_cards):
            card_image = Image(
                source=card_back_path or '',
                allow_stretch=True,
                keep_ratio=True
            )
            self.card_images.append(card_image)
            self.card_layout.add_widget(card_image)

        card_container.add_widget(self.card_layout)
        self.main_layout.add_widget(card_container)

        # Back button
        back_button = Button(
            text="Back to Menu", 
            size_hint=(1, 0.1),
            background_color=(0.6, 0.2, 0.2, 1),
            color=(1, 1, 1, 1),
            font_size='16sp'
        )
        back_button.bind(on_press=lambda btn: self.show_spread_selection())
        self.main_layout.add_widget(back_button)

    def reveal_cards(self, num_cards):
        """Reveal the drawn cards - simplified without rotation"""
        # Clear the card container and rebuild with revealed cards
        card_container = self.main_layout.children[1]  # The card container
        card_container.clear_widgets()

        # Reveal all cards
        for i in range(num_cards):
            card_image = self.card_images[i]
            random_card = self.cards_to_draw[i]
            # Always show upright image (no PIL rotation)

            try:
                image_source, is_missing = self.get_card_image_path(random_card, "Upright")
                if image_source:
                    card_image.source = image_source
                    card_image.reload()
            except Exception as e:
                print(f"Error loading card {random_card}: {e}")
                # Fallback to card back
                card_back = self.get_card_back_path()
                if card_back:
                    card_image.source = card_back

        # Add the card layout back
        card_container.add_widget(self.card_layout)

        # Add card names with orientation indicators
        def show_card_names(dt):
            card_texts = []
            for i in range(num_cards):
                card_name = self.cards_to_draw[i]
                orientation = self.orientations[i]
                # Add visual indicator for reversed cards
                if orientation == "Reversed":
                    display_text = f"{card_name} (↓ Reversed)"
                else:
                    display_text = f"{card_name} (↑ Upright)"
                card_texts.append(display_text)

            cards_label = Label(
                text="\n".join(card_texts), 
                font_size='14sp', 
                halign='center',
                color=(1, 1, 1, 1),
                text_size=(Window.width - 40, None)
            )
            card_container.add_widget(cards_label)

        Clock.schedule_once(show_card_names, 0.5)

if __name__ == '__main__':
    TarotApp().run()
