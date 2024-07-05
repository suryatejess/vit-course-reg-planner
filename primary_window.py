import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd

# Create the main window
root = tk.Tk()
root.title("Course Code and Slot Selector")

root2 = tk.Tk()
root2.title("Course Code and Course Name reference")

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

# Define the table data
table_data = [
    ["Day/Time",  "8 - 9","9 - 10","10 - 11","11 - 12","12 - 1","1 - 1:30","2 - 3","3 - 4","4 - 5","5 - 6","6 - 7","7 - 7:30"],
    ["Tue","TF1+L1","TA1+L2","E1+STC2+L3","D1+L4","B1+L5","L6","TA2+L31","E2+STC1+L32","D2+L33","B2+L34","TF2+L35","L36"],
    ["Wed","TCC1+L7","E1+STA2+L8","G1+TFF1+L9","TBB1+L10","TDD1+L11","L12","E2+STA1+L37","G2+TFF2+L38","TBB2+L39","TDD2+L40","TCC2+L41","L42"],
    ["Thu","TE1+L13","C1+L14","A1+L15","F1+L16","D1+L17","L18","C2+L43","A2+L44","F2+L45","D2+L46","TE2+L47","L48"],
    ["Fri","TAA1+L19","TD1+L20","B1+L21","G1+TEE1+L22","C1+L23","L24","TD2+L49","B2+L50","G2+TEE2+L51","C2+L52","TAA2+L53","L54"],
    ["Sat","TG1+L25","TB1+L26","TC1+L27","A1+L28","F1+L29","L30","TB2+L55","TC2+L56","A2+L57","F2+L58","TG2+L59","L60"]
]

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
        # Remove slot from selected_slots if present
        slot = slot_var.get()
        slot_parts = slot.split('+')
        for part in slot_parts:
            if part in selected_slots:
                del selected_slots[part]
        update_table()

    def apply_color():
        slot = slot_var.get()
        color = color_var.get()
        if slot != "N/A" and color != "Choose Color":
            slot_parts = slot.split('+')
            for part in slot_parts:
                if part in selected_slots:
                    messagebox.showwarning("Slot Clash", f"The slot '{part}' is already filled by another course.")
                    frame.destroy()
                    frames_list.remove(frame)
                    return
                if part in conflict_dict:
                    for conflict in conflict_dict[part]:
                        if conflict in selected_slots:
                            messagebox.showwarning("Slot Clash", f"The slot '{part}' cannot be selected when '{conflict}' is already selected.")
                            frame.destroy()
                            frames_list.remove(frame)
                            return
            for part in slot_parts:
                selected_slots[part] = color_dict[color]
        update_table()

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

reset_button = ttk.Button(plus_button_frame, text="Reset", command=reset_table)
reset_button.pack()

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
    "Orange": "#FFA500",
}

root.mainloop()
root2.mainloop()
