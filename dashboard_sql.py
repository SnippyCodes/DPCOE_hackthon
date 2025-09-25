import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.spinner import Spinner
from kivy.uix.scrollview import ScrollView
from kivy.uix.image import Image
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.graphics import Color, Rectangle, Ellipse
import sqlite3

kivy.require('2.2.1') 

# --- Configuration Lists ---
ALL_DIVISIONS = ["DIVISION A", "DIVISION B"] 
DAYS = ["MONDAY", "TUESDAY", "WEDNESDAY", "THURSDAY", "FRIDAY", "SATURDAY"]


# --- 2. THE MAIN WIDGET / SCREEN ---
class TimetableDashboardScreen(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.spacing = dp(10)
        self.padding = dp(15)
        
        self.background_color = (0.07, 0.07, 0.07, 1) 
        
        # Apply main dark background
        with self.canvas.before:
            Color(*self.background_color[:3], 1)
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_rect, pos=self._update_rect)

        # --- A. HEADER/PROFILE SECTION ---
        header = BoxLayout(size_hint_y=None, height=dp(100), padding=dp(5), spacing=dp(15))
        
        # Profile Image (Simulated Circular Effect)
        profile_box = BoxLayout(orientation='vertical', size_hint_x=None, width=dp(80))
        try:
            # Note: Ensure you have 'profile_pic.png' in the same folder or remove the try/except block
            profile_image = Image(source='profile_pic.png', size_hint=(None, None), size=(dp(70), dp(70)))
            
            with profile_image.canvas.before:
                Color(0, 0.75, 1, 1) # Accent color border
                # The Ellipse creates the circular border visual effect
                self.border = Ellipse(size=(dp(80), dp(80)), pos=(profile_image.x - dp(5), profile_image.y - dp(5)))
            
            profile_image.bind(pos=lambda *args: self.update_profile_pos(profile_image))
            
            profile_box.add_widget(profile_image)
            profile_box.add_widget(Label(text="Hello, Student!", size_hint_y=None, height=dp(20), color=(1, 1, 1, 1)))
            
        except:
            # Fallback if image is missing
            profile_box.add_widget(Label(text="Profile Image Missing", color=(1, 0, 0, 1)))

        header.add_widget(profile_box)

        # Welcome Text and Main Title
        header_text = BoxLayout(orientation='vertical', padding=(0, dp(10), 0, 0))
        header_text.add_widget(Label(text='[b]Welcome to Your Dashboard[/b]', markup=True, size_hint_y=None, height=dp(30), font_size='20sp', color=(0, 0.75, 1, 1), halign='left', text_size=(300, 30)))
        header_text.add_widget(Label(text='Academic Year: 2024-2025', size_hint_y=None, height=dp(20), color=(0.8, 0.8, 0.8, 1), halign='left', text_size=(300, 20)))
        
        header.add_widget(header_text)
        
        self.add_widget(header)

        # --- B. TIMETABLE SELECTOR & VIEWER SECTION (Main Content) ---
        timetable_section = BoxLayout(orientation='vertical', size_hint_y=0.6, spacing=dp(5))

        # Selector Bar
        selector_bar = BoxLayout(size_hint_y=None, height=dp(40), spacing=dp(10))

        self.section_spinner = Spinner(text='-- Select Division --', values=ALL_DIVISIONS, size_hint_x=0.5, background_color=(0.15, 0.15, 0.15, 1), color=(1, 1, 1, 1))
        self.section_spinner.bind(text=self.update_timetable)
        selector_bar.add_widget(self.section_spinner)

        self.day_spinner = Spinner(text='-- Select Day --', values=DAYS, size_hint_x=0.5, background_color=(0.15, 0.15, 0.15, 1), color=(1, 1, 1, 1))
        self.day_spinner.bind(text=self.update_timetable)
        selector_bar.add_widget(self.day_spinner)

        timetable_section.add_widget(selector_bar)
        
        # Timetable Display Area
        self.scroll_view = ScrollView()
        self.timetable_container = BoxLayout(orientation='vertical', size_hint_y=None, spacing=dp(2))
        self.timetable_container.bind(minimum_height=self.timetable_container.setter('height'))
        self.scroll_view.add_widget(self.timetable_container)
        timetable_section.add_widget(self.scroll_view)
        
        self.add_widget(timetable_section)
        
        self.display_placeholder("Select your schedule above.", container=self.timetable_container)


        # --- C. CURRICULAR ACTIVITIES SECTION ---
        activity_section = BoxLayout(orientation='vertical', size_hint_y=0.4, padding=(0, dp(10), 0, 0))
        activity_section.add_widget(Label(text='[b]Curricular Activities[/b]', markup=True, size_hint_y=None, height=dp(25), font_size='16sp', color=(0, 0.75, 1, 1), halign='left', text_size=(Window.width - dp(30), None)))
        
        # Add placeholder activities
        activities_list = ['Robotics Club Meeting (Thurs 4 PM)', 'NSS Volunteer Drive (Fri 3 PM)', 'Advanced Python Workshop (Sat 10 AM)']
        for activity in activities_list:
            activity_label = Label(text=f'- {activity}', size_hint_y=None, height=dp(20), color=(0.9, 0.9, 0.9, 1), halign='left', text_size=(Window.width - dp(30), None))
            activity_section.add_widget(activity_label)
            
        activity_section.add_widget(Label(text='[i]Stay engaged![/i]', markup=True, size_hint_y=None, height=dp(20), color=(0.6, 0.6, 0.6, 1), halign='left', text_size=(Window.width - dp(30), None)))

        self.add_widget(activity_section)

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def update_profile_pos(self, img_widget):
        # Update border position to follow the image widget
        self.border.pos = (img_widget.x - dp(5), img_widget.y - dp(5))

    def display_placeholder(self, text, color=(0.5, 0.5, 0.5, 1), container=None):
        container = container or self.timetable_container
        container.clear_widgets()
        placeholder = Label(text=text, size_hint_y=None, height=dp(100), color=color)
        container.add_widget(placeholder)

    def update_timetable(self, instance, value):
        selected_section = self.section_spinner.text
        selected_day = self.day_spinner.text

        self.timetable_container.clear_widgets()

        if selected_section == '-- Select Division --' or selected_day == '-- Select Day --':
            self.display_placeholder("Please select both a Division and a Day.")
            return

        # --- 1. SQL QUERY EXECUTION ---
        try:
            conn = sqlite3.connect('timetable.db')
            cursor = conn.cursor()
            query = "SELECT time_slot, subject, location FROM schedule WHERE division = ? AND day = ? ORDER BY time_slot"
            cursor.execute(query, (selected_section, selected_day))
            filtered_data = cursor.fetchall()
            
        except sqlite3.OperationalError:
            self.display_placeholder("ERROR: Database file (timetable.db) not found or table is missing.", color=(1, 0, 0, 1))
            return
        finally:
            if 'conn' in locals() and conn:
                conn.close()

        # --- 2. DISPLAY RESULTS ---
        if not filtered_data:
            self.display_placeholder(f"No classes scheduled for {selected_day} in {selected_section}.", color=(0, 0.75, 1, 1))
            return
        
        # Schedule Header
        self.timetable_container.add_widget(Label(text=f"{selected_day} Schedule for {selected_section}", size_hint_y=None, height=dp(30), font_size='16sp', color=(1, 1, 1, 1)))
        
        # Table Header Row
        header_row = BoxLayout(size_hint_y=None, height=dp(30))
        header_color = (0.2, 0.2, 0.2, 1)
        
        def create_header(text, width):
            lbl = Label(text=text, size_hint_x=width, color=(1, 1, 1, 1))
            with lbl.canvas.before:
                Color(*header_color)
                Rectangle(size=lbl.size, pos=lbl.pos)
            return lbl

        header_row.add_widget(create_header("Time Slot", 0.3))
        header_row.add_widget(create_header("Subject / Activity", 0.5))
        header_row.add_widget(create_header("Batch/Room", 0.2))
        self.timetable_container.add_widget(header_row)

        # Populate Timetable Rows
        for i, item in enumerate(filtered_data):
            row = BoxLayout(size_hint_y=None, height=dp(30))
            row_color = (0.1, 0.1, 0.1, 1) if i % 2 == 0 else (0.15, 0.15, 0.15, 1)
            
            def create_data_label(text, width):
                lbl = Label(text=text, size_hint_x=width, color=(1, 1, 1, 1))
                with lbl.canvas.before:
                    Color(*row_color)
                    Rectangle(size=lbl.size, pos=lbl.pos)
                return lbl

            row.add_widget(create_data_label(item[0], 0.3))
            row.add_widget(create_data_label(item[1], 0.5))
            row.add_widget(create_data_label(item[2], 0.2))
            
            self.timetable_container.add_widget(row)


# --- 3. THE KIVY APP CLASS ---
class TimetableApp(App):
    def build(self):
        self.title = 'Student Dashboard'
        # Set window size to simulate a mobile screen for desktop testing
        Window.size = (400, 700) 
        # The correct line: It calls the screen class and returns its instance
        return TimetableDashboardScreen() 

if __name__ == '__main__':
    TimetableApp().run()