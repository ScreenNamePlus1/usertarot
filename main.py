import random
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from PIL import Image as PilImage

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
    image_path = f'images/{card_name.replace(" ", "_")}.jpg'
    
    if orientation == "Reversed":
        try:
            pil_img = PilImage.open(image_path)
            pil_img_flipped = pil_img.transpose(PilImage.ROTATE_180) # Flip upside down for "reversed"
            # Kivy can't load from PIL object directly, save it temporarily
            temp_path = 'temp_card.png'
            pil_img_flipped.save(temp_path)
            return temp_path
        except FileNotFoundError:
            return image_path  # Fallback if image doesn't exist
    return image_path

class TarotApp(App):
    def build(self):
        self.sm = ScreenManager()

        # Main Screen
        main_screen = Screen(name='main')
        main_layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        
        main_layout.add_widget(Label(text="Select a Tarot Configuration", font_size='20sp', size_hint_y=0.1))
        
        single_card_button = Button(text="Single Card Draw", size_hint=(0.8, 0.2), pos_hint={'center_x': 0.5})
        single_card_button.bind(on_press=self.draw_single_card)
        main_layout.add_widget(single_card_button)
        
        # Add other configurations here later
        
        main_screen.add_widget(main_layout)
        self.sm.add_widget(main_screen)

        # Draw Screen
        self.draw_screen = Screen(name='draw')
        self.draw_layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        
        self.card_label = Label(text="", font_size='24sp', size_hint_y=0.1)
        self.card_image = Image(size_hint=(0.8, 0.8), pos_hint={'center_x': 0.5})
        
        back_button = Button(text="Go Back", size_hint=(0.5, 0.1), pos_hint={'center_x': 0.5})
        back_button.bind(on_press=self.go_back)
        
        self.draw_layout.add_widget(self.card_label)
        self.draw_layout.add_widget(self.card_image)
        self.draw_layout.add_widget(back_button)
        self.draw_screen.add_widget(self.draw_layout)
        self.sm.add_widget(self.draw_screen)

        return self.sm

    def draw_single_card(self, instance):
        random_card = random.choice(tarot_cards)
        orientation = random.choice(["Upright", "Reversed"])
        
        self.card_label.text = f"{random_card} ({orientation})"
        
        image_path = get_card_image(random_card, orientation)
        self.card_image.source = image_path
        self.card_image.reload()
        
        self.sm.current = 'draw'

    def go_back(self, instance):
        self.sm.current = 'main'

if __name__ == '__main__':
    TarotApp().run()
