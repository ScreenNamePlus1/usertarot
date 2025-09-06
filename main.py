import random
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.core.window import Window
from PIL import Image as PilImage
import os
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout

# Set the window background color to black
Window.clearcolor = (0, 0, 0, 1)

# Define the suits and ranks of the tarot cards
suits = ["Wands", "Cups", "Swords", "Pentacles"]
ranks = ["Ace", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine", "Ten", "Page", "Knight", "Queen", "King"]
major_arcana = ["The Fool", "The Magician", "The High Priestess", "The Empress", "The Emperor", "The Hierophant", "The Lovers", "The Chariot", "Strength", "The Hermit", "Wheel of Fortune", "Justice", "The Hanged Man", "Death", "Temperance", "The Devil", "The Tower", "The Star", "The Moon", "The Sun", "Judgement", "The World"]

# Create a list of all the tarot cards
tarot_cards = []
for suit in suits:
    for rank in ranks:
        tarot_cards.append(rank + " of " + suit)
tarot_cards.extend(major_arcana)

# Helper function to get the image path and flip if reversed
def get_card_image(card_name, orientation):
    formatted_name = card_name.replace(" ", "_").replace("The_", "")
    if card_name.startswith("The"):
        formatted_name = card_name.replace(" ", "_")
    
    # Check for both .png and .jpg for the card backs
    if formatted_name == "CardBacks":
        if os.path.exists(f'rider-waite-tarot/CardBacks.png'):
            return 'rider-waite-tarot/CardBacks.png', False
        elif os.path.exists(f'rider-waite-tarot/CardBacks.jpg'):
            return 'rider-waite-tarot/CardBacks.jpg', False
        else:
            return None, True

    image_path = f'rider-waite-tarot/{formatted_name}.png'

    if orientation == "Reversed":
        try:
            pil_img = PilImage.open(image_path)
            pil_img_flipped = pil_img.transpose(PilImage.ROTATE_180)
            temp_path = 'temp_card.png'
            pil_img_flipped.save(temp_path)
            return temp_path, False
        except FileNotFoundError:
            return get_card_image("CardBacks", "Upright")[0], True
    try:
        PilImage.open(image_path)
        return image_path, False
    except FileNotFoundError:
        return get_card_image("CardBacks", "Upright")[0], True

class TarotApp(App):
    def build(self):
        # Set the application icon to CardBacks.jpg
        self.icon = 'rider-waite-tarot/CardBacks.jpg'
        
        self.main_layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        self.show_spread_selection()
        return self.main_layout

    def show_spread_selection(self):
        self.main_layout.clear_widgets() # Clear all widgets
        self.main_layout.add_widget(Label(text="Select a Tarot Spread", font_size='24sp', size_hint_y=0.1))

        # Use a grid layout for a clean menu of options
        spreads_grid = GridLayout(cols=3, spacing=10)
        
        spread_options = {
            "Single Card": 1,
            "Three-Card": 3,
            "Five-Card": 5,
            "Seven-Card": 7,
            "Celtic Cross": 10,
            "The Cross": 2
        }

        for name, num_cards in spread_options.items():
            spread_button = BoxLayout(orientation='vertical', size_hint_y=None, height=150)
            
            card_button = Button(
                background_normal=get_card_image("CardBacks", "Upright")[0],
                background_down=get_card_image("CardBacks", "Upright")[0],
                background_color=(1, 1, 1, 1),
                border=(0, 0, 0, 0)
            )
            card_button.bind(on_press=lambda btn, c=num_cards, n=name: self.draw_and_display_spread(c, n))
            
            label = Label(text=name, font_size='14sp', halign='center')
            
            spread_button.add_widget(card_button)
            spread_button.add_widget(label)
            spreads_grid.add_widget(spread_button)
        
        self.main_layout.add_widget(spreads_grid)

    def draw_and_display_spread(self, num_cards, spread_name):
        self.main_layout.clear_widgets()
        
        # Add the title label for the spread
        self.main_layout.add_widget(Label(text=spread_name, font_size='24sp', size_hint_y=0.1))
        
        # Create a container for the cards and bind a touch event to it
        card_container = BoxLayout(orientation='vertical', size_hint_y=0.8)
        
        # Add a "Draw" button
        draw_button = Button(text="Draw Cards", size_hint=(1, 0.1), on_press=lambda btn: self.reveal_cards(num_cards))
        card_container.add_widget(draw_button)
        
        # The layout for the cards themselves
        self.card_layout = BoxLayout(orientation='horizontal', spacing=10)
        
        if spread_name == "Celtic Cross":
            # Simplified Celtic Cross layout for demonstration
            self.card_layout = GridLayout(cols=3, spacing=10)
            self.card_labels = []
            
        self.cards_to_draw = random.sample(tarot_cards, num_cards)
        self.card_images = []
        
        for _ in range(num_cards):
            card_image = Image(
                source=get_card_image("CardBacks", "Upright")[0],
                allow_stretch=True,
                keep_ratio=True
            )
            self.card_images.append(card_image)
            self.card_layout.add_widget(card_image)
            
        card_container.add_widget(self.card_layout)
        self.main_layout.add_widget(card_container)
        
        # Add a back button
        back_button = Button(text="Back to Menu", size_hint=(1, 0.1), on_press=lambda btn: self.show_spread_selection())
        self.main_layout.add_widget(back_button)
        
    def reveal_cards(self, num_cards):
        self.main_layout.children[-2].clear_widgets() # Clear the previous layout

        card_layout_container = BoxLayout(orientation='horizontal', spacing=10)
        card_texts = []
        for i in range(num_cards):
            random_card = self.cards_to_draw[i]
            orientation = random.choice(["Upright", "Reversed"])
            image_path, is_missing = get_card_image(random_card, orientation)
            
            # Create new image widgets with the drawn cards
            card_image = Image(source=image_path, allow_stretch=True, keep_ratio=True)
            card_layout_container.add_widget(card_image)
            
            card_texts.append(f"{random_card} ({orientation})")

        self.main_layout.children[-2].add_widget(card_layout_container)
        self.main_layout.children[-2].add_widget(Label(text="\n".join(card_texts), font_size='18sp', halign='center'))
