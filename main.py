"""
Smart Word Practice - Mobile App
Step 1: Basic Kivy App Structure
"""

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.clock import Clock
import threading
import requests
import csv
import json
import random
from io import StringIO
from datetime import datetime

class WordPracticeApp(App):
    def load_app_config(self):
        """Load app configuration"""
        try:
            with open('config.json', 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {
                'default_word_count': 5,
                'google_sheet_url': 'https://docs.google.com/spreadsheets/d/12p3nPxIYYov06dj2lqAgVt_gz3azHHCmLe09qJwCbT4/edit?usp=sharing'
            }
    
    def build(self):
        self.title = "Smart Word Practice"
        
        # Main layout
        main_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Header
        header = Label(
            text='📚 Smart Word Practice',
            size_hint_y=None,
            height='48dp',
            font_size='20sp',
            bold=True
        )
        main_layout.add_widget(header)
        
        # Load config
        self.config = self.load_app_config()
        
        # Configuration section
        config_layout = GridLayout(cols=2, size_hint_y=None, height='120dp', spacing=5)
        
        config_layout.add_widget(Label(text='Words to practice:', size_hint_y=None, height='30dp'))
        self.word_count_input = TextInput(
            text=str(self.config.get('default_word_count', 5)),
            multiline=False,
            size_hint_y=None,
            height='30dp',
            input_filter='int'
        )
        config_layout.add_widget(self.word_count_input)
        
        config_layout.add_widget(Label(text='Google Sheet URL:', size_hint_y=None, height='30dp'))
        self.sheet_url_input = TextInput(
            text=self.config.get('google_sheet_url', 'https://docs.google.com/spreadsheets/d/YOUR_SHEET_ID/export?format=csv'),
            multiline=False,
            size_hint_y=None,
            height='30dp'
        )
        config_layout.add_widget(self.sheet_url_input)
        
        main_layout.add_widget(config_layout)
        
        # Action button
        self.fetch_button = Button(
            text='📖 Get Practice Words',
            size_hint_y=None,
            height='50dp',
            font_size='16sp'
        )
        self.fetch_button.bind(on_press=self.fetch_words)
        main_layout.add_widget(self.fetch_button)
        
        # Status label
        self.status_label = Label(
            text='Ready to fetch words...',
            size_hint_y=None,
            height='30dp',
            color=(0.7, 0.7, 0.7, 1)
        )
        main_layout.add_widget(self.status_label)
        
        # Scrollable results area
        scroll = ScrollView()
        self.results_layout = BoxLayout(orientation='vertical', size_hint_y=None, spacing=5)
        self.results_layout.bind(minimum_height=self.results_layout.setter('height'))
        scroll.add_widget(self.results_layout)
        main_layout.add_widget(scroll)
        
        return main_layout
    
    def update_status(self, message, color=(1, 1, 1, 1)):
        """Update status label on main thread"""
        self.status_label.text = message
        self.status_label.color = color
    
    def fetch_words(self, instance):
        """Fetch words from Google Sheet in background thread"""
        self.fetch_button.disabled = True
        self.update_status("📡 Fetching words from Google Sheet...", (1, 1, 0, 1))
        
        # Clear previous results
        self.results_layout.clear_widgets()
        
        # Start background thread
        threading.Thread(target=self._fetch_words_background, daemon=True).start()
    
    def _fetch_words_background(self):
        """Background thread to fetch and process words"""
        try:
            # Get parameters
            num_words = int(self.word_count_input.text) if self.word_count_input.text else 5
            sheet_url = self.sheet_url_input.text.strip()
            
            if not sheet_url or 'YOUR_SHEET_ID' in sheet_url:
                Clock.schedule_once(lambda dt: self.show_error("Please enter a valid Google Sheet URL"))
                return
            
            # Fetch data
            Clock.schedule_once(lambda dt: self.update_status("📡 Downloading sheet data...", (1, 1, 0, 1)))
            data = self.read_sheet_as_csv(sheet_url)
            
            if not data:
                Clock.schedule_once(lambda dt: self.show_error("Failed to read data from Google Sheet"))
                return
            
            Clock.schedule_once(lambda dt: self.update_status(f"✅ Loaded {len(data)} words", (0, 1, 0, 1)))
            
            # Select words
            Clock.schedule_once(lambda dt: self.update_status("🎯 Selecting practice words...", (1, 1, 0, 1)))
            selected = self.select_words_for_practice(data, num_words)
            
            # Show results on main thread
            Clock.schedule_once(lambda dt: self.show_results(data, selected))
            
        except Exception as e:
            Clock.schedule_once(lambda dt: self.show_error(f"Error: {str(e)}"))
    
    def read_sheet_as_csv(self, sheet_url):
        """Read Google Sheet as CSV"""
        try:
            response = requests.get(sheet_url, timeout=30)
            response.raise_for_status()
            
            csv_content = StringIO(response.text)
            reader = csv.DictReader(csv_content)
            
            data = []
            for row in reader:
                practiced = 0
                if 'Practiced' in row and row['Practiced']:
                    try:
                        practiced = int(float(row['Practiced']))
                    except (ValueError, TypeError):
                        practiced = 0
                
                word = row.get('Word', '').strip()
                if word:
                    data.append({
                        'Word': word,
                        'Category': row.get('Category', '').strip(),
                        'Practiced': practiced
                    })
            
            return data
            
        except Exception as e:
            print(f"Error reading sheet: {e}")
            return None
    
    def select_words_for_practice(self, data, num_words):
        """Select words based on practice count"""
        if not data:
            return []
        
        # Sort by practice count, then randomly
        data_sorted = sorted(data, key=lambda x: (x['Practiced'], random.random()))
        return data_sorted[:num_words]
    
    def show_results(self, data, selected):
        """Show results on main thread"""
        # Statistics
        stats_text = self.format_statistics(data, selected)
        stats_label = Label(
            text=stats_text,
            size_hint_y=None,
            height='100dp',  # Fixed height to avoid sizing issues
            text_size=(None, None),
            markup=True,
            font_size='14sp',
            halign='left',
            valign='top'
        )
        # Use a safer binding approach
        def update_stats_size(instance, value):
            if hasattr(instance, 'texture') and instance.texture:
                instance.height = max(100, instance.texture.height + 20)
        stats_label.bind(texture_size=update_stats_size)
        self.results_layout.add_widget(stats_label)
        
        # Word list
        words_text = self.format_word_list(selected)
        words_label = Label(
            text=words_text,
            size_hint_y=None,
            height='200dp',  # Fixed height to avoid sizing issues
            text_size=(None, None),
            markup=True,
            font_size='16sp',
            halign='left',
            valign='top'
        )
        # Use a safer binding approach
        def update_words_size(instance, value):
            if hasattr(instance, 'texture') and instance.texture:
                instance.height = max(200, instance.texture.height + 20)
        words_label.bind(texture_size=update_words_size)
        self.results_layout.add_widget(words_label)
        
        self.update_status(f"✅ Ready! Selected {len(selected)} words for practice", (0, 1, 0, 1))
        self.fetch_button.disabled = False
    
    def format_statistics(self, data, selected):
        """Format statistics"""
        total_words = len(data)
        
        # Count by practice levels
        practice_counts = {}
        for item in data:
            count = item['Practiced']
            practice_counts[count] = practice_counts.get(count, 0) + 1
        
        levels = sorted(practice_counts.keys())
        
        stats = f"[b]📊 Practice Statistics[/b]\n"
        stats += "━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        stats += f"📚 Total Words: {total_words}\n\n"
        stats += "📈 Practice Levels:\n"
        
        for level in levels:
            count = practice_counts[level]
            stats += f"• Level {level}: {count} words\n"
        
        stats += f"\n🎯 Today's Selection: {len(selected)} words\n"
        
        # Selection breakdown
        sel_counts = {}
        for item in selected:
            count = item['Practiced']
            sel_counts[count] = sel_counts.get(count, 0) + 1
        
        for level in sorted(sel_counts.keys()):
            count = sel_counts[level]
            stats += f"   → {count} from Level {level}\n"
        
        return stats
    
    def format_word_list(self, selected):
        """Format word list"""
        if not selected:
            return "No words selected"
        
        words = f"\n[b]📚 Today's Practice Words[/b]\n"
        words += "━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        
        for i, item in enumerate(selected, 1):
            word = item['Word']
            category = item.get('Category', '').strip()
            
            if category and category != 'nan':
                words += f"{i}. {word} ({category})\n"
            else:
                words += f"{i}. {word}\n"
        
        words += f"\n🎯 Focus Areas: Vocabulary building\n"
        words += f"📅 Practice Date: {datetime.now().strftime('%Y-%m-%d')}\n\n"
        words += "[i]First make a separate sentence with each word and number the sentences[/i]"
        
        return words
    
    def show_error(self, message):
        """Show error message"""
        self.update_status(f"❌ {message}", (1, 0, 0, 1))
        self.fetch_button.disabled = False

# Run the app
if __name__ == '__main__':
    WordPracticeApp().run()