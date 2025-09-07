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
from kivy.graphics.context_instructions import PushMatrix, PopMatrix
from kivy.graphics.vertex_instructions import Rotate
from kivy.uix.carousel import Carousel
from kivy.uix.relativelayout import RelativeLayout

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


class RotatableImage(Image):
    """A custom Image widget that can be rotated on its canvas."""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.angle = 0  # Default rotation angle
        self.bind(pos=self.update_rotation, size=self.update_rotation)

    def update_rotation(self, *args):
        self.canvas.before.clear()
        with self.canvas.before:
            PushMatrix()
            Rotate(
                angle=self.angle,
                axis=(0, 0, 1),
                origin=self.center
            )
    
    def on_angle(self, instance, value):
        self.angle = value
        self.update_rotation()


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
        """Display the spread selection screen with a new layout."""
        self.main_layout.clear_widgets()

        # Title
        title = Label(
            text="Select a Tarot Spread",
            font_size='24sp',
            size_hint_y=0.15,
            color=(1, 1, 1, 1)
        )
        self.main_layout.add_widget(title)

        # Use a RelativeLayout to place buttons in a custom pattern
        spreads_layout = RelativeLayout(size_hint_y=0.85)

        spread_options = {
            "Single Card": {"cards": 1, "description": "Focus on one question"},
            "Three-Card": {"cards": 3, "description": "Past, Present, Future"},
            "Five-Card": {"cards": 5, "description": "Detailed insight"},
            "Celtic Cross": {"cards": 10, "description": "Complete reading"}
        }

        card_back_path = self.get_card_back_path()
        
        # Position and size the buttons manually
        button_positions = {
            "Single Card": {'pos_hint': {'center_x': 0.25, 'center_y': 0.75}, 'size_hint': (0.4, 0.3)},
            "Three-Card": {'pos_hint': {'center_x': 0.75, 'center_y': 0.75}, 'size_hint': (0.4, 0.3)},
            "Five-Card": {'pos_hint': {'center_x': 0.25, 'center_y': 0.25}, 'size_hint': (0.4, 0.3)},
            "Celtic Cross": {'pos_hint': {'center_x': 0.75, 'center_y': 0.25}, 'size_hint': (0.4, 0.3)}
        }

        for name, info in spread_options.items():
            button_data = button_positions[name]
            
            # Create the button with the new position and size hints
            card_button = Button(
                background_normal=card_back_path or '',
                background_down=card_back_path or '',
                background_color=(1, 1, 1, 1),
                border=(0, 0, 0, 0),
                pos_hint=button_data['pos_hint'],
                size_hint=button_data['size_hint']
            )
            card_button.bind(on_press=lambda btn, c=info["cards"], n=name: self.draw_and_display_spread(c, n))

            # Add labels on top of the button
            name_label = Label(
                text=name,
                font_size='16sp',
                pos_hint=button_data['pos_hint'],
                size_hint=(0.4, 0.3), # Use same size hint as the button
                halign='center',
                color=(1, 1, 1, 1)
            )
            desc_label = Label(
                text=info["description"],
                font_size='12sp',
                pos_hint={'center_x': button_data['pos_hint']['center_x'], 'center_y': button_data['pos_hint']['center_y'] - 0.15},
                size_hint=(0.4, 0.15),
                halign='center',
                color=(0.8, 0.8, 0.8, 1)
            )

            spreads_layout.add_widget(card_button)
            spreads_layout.add_widget(name_label)
            spreads_layout.add_widget(desc_label)

        self.main_layout.add_widget(spreads_layout)


    def draw_and_display_spread(self, num_cards, spread_name):
        """Set up the spread display with a Carousel for one card at a time."""
        self.main_layout.clear_widgets()

        # Title
        title = Label(
            text=spread_name,
            font_size='24sp',
            size_hint_y=0.1,
            color=(1, 1, 1, 1)
        )
        self.main_layout.add_widget(title)

        # The Carousel will hold the individual card widgets
        self.card_carousel = Carousel(direction='right', size_hint_y=0.8)
        self.card_images = []
        self.cards_to_draw = random.sample(tarot_cards, num_cards)
        self.orientations = [random.choice(["Upright", "Reversed"]) for _ in range(num_cards)]
        card_back_path = self.get_card_back_path()

        for i in range(num_cards):
            # Container for each card and its label
            card_container = BoxLayout(orientation='vertical', padding=10, spacing=5)

            # Create the card image
            card_image = RotatableImage(
                source=card_back_path or '',
                allow_stretch=True,
                keep_ratio=True
            )
            # We'll use the ID to reference the correct card data
            card_image.id = str(i)
            # This flag prevents a card from being flipped again
            card_image.revealed = False
            
            # Bind a touch event to each card image
            card_image.bind(on_touch_down=self.on_card_touch)
            
            self.card_images.append(card_image)

            # Label to show card name and position
            position_label = Label(
                text=f"Position {i + 1}",
                font_size='20sp',
                color=(1,1,1,1)
            )
            
            card_container.add_widget(card_image)
            card_container.add_widget(position_label)
            
            self.card_carousel.add_widget(card_container)

        self.main_layout.add_widget(self.card_carousel)

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

    def on_card_touch(self, instance, touch):
        """Handles the tap on a card image to reveal it."""
        # Check if the touch is within the widget's bounds and it hasn't been revealed
        if instance.collide_point(*touch.pos) and not instance.revealed:
            instance.revealed = True
            card_index = int(instance.id)

            # Get the card's data
            card_name = self.cards_to_draw[card_index]
            orientation = self.orientations[card_index]

            # Set the rotation angle
            if orientation == "Reversed":
                instance.angle = 180
            else:
                instance.angle = 0

            # Update the card image source
            image_source, is_missing = self.get_card_image_path(card_name, "Upright")
            if image_source:
                instance.source = image_source
                instance.reload()

            # Update the label with the card name
            # The label is the first child of the parent container
            card_container = instance.parent
            position_label = card_container.children[0]
            
            # Use a short delay to allow the card flip to be seen
            def update_label(dt):
                position_label.text = f"{card_name}\n({position_label.text})"
            
            Clock.schedule_once(update_label, 0.1)


if __name__ == '__main__':
    TarotApp().run()

