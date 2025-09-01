import random
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivy.graphics import Color, RoundedRectangle
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
        self.sm = ScreenManager()

        # Main Screen
        main_screen = Screen(name='main')
        main_layout = BoxLayout(orientation='vertical', padding=20, spacing=10)

        main_layout.add_widget(Label(text="Select a Tarot Configuration", font_size='20sp', size_hint_y=0.1))

        # The "Single Card Draw" button now uses the card back image
        single_card_button = Button(
            text="Single Card Draw",
            size_hint=(0.8, 0.2),
            pos_hint={'center_x': 0.5},
            background_normal='images/images/CardBacks.jpg',
            background_down='images/images/CardBacks.jpg'
        )
        single_card_button.bind(on_press=self.draw_single_card)
        main_layout.add_widget(single_card_button)

        main_screen.add_widget(main_layout)
        self.sm.add_widget(main_screen)

        # Draw Screen
        self.draw_screen = Screen(name='draw')
        self.draw_layout = BoxLayout(orientation='vertical', padding=20, spacing=10)

        self.card_label = Label(text="Click to reveal your card", font_size='24sp', size_hint_y=0.1)
        self.card_image = Image(source='images/images/CardBacks.jpg', size_hint=(0.8, 0.8), pos_hint={'center_x': 0.5})

        # The "Reveal Card" and "Go Back" buttons with purple, shiny glass-like style
        class GlassButton(Button):
            def __init__(self, **kwargs):
                super(GlassButton, self).__init__(**kwargs)
                self.background_normal = ''
                self.background_down = ''
                self.bind(pos=self.update_canvas, size=self.update_canvas)
                self.update_canvas()

            def update_canvas(self, *args):
                self.canvas.before.clear()
                with self.canvas.before:
                    Color(0.5, 0, 0.5, 1) # Purple
                    RoundedRectangle(pos=self.pos, size=self.size, radius=[20,])

        reveal_button = GlassButton(
            text="Reveal Card",
            size_hint=(0.5, 0.1),
            pos_hint={'center_x': 0.5}
        )
        reveal_button.bind(on_press=self.draw_single_card)

        back_button = GlassButton(
            text="Go Back",
            size_hint=(0.5, 0.1),
            pos_hint={'center_x': 0.5}
        )
        back_button.bind(on_press=self.go_back)

        self.draw_layout.add_widget(self.card_label)
        self.draw_layout.add_widget(self.card_image)
        self.draw_layout.add_widget(reveal_button)
        self.draw_layout.add_widget(back_button)
        self.draw_screen.add_widget(self.draw_layout)
        self.sm.add_widget(self.draw_screen)

        return self.sm

    def draw_single_card(self, instance):
        random_card = random.choice(tarot_cards)
        orientation = random.choice(["Upright", "Reversed"])

        image_path, is_missing = get_card_image(random_card, orientation)
        self.card_label.text = f"{random_card} ({orientation})" if not is_missing else f"{random_card} ({orientation}) - Image Missing"
        self.card_image.source = image_path
        self.card_image.reload()

        self.sm.current = 'draw'

    def go_back(self, instance):
        self.card_label.text = "Click to reveal your card"
        self.card_image.source = 'images/images/CardBacks.jpg'
        self.card_image.reload()
        self.sm.current = 'main'

if __name__ == '__main__':
    TarotApp().run()
