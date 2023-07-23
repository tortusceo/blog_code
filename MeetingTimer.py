import tkinter as tk
from tkinter import ttk, font
import threading
import time

# Here the rates are stored as per-second values (annual salary / total seconds in a year)
salaries = {
    "Software Engineer": 60000 / 31536000,
    "Project Manager": 80000 / 31536000,
}

def get_salary(role):
    if role in salaries:
        return salaries[role]
    else:
        return 0

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()
        self.running = False

    def create_widgets(self):
        self.role_label = tk.Label(self, text="Enter roles (comma separated):")
        self.role_label.pack(side="top")
        
        self.role_entry = tk.Entry(self)
        self.role_entry.pack(side="top")

        self.role_list = tk.Listbox(self)
        self.role_list.pack(side="top")

        self.start = tk.Button(self)
        self.start["text"] = "Start Meeting"
        self.start["command"] = self.start_meeting
        self.start.pack(side="top")

        self.stop = tk.Button(self)
        self.stop["text"] = "Stop Meeting"
        self.stop["command"] = self.stop_meeting
        self.stop.pack(side="top")

        # Reset button
        self.reset = tk.Button(self)
        self.reset["text"] = "Reset Meeting"
        self.reset["command"] = self.reset_meeting
        self.reset.pack(side="top")

        self.cost = tk.Label(self, fg="red")
        self.cost.pack(side="top")
        
        self.large_font = font.Font(size=24)

        # Button to open roles modification window
        self.modify_roles_button = tk.Button(self, text="Modify Roles", command=self.open_roles_window)
        self.modify_roles_button.pack(side="top")

    def start_meeting(self):
        roles = self.role_entry.get().split(",")
        roles = [role.strip() for role in roles]
        for role in roles:
            self.role_list.insert(tk.END, role)
        self.total_cost_per_second = sum(get_salary(role) for role in roles)
        self.start_time = time.time()
        self.running = True
        self.update_cost()

    def stop_meeting(self):
        self.running = False

    def reset_meeting(self):
        self.stop_meeting()
        self.role_list.delete(0, tk.END)
        self.role_entry.delete(0, tk.END)
        self.cost["text"] = ""
        
    def update_cost(self):
        if self.running:
            elapsed_time = time.time() - self.start_time
            total_cost = self.total_cost_per_second * elapsed_time

            self.cost["text"] = f"Total cost: £{total_cost:.2f}"
            self.cost["font"] = self.large_font

            # schedule the next update in 1 second
            self.after(1000, self.update_cost)

    def open_roles_window(self):
        RolesWindow(self)

class RolesWindow(tk.Toplevel):
    def __init__(self, parent):
        tk.Toplevel.__init__(self, parent)
        self.title("Modify Roles")
        
        # Role and rate modification section
        self.modify_role_label = tk.Label(self, text="Modify roles and rates:")
        self.modify_role_label.pack(side="top")

        self.roles_rates_list = tk.Listbox(self)
        self.roles_rates_list.pack(side="top")
        self.update_roles_rates_list()

        self.modify_role_label = tk.Label(self, text="Role:")
        self.modify_role_label.pack(side="top")

        self.modify_role_entry = tk.Entry(self)
        self.modify_role_entry.pack(side="top")

        self.modify_rate_label = tk.Label(self, text="Annual Salary (£):")
        self.modify_rate_label.pack(side="top")

        self.modify_rate_entry = tk.Entry(self)
        self.modify_rate_entry.pack(side="top")

        self.add_role_button = tk.Button(self, text="Add/Update Role", command=self.add_role)
        self.add_role_button.pack(side="top")

        self.remove_role_button = tk.Button(self, text="Remove Role", command=self.remove_role)
        self.remove_role_button.pack(side="top")

    def add_role(self):
        role = self.modify_role_entry.get().strip()
        annual_salary = float(self.modify_rate_entry.get())
        # Convert annual salary to per second salary
        salaries[role] = annual_salary / 31536000
        self.update_roles_rates_list()

    def remove_role(self):
        role = self.modify_role_entry.get().strip()
        if role in salaries:
            del salaries[role]
        self.update_roles_rates_list()

    def update_roles_rates_list(self):
        self.roles_rates_list.delete(0, tk.END)
        for role, rate in salaries.items():
            annual_salary = rate * 31536000  # convert back to annual salary for displaying
            self.roles_rates_list.insert(tk.END, f"{role}: £{annual_salary:.2f}/year")

root = tk.Tk()
root.title("Meeting Cost Timer")
app = Application(master=root)
app.mainloop()

