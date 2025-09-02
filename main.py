import random
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.core.window import Window
from PIL import Image as PilImage
import os

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
    # Map mismatched card names to correct image files
    image_map = {
        "Ten of Cups": "Page_of_Cups",
        "Ten of Pentacles": "Page_of_Pentacles"
    }
    image_name = image_map.get(card_name, card_name)
    image_path = f'images/images/{image_name.replace(" ", "_")}.jpg'

    if orientation == "Reversed":
        try:
            pil_img = PilImage.open(image_path)
            pil_img_flipped = pil_img.transpose(PilImage.ROTATE_180)
            temp_path = 'temp_card.png'
            pil_img_flipped.save(temp_path)
            return temp_path, False
        except FileNotFoundError:
            return 'images/images/CardBacks.jpg', True
    try:
        PilImage.open(image_path)
        return image_path, False
    except FileNotFoundError:
        return 'images/images/CardBacks.jpg', True

class TarotApp(App):
    def build(self):
        # Set up a single main layout
        main_layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        
        # Add a title label
        main_layout.add_widget(Label(text="Tarot Card Draw", font_size='24sp', size_hint_y=0.1))

        # Add the main card image, initially showing the card back
        self.card_image = Image(source='images/images/CardBacks.jpg', size_hint=(0.8, 0.6), pos_hint={'center_x': 0.5})
        main_layout.add_widget(self.card_image)

        # Bind the touch event directly to the card image
        self.card_image.bind(on_touch_down=self.on_card_tap)

        # Add a label to display the card name
        self.card_label = Label(text="Tap the card to reveal your destiny", font_size='18sp', size_hint_y=0.1)
        main_layout.add_widget(self.card_label)

        return main_layout
    
    def on_card_tap(self, instance, touch):
        # Check if the touch is within the bounds of the image
        if instance.collide_point(*touch.pos):
            self.draw_single_card()

    def draw_single_card(self):
        # Select a random card and orientation
        random_card = random.choice(tarot_cards)
        orientation = random.choice(["Upright", "Reversed"])

        # Get the correct image path
        image_path, is_missing = get_card_image(random_card, orientation)

        # Update the card image source and the label text on the same screen
        self.card_image.source = image_path
        self.card_image.reload() # Force a reload to show the new image

        # Update the label with the card name and orientation
        if is_missing:
            self.card_label.text = f"{random_card} ({orientation}) - Image Missing"
        else:
            self.card_label.text = f"{random_card} ({orientation})"

if __name__ == '__main__':
    TarotApp().run()
