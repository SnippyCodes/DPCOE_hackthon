import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.spinner import Spinner
from kivy.uix.scrollview import ScrollView
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.relativelayout import RelativeLayout
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.graphics import Color, Rectangle, Ellipse
from kivy.uix.popup import Popup
from kivy.uix.filechooser import FileChooserListView
from kivy.properties import StringProperty, ListProperty
import sqlite3
import os

kivy.require('2.2.1') 

# --- Configuration Lists ---
ALL_DIVISIONS = ["DIVISION A", "DIVISION B", "DIVISION C", "DIVISION D"] 
DAYS = ["MONDAY", "TUESDAY", "WEDNESDAY", "THURSDAY", "FRIDAY", "SATURDAY"]

# --- 2. THE MAIN WIDGET / SCREEN ---
class TimetableDashboardScreen(BoxLayout):
    # Kivy Properties for cleaner data binding
    section_values = ListProperty(ALL_DIVISIONS)
    day_values = ListProperty(DAYS)
    profile_image_source = StringProperty('default_profile.png') 
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.spacing = dp(10)
        self.padding = dp(15)
        self.background_color = (0.07, 0.07, 0.07, 1) 
        
        # Ensure a minimal placeholder exists if the expected file is missing
        if not os.path.exists(self.profile_image_source):
            self.profile_image_source = 'atlas://data/images/defaulttheme/nocheck-box' 

        self.setup_ui()
        
    def setup_ui(self):
        """Builds the entire UI structure concisely."""
        
        # Apply main dark background
        with self.canvas.before:
            Color(*self.background_color[:3], 1)
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_rect, pos=self._update_rect)

        # ----------------------------------------------------
        # A. HEADER/PROFILE SECTION
        # ----------------------------------------------------
        header = BoxLayout(size_hint_y=None, height=dp(100), padding=dp(5), spacing=dp(15))
        
        profile_box = self.create_profile_widget()
        header.add_widget(profile_box)

        # Welcome Text
        header_text = BoxLayout(orientation='vertical', padding=(0, dp(10), 0, 0))
        header_text.add_widget(Label(text='[b]Welcome to Your Dashboard[/b]', markup=True, size_hint_y=None, height=dp(30), font_size='20sp', color=(0, 0.75, 1, 1), halign='left', text_size=(300, 30)))
        header_text.add_widget(Label(text='Academic Year: 2024-2025', size_hint_y=None, height=dp(20), color=(0.8, 0.8, 0.8, 1), halign='left', text_size=(300, 20)))
        header.add_widget(header_text)
        
        self.add_widget(header)

        # ----------------------------------------------------
        # B. TIMETABLE SELECTOR & VIEWER SECTION
        # ----------------------------------------------------
        timetable_section = self.create_timetable_viewer()
        self.add_widget(timetable_section)

        # ----------------------------------------------------
        # C. CURRICULAR ACTIVITIES SECTION
        # ----------------------------------------------------
        activity_section = self.create_activities_viewer()
        self.add_widget(activity_section)
        
    # --- UI Component Builders ---

    def create_profile_widget(self):
        """Creates the layered PFP widget with a black clickable circle."""
        
        profile_box = BoxLayout(orientation='vertical', size_hint_x=None, width=dp(90))
        # Use RelativeLayout for positioning graphics and button
        image_container = RelativeLayout(size_hint_x=None, width=dp(80), size_hint_y=None, height=dp(80))

        # 1. Outer Accent Border (80dp)
        with image_container.canvas.before:
            Color(0, 0.75, 1, 1)  # Vibrant Accent Color
            self.border = Ellipse(size=(dp(80), dp(80)), pos=image_container.pos)

        # 2. Inner Black Mask (74dp) - PURE BLACK
        with image_container.canvas.before:
            Color(0, 0, 0, 1)  # PURE BLACK background (RGB: 0, 0, 0)
            self.inner_mask = Ellipse(size=(dp(74), dp(74)), pos=(image_container.x + dp(3), image_container.y + dp(3)))

        # 3. Profile Image (70dp) - The Image Widget
        self.profile_image_widget = Image(
            source=self.profile_image_source, 
            size_hint=(None, None), size=(dp(70), dp(70)),
            pos=(dp(5), dp(5)), 
            allow_stretch=True, keep_ratio=True
        )
        self.bind(profile_image_source=self.on_profile_image_source_change)
        self.profile_image_widget.bind(pos=self.update_graphics_pos)
        
        # 4. Transparent Button for click event (80dp)
        profile_btn = Button(
            size_hint=(1, 1), 
            background_color=(0, 0, 0, 0),
            background_normal='',
            background_down=''
        )
        profile_btn.bind(on_release=self.show_load_dialog)

        # Add components to the container
        image_container.add_widget(self.profile_image_widget)
        image_container.add_widget(profile_btn)

        profile_box.add_widget(image_container)
        profile_box.add_widget(Label(text="Hello, Student!", size_hint_y=None, height=dp(20), color=(1, 1, 1, 1)))
        
        return profile_box

    def create_timetable_viewer(self):
        """Creates the timetable viewer section."""
        timetable_section = BoxLayout(orientation='vertical', size_hint_y=0.6, spacing=dp(5))

        # Selector Bar
        selector_bar = BoxLayout(size_hint_y=None, height=dp(40), spacing=dp(10))

        # NOTE: Using the ListProperty bound to the class
        self.section_spinner = Spinner(text='-- Select Division --', values=self.section_values, size_hint_x=0.5, background_color=(0.15, 0.15, 0.15, 1), color=(1, 1, 1, 1))
        self.section_spinner.bind(text=self.update_timetable)
        selector_bar.add_widget(self.section_spinner)

        self.day_spinner = Spinner(text='-- Select Day --', values=self.day_values, size_hint_x=0.5, background_color=(0.15, 0.15, 0.15, 1), color=(1, 1, 1, 1))
        self.day_spinner.bind(text=self.update_timetable)
        selector_bar.add_widget(self.day_spinner)

        timetable_section.add_widget(selector_bar)
        
        # Timetable Display Area
        self.scroll_view = ScrollView()
        self.timetable_container = BoxLayout(orientation='vertical', size_hint_y=None, spacing=dp(2))
        self.timetable_container.bind(minimum_height=self.timetable_container.setter('height'))
        self.scroll_view.add_widget(self.timetable_container)
        timetable_section.add_widget(self.scroll_view)
        
        self.display_placeholder("Select your schedule above.", container=self.timetable_container)
        return timetable_section

    def create_activities_viewer(self):
        """Creates the curricular activities section."""
        activity_section = BoxLayout(orientation='vertical', size_hint_y=0.4, padding=(0, dp(10), 0, 0))
        activity_section.add_widget(Label(text='[b]Curricular Activities[/b]', markup=True, size_hint_y=None, height=dp(25), font_size='16sp', color=(0, 0.75, 1, 1), halign='left', text_size=(Window.width - dp(30), None)))
        
        activities_list = ['Robotics Club Meeting (Thurs 4 PM)', 'NSS Volunteer Drive (Fri 3 PM)', 'Advanced Python Workshop (Sat 10 AM)']
        for activity in activities_list:
            activity_label = Label(text=f'- {activity}', size_hint_y=None, height=dp(20), color=(0.9, 0.9, 0.9, 1), halign='left', text_size=(Window.width - dp(30), None))
            activity_section.add_widget(activity_label)
            
        activity_section.add_widget(Label(text='[i]Stay engaged![/i]', markup=True, size_hint_y=None, height=dp(20), color=(0.6, 0.6, 0.6, 1), halign='left', text_size=(Window.width - dp(30), None)))

        return activity_section
    
    # --- Graphics and File Chooser Logic ---
    
    def on_profile_image_source_change(self, instance, value):
        """Updates the image widget source when the property changes."""
        self.profile_image_widget.source = value
        
    def update_graphics_pos(self, instance, value):
        """Updates border and inner mask position to track the image."""
        
        self.border.pos = (instance.x - dp(5), instance.y - dp(5))
        self.inner_mask.pos = (instance.x - dp(2), instance.y - dp(2))

    def show_load_dialog(self, instance):
        """Creates and displays the file chooser popup."""
        
        content = BoxLayout(orientation='vertical', spacing=dp(10))
        self.file_chooser = FileChooserListView(filters=['*.png', '*.jpg', '*.jpeg'])
        
        button_box = BoxLayout(size_hint_y=None, height=dp(40), spacing=dp(10))
        load_button = Button(text='Load Image')
        cancel_button = Button(text='Cancel')
        
        load_button.bind(on_release=lambda btn: self.load_profile_image(self.file_chooser.selection))
        cancel_button.bind(on_release=lambda btn: self.popup.dismiss())
        
        button_box.add_widget(load_button)
        button_box.add_widget(cancel_button)
        
        content.add_widget(self.file_chooser)
        content.add_widget(button_box)
        
        self.popup = Popup(title='Select Profile Picture', content=content, size_hint=(0.9, 0.9))
        self.popup.open()
        
    def load_profile_image(self, selection):
        """Loads the selected file into the profile image widget."""
        
        if selection:
            self.profile_image_source = selection[0] 
            self.popup.dismiss()
        else:
            print("No file selected.")

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    # --- Timetable Logic (SQL) ---

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

        # SQL QUERY EXECUTION
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

        # DISPLAY RESULTS
        if not filtered_data:
            self.display_placeholder(f"No classes scheduled for {selected_day} in {selected_section}.", color=(0, 0.75, 1, 1))
            return
        
        # Schedule Header and Rows
        self.timetable_container.add_widget(Label(text=f"[b]{selected_day} Schedule for {selected_section}[/b]", markup=True, size_hint_y=None, height=dp(30), font_size='16sp', color=(1, 1, 1, 1)))
        
        # Table Header Row
        header_row = self.create_timetable_header_row()
        self.timetable_container.add_widget(header_row)

        # Populate Rows
        for i, item in enumerate(filtered_data):
            row = self.create_timetable_data_row(item, i)
            self.timetable_container.add_widget(row)

    def create_timetable_header_row(self):
        """Helper to create the table header row."""
        header_row = BoxLayout(size_hint_y=None, height=dp(30))
        header_color = (0.2, 0.2, 0.2, 1)
        
        def create_header(text, width):
            lbl = Label(text=text, size_hint_x=width, color=(1, 1, 1, 1), font_size='13sp')
            with lbl.canvas.before:
                Color(*header_color)
                Rectangle(size=lbl.size, pos=lbl.pos)
            return lbl

        header_row.add_widget(create_header("Time Slot", 0.3))
        header_row.add_widget(create_header("Subject / Activity", 0.5))
        header_row.add_widget(create_header("Batch/Room", 0.2))
        return header_row

    def create_timetable_data_row(self, item, index):
        """Helper to create one data row."""
        row = BoxLayout(size_hint_y=None, height=dp(30))
        row_color = (0.1, 0.1, 0.1, 1) if index % 2 == 0 else (0.15, 0.15, 0.15, 1)
        
        def create_data_label(text, width):
            lbl = Label(text=text, size_hint_x=width, color=(1, 1, 1, 1), font_size='12sp')
            with lbl.canvas.before:
                Color(*row_color)
                Rectangle(size=lbl.size, pos=lbl.pos)
            return lbl

        # item is (Time, Subject, Location)
        row.add_widget(create_data_label(item[0], 0.3))
        row.add_widget(create_data_label(item[1], 0.5))
        row.add_widget(create_data_label(item[2], 0.2))
        return row


# --- 3. THE KIVY APP CLASS ---
class TimetableApp(App):
    def build(self):
        self.title = 'Student Dashboard'
        Window.size = (400, 700) 
        return TimetableDashboardScreen() 

if __name__ == '__main__':
    TimetableApp().run()