import tkinter as tk
from tkinter import ttk

# --- 1. DATA STRUCTURE: Timetable Data ---
TIMETABLES = {
    # Timetable for Section A
    "DIVISION A":
    [
        ("MONDAY", "1st Hour (9-10 AM)", "M-1", "Batch-everyone"),
        ("MONDAY", "2nd Hour (10-11 AM)", "PHY", "Batch-everyone"),
        ("MONDAY","ShortBreak!", "(11-11:15AM)", "Break", ""), 
        ("MONDAY", "3rd Hour (11:15-1:15 AM)", "EM", "Batch A1"),
        ("MONDAY", "3rd Hour (11:15-1:15 AM)", "BEE", "Batch A2"),
        ("MONDAY", "3rd Hour and 4th Hour (11:15-1:15 AM)", "PHY", "Batch A3"),
        ("MONDAY", "1:15-2 PM", "Long Break", "Canteen/Home"), 
        ("MONDAY", "3rd Hour and 4th Hour 2-4 PM", "PHY", "Batch A1"),
        ("MONDAY", "3rd Hour and 4th Hour 2-4 PM", "PHY", "Batch A2"),
        ("MONDAY", "3rd Hour and 4th Hour 2-4 PM", "PHY", "Batch A3"),
        
        ("TUESDAY", "1st Hour (9-10 AM)", "FPL", "Everyone"),
        ("TUESDAY", "2nd Hour (10-11 AM)", "EM", "Everyone"),
        ("TUESDAY","ShortBreak!", "(11-11:15AM)", "Break", ""), 
        ("TUESDAY", "3rd Hour (11:15-12:15 AM)", "PHY", "Everyone"),
        ("TUESDAY", "4th Hour (12:15-1:15 PM)", "M-I", "Everyone"),
        ("TUESDAY", "1:15-2 PM", "Long Break", "Canteen/Home"), 
        ("TUESDAY", "5th Hour (2-3 PM)", "DTIL", "Everyone"),
        ("TUESDAY", "6th Hour (3-4 PM)", "BEE", "Everyone"), 
        
        ("WEDNESDAY", "1st Hour (9-10 AM)", "EM", "Everyone"),
        ("WEDNESDAY", "2nd Hour (10-11 AM)", "PHY", "Everyone"),
        ("THRUSDAY","ShortBreak!", "(11-11:15AM)", "Break", ""),
        ("WEDNESDAY", "3rd and 4th Hour (11:15-1:15 PM)", "PCS", "Batch A-1"),
        ("WEDNESDAY", "3rd and 4th Hour (11:15-1:15 PM)", "library", "Batch A-2"),
        ("WEDNESDAY", "3rd and 4th Hour (11:15-1:15 PM)", "FPL", "Batch A-3"),
        ("WEDNESDAY", "5th Hour (2-3 PM)", "FPL", "Everyone"), 
        ("WEDNESDAY", "6th Hour (4-5 PM)", "EM", "Everyone"),
        
        ("THURSDAY", "1st Hour (9-11 AM)", "BEE", "Everyone"),
        ("THURSDAY", "1st Hour (9-11 AM)", "PHY", "Everyone"),
        ("THURSDAY", "1st Hour (9-11 AM)", "EM", "Everyone"),
        ("THRUSDAY","(11-11:15AM)", "Break", "Canteen"),
        ("THRUSDAY","3rd Hour and 4th Hour 2-4 PM", "PHY", "Batch A1"),
        ("THRUSDAY","3rd Hour and 4th Hour 2-4 PM", "EM", "Batch A2"),
        ("THRUSDAY","3rd Hour and 4th Hour 2-4 PM", "BEE", "Batch A3"),
        ("THRUSDAY", "1:15-2 PM", "Long Break", "Canteen/Home"), 
        ("THURSDAY", "5th Hour (2-3 PM)", "DTIL" "Room A-2"),

        ("FRIDAY", "1st Hour (9-10 AM)", "BEE", "Everyone"),
        ("FRIDAY", "2nd Hour (10-11 AM)", "PHY", "Everyone"),
        ("FRIDAY", "11-11:15", "Break", "Canteen"),
        ("FRIDAY", "3rd Hour and 4th Hour 11:15-1:15 PM", "FPL", "Batch A1"),
        ("FRIDAY", "3rd Hour and 4th Hour 11:15-1:15 PM", "PCS", "Batch A2"),
        ("FRIDAY", "3rd Hour and 4th Hour 11:15-1:15", "Library", "Batch A3"),
        ("FRIDAY", "1:15-2 PM", "Long Break", "Canteen/Home"),
        ("FRIDAY", "2-3 PM", "FPL", "Canteen/Home"),

    ],
    
    # Timetable for Section B 
    "DIVISION B":
    [
        ("MONDAY", "1st Hour (9-10 AM)", "EM", "Room B-1"),
        ("MONDAY", "2nd Hour (10-11 AM)", "M-I", "Room B-2"),
        ("MONDAY", "3rd Hour (11-12 AM)", "CCC-I", "Lab 3"),

        ("TUESDAY", "1st Hour (9-10 AM)", "BEE", "Room B-3"),
        ("TUESDAY", "2nd Hour (10-11 AM)", "M-I", "Room B-1"),
        ("TUESDAY", "3rd Hour (11-12 AM)", "PHY", "Room B-2"),
        ("TUESDAY", "4th Hour (12-1 PM)", "DL-B1-BEE, D1-PHY, D1-M-I", "Lab 4"),
        ("TUESDAY", "5th Hour (1:30-2:30 PM)", "DTIL", "Lab 1"),

        ("WEDNESDAY", "1st Hour (9-10 AM)", "PHY", "Room B-2"),
        ("WEDNESDAY", "2nd Hour (10-11 AM)", "M-I", "Room B-1"),
        ("WEDNESDAY", "3rd Hour (11-12 AM)", "EM", "Room B-3"),
        ("WEDNESDAY", "4th Hour (12-1 PM)", "DL-B1-BEE, D1-PHY, D1-M-I", "Lab 4"),

        ("THURSDAY", "1st Hour (9-10 AM)", "EM", "Room B-3"),
        ("THURSDAY", "2nd Hour (10-11 AM)", "M-I", "Room B-1"),
        ("THURSDAY", "3rd Hour (11-12 AM)", "PHY", "Room B-2"),
        ("THURSDAY", "4th Hour (12-1 PM)", "DL-B1-BEE, D1-PHY, D1-M-I", "Lab 4"),

        ("FRIDAY", "1st Hour (9-10 AM)", "BEE", "Room B-3"),
        ("FRIDAY", "2nd Hour (10-11 AM)", "EM", "Room B-1"),
        ("FRIDAY", "3rd Hour (11-12 AM)", "CCC-I", "Lab 3"),
        ("FRIDAY", "4th Hour (12-1 PM)", "DTIL", "Lab 1"),
        ("FRIDAY", "5th Hour (1:30-2:30 PM)", "TG", "Room B-2"),

       
    ],
    
}
Days = ["MONDAY", "TUESDAY", "WEDNESDAY", "THURSDAY", "FRIDAY", "SATURDAY"]
# --- 2. GUI Application Class ---
class StudentDashboard:
    def __init__(self, master):
        self.master = master
        master.title("Student Timetable Dashboard")
        master.geometry("750x550") # Increased size to fit selectors better

        # Styles
        self.style = ttk.Style()
        self.style.configure('TFrame', background='#f4f7f6')
        self.style.configure('TLabel', background='#f4f7f6', font=('Arial', 12))
        self.style.configure('Header.TLabel', font=('Arial', 18, 'bold'), foreground='#007bff')

        main_frame = ttk.Frame(master, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(main_frame, text="Student Timetable Dashboard", style='Header.TLabel').pack(pady=10)

        # --- Section and Day Selector Frame ---
        selector_group_frame = ttk.Frame(main_frame)
        selector_group_frame.pack(pady=15)

        # 1. Section Selector
        ttk.Label(selector_group_frame, text="Select Division:").pack(side=tk.LEFT, padx=(0, 10))
        self.section_var = tk.StringVar(master)
        self.section_var.set("-- Select Division --")

        sections = sorted(list(TIMETABLES.keys()))
        self.section_combo = ttk.Combobox(
            selector_group_frame,
            textvariable=self.section_var,
            values=sections,
            state="readonly",
            width=18
        )
        self.section_combo.pack(side=tk.LEFT, padx=15)
        
        # 2. Day Selector (NEW)
        ttk.Label(selector_group_frame, text="Select Day:").pack(side=tk.LEFT, padx=(15, 10))
        self.day_var = tk.StringVar(master)
        self.day_var.set("-- Select Day --")
        
        self.day_combo = ttk.Combobox(
            selector_group_frame,
            textvariable=self.day_var,
            values=Days, # Use the list of all days
            state="readonly",
            width=15
        )
        self.day_combo.pack(side=tk.LEFT, padx=5)

        # Bind the display function to both dropdowns
        self.section_combo.bind("<<ComboboxSelected>>", self.display_timetable)
        self.day_combo.bind("<<ComboboxSelected>>", self.display_timetable)


        # Timetable Display Area
        self.timetable_frame = ttk.Frame(main_frame)
        self.timetable_frame.pack(pady=20, fill=tk.BOTH, expand=True)
        
        ttk.Label(self.timetable_frame, text="Select a division and a day to view your schedule.", font=('Arial', 12, 'italic'), foreground='#6c757d').pack(expand=True, fill=tk.BOTH)

        self.tree = None

    # --- 3. Timetable Display Function ---
    def display_timetable(self, event=None):
        selected_section = self.section_var.get()
        selected_day = self.day_var.get() # Get the selected day

        # Clear existing content
        for widget in self.timetable_frame.winfo_children():
            widget.destroy()
        
        # Check for incomplete selection
        if selected_section not in TIMETABLES or selected_day == "-- Select Day --":
            msg = "Please select both a **Division** and a **Day**."
            ttk.Label(self.timetable_frame, text=msg, font=('Arial', 12, 'italic'), foreground='#dc3545').pack(expand=True, fill=tk.BOTH)
            return

        full_section_data = TIMETABLES[selected_section]

        # FILTER THE DATA based on the selected day
        filtered_data = [item for item in full_section_data if item[0] == selected_day]

        if not filtered_data:
            msg = f"No classes scheduled for **{selected_day}** in **{selected_section}**."
            ttk.Label(self.timetable_frame, text=msg, font=('Arial', 12, 'bold'), foreground='#007bff').pack(expand=True, fill=tk.BOTH)
            return

        # Display Header
        ttk.Label(self.timetable_frame, text=f"{selected_day} Schedule for {selected_section}", font=('Arial', 14, 'bold')).pack(pady=5)


        # Define columns for the Treeview
        columns = ("time", "subject", "room")
        
        self.tree = ttk.Treeview(self.timetable_frame, columns=columns, show='headings')
        self.tree.pack(fill=tk.BOTH, expand=True)

        # Define column headings
        self.tree.heading("time", text="Time Slot")
        self.tree.heading("subject", text="Subject / Activity")
        self.tree.heading("room", text="Batch/Room")
        
        # Define column widths
        self.tree.column("time", width=120, anchor=tk.CENTER)
        self.tree.column("subject", width=300, anchor=tk.W)
        self.tree.column("room", width=150, anchor=tk.CENTER)

        # Insert the filtered data
        for item in filtered_data:
            # Note: We skip the Day element (item[0]) since it's redundant here
            self.tree.insert("", tk.END, values=(item[1], item[2], item[3]))

        # Scrollbar
        vsb = ttk.Scrollbar(self.timetable_frame, orient="vertical", command=self.tree.yview)
        vsb.pack(side='right', fill='y')
        self.tree.configure(yscrollcommand=vsb.set)


# --- 4. Main Execution Block ---
if __name__ == "__main__":
    root = tk.Tk()
    # FIX 1: You must instantiate the class by adding (root)
    app = StudentDashboard(root) 
    # FIX 2: You must call mainloop() to start the GUI
    root.mainloop()