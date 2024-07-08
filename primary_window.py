import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
from ics import Calendar, Event
from datetime import datetime, timedelta
import pytz

# Create the main window
root = tk.Tk()
root.title("Course Code and Slot Selector")

root2 = tk.Tk()
root2.title("Course Code and Course Name Reference")

df_2_theory = pd.read_csv('data/Theory_Slots.csv')
df_2_lab = pd.read_csv('data/Lab_Slots.csv')
df_2_theory = df_2_theory[['COURSE CODE', 'COURSE TITLE']]
df_2_lab = df_2_lab[['COURSE CODE', 'COURSE TITLE']]
# remove "COURSE CODE" duplicates along with their respective "COURSE TITLE"
df_2_theory = df_2_theory[['COURSE CODE', 'COURSE TITLE']].drop_duplicates()
df_2_lab = df_2_lab[['COURSE CODE', 'COURSE TITLE']].drop_duplicates()
# combine df_2_theory and df_2_lab into a dataframe called df_2
frames = [df_2_theory, df_2_lab]
df_2 = pd.concat(frames)
df_2 = df_2[['COURSE CODE', 'COURSE TITLE']].drop_duplicates()

# Display df_2 in root2 window
tree = ttk.Treeview(root2, columns=("Course Code", "Course Title"), show='headings')
tree.heading("Course Code", text="Course Code")
tree.heading("Course Title", text="Course Title")
tree.pack(fill=tk.BOTH, expand=True)

# Insert data into treeview
for index, row in df_2.iterrows():
    tree.insert("", tk.END, values=(row['COURSE CODE'], row['COURSE TITLE']))

secondary_window = tk.Label(root, text='hi')

# Read data from theory CSV into a DataFrame
df_theory = pd.read_csv('data/Theory_Slots.csv')
course_data_theory = {}
for index, row in df_theory.iterrows():
    course = row['COURSE CODE']
    slot = row['SLOT']
    if course in course_data_theory:
        course_data_theory[course].append(slot)
    else:
        course_data_theory[course] = [slot]

# Read data from lab CSV into a DataFrame
df_lab = pd.read_csv('data/Lab_Slots.csv')
course_data_lab = {}
for index, row in df_lab.iterrows():
    course = row['COURSE CODE']
    slot = row['SLOT']
    if course in course_data_lab:
        course_data_lab[course].append(slot)
    else:
        course_data_lab[course] = [slot]

selected_slots = {}  # Dictionary to store selected slots and their colors
selected_course_codes = {}  # Dictionary to store course code and their slots (slots as string)

# Define the table data
table_data = [
    ["Day/Time",  "08:00 - 09:00","09:00 - 10:00","10:00 - 11:00","11:00 - 12:00","12:00 - 13:00","13 - 13:30","14:00 - 15:00","15:00 - 16:00","16:00 - 17:00","17:00 - 18:00","18:00 - 19:00","19:00 - 19:30"],
    ["Tuesday","TF1+L1","TA1+L2","E1+STC2+L3","D1+L4","B1+L5","L6","TA2+L31","E2+STC1+L32","D2+L33","B2+L34","TF2+L35","L36"],
    ["Wednesday","TCC1+L7","E1+STA2+L8","G1+TFF1+L9","TBB1+L10","TDD1+L11","L12","E2+STA1+L37","G2+TFF2+L38","TBB2+L39","TDD2+L40","TCC2+L41","L42"],
    ["Thursday","TE1+L13","C1+L14","A1+L15","F1+L16","D1+L17","L18","C2+L43","A2+L44","F2+L45","D2+L46","TE2+L47","L48"],
    ["Friday","TAA1+L19","TD1+L20","B1+L21","G1+TEE1+L22","C1+L23","L24","TD2+L49","B2+L50","G2+TEE2+L51","C2+L52","TAA2+L53","L54"],
    ["Saturday","TG1+L25","TB1+L26","TC1+L27","A1+L28","F1+L29","L30","TB2+L55","TC2+L56","A2+L57","F2+L58","TG2+L59","L60"]
]

# Calendar
slot_timings = {}
for i in range(1, len(table_data)):
    for j in range(1, len(table_data[i])):
        slot_parts = table_data[i][j].split("+")
        for part in slot_parts:
            if part not in slot_timings:
                slot_timings[part] = [table_data[0][j] +"+"+ table_data[i][0]]
            elif part in slot_timings:
                slot_timings[part].append(table_data[0][j]+"+"+table_data[i][0])
'''
slot_timings = 
{
'B1': ['12:00 - 13:00+Tuesday', '10:00 - 11:00+Friday'],
'L5': ['12:00 - 13:00+Tuesday'],
...
...
}

selected_course_codes = # example
{'ECE3010': 'C1+TC1', 'CHY1001': 'G2'} 
'''


def export_cal_csv():
    save_table()

    cal_load = pd.read_csv('user_data/saved_table.csv')

    # Data frame with COURSE CODE, SLOT, TIMINGS, DAY with each slot part and its respective timings and day
    cal_exp = pd.DataFrame(columns=['COURSE CODE', 'SLOT', 'TIMINGS', 'DAY'])
    for index, row in cal_load.iterrows():
        course_code = row['COURSE CODE']
        slot = row['SLOT']
        slot_parts = slot.split('+')
        for part in slot_parts:
            if part in slot_timings:
                for time_day in slot_timings[part]:
                    time, day = time_day.split('+')
                    new_row = pd.DataFrame({'COURSE CODE': [course_code], 'SLOT': [part], 'TIMINGS': [time], 'DAY': [day]})
                    cal_exp = pd.concat([cal_exp, new_row], ignore_index=True)

    # export this to csv file named 'export_ics.csv'
    cal_exp.to_csv('user_data/export_ics.csv', index=False)

def export_cal_ics():
    export_cal_csv()

    # Put a dialog box with 'added' and 'dont know how to add' buttons
    # add an if condition so that the following code will get executed only if the user clikcs 'added' button
    # when the user clicks 'dont know how to add button', it will redirect the user to open browser and play this youtube video : https://youtu.be/MKM90u7pf3U?si=st3S1adZ5g-QcpJ9&t=65

    # Ask the user if they have added the venue/location
    user_response = messagebox.askquestion("Venue/Location", "Have you added the venue/location information?")

    if user_response == 'yes':
        # File paths
        csv_file_path = 'user_data/export_ics.csv'
        ics_file_path = 'time_table_calendar.ics'

        # Load the CSV data
        df = pd.read_csv(csv_file_path)

        # Define the time zone for India
        tz = pytz.timezone('Asia/Kolkata')

        # Define the end date
        end_date = datetime(2024, 9, 9, tzinfo=tz)

        # Create a new calendar
        calendar = Calendar()

        # Function to parse time and create events
        def create_event(row):
            start_time_str, end_time_str = row['TIMINGS'].split(' - ')
            start_time = datetime.strptime(start_time_str, '%H:%M').time()
            end_time = datetime.strptime(end_time_str, '%H:%M').time()

            # Map days to weekdays
            day_map = {
                'Monday': 0,
                'Tuesday': 1,
                'Wednesday': 2,
                'Thursday': 3,
                'Friday': 4,
                'Saturday': 5,
                'Sunday': 6
            }
            day_of_week = day_map[row['DAY']]

            # Starting date (Assuming the first week is the week starting from today)
            start_date = datetime.now(tz) + timedelta(days=(day_of_week - datetime.now(tz).weekday()) % 7)

            # Create events for each week until the end date
            current_date = start_date
            while current_date <= end_date:
                event = Event()
                event.name = row['COURSE CODE']
                event.begin = tz.localize(datetime.combine(current_date.date(), start_time))
                event.end = tz.localize(datetime.combine(current_date.date(), end_time))
                event.location = row['VENUE']

                calendar.events.add(event)

                current_date += timedelta(weeks=1)

        # Create events for each row in the CSV
        df.apply(create_event, axis=1)

        # Write the calendar to an ICS file
        with open(ics_file_path, 'w') as f:
            f.writelines(calendar)

        print(f'ICS file has been created: {ics_file_path}')

    elif user_response == 'no':
        # Redirect to the YouTube video
        import webbrowser
        webbrowser.open("https://youtu.be/MKM90u7pf3U?si=st3S1adZ5g-QcpJ9&t=65")

    # File paths
    csv_file_path = 'user_data/export_ics.csv'
    ics_file_path = 'time_table_calendar.ics'

    # Load the CSV data
    df = pd.read_csv(csv_file_path)

    # Define the time zone for India
    tz = pytz.timezone('Asia/Kolkata')

    # Define the end date
    end_date = datetime(2024, 9, 9, tzinfo=tz)

    # Create a new calendar
    calendar = Calendar()

    # Function to parse time and create events
    def create_event(row):
        start_time_str, end_time_str = row['TIMINGS'].split(' - ')
        start_time = datetime.strptime(start_time_str, '%H:%M').time()
        end_time = datetime.strptime(end_time_str, '%H:%M').time()

        # Map days to weekdays
        day_map = {
            'Monday': 0,
            'Tuesday': 1,
            'Wednesday': 2,
            'Thursday': 3,
            'Friday': 4,
            'Saturday': 5,
            'Sunday': 6
        }
        day_of_week = day_map[row['DAY']]

        # Starting date (Assuming the first week is the week starting from today)
        start_date = datetime.now(tz) + timedelta(days=(day_of_week - datetime.now(tz).weekday()) % 7)

        # Create events for each week until the end date
        current_date = start_date
        while current_date <= end_date:
            event = Event()
            event.name = row['COURSE CODE']
            event.begin = tz.localize(datetime.combine(current_date.date(), start_time))
            event.end = tz.localize(datetime.combine(current_date.date(), end_time))
            event.location = row['VENUE']

            calendar.events.add(event)

            current_date += timedelta(weeks=1)

    # Create events for each row in the CSV
    df.apply(create_event, axis=1)

    # Write the calendar to an ICS file
    with open(ics_file_path, 'w') as f:
        f.writelines(calendar)

    print(f'ICS file has been created: {ics_file_path}')


# Define conflicting slots
conflict_pairs = []
for i in range(1, len(table_data)):
    for j in range(1, len(table_data[i])):
        slots = table_data[i][j].split("+")
        conflict_pairs.append(slots)

conflict_dict = {}
for pair in conflict_pairs:
    for slot in pair:
        if slot not in conflict_dict:
            conflict_dict[slot] = set()
        conflict_dict[slot].update(pair)
        conflict_dict[slot].remove(slot)

# Function to update the slot dropdown based on the selected course code
def update_slot_dropdown(event, slot_dropdown, course_code_var, course_data):
    selected_course = course_code_var.get()
    slots = course_data.get(selected_course, ["N/A"])
    slot_dropdown['values'] = slots

# List to store frame references
frames_list = []

# Function to add new set of dropdown menus
def add_dropdowns():
    def remove_dropdowns():
        frame.destroy()
        frames_list.remove(frame)
        # Remove slot from selecteld_sots if present
        slot = slot_var.get()
        slot_parts = slot.split('+')
        for part in slot_parts:
            if part in selected_slots:
                del selected_slots[part]
        # Remove course_code from selected_course_codes if present
        course = course_code_var.get()
        del selected_course_codes[course]

        update_table()

    def apply_color():
        slot = slot_var.get()
        color = color_var.get()
        course = course_code_var.get()

        if slot != "N/A" and color != "Choose Color":
            slot_parts = slot.split('+')

            # Check for slot conflicts
            for part in slot_parts:
                if part in selected_slots:
                    messagebox.showwarning("Slot Clash", f"The slot '{part}' is already filled by another course.")
                    frame.destroy()
                    frames_list.remove(frame)
                    return
                if part in conflict_dict:
                    for conflict in conflict_dict[part]:
                        if conflict in selected_slots:
                            messagebox.showwarning("Slot Clash",
                                                   f"The slot '{part}' cannot be selected when '{conflict}' is already selected.")
                            frame.destroy()
                            frames_list.remove(frame)
                            return

            # Update selected_slots with the new color
            for part in slot_parts:
                selected_slots[part] = color_dict[color]

            # Update the selected_course_codes dictionary
            selected_course_codes[course] = slot

            # Update the table to reflect the new color
            update_table()
        else:
            messagebox.showwarning("Incomplete Selection", "Please select a slot and a color.")

    course_code_var = tk.StringVar()
    slot_var = tk.StringVar()
    color_var = tk.StringVar()
    course_type_var = tk.StringVar(value="Theory")

    # Create a new frame for each set of dropdowns
    frame = tk.Frame(main_frame)
    frame.pack(pady=5, anchor='w')
    frames_list.append(frame)  # Add frame reference to list

    # Theory/ Lab Radio Buttons
    theory_radio = ttk.Radiobutton(frame, text="Theory", variable=course_type_var, value="Theory", command=lambda: update_slot_dropdown(None, slot_dropdown, course_code_var, course_data_theory))
    lab_radio = ttk.Radiobutton(frame, text="Lab", variable=course_type_var, value="Lab", command=lambda: update_slot_dropdown(None, slot_dropdown, course_code_var, course_data_lab))

    theory_radio.pack(side=tk.LEFT, padx=5)
    lab_radio.pack(side=tk.LEFT, padx=5)

    # Course Code Dropdown
    course_code_label = ttk.Label(frame, text="Select Course Code:")
    course_code_label.pack(side=tk.LEFT, padx=5)

    course_code_dropdown = ttk.Combobox(frame, textvariable=course_code_var)
    course_code_dropdown['values'] = list(course_data_theory.keys())
    course_code_dropdown.pack(side=tk.LEFT, padx=5)
    course_code_dropdown.bind("<<ComboboxSelected>>",
                              lambda event: update_slot_dropdown(event, slot_dropdown, course_code_var, course_data_theory if course_type_var.get() == "Theory" else course_data_lab))

    # Slot Dropdown
    slot_label = ttk.Label(frame, text="Select Slot:")
    slot_label.pack(side=tk.LEFT, padx=5)

    slot_dropdown = ttk.Combobox(frame, textvariable=slot_var, state='readonly')
    slot_dropdown.pack(side=tk.LEFT, padx=5)

    # Color Dropdown
    color_label = ttk.Label(frame, text="Select Color:")
    color_label.pack(side=tk.LEFT, padx=5)

    color_dropdown = ttk.Combobox(frame, textvariable=color_var)
    color_dropdown['values'] = list(color_dict.keys())
    color_dropdown.pack(side=tk.LEFT, padx=5)

    # Apply Color Button
    def handle_button_click():
        apply_color()
        apply_button.config(state=tk.DISABLED)

    apply_button = ttk.Button(frame, text="Apply Color", command=handle_button_click)
    apply_button.pack(side=tk.RIGHT, padx=5)

    # Cancel Button
    cancel_button = ttk.Button(frame, text="Cancel", command=remove_dropdowns)
    cancel_button.pack(side=tk.RIGHT, padx=5)

    # Set default course code and slot
    course_code_var.set(list(course_data_theory.keys())[0])
    update_slot_dropdown(None, slot_dropdown, course_code_var, course_data_theory)

    # Move the '+' button below the new frame
    plus_button_frame.pack_forget()
    plus_button_frame.pack(pady=5)

# Function to update the table with selected slot colors
def update_table():
    for I in range(1, len(table_data)):  # Rows (excluding header row)
        for j in range(1, len(table_data[I])):  # Columns (excluding first column)
            slot = table_data[I][j]
            slot_parts = slot.split('+')
            for part in slot_parts:
                if part in selected_slots:
                    labels[I][j].config(bg=selected_slots[part])
                    break  # Use the first matching part's color
                else:
                    labels[I][j].config(bg="white")


# Create a frame for the course selection and table
main_frame = tk.Frame(root)
main_frame.pack(side=tk.TOP, fill='both', expand=True)

# Create a frame for the '+' button
plus_button_frame = tk.Frame(main_frame)
plus_button_frame.pack(pady=5)

# Create the '+' button
plus_button = ttk.Button(plus_button_frame, text="+ Add", command=add_dropdowns)
plus_button.pack()

# Create the reset button
def reset_table():
    global selected_slots
    selected_slots.clear()
    for frame in frames_list:
        frame.destroy()
    frames_list.clear()  # Clear the list after destroying all frames
    update_table()

    global selected_course_codes
    selected_course_codes.clear()

reset_button = ttk.Button(plus_button_frame, text="Reset", command=reset_table)
reset_button.pack()

# Create the save button
def save_table():
    if len(selected_course_codes) == 0:
        messagebox.showwarning("No Selection", "Please select at least one course code and slot.")
        return

    # Create a DataFrame to store the selected course codes and slots
    df = pd.DataFrame(selected_course_codes.items(), columns=['COURSE CODE', 'SLOT'])
    df.to_csv('user_data/saved_table.csv', index=False)
    messagebox.showinfo("Selection Saved", "The selected slots have been saved successfully. Add the Venue/Location manually if you wanna make use of the calendar feature")

save_button = ttk.Button(plus_button_frame, text="Save time table", command=save_table)
save_button.pack()


# export_calendar_button = ttk.Button(plus_button_frame, text="Export Calendar", command=export_cal_csv)
# export_calendar_button.pack()


make_ics_file_button = ttk.Button(plus_button_frame, text="Make ics file", command=export_cal_ics)
make_ics_file_button.pack()




# Create a frame for the table
table_frame = tk.Frame(main_frame)
table_frame.pack(pady=10)
labels = []
for I in range(len(table_data)):  # Rows
    row_labels = []
    for j in range(len(table_data[I])):  # Columns
        label = tk.Label(table_frame, text=table_data[I][j], width=10, height=2, borderwidth=1, relief="solid")
        label.grid(row=I, column=j)
        row_labels.append(label)
    labels.append(row_labels)

color_dict = {
    "Red": "#FF0000",
    "Green": "#00FF00",
    "Blue": "#0000FF",
    "Yellow": "#FFFF00",
    "Purple": "#800080",
    "Orange": "#FFA500"
}

root.mainloop()
root2.mainloop()

