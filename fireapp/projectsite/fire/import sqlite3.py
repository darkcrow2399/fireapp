import sqlite3
import tkinter as tk
from tkinter import messagebox, ttk

class StudentDBApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Database")
        self.root.geometry("700x450")
        self.root.configure(bg="#f0f4f7")  # Soft background color

        # Set ttk theme
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TButton", font=("Segoe UI", 10), padding=6)
        style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"))
        style.configure("Treeview", font=("Segoe UI", 10), rowheight=24)
        style.configure("TLabel", background="#f0f4f7", font=("Segoe UI", 10))
        style.configure("TEntry", font=("Segoe UI", 10))

        # Connect to database
        self.conn = sqlite3.connect("students.db")
        self.cursor = self.conn.cursor()
        self.create_table()

        # Set up UI
        self.setup_widgets()
        self.load_students()

    def create_table(self):
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS students (
                               id INTEGER PRIMARY KEY AUTOINCREMENT,
                               name TEXT NOT NULL,
                               age INTEGER NOT NULL)""")
        self.conn.commit()

    def setup_widgets(self):
        # === Input Frame ===
        input_frame = ttk.Frame(self.root, padding=10)
        input_frame.pack(fill=tk.X)

        ttk.Label(input_frame, text="Name:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.name_entry = ttk.Entry(input_frame, width=25)
        self.name_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(input_frame, text="Age:").grid(row=0, column=2, padx=5, pady=5, sticky=tk.W)
        self.age_entry = ttk.Entry(input_frame, width=10)
        self.age_entry.grid(row=0, column=3, padx=5, pady=5)

        # === Button Frame ===
        button_frame = ttk.Frame(self.root, padding=10)
        button_frame.pack(fill=tk.X)

        ttk.Button(button_frame, text="Add Student", command=self.add_student).grid(row=0, column=0, padx=5)
        ttk.Button(button_frame, text="Update Student", command=self.update_student).grid(row=0, column=1, padx=5)
        ttk.Button(button_frame, text="Delete Student", command=self.delete_student).grid(row=0, column=2, padx=5)
        ttk.Button(button_frame, text="Refresh", command=self.load_students).grid(row=0, column=3, padx=5)

        # === Treeview Frame ===
        tree_frame = ttk.Frame(self.root, padding=10)
        tree_frame.pack(fill=tk.BOTH, expand=True)

        columns = ("ID", "Name", "Age")
        self.tree = ttk.Treeview(tree_frame, columns=columns, show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Name", text="Name")
        self.tree.heading("Age", text="Age")

        self.tree.column("ID", width=50, anchor=tk.CENTER)
        self.tree.column("Name", width=200)
        self.tree.column("Age", width=50, anchor=tk.CENTER)

        self.tree.bind("<<TreeviewSelect>>", self.on_row_selected)

        vsb = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)
        self.tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")

        tree_frame.columnconfigure(0, weight=1)
        tree_frame.rowconfigure(0, weight=1)

    def add_student(self):
        name = self.name_entry.get().strip()
        age = self.age_entry.get().strip()

        if not name:
            messagebox.showerror("Input Error", "Name cannot be empty.")
            return
        if not age.isdigit():
            messagebox.showerror("Input Error", "Age must be a number.")
            return

        self.cursor.execute("INSERT INTO students (name, age) VALUES (?, ?)", (name, int(age)))
        self.conn.commit()
        messagebox.showinfo("Success", f"Student '{name}' added successfully!")
        self.clear_fields()
        self.load_students()

    def update_student(self):
        selected = self.tree.focus()
        if not selected:
            messagebox.showwarning("No selection", "Please select a student to update.")
            return

        student_id = self.tree.item(selected)["values"][0]
        name = self.name_entry.get().strip()
        age = self.age_entry.get().strip()

        if not name:
            messagebox.showerror("Input Error", "Name cannot be empty.")
            return
        if not age.isdigit():
            messagebox.showerror("Input Error", "Age must be a number.")
            return

        self.cursor.execute("UPDATE students SET name = ?, age = ? WHERE id = ?", (name, int(age), student_id))
        self.conn.commit()
        messagebox.showinfo("Success", "Student updated successfully!")
        self.clear_fields()
        self.load_students()

    def delete_student(self):
        selected = self.tree.focus()
        if not selected:
            messagebox.showwarning("No selection", "Please select a student to delete.")
            return

        student_id = self.tree.item(selected)["values"][0]
        confirm = messagebox.askyesno("Confirm Deletion", f"Delete student with ID {student_id}?")
        if confirm:
            self.cursor.execute("DELETE FROM students WHERE id = ?", (student_id,))
            self.conn.commit()
            messagebox.showinfo("Deleted", "Student deleted successfully.")
            self.clear_fields()
            self.load_students()

    def load_students(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        self.cursor.execute("SELECT * FROM students")
        for student in self.cursor.fetchall():
            self.tree.insert("", tk.END, values=student)

    def on_row_selected(self, event):
        selected = self.tree.focus()
        if selected:
            values = self.tree.item(selected, "values")
            self.name_entry.delete(0, tk.END)
            self.name_entry.insert(0, values[1])
            self.age_entry.delete(0, tk.END)
            self.age_entry.insert(0, values[2])

    def clear_fields(self):
        self.name_entry.delete(0, tk.END)
        self.age_entry.delete(0, tk.END)

def main():
    root = tk.Tk()
    app = StudentDBApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()