import random
import json
import os
from datetime import datetime, date
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.uix.slider import Slider
from kivy.uix.switch import Switch
from kivy.logger import Logger
from kivy.graphics import PushMatrix, PopMatrix, Rotate, Color, Rectangle
from kivy.uix.behaviors import ButtonBehavior
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.core.audio import SoundLoader

# Force portrait orientation and set mystical dark background
Window.clearcolor = (0.05, 0.05, 0.15, 1)  # Deep purple-black

# Enhanced card definitions with meanings
suits = ["Wands", "Cups", "Swords", "Pentacles"]
ranks = ["Ace", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine", "Ten", "Page", "Knight", "Queen", "King"]
major_arcana = ["The Fool", "The Magician", "The High Priestess", "The Empress", "The Emperor", "The Hierophant", "The Lovers",
                "The Chariot", "Strength", "The Hermit", "Wheel of Fortune", "Justice", "The Hanged Man", "Death",
                "Temperance", "The Devil", "The Tower", "The Star", "The Moon", "The Sun", "Judgement", "The World"]

# Card meanings database
CARD_MEANINGS = {
    # Major Arcana
    "The Fool": {
        "upright": "New beginnings, innocence, spontaneity, free spirit",
        "reversed": "Recklessness, taken advantage of, inconsideration"
    },
    "The Magician": {
        "upright": "Manifestation, resourcefulness, power, inspired action",
        "reversed": "Manipulation, poor planning, untapped talents"
    },
    "Death": {
        "upright": "Endings, transformation, transition, new beginnings",
        "reversed": "Resistance to change, personal transformation, inner purging"
    },
    "The Star": {
        "upright": "Hope, faith, purpose, renewal, spirituality",
        "reversed": "Lack of faith, despair, self-trust, disconnection"
    },
    # Add more as needed - this is just a sample
}

# Spread definitions
SPREADS = {
    "Daily Guidance": {
        "cards": 1,
        "positions": ["Your guidance for today"],
        "description": "A single card to guide your day"
    },
    "Past-Present-Future": {
        "cards": 3,
        "positions": ["Past influences", "Present situation", "Future potential"],
        "description": "Classic three-card timeline reading"
    },
    "Love & Relationships": {
        "cards": 5,
        "positions": ["You in love", "Your partner", "The relationship", "Challenges", "Outcome"],
        "description": "Deep dive into your romantic life"
    },
    "Career Path": {
        "cards": 4,
        "positions": ["Current career", "Hidden talents", "Obstacles", "Next steps"],
        "description": "Navigate your professional journey"
    },
    "Celtic Cross": {
        "cards": 10,
        "positions": ["Present", "Challenge", "Distant Past", "Recent Past", "Possible Outcome", 
                     "Near Future", "Your Approach", "External Influences", "Hopes & Fears", "Final Outcome"],
        "description": "The most comprehensive tarot spread"
    },
    "Chakra Balance": {
        "cards": 7,
        "positions": ["Root Chakra", "Sacral Chakra", "Solar Plexus", "Heart Chakra", 
                     "Throat Chakra", "Third Eye", "Crown Chakra"],
        "description": "Align your spiritual energy centers"
    }
}

# Create full deck
tarot_cards = []
for suit in suits:
    for rank in ranks:
        tarot_cards.append(f"{rank} of {suit}")
tarot_cards.extend(major_arcana)


class AnimatedButton(ButtonBehavior, FloatLayout):
    """Animated button with glow effects"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.original_size = None
        
    def on_press(self):
        if not self.original_size:
            self.original_size = self.size[:]
        # Subtle press animation
        anim = Animation(size=(self.width * 0.95, self.height * 0.95), duration=0.1)
        anim.bind(on_complete=lambda *x: Animation(size=self.original_size, duration=0.1).start(self))
        anim.start(self)


class TarotCardImage(AnimatedButton, Image):
    """Enhanced tarot card with animations and sound"""
    def __init__(self, card_name, orientation, app_instance, **kwargs):
        super().__init__(**kwargs)
        self.card_name = card_name
        self.orientation = orientation
        self.is_revealed = False
        self.app_instance = app_instance
        
        # Apply rotation immediately if reversed
        if orientation == "Reversed":
            self._apply_rotation()
    
    def _apply_rotation(self):
        """Apply 180-degree rotation with smooth animation"""
        self.canvas.before.clear()
        self.canvas.after.clear()
        
        with self.canvas.before:
            PushMatrix()
            Rotate(angle=180, origin=(self.center_x, self.center_y))
            
        with self.canvas.after:
            PopMatrix()
            
        self.bind(pos=self._update_rotation, size=self._update_rotation)
    
    def _update_rotation(self, *args):
        if self.orientation == "Reversed":
            self.canvas.before.clear()
            self.canvas.after.clear()
            
            with self.canvas.before:
                PushMatrix()
                Rotate(angle=180, origin=(self.center_x, self.center_y))
                
            with self.canvas.after:
                PopMatrix()

    def on_press(self):
        super().on_press()
        # Play card flip sound if enabled
        if self.app_instance.sound_enabled and hasattr(self.app_instance, 'flip_sound'):
            try:
                self.app_instance.flip_sound.play()
            except:
                pass


class MysticalButton(AnimatedButton):
    """Mystical-themed button with gradient background"""
    def __init__(self, text, **kwargs):
        super().__init__(**kwargs)
        
        # Gradient background
        with self.canvas.before:
            Color(0.2, 0.1, 0.4, 0.8)  # Purple
            self.bg_rect = Rectangle(pos=self.pos, size=self.size)
            
        self.bind(pos=self._update_bg, size=self._update_bg)
        
        # Text label
        self.label = Label(
            text=text,
            font_size='16sp',
            bold=True,
            color=(1, 1, 1, 1),
            outline_color=(0.3, 0.1, 0.5, 1),
            outline_width=1
        )
        self.add_widget(self.label)
    
    def _update_bg(self, *args):
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size


class ReadingHistoryManager:
    """Manages reading history and journal entries"""
    def __init__(self):
        self.history_file = "tarot_history.json"
        self.load_history()
    
    def load_history(self):
        try:
            with open(self.history_file, 'r') as f:
                self.history = json.load(f)
        except:
            self.history = {"readings": [], "journal": []}
    
    def save_history(self):
        try:
            with open(self.history_file, 'w') as f:
                json.dump(self.history, f, indent=2)
        except Exception as e:
            Logger.error(f"Failed to save history: {e}")
    
    def add_reading(self, spread_name, cards, orientations, notes=""):
        reading = {
            "date": datetime.now().isoformat(),
            "spread": spread_name,
            "cards": cards,
            "orientations": orientations,
            "notes": notes
        }
        self.history["readings"].insert(0, reading)  # Most recent first
        
        # Keep only last 50 readings
        if len(self.history["readings"]) > 50:
            self.history["readings"] = self.history["readings"][:50]
        
        self.save_history()
    
    def add_journal_entry(self, entry_text):
        entry = {
            "date": datetime.now().isoformat(),
            "text": entry_text
        }
        self.history["journal"].insert(0, entry)
        
        # Keep only last 100 entries
        if len(self.history["journal"]) > 100:
            self.history["journal"] = self.history["journal"][:100]
        
        self.save_history()


class PictureTarotApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Logger.info("PictureTarotApp: Initializing enhanced app")
        self.history_manager = ReadingHistoryManager()
        self.sound_enabled = True
        self.animation_enabled = True
        self.daily_card_drawn = False
        self.load_settings()
        self.load_sounds()

    def load_settings(self):
        """Load user settings"""
        try:
            with open("settings.json", 'r') as f:
                settings = json.load(f)
                self.sound_enabled = settings.get("sound_enabled", True)
                self.animation_enabled = settings.get("animation_enabled", True)
        except:
            pass  # Use defaults

    def save_settings(self):
        """Save user settings"""
        try:
            settings = {
                "sound_enabled": self.sound_enabled,
                "animation_enabled": self.animation_enabled
            }
            with open("settings.json", 'w') as f:
                json.dump(settings, f)
        except Exception as e:
            Logger.error(f"Failed to save settings: {e}")

    def load_sounds(self):
        """Load sound effects"""
        try:
            # Try to load sound files if they exist
            sound_paths = ['sounds/card_flip.wav', 'sounds/flip.wav', 'card_flip.wav']
            for path in sound_paths:
                if os.path.exists(path):
                    self.flip_sound = SoundLoader.load(path)
                    break
        except:
            self.flip_sound = None

    def build(self):
        Logger.info("PictureTarotApp: Building enhanced app")
        
        # Set application icon
        icon_paths = [
            'images/AppIcons/transparent.png',
            'images/AppIcons/playstore.png',
            'images/rider-waite-tarot/CardBacks.jpg'
        ]

        for path in icon_paths:
            if os.path.exists(path):
                self.icon = path
                break

        self.main_layout = FloatLayout()
        self.show_main_menu()
        return self.main_layout

    def get_image_base_path(self):
        """Determine the correct base path for images"""
        possible_paths = ['images/rider-waite-tarot/', 'images/', '']
        for path in possible_paths:
            test_files = ['CardBacks.png', 'CardBacks.jpg', 'The_Fool.png']
            for test_file in test_files:
                if os.path.exists(f"{path}{test_file}"):
                    return path
        return 'images/'

    def get_card_image_path(self, card_name):
        """Get the correct image path for a card"""
        base_path = self.get_image_base_path()
        formatted_name = card_name.replace(" ", "_")
        
        if formatted_name == "CardBacks" or card_name == "CardBacks":
            for ext in ['.png', '.jpg', '.jpeg']:
                path = f'{base_path}CardBacks{ext}'
                if os.path.exists(path):
                    return path
            return None

        for ext in ['.png', '.jpg', '.jpeg']:
            image_path = f'{base_path}{formatted_name}{ext}'
            if os.path.exists(image_path):
                return image_path

        return self.get_card_back_path()

    def get_card_back_path(self):
        """Get the path to the card back image"""
        base_path = self.get_image_base_path()
        for ext in ['.png', '.jpg', '.jpeg']:
            path = f'{base_path}CardBacks{ext}'
            if os.path.exists(path):
                return path
        return None

    def show_main_menu(self):
        """Enhanced main menu with multiple options"""
        self.main_layout.clear_widgets()
        
        # Mystical background
        with self.main_layout.canvas.before:
            Color(0.05, 0.05, 0.15, 1)
            Rectangle(pos=(0, 0), size=Window.size)

        container = BoxLayout(
            orientation='vertical',
            padding=20,
            spacing=15,
            size_hint=(0.95, 0.95),
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )

        # Mystical title
        title = Label(
            text="✦ PICTURE TAROT ✦",
            font_size='32sp',
            bold=True,
            color=(1, 1, 0.8, 1),
            outline_color=(0.3, 0.1, 0.5, 1),
            outline_width=2,
            size_hint_y=0.15
        )
        container.add_widget(title)

        # Check if daily card was drawn
        today = date.today().isoformat()
        daily_drawn = any(r["date"].startswith(today) and r["spread"] == "Daily Guidance" 
                         for r in self.history_manager.history["readings"])

        # Menu options
        menu_options = [
            ("🔮 Daily Card", lambda x: self.start_daily_reading(), not daily_drawn),
            ("📚 Tarot Spreads", lambda x: self.show_spreads_menu(), True),
            ("📖 Reading History", lambda x: self.show_history(), True),
            ("✍️ Tarot Journal", lambda x: self.show_journal(), True),
            ("⚙️ Settings", lambda x: self.show_settings(), True)
        ]

        for text, callback, enabled in menu_options:
            btn = MysticalButton(
                text=text if enabled else f"{text} (Done Today)" if "Daily" in text else text,
                size_hint_y=0.15
            )
            if enabled:
                btn.bind(on_press=callback)
            else:
                btn.label.color = (0.5, 0.5, 0.5, 1)
            container.add_widget(btn)

        self.main_layout.add_widget(container)

    def start_daily_reading(self):
        """Start daily guidance reading"""
        self.start_reading(1, "Daily Guidance", special=True)

    def show_spreads_menu(self):
        """Show available tarot spreads"""
        self.main_layout.clear_widgets()
        
        container = BoxLayout(orientation='vertical', padding=20, spacing=10)
        
        # Header
        header = BoxLayout(size_hint_y=0.1)
        back_btn = MysticalButton("← Back", size_hint_x=0.3)
        back_btn.bind(on_press=lambda x: self.show_main_menu())
        
        title = Label(
            text="Choose Your Spread",
            font_size='24sp',
            bold=True,
            color=(1, 1, 0.8, 1),
            size_hint_x=0.7
        )
        
        header.add_widget(back_btn)
        header.add_widget(title)
        container.add_widget(header)
        
        # Scrollable spread list
        scroll = ScrollView()
        spread_container = BoxLayout(orientation='vertical', spacing=10, size_hint_y=None)
        spread_container.bind(minimum_height=spread_container.setter('height'))
        
        for spread_name, spread_info in SPREADS.items():
            if spread_name == "Daily Guidance":
                continue  # Skip daily card here
                
            spread_btn = BoxLayout(
                orientation='vertical', 
                size_hint_y=None, 
                height=120,
                padding=10
            )
            
            # Add mystical background
            with spread_btn.canvas.before:
                Color(0.15, 0.1, 0.25, 0.7)
                Rectangle(pos=spread_btn.pos, size=spread_btn.size)
            
            name_label = Label(
                text=f"✨ {spread_name} ({spread_info['cards']} cards)",
                font_size='18sp',
                bold=True,
                color=(1, 1, 1, 1),
                size_hint_y=0.6
            )
            
            desc_label = Label(
                text=spread_info['description'],
                font_size='14sp',
                color=(0.9, 0.9, 0.9, 1),
                size_hint_y=0.4
            )
            
            spread_btn.add_widget(name_label)
            spread_btn.add_widget(desc_label)
            
            # Make clickable
            clickable = AnimatedButton(size_hint_y=None, height=120)
            clickable.add_widget(spread_btn)
            clickable.bind(on_press=lambda btn, name=spread_name, info=spread_info: 
                          self.start_reading(info['cards'], name))
            
            spread_container.add_widget(clickable)
        
        scroll.add_widget(spread_container)
        container.add_widget(scroll)
        self.main_layout.add_widget(container)

    def start_reading(self, num_cards, spread_name, special=False):
        """Start a tarot reading with enhanced features"""
        Logger.info(f"Starting {spread_name} reading with {num_cards} cards")
        
        self.current_cards = random.sample(tarot_cards, num_cards)
        self.current_orientations = [random.choice(["Upright", "Reversed"]) for _ in range(num_cards)]
        self.current_spread_name = spread_name
        self.current_spread_info = SPREADS.get(spread_name, {"positions": [f"Card {i+1}" for i in range(num_cards)]})
        self.card_index = 0
        self.is_special = special
        
        self.show_card_with_position()

    def show_card_with_position(self):
        """Display card with position meaning"""
        self.main_layout.clear_widgets()
        
        card_name = self.current_cards[self.card_index]
        orientation = self.current_orientations[self.card_index]
        positions = self.current_spread_info["positions"]
        position = positions[self.card_index] if self.card_index < len(positions) else f"Card {self.card_index + 1}"
        
        container = BoxLayout(
            orientation='vertical',
            padding=30,
            spacing=15,
            size_hint=(0.95, 0.95),
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )

        # Progress and position info
        progress_text = f"✨ {self.current_spread_name} ✨\nCard {self.card_index + 1} of {len(self.current_cards)}"
        progress_label = Label(
            text=progress_text,
            font_size='16sp',
            color=(1, 1, 0.8, 1),
            size_hint_y=0.12,
            halign='center'
        )
        progress_label.bind(size=progress_label.setter('text_size'))
        
        position_label = Label(
            text=f"Position: {position}",
            font_size='18sp',
            bold=True,
            color=(0.9, 0.9, 1, 1),
            size_hint_y=0.08,
            halign='center'
        )
        position_label.bind(size=position_label.setter('text_size'))
        
        container.add_widget(progress_label)
        container.add_widget(position_label)

        # Card image
        card_back_path = self.get_card_back_path()
        self.current_card_widget = TarotCardImage(
            card_name=card_name,
            orientation=orientation,
            app_instance=self,
            source=card_back_path,
            allow_stretch=True,
            keep_ratio=True,
            size_hint=(1, 0.65)
        )
        
        self.current_card_widget.bind(on_press=self.reveal_card_with_meaning)
        container.add_widget(self.current_card_widget)

        # Instructions
        instruction_label = Label(
            text="🎭 Tap the card to reveal your destiny 🎭",
            font_size='16sp',
            color=(1, 1, 0.8, 1),
            size_hint_y=0.15,
            halign='center'
        )
        instruction_label.bind(size=instruction_label.setter('text_size'))
        container.add_widget(instruction_label)

        self.main_layout.add_widget(container)

    def reveal_card_with_meaning(self, instance):
        """Reveal card with meaning and interpretation"""
        if instance.is_revealed:
            self.next_card_or_complete()
            return
            
        # Reveal the card
        card_image_path = self.get_card_image_path(instance.card_name)
        if card_image_path and os.path.exists(card_image_path):
            instance.source = card_image_path
            instance.is_revealed = True
            
            # Show meaning popup
            self.show_card_meaning_popup(instance.card_name, instance.orientation)

    def show_card_meaning_popup(self, card_name, orientation):
        """Show card meaning in a popup"""
        # Get meaning from database or create generic one
        meaning_key = orientation.lower()
        meaning = CARD_MEANINGS.get(card_name, {}).get(meaning_key, 
                  f"Meditate on the symbolism of {card_name} in {orientation.lower()} position.")
        
        content = BoxLayout(orientation='vertical', spacing=10, padding=20)
        
        title = Label(
            text=f"{card_name}\n({orientation})",
            font_size='20sp',
            bold=True,
            size_hint_y=0.3,
            halign='center'
        )
        title.bind(size=title.setter('text_size'))
        
        meaning_label = Label(
            text=meaning,
            font_size='16sp',
            text_size=(None, None),
            size_hint_y=0.5,
            halign='center',
            valign='middle'
        )
        meaning_label.bind(size=meaning_label.setter('text_size'))
        
        close_btn = MysticalButton("Continue", size_hint_y=0.2)
        
        content.add_widget(title)
        content.add_widget(meaning_label)
        content.add_widget(close_btn)
        
        popup = Popup(
            title="Card Revealed",
            content=content,
            size_hint=(0.9, 0.7),
            background_color=(0.1, 0.05, 0.2, 0.95)
        )
        
        close_btn.bind(on_press=popup.dismiss)
        popup.open()

    def next_card_or_complete(self):
        """Move to next card or complete reading"""
        self.card_index += 1
        
        if self.card_index >= len(self.current_cards):
            self.complete_reading()
        else:
            self.show_card_with_position()

    def complete_reading(self):
        """Complete the reading and save to history"""
        # Save reading to history
        self.history_manager.add_reading(
            self.current_spread_name,
            self.current_cards,
            self.current_orientations
        )
        
        # Show completion screen
        self.show_reading_complete()

    def show_reading_complete(self):
        """Show reading completion with options"""
        self.main_layout.clear_widgets()
        
        container = BoxLayout(orientation='vertical', padding=30, spacing=20)
        
        title = Label(
            text="🌟 Reading Complete! 🌟",
            font_size='28sp',
            bold=True,
            color=(1, 1, 0.8, 1),
            size_hint_y=0.2
        )
        
        message = Label(
            text=f"Your {self.current_spread_name} reading has been saved.\nTake time to reflect on the messages revealed.",
            font_size='16sp',
            color=(0.9, 0.9, 0.9, 1),
            size_hint_y=0.3,
            halign='center'
        )
        message.bind(size=message.setter('text_size'))
        
        # Options
        options_layout = BoxLayout(orientation='vertical', spacing=10, size_hint_y=0.5)
        
        journal_btn = MysticalButton("📝 Add to Journal")
        journal_btn.bind(on_press=lambda x: self.quick_journal_entry())
        
        history_btn = MysticalButton("📚 View Reading History")
        history_btn.bind(on_press=lambda x: self.show_history())
        
        new_reading_btn = MysticalButton("🔮 New Reading")
        new_reading_btn.bind(on_press=lambda x: self.show_spreads_menu())
        
        home_btn = MysticalButton("🏠 Home")
        home_btn.bind(on_press=lambda x: self.show_main_menu())
        
        options_layout.add_widget(journal_btn)
        options_layout.add_widget(history_btn)
        options_layout.add_widget(new_reading_btn)
        options_layout.add_widget(home_btn)
        
        container.add_widget(title)
        container.add_widget(message)
        container.add_widget(options_layout)
        
        self.main_layout.add_widget(container)

    def quick_journal_entry(self):
        """Quick journal entry popup"""
        content = BoxLayout(orientation='vertical', spacing=10, padding=10)
        
        text_input = TextInput(
            hint_text="Reflect on your reading...",
            multiline=True,
            size_hint_y=0.7
        )
        
        buttons = BoxLayout(size_hint_y=0.3, spacing=10)
        save_btn = MysticalButton("Save")
        cancel_btn = MysticalButton("Cancel")
        
        buttons.add_widget(save_btn)
        buttons.add_widget(cancel_btn)
        
        content.add_widget(text_input)
        content.add_widget(buttons)
        
        popup = Popup(
            title="Journal Entry",
            content=content,
            size_hint=(0.9, 0.6)
        )
        
        def save_entry(*args):
            if text_input.text.strip():
                self.history_manager.add_journal_entry(text_input.text.strip())
            popup.dismiss()
        
        save_btn.bind(on_press=save_entry)
        cancel_btn.bind(on_press=popup.dismiss)
        
        popup.open()

    def show_history(self):
        """Show reading history"""
        self.main_layout.clear_widgets()
        
        container = BoxLayout(orientation='vertical', padding=20, spacing=10)
        
        # Header
        header = BoxLayout(size_hint_y=0.1)
        back_btn = MysticalButton("← Back", size_hint_x=0.3)
        back_btn.bind(on_press=lambda x: self.show_main_menu())
        
        title = Label(
            text="Reading History",
            font_size='24sp',
            bold=True,
            color=(1, 1, 0.8, 1),
            size_hint_x=0.7
        )
        
        header.add_widget(back_btn)
        header.add_widget(title)
        container.add_widget(header)
        
        # History list
        scroll = ScrollView()
        history_container = BoxLayout(orientation='vertical', spacing=5, size_hint_y=None)
        history_container.bind(minimum_height=history_container.setter('height'))
        
        readings = self.history_manager.history["readings"]
        
        if not readings:
            no_history = Label(
                text="No readings yet. Start your tarot journey!",
                font_size='16sp',
                color=(0.7, 0.7, 0.7, 1),
                size_hint_y=None,
                height=100
            )
            history_container.add_widget(no_history)
        else:
            for reading in readings:
                date_str = datetime.fromisoformat(reading["date"]).strftime("%B %d, %Y at %I:%M %p")
                
                item = Label(
                    text=f"🔮 {reading['spread']}\n📅 {date_str}\n🃏 {len(reading['cards'])} cards drawn",
                    font_size='14sp',
                    color=(0.9, 0.9, 0.9, 1),
                    size_hint_y=None,
                    height=80,
                    halign='left'
                )
                item.bind(size=item.setter('text_size'))
                history_container.add_widget(item)
        
        scroll.add_widget(history_container)
        container.add_widget(scroll)
        self.main_layout.add_widget(container)

    def show_journal(self):
        """Show tarot journal"""
        self.main_layout.clear_widgets()
        
        container = BoxLayout(orientation='vertical', padding=20, spacing=10)
        
        # Header with back button and add entry button
        header = BoxLayout(size_hint_y=0.1)
        back_btn = MysticalButton("← Back", size_hint_x=0.25)
        back_btn.bind(on_press=lambda x: self.show_main_menu())
        
        title = Label(
            text="Tarot Journal",
            font_size='22sp',
            bold=True,
            color=(1, 1, 0.8, 1),
            size_hint_x=0.5
        )
        
        add_btn = MysticalButton("+ New Entry", size_hint_x=0.25)
        add_btn.bind(on_press=lambda x: self.add_journal_entry())
        
        header.add_widget(back_btn)
        header.add_widget(title)
        header.add_widget(add_btn)
        container.add_widget(header)
        
        # Journal entries
        scroll = ScrollView()
        journal_container = BoxLayout(orientation='vertical', spacing=10, size_hint_y=None)
        journal_container.bind(minimum_height=journal_container.setter('height'))
        
        entries = self.history_manager.history["journal"]
        
        if not entries:
            no_entries = Label(
                text="📝 No journal entries yet.\nStart documenting your tarot insights!",
                font_size='16sp',
                color=(0.7, 0.7, 0.7, 1),
                size_hint_y=None,
                height=100,
                halign='center'
            )
            no_entries.bind(size=no_entries.setter('text_size'))
            journal_container.add_widget(no_entries)
        else:
            for entry in entries:
                date_str = datetime.fromisoformat(entry["date"]).strftime("%B %d, %Y")
                
                entry_box = BoxLayout(
                    orientation='vertical',
                    size_hint_y=None,
                    height=120,
                    padding=15,
                    spacing=5
                )
                
                # Add mystical background to entry
                with entry_box.canvas.before:
                    Color(0.15, 0.1, 0.25, 0.5)
                    Rectangle(pos=entry_box.pos, size=entry_box.size)
                
                entry_box.bind(pos=self._update_entry_bg, size=self._update_entry_bg)
                
                date_label = Label(
                    text=f"✨ {date_str}",
                    font_size='14sp',
                    bold=True,
                    color=(1, 1, 0.8, 1),
                    size_hint_y=0.3,
                    halign='left'
                )
                date_label.bind(size=date_label.setter('text_size'))
                
                text_label = Label(
                    text=entry["text"][:150] + ("..." if len(entry["text"]) > 150 else ""),
                    font_size='13sp',
                    color=(0.9, 0.9, 0.9, 1),
                    size_hint_y=0.7,
                    halign='left',
                    valign='top'
                )
                text_label.bind(size=text_label.setter('text_size'))
                
                entry_box.add_widget(date_label)
                entry_box.add_widget(text_label)
                journal_container.add_widget(entry_box)
        
        scroll.add_widget(journal_container)
        container.add_widget(scroll)
        self.main_layout.add_widget(container)
    
    def _update_entry_bg(self, instance, *args):
        """Update journal entry background"""
        if hasattr(instance, 'canvas') and instance.canvas.before:
            instance.canvas.before.clear()
            with instance.canvas.before:
                Color(0.15, 0.1, 0.25, 0.5)
                Rectangle(pos=instance.pos, size=instance.size)

    def add_journal_entry(self):
        """Add new journal entry"""
        content = BoxLayout(orientation='vertical', spacing=15, padding=15)
        
        title_label = Label(
            text="✍️ New Journal Entry",
            font_size='20sp',
            bold=True,
            color=(1, 1, 0.8, 1),
            size_hint_y=0.15
        )
        
        text_input = TextInput(
            hint_text="Share your tarot insights, reflections, or questions...",
            multiline=True,
            size_hint_y=0.6,
            background_color=(0.2, 0.15, 0.3, 0.8),
            foreground_color=(1, 1, 1, 1)
        )
        
        buttons = BoxLayout(size_hint_y=0.25, spacing=10)
        save_btn = MysticalButton("💾 Save Entry")
        cancel_btn = MysticalButton("❌ Cancel")
        
        buttons.add_widget(save_btn)
        buttons.add_widget(cancel_btn)
        
        content.add_widget(title_label)
        content.add_widget(text_input)
        content.add_widget(buttons)
        
        popup = Popup(
            title="",
            content=content,
            size_hint=(0.9, 0.8),
            background_color=(0.05, 0.05, 0.15, 0.95),
            separator_color=(0.3, 0.2, 0.5, 1)
        )
        
        def save_entry(*args):
            if text_input.text.strip():
                self.history_manager.add_journal_entry(text_input.text.strip())
                popup.dismiss()
                self.show_journal()  # Refresh the journal view
        
        save_btn.bind(on_press=save_entry)
        cancel_btn.bind(on_press=popup.dismiss)
        
        popup.open()

    def show_settings(self):
        """Show app settings"""
        self.main_layout.clear_widgets()
        
        container = BoxLayout(orientation='vertical', padding=25, spacing=20)
        
        # Header
        header = BoxLayout(size_hint_y=0.12)
        back_btn = MysticalButton("← Back", size_hint_x=0.3)
        back_btn.bind(on_press=lambda x: self.show_main_menu())
        
        title = Label(
            text="⚙️ Settings",
            font_size='24sp',
            bold=True,
            color=(1, 1, 0.8, 1),
            size_hint_x=0.7
        )
        
        header.add_widget(back_btn)
        header.add_widget(title)
        container.add_widget(header)
        
        # Settings options
        settings_container = BoxLayout(orientation='vertical', spacing=15, size_hint_y=0.7)
        
        # Sound setting
        sound_box = BoxLayout(size_hint_y=None, height=60, spacing=15)
        sound_label = Label(
            text="🔊 Sound Effects",
            font_size='18sp',
            color=(1, 1, 1, 1),
            size_hint_x=0.7,
            halign='left'
        )
        sound_label.bind(size=sound_label.setter('text_size'))
        
        sound_switch = Switch(
            active=self.sound_enabled,
            size_hint_x=0.3
        )
        sound_switch.bind(active=self.toggle_sound)
        
        sound_box.add_widget(sound_label)
        sound_box.add_widget(sound_switch)
        
        # Animation setting
        anim_box = BoxLayout(size_hint_y=None, height=60, spacing=15)
        anim_label = Label(
            text="✨ Animations",
            font_size='18sp',
            color=(1, 1, 1, 1),
            size_hint_x=0.7,
            halign='left'
        )
        anim_label.bind(size=anim_label.setter('text_size'))
        
        anim_switch = Switch(
            active=self.animation_enabled,
            size_hint_x=0.3
        )
        anim_switch.bind(active=self.toggle_animations)
        
        anim_box.add_widget(anim_label)
        anim_box.add_widget(anim_switch)
        
        settings_container.add_widget(sound_box)
        settings_container.add_widget(anim_box)
        
        # App info
        info_container = BoxLayout(orientation='vertical', spacing=10, size_hint_y=0.18)
        
        app_info = Label(
            text="📱 Picture Tarot v1.0\nCreated with mystical energy ✨\n\nMay your readings bring insight and wisdom",
            font_size='14sp',
            color=(0.7, 0.7, 0.8, 1),
            halign='center'
        )
        app_info.bind(size=app_info.setter('text_size'))
        
        info_container.add_widget(app_info)
        
        container.add_widget(settings_container)
        container.add_widget(info_container)
        
        self.main_layout.add_widget(container)

    def toggle_sound(self, instance, value):
        """Toggle sound effects"""
        self.sound_enabled = value
        self.save_settings()
        Logger.info(f"Sound effects {'enabled' if value else 'disabled'}")

    def toggle_animations(self, instance, value):
        """Toggle animations"""
        self.animation_enabled = value
        self.save_settings()
        Logger.info(f"Animations {'enabled' if value else 'disabled'}")

    def get_daily_affirmation(self):
        """Get a daily tarot affirmation"""
        affirmations = [
            "✨ Trust in the wisdom the cards reveal to you today",
            "🌟 You have the power to shape your destiny",
            "🔮 Let intuition be your guide on this journey",
            "🌙 The universe conspires to help those who seek truth",
            "⭐ Every card drawn is a step toward enlightenment",
            "🌸 Embrace the mysteries that unfold before you",
            "🦋 Transformation comes to those who are ready",
            "🌊 Flow with the currents of cosmic energy",
        ]
        return random.choice(affirmations)


if __name__ == '__main__':
    Logger.info("PictureTarotApp: Starting enhanced mystical application")
    PictureTarotApp().run()