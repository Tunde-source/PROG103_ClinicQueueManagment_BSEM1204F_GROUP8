import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

APP_TITLE = "Clinic Queue Management System - Sierra Leone"

PRIORITY_LEVELS = ["Emergency", "High", "Normal", "Low"]
DEPARTMENTS = [
    "General OPD",
    "Maternal Health",
    "Pediatrics",
    "TB / Infectious Disease",
    "Eye Clinic",
    "Pharmacy"
]

BG_COLOR = "#F0F4F7"
HEADER_COLOR = "#2C5F8A"
BUTTON_COLOR = "#2C5F8A"
TEXT_COLOR = "#222222"

patients = []
queue_counter = [0]


def generate_queue_number(priority):
    """
    Generate a queue number based on priority.
    Emergency = E-001, High = H-001, Normal = N-001, Low = L-001
    """
    queue_counter[0] += 1
    prefix_map = {"Emergency": "E", "High": "H", "Normal": "N", "Low": "L"}
    prefix = prefix_map.get(priority, "X")
    return prefix + "-" + str(queue_counter[0]).zfill(3)


def calculate_wait_time(priority, position):
    """
    Estimate waiting time in minutes based on priority and queue position.
    Uses a loop to add time for each patient ahead in the queue.
    """
    base_times = {"Emergency": 0, "High": 5, "Normal": 15, "Low": 20}
    wait = base_times.get(priority, 15)

    for i in range(position):
        if priority == "Emergency":
            wait += 2
        elif priority == "High":
            wait += 5
        elif priority == "Normal":
            wait += 8
        else:
            wait += 10

    return wait


def validate_patient_input(name, age_str, contact):
    """
    Validate patient input before processing.
    Returns a tuple: (True/False, message)
    """
    if not name.strip():
        return False, "Patient name cannot be empty."

    if len(name.strip()) < 2:
        return False, "Patient name must be at least 2 characters."

    if not age_str.strip().isdigit():
        return False, "Age must be a whole number (e.g. 25)."

    age = int(age_str.strip())
    if age < 1 or age > 119:
        return False, "Age must be between 1 and 119."

    if contact.strip():
        check = contact.strip()
        if check.startswith("+"):
            check = check[1:]
        if not check.isdigit():
            return False, "Contact number must contain digits only."

    return True, "OK"


def register_patient(name, age, gender, department, priority, contact):
    """
    Create a patient record and add it to the patients list.
    Returns the new patient record.
    """
    queue_no = generate_queue_number(priority)

    position = 0
    for p in patients:
        if p["status"] == "Waiting":
            position += 1

    wait = calculate_wait_time(priority, position)

    record = {
        "queue_no": queue_no,
        "name": name.strip().title(),
        "age": age,
        "gender": gender,
        "department": department,
        "priority": priority,
        "contact": contact.strip() if contact.strip() else "N/A",
        "wait_min": wait,
        "status": "Waiting",
        "reg_time": datetime.now().strftime("%H:%M:%S"),
    }

    patients.append(record)
    return record


def mark_patient_seen(queue_no):
    """
    Find a patient by queue number and mark them as Seen.
    Returns True if updated, False if not found.
    """
    for p in patients:
        if p["queue_no"] == queue_no and p["status"] == "Waiting":
            p["status"] = "Seen"
            return True
    return False


def count_waiting_patients():
    """
    Count how many patients are currently waiting.
    Demonstrates iteration over the patient list.
    """
    total = 0
    for p in patients:
        if p["status"] == "Waiting":
            total += 1
    return total


def get_queue_statistics():
    """
    Calculate summary statistics from the current patient list.
    Uses loops to count and sum data for the Dashboard tab.
    """
    total = len(patients)
    waiting = 0
    seen = 0
    emergency = 0
    total_wait = 0

    for p in patients:
        if p["status"] == "Waiting":
            waiting += 1
            total_wait += p["wait_min"]
            if p["priority"] == "Emergency":
                emergency += 1
        else:
            seen += 1

    if waiting > 0:
        avg_wait = total_wait // waiting
    else:
        avg_wait = 0

    return {
        "total": total,
        "waiting": waiting,
        "seen": seen,
        "emergency": emergency,
        "avg_wait": avg_wait,
    }


class ClinicApp:
    """Main application class - builds the GUI and handles user actions."""

    def __init__(self, root):
        self.root = root
        self.root.title(APP_TITLE)
        self.root.geometry("950x680")
        self.root.configure(bg=BG_COLOR)

        self.build_header()
        self.build_notebook()
        self.build_status_bar()

    def build_header(self):
        header = tk.Frame(self.root, bg=HEADER_COLOR, pady=12)
        header.pack(fill="x")

        tk.Label(header, text="Clinic Queue Management System",
                 font=("Arial", 16, "bold"),
                 bg=HEADER_COLOR, fg="white").pack()

        tk.Label(header, text="Sierra Leone  |  SDG 3: Good Health and Well-Being",
                 font=("Arial", 10),
                 bg=HEADER_COLOR, fg="white").pack()

    def build_notebook(self):
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)

        self.tab_register = tk.Frame(self.notebook, bg=BG_COLOR)
        self.tab_queue = tk.Frame(self.notebook, bg=BG_COLOR)
        self.tab_dashboard = tk.Frame(self.notebook, bg=BG_COLOR)

        self.notebook.add(self.tab_register, text="Register Patient")
        self.notebook.add(self.tab_queue, text="Queue List")
        self.notebook.add(self.tab_dashboard, text="Dashboard")

        self.build_register_tab()
        self.build_queue_tab()
        self.build_dashboard_tab()

    def build_register_tab(self):
        frame = self.tab_register

        tk.Label(frame, text="Patient Registration", font=("Arial", 13, "bold"),
                 bg=BG_COLOR, fg=TEXT_COLOR).grid(row=0, column=0, columnspan=2,
                                                  pady=(15, 10))

        tk.Label(frame, text="Full Name:", bg=BG_COLOR, fg=TEXT_COLOR).grid(
            row=1, column=0, sticky="w", padx=20, pady=6)
        self.var_name = tk.StringVar()
        tk.Entry(frame, textvariable=self.var_name, width=30).grid(
            row=1, column=1, padx=10, pady=6)

        tk.Label(frame, text="Age:", bg=BG_COLOR, fg=TEXT_COLOR).grid(
            row=2, column=0, sticky="w", padx=20, pady=6)
        self.var_age = tk.StringVar()
        tk.Entry(frame, textvariable=self.var_age, width=30).grid(
            row=2, column=1, padx=10, pady=6)

        tk.Label(frame, text="Gender:", bg=BG_COLOR, fg=TEXT_COLOR).grid(
            row=3, column=0, sticky="w", padx=20, pady=6)
        self.var_gender = tk.StringVar(value="Male")
        gender_frame = tk.Frame(frame, bg=BG_COLOR)
        gender_frame.grid(row=3, column=1, sticky="w")
        for gender in ("Male", "Female", "Other"):
            tk.Radiobutton(gender_frame, text=gender, variable=self.var_gender,
                           value=gender, bg=BG_COLOR).pack(side="left")

        tk.Label(frame, text="Department:", bg=BG_COLOR, fg=TEXT_COLOR).grid(
            row=4, column=0, sticky="w", padx=20, pady=6)
        self.var_dept = tk.StringVar(value=DEPARTMENTS[0])
        ttk.Combobox(frame, textvariable=self.var_dept, values=DEPARTMENTS,
                    state="readonly", width=28).grid(row=4, column=1, padx=10, pady=6)

        tk.Label(frame, text="Priority:", bg=BG_COLOR, fg=TEXT_COLOR).grid(
            row=5, column=0, sticky="w", padx=20, pady=6)
        self.var_priority = tk.StringVar(value="Normal")
        ttk.Combobox(frame, textvariable=self.var_priority, values=PRIORITY_LEVELS,
                    state="readonly", width=28).grid(row=5, column=1, padx=10, pady=6)

        tk.Label(frame, text="Contact No.:", bg=BG_COLOR, fg=TEXT_COLOR).grid(
            row=6, column=0, sticky="w", padx=20, pady=6)
        self.var_contact = tk.StringVar()
        tk.Entry(frame, textvariable=self.var_contact, width=30).grid(
            row=6, column=1, padx=10, pady=6)

        btn_frame = tk.Frame(frame, bg=BG_COLOR)
        btn_frame.grid(row=7, column=0, columnspan=2, pady=15)

        tk.Button(btn_frame, text="Register", width=10, bg=BUTTON_COLOR, fg="white",
                 command=self.handle_register).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Clear", width=10,
                 command=self.handle_clear).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Exit", width=10, bg="#B33A3A", fg="white",
                 command=self.root.quit).pack(side="left", padx=5)

        tk.Label(frame, text="Registration Receipt:", bg=BG_COLOR, fg=TEXT_COLOR).grid(
            row=8, column=0, columnspan=2, sticky="w", padx=20)

        self.receipt_box = tk.Text(frame, height=9, width=55, state="disabled")
        self.receipt_box.grid(row=9, column=0, columnspan=2, padx=20, pady=10)

    def build_queue_tab(self):
        frame = self.tab_queue

        tk.Label(frame, text="Patient Queue", font=("Arial", 13, "bold"),
                 bg=BG_COLOR, fg=TEXT_COLOR).pack(pady=(15, 10))

        columns = ("Queue No", "Name", "Age", "Department", "Priority",
                  "Wait (min)", "Status")

        self.tree = ttk.Treeview(frame, columns=columns, show="headings", height=14)
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=110, anchor="center")
        self.tree.pack(fill="both", expand=True, padx=15, pady=5)

        btn_frame = tk.Frame(frame, bg=BG_COLOR)
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="Refresh", bg=BUTTON_COLOR, fg="white",
                 command=self.handle_refresh_queue).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Mark as Seen", bg="#2D7D46", fg="white",
                 command=self.handle_mark_seen).pack(side="left", padx=5)

    def build_dashboard_tab(self):
        frame = self.tab_dashboard

        tk.Label(frame, text="Queue Dashboard", font=("Arial", 13, "bold"),
                 bg=BG_COLOR, fg=TEXT_COLOR).pack(pady=(15, 10))

        card_frame = tk.Frame(frame, bg=BG_COLOR)
        card_frame.pack(fill="x", padx=20, pady=5)

        self.stat_labels = {}
        stats_info = [
            ("total", "Total Registered"),
            ("waiting", "Currently Waiting"),
            ("seen", "Patients Seen"),
            ("emergency", "Emergency Cases"),
            ("avg_wait", "Avg Wait (min)"),
        ]

        for key, label in stats_info:
            card = tk.Frame(card_frame, bg="white", relief="solid", bd=1)
            card.pack(side="left", expand=True, fill="both", padx=5)

            tk.Label(card, text=label, font=("Arial", 9),
                     bg="white", fg=TEXT_COLOR).pack(pady=(10, 2))

            value_label = tk.Label(card, text="0", font=("Arial", 20, "bold"),
                                   bg="white", fg=HEADER_COLOR)
            value_label.pack(pady=(0, 10))
            self.stat_labels[key] = value_label

        tk.Label(frame, text="Priority Breakdown:", bg=BG_COLOR, fg=TEXT_COLOR).pack(
            anchor="w", padx=20, pady=(15, 2))

        self.breakdown_box = tk.Text(frame, height=10, width=70, state="disabled")
        self.breakdown_box.pack(padx=20, pady=5)

        tk.Button(frame, text="Refresh Dashboard", bg=BUTTON_COLOR, fg="white",
                 command=self.handle_refresh_dashboard).pack(pady=10)

    def build_status_bar(self):
        self.status_var = tk.StringVar(value="Ready")
        bar = tk.Label(self.root, textvariable=self.status_var,
                       bg="#DDDDDD", anchor="w", padx=10)
        bar.pack(fill="x", side="bottom")

    def handle_register(self):
        """Called when the Register button is clicked."""
        name = self.var_name.get()
        age_str = self.var_age.get()
        contact = self.var_contact.get()
        gender = self.var_gender.get()
        dept = self.var_dept.get()
        priority = self.var_priority.get()

        valid, message = validate_patient_input(name, age_str, contact)
        if not valid:
            messagebox.showerror("Input Error", message)
            return

        record = register_patient(name, int(age_str), gender, dept, priority, contact)

        receipt = (
            "----------------------------------------\n"
            "  CLINIC QUEUE RECEIPT\n"
            "----------------------------------------\n"
            "  Queue Number : " + record["queue_no"] + "\n"
            "  Name         : " + record["name"] + "\n"
            "  Age / Gender : " + str(record["age"]) + " yrs / " + record["gender"] + "\n"
            "  Department   : " + record["department"] + "\n"
            "  Priority     : " + record["priority"] + "\n"
            "  Est. Wait    : " + str(record["wait_min"]) + " minutes\n"
            "  Status       : " + record["status"] + "\n"
            "----------------------------------------\n"
        )

        self.set_text(self.receipt_box, receipt)
        self.set_status("Registered: " + record["name"] + " (" + record["queue_no"] + ")")
        self.handle_refresh_queue()

    def handle_clear(self):
        """Called when the Clear button is clicked."""
        self.var_name.set("")
        self.var_age.set("")
        self.var_contact.set("")
        self.var_gender.set("Male")
        self.var_dept.set(DEPARTMENTS[0])
        self.var_priority.set("Normal")
        self.set_text(self.receipt_box, "")
        self.set_status("Form cleared.")

    def handle_refresh_queue(self):
        """Reload the queue table with current patient data."""
        for row in self.tree.get_children():
            self.tree.delete(row)

        for p in patients:
            self.tree.insert("", "end", values=(
                p["queue_no"], p["name"], p["age"], p["department"],
                p["priority"], p["wait_min"], p["status"]
            ))

        waiting = count_waiting_patients()
        self.set_status(str(waiting) + " patient(s) currently waiting.")

    def handle_mark_seen(self):
        """Mark the selected patient as Seen."""
        selected = self.tree.focus()
        if not selected:
            messagebox.showwarning("No Selection", "Please select a patient first.")
            return

        values = self.tree.item(selected, "values")
        if not values:
            return

        queue_no = values[0]
        if mark_patient_seen(queue_no):
            self.handle_refresh_queue()
            self.handle_refresh_dashboard()
            self.set_status("Patient " + queue_no + " marked as Seen.")
        else:
            messagebox.showinfo("Already Seen", "This patient has already been seen.")

    def handle_refresh_dashboard(self):
        """Update the statistics cards and priority breakdown text."""
        stats = get_queue_statistics()

        for key, label in self.stat_labels.items():
            label.config(text=str(stats[key]))

        lines = []
        lines.append("----------------------------------------\n")
        lines.append("  PRIORITY BREAKDOWN\n")
        lines.append("----------------------------------------\n")

        for priority in PRIORITY_LEVELS:
            waiting_count = 0
            seen_count = 0
            for p in patients:
                if p["priority"] == priority:
                    if p["status"] == "Waiting":
                        waiting_count += 1
                    else:
                        seen_count += 1
            lines.append("  " + priority.ljust(12) +
                         "  Waiting: " + str(waiting_count).rjust(3) +
                         "   Seen: " + str(seen_count).rjust(3) + "\n")

        lines.append("----------------------------------------\n")

        self.set_text(self.breakdown_box, "".join(lines))
        self.set_status("Dashboard updated.")

    @staticmethod
    def set_text(widget, content):
        widget.config(state="normal")
        widget.delete("1.0", "end")
        widget.insert("1.0", content)
        widget.config(state="disabled")

    def set_status(self, message):
        self.status_var.set(message)


def main():
    root = tk.Tk()
    app = ClinicApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()