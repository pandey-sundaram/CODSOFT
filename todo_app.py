# -----------------------------------------------------------------------------
# File: todo_app.py
# Description: A classic-themed, detailed To-Do List application with
#              Create, Update, Delete, Search, and Track functionality.
#              Includes a pop-up calendar and time selectors.
# -----------------------------------------------------------------------------

import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
import datetime

# --- CONSTANTS ---
SAVE_FILE = "tasks.json"

# --- CALENDAR WIDGET ---
class CalendarPopup(tk.Toplevel):
    """A pop-up window that displays a calendar to select a date."""
    def __init__(self, parent, entry_widget):
        super().__init__(parent)
        self.entry_widget = entry_widget
        self.title("Select Date")
        self.geometry("280x220")
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()

        self.today = datetime.date.today()
        self.cal = datetime.datetime(self.today.year, self.today.month, 1)

        self.create_widgets()
        self.update_calendar()

    def create_widgets(self):
        header_frame = ttk.Frame(self)
        header_frame.pack(pady=5)

        ttk.Button(header_frame, text="<", command=self.prev_month, width=3).pack(side=tk.LEFT, padx=5)
        self.month_year_label = ttk.Label(header_frame, text="", font=("Helvetica", 12, "bold"), width=15, anchor="center")
        self.month_year_label.pack(side=tk.LEFT)
        ttk.Button(header_frame, text=">", command=self.next_month, width=3).pack(side=tk.LEFT, padx=5)

        days_frame = ttk.Frame(self)
        days_frame.pack()
        days = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
        for i, day in enumerate(days):
            ttk.Label(days_frame, text=day, width=4, anchor="center").grid(row=0, column=i)

        self.calendar_frame = ttk.Frame(self)
        self.calendar_frame.pack(pady=5)

    def update_calendar(self):
        for widget in self.calendar_frame.winfo_children():
            widget.destroy()

        self.month_year_label.config(text=self.cal.strftime("%B %Y"))
        month_starts_on = (self.cal.weekday() + 1) % 7
        days_in_month = (self.cal.replace(month=self.cal.month % 12 + 1, day=1) - datetime.timedelta(days=1)).day

        row, col = 0, month_starts_on
        for day in range(1, days_in_month + 1):
            btn = tk.Button(self.calendar_frame, text=str(day), width=3, relief="flat",
                            command=lambda d=day: self.select_date(d))
            btn.grid(row=row, column=col, padx=1, pady=1)
            if day == self.today.day and self.cal.month == self.today.month and self.cal.year == self.today.year:
                btn.config(bg="#a0a0a0", fg="white")
            col += 1
            if col > 6:
                col = 0
                row += 1

    def prev_month(self):
        self.cal = self.cal.replace(day=1) - datetime.timedelta(days=1)
        self.cal = self.cal.replace(day=1)
        self.update_calendar()

    def next_month(self):
        last_day = (self.cal.replace(month=self.cal.month % 12 + 1, day=1) - datetime.timedelta(days=1)).day
        self.cal = self.cal.replace(day=last_day) + datetime.timedelta(days=1)
        self.update_calendar()

    def select_date(self, day):
        selected_date = datetime.date(self.cal.year, self.cal.month, day)
        self.entry_widget.delete(0, tk.END)
        self.entry_widget.insert(0, selected_date.strftime("%Y-%m-%d"))
        self.destroy()

# --- DATA HANDLING ---
def load_tasks():
    if not os.path.exists(SAVE_FILE): return []
    try:
        with open(SAVE_FILE, "r") as f: return json.load(f)
    except (json.JSONDecodeError, IOError):
        messagebox.showerror("Error", "Could not load tasks from file.")
        return []

def save_tasks(tasks):
    try:
        with open(SAVE_FILE, "w") as f: json.dump(tasks, f, indent=4)
    except IOError:
        messagebox.showerror("Error", "Could not save tasks to file.")

# --- GUI ACTIONS ---
def populate_task_list(tasks_to_display=None):
    if tasks_to_display is None: tasks_to_display = app_tasks
    for item in tree.get_children(): tree.delete(item)
    for i, task in enumerate(app_tasks):
        if task in tasks_to_display:
            status = "Complete" if task["completed"] else "Pending"
            tags = ['completed'] if task["completed"] else []
            tags.append(f'priority_{task["priority"].lower()}')
            tree.insert("", tk.END, iid=i, values=(task["topic"], task["description"], task["date"], task["time"], task["priority"], status), tags=tuple(tags))

def add_task():
    time_str = f"{hour_var.get()}:{minute_var.get()} {ampm_var.get()}"
    task = {"topic": topic_entry.get(), "description": desc_entry.get(), "date": date_entry.get(), "time": time_str, "priority": priority_var.get(), "completed": False}
    if not all([task["topic"], task["description"], task["date"], task["priority"]]):
        messagebox.showwarning("Input Error", "Topic, Description, Date, and Priority are required.")
        return
    app_tasks.append(task)
    populate_task_list()
    clear_input_fields()
    save_tasks(app_tasks)

def update_task():
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showwarning("Selection Error", "Please select a task to update.")
        return
    item_index = int(selected_item[0])
    time_str = f"{hour_var.get()}:{minute_var.get()} {ampm_var.get()}"
    updated_task = {"topic": topic_entry.get(), "description": desc_entry.get(), "date": date_entry.get(), "time": time_str, "priority": priority_var.get(), "completed": app_tasks[item_index]["completed"]}
    if not all([updated_task["topic"], updated_task["description"], updated_task["date"], updated_task["priority"]]):
        messagebox.showwarning("Input Error", "Topic, Description, Date, and Priority are required.")
        return
    app_tasks[item_index] = updated_task
    populate_task_list()
    clear_input_fields()
    save_tasks(app_tasks)

def delete_task():
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showwarning("Selection Error", "Please select a task to delete.")
        return
    if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete the selected task?"):
        item_index = int(selected_item[0])
        del app_tasks[item_index]
        populate_task_list()
        clear_input_fields()
        save_tasks(app_tasks)

def toggle_complete():
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showwarning("Selection Error", "Please select a task to mark as complete.")
        return
    item_index = int(selected_item[0])
    app_tasks[item_index]["completed"] = not app_tasks[item_index]["completed"]
    populate_task_list()
    save_tasks(app_tasks)

def search_tasks():
    query = search_entry.get().lower()
    if not query:
        populate_task_list()
        return
    filtered_tasks = [task for task in app_tasks if query in task["topic"].lower() or query in task["description"].lower()]
    populate_task_list(filtered_tasks)

def clear_search():
    search_entry.delete(0, tk.END)
    populate_task_list()

def on_item_select(event):
    selected_item = tree.selection()
    if not selected_item: return
    item_index = int(selected_item[0])
    task = app_tasks[item_index]
    clear_input_fields()
    topic_entry.insert(0, task["topic"])
    desc_entry.insert(0, task["description"])
    date_entry.insert(0, task["date"])
    try:
        time_parts = task["time"].replace(":", " ").split()
        hour_var.set(time_parts[0])
        minute_var.set(time_parts[1])
        ampm_var.set(time_parts[2])
    except (IndexError, ValueError):
        hour_var.set("12")
        minute_var.set("00")
        ampm_var.set("PM")
    priority_var.set(task["priority"])

def clear_input_fields():
    topic_entry.delete(0, tk.END)
    desc_entry.delete(0, tk.END)
    date_entry.delete(0, tk.END)
    hour_var.set("12")
    minute_var.set("00")
    ampm_var.set("PM")
    priority_var.set("Medium")

def open_calendar():
    CalendarPopup(root, date_entry)

# --- GUI SETUP ---
root = tk.Tk()
root.title("Classic To-Do List")
root.geometry("850x650")
root.minsize(700, 550)
root.configure(bg="#fdfdfd")

# --- STYLING ---
style = ttk.Style(root)
style.theme_use("clam")
style.configure("TFrame", background="#fdfdfd")
style.configure("TLabel", background="#fdfdfd", font=("Helvetica", 10))
style.configure("TButton", font=("Helvetica", 10, "bold"), padding=6)
style.configure("Treeview", rowheight=25, font=("Helvetica", 10))
style.configure("Treeview.Heading", font=("Helvetica", 11, "bold"))
style.map("TButton", background=[('active', '#e0e0e0')])

# --- INPUT FRAME ---
input_frame = ttk.Frame(root, padding="10")
input_frame.pack(fill=tk.X, padx=10, pady=5)
input_frame.columnconfigure(1, weight=1)
input_frame.columnconfigure(3, weight=1)

ttk.Label(input_frame, text="Topic:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
topic_entry = ttk.Entry(input_frame, width=30, font=("Helvetica", 10))
topic_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

date_frame = ttk.Frame(input_frame)
date_frame.grid(row=0, column=3, padx=5, pady=5, sticky="ew")
ttk.Label(input_frame, text="Date:").grid(row=0, column=2, padx=5, pady=5, sticky="w")
date_entry = ttk.Entry(date_frame, width=22, font=("Helvetica", 10))
date_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
cal_button = ttk.Button(date_frame, text="📅", command=open_calendar, width=3)
cal_button.pack(side=tk.LEFT, padx=(5,0))

ttk.Label(input_frame, text="Description:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
desc_entry = ttk.Entry(input_frame, width=30, font=("Helvetica", 10))
desc_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

ttk.Label(input_frame, text="Time:").grid(row=1, column=2, padx=5, pady=5, sticky="w")
time_frame = ttk.Frame(input_frame)
time_frame.grid(row=1, column=3, padx=5, pady=5, sticky="ew")
hour_var = tk.StringVar(value="12")
hour_spinbox = ttk.Spinbox(time_frame, from_=1, to=12, textvariable=hour_var, width=4, font=("Helvetica", 10))
hour_spinbox.pack(side=tk.LEFT)
minute_var = tk.StringVar(value="00")
minute_spinbox = ttk.Spinbox(time_frame, from_=0, to=59, format="%02.0f", textvariable=minute_var, width=4, font=("Helvetica", 10))
minute_spinbox.pack(side=tk.LEFT, padx=5)
ampm_var = tk.StringVar(value="PM")
ampm_menu = ttk.OptionMenu(time_frame, ampm_var, "PM", "AM", "PM")
ampm_menu.pack(side=tk.LEFT)

ttk.Label(input_frame, text="Priority:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
priority_var = tk.StringVar(value="Medium")
priority_menu = ttk.OptionMenu(input_frame, priority_var, "Medium", "High", "Medium", "Low")
priority_menu.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

# --- SEARCH FRAME ---
search_frame = ttk.Frame(root, padding="10 0 10 10")
search_frame.pack(fill=tk.X, padx=10, pady=0)
search_frame.columnconfigure(1, weight=1)
ttk.Label(search_frame, text="Search:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
search_entry = ttk.Entry(search_frame, font=("Helvetica", 10))
search_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
search_btn = ttk.Button(search_frame, text="Search", command=search_tasks)
search_btn.grid(row=0, column=2, padx=5)
clear_btn = ttk.Button(search_frame, text="Clear Search", command=clear_search)
clear_btn.grid(row=0, column=3, padx=5)

# --- BUTTONS FRAME ---
button_frame = ttk.Frame(root, padding="10")
button_frame.pack(fill=tk.X, padx=10, pady=5)
button_frame.columnconfigure((0,1,2,3), weight=1)
add_btn = ttk.Button(button_frame, text="Add Task", command=add_task)
add_btn.grid(row=0, column=0, padx=5, sticky="ew")
update_btn = ttk.Button(button_frame, text="Update Task", command=update_task)
update_btn.grid(row=0, column=1, padx=5, sticky="ew")
delete_btn = ttk.Button(button_frame, text="Delete Task", command=delete_task)
delete_btn.grid(row=0, column=2, padx=5, sticky="ew")
complete_btn = ttk.Button(button_frame, text="Toggle Complete", command=toggle_complete)
complete_btn.grid(row=0, column=3, padx=5, sticky="ew")

# --- TASK LIST (TREEVIEW) FRAME ---
tree_frame = ttk.Frame(root, padding="10")
tree_frame.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)
columns = ("topic", "description", "date", "time", "priority", "status")
tree = ttk.Treeview(tree_frame, columns=columns, show="headings")
for col in columns: tree.heading(col, text=col.capitalize())
tree.column("topic", width=150); tree.column("description", width=250); tree.column("date", width=100, anchor="center")
tree.column("time", width=100, anchor="center"); tree.column("priority", width=80, anchor="center"); tree.column("status", width=80, anchor="center")
tree.tag_configure('completed', foreground='grey', font=("Helvetica", 10, "overstrike"))
tree.tag_configure('priority_high', background='#ffdddd')
tree.tag_configure('priority_medium', background='#ffffcc')
tree.tag_configure('priority_low', background='#ddffdd')
tree.bind("<<TreeviewSelect>>", on_item_select)
scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=tree.yview)
tree.configure(yscrollcommand=scrollbar.set)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
tree.pack(expand=True, fill=tk.BOTH)

# --- INITIALIZE APP ---
if __name__ == "__main__":
    app_tasks = load_tasks()
    populate_task_list()
    root.mainloop()
