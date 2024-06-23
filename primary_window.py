# TODO: add a file dialog to select the CSV file

import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd

# Read data from CSV into a DataFrame
df = pd.read_csv("/Users/suryatejess/Documents/Projects/gui-course-reg/data/Theory_Slots.csv")
course_data1 = {}
for index, row in df.iterrows():
    course = row['COURSE CODE']
    slot = row['SLOT']
    if course in course_data1:
        course_data1[course].append(slot)
    else:
        course_data1[course] = [slot]

# TODO: read data from Lab_Slots.csv

selected_slots = {}  # Dictionary to store selected slots and their colors

# Function to update the slot dropdown based on the selected course code
def update_slot_dropdown(event, slot_dropdown, course_code_var):
    selected_course = course_code_var.get()
    slots = course_data1.get(selected_course, ["N/A"])
    slot_dropdown['values'] = slots

# Function to add new set of dropdown menus
def add_dropdowns():
    def remove_dropdowns():
        frame.destroy()
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
            # Check if any part of the slot is already selected or conflicts with existing selections
            conflict_pairs = {
                "E1": ["STC2", "STA2"],
                "STC2": ["E1"],
                "E2": ["STC1", "STA1"],
                "STC1": ["E2"],
                "STA2": ["E1"],
                "STA1": ["E2"],
                "G1": ["TFF1", "TEE1"],
                "TFF1": ["G1"],
                "G2": ["TFF2", "TEE2"],
                "TFF2": ["G2"],
                "TEE1": ["G1"],
                "TEE2": ["G2"]
            }
            for part in slot_parts:
                if part in selected_slots:
                    messagebox.showwarning("Slot Clash", f"The slot '{part}' is already filled by another course.")
                    return
                for conflict in conflict_pairs.get(part, []):
                    if conflict in selected_slots:
                        messagebox.showwarning("Slot Clash", f"The slot '{part}' cannot be selected when '{conflict}' is already selected.")
                        return
            for part in slot_parts:
                selected_slots[part] = color_dict[color]
        update_table()

    course_code_var = tk.StringVar()
    slot_var = tk.StringVar()
    color_var = tk.StringVar()

    # Create a new frame for each set of dropdowns
    frame = tk.Frame(root)
    frame.pack(pady=5)

    # Course Code Dropdown
    course_code_label = ttk.Label(frame, text="Select Course Code:")
    course_code_label.pack(side=tk.LEFT, padx=5)

    course_code_dropdown = ttk.Combobox(frame, textvariable=course_code_var)
    course_code_dropdown['values'] = list(course_data1.keys())
    course_code_dropdown.pack(side=tk.LEFT, padx=5)
    course_code_dropdown.bind("<<ComboboxSelected>>",
                              lambda event: update_slot_dropdown(event, slot_dropdown, course_code_var))

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
    apply_button = ttk.Button(frame, text="Apply Color", command=apply_color)
    apply_button.pack(side=tk.RIGHT, padx=5)

    # Cancel Button
    cancel_button = ttk.Button(frame, text="Cancel", command=remove_dropdowns)
    cancel_button.pack(side=tk.RIGHT, padx=5)

    # Set default course code and slot
    course_code_var.set(list(course_data1.keys())[0])
    update_slot_dropdown(None, slot_dropdown, course_code_var)

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

# Create the main window
root = tk.Tk()
root.title("Course Code and Slot Selector")

# Create a frame for the '+' button
plus_button_frame = tk.Frame(root)
plus_button_frame.pack(pady=5)

# Create the '+' button
plus_button = ttk.Button(plus_button_frame, text="+ Add", command=add_dropdowns)
plus_button.pack()

# Define the table data
table_data = [
    ["Day/Time", "8 - 9", "9 - 10", "10 - 11", "11 - 12", "12 - 1", "2 - 3", "3 - 4", "4 - 5", "5 - 6", "6 - 7"],
    ["Tue", "TF1", "TA1", "E1+STC2", "D1", "B1", "TA2", "E2+STC1", "D2", "B2", "TF2"],
    ["Wed", "TCC1", "E1+STA2", "G1+TFF1", "TBB1", "TDD1", "E2+STA1", "G2+TFF2", "TBB2", "TDD2", "TCC2"],
    ["Thu", "TE1", "C1", "A1", "F1", "D1", "C2", "A2", "F2", "D2", "TE2"],
    ["Fri", "TAA1", "TD1", "B1", "G1+TEE1", "C1", "TD2", "B2", "G2+TEE2", "C2", "TAA2"],
    ["Sat", "TG1", "TB1", "TC1", "A1", "F1", "TB2", "TC2", "A2", "F2", "TG2"]
]

# Create a frame for the table
table_frame = tk.Frame(root)
table_frame.pack(pady=10)

# Create a grid of labels and keep a reference to the labels
labels = []
for I in range(len(table_data)):  # Rows
    row_labels = []
    for j in range(len(table_data[I])):  # Columns
        label = tk.Label(table_frame, text=table_data[I][j], width=10, height=2, borderwidth=1, relief="solid")
        label.grid(row=I, column=j)
        row_labels.append(label)
    labels.append(row_labels)

# Define the colors and their codes
color_dict = {
    "Choose Color": "white",
    "Red": "#FF0000",
    "Green": "#00FF00",
    "Blue": "#0000FF",
    "Yellow": "#FFFF00",
    "Purple": "#800080",
    "Orange": "#FFA500",
    "Pink": "#FFC0CB",
    "LightBlue": "#ADD8E6",
    "LightGreen": "#90EE90",
    "LightYellow": "#FFFFE0",
    "LightCoral": "#F08080",
    "LightSalmon": "#FFA07A",
    "LightGray": "#D3D3D3",
    "DarkRed": "#8B0000",
    "DarkGreen": "#006400",
    "DarkBlue": "#00008B",
    "DarkYellow": "#FFD700",
    "DarkPurple": "#4B0082",
    "DarkOrange": "#FF8C00"
}

# Start the Tkinter event loop
root.mainloop()

# TODO: add a submit button to save the selected slots to a CSV file
# TODO: ics file generation for the whole semester