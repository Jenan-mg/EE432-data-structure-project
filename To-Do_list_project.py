import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk

# Task class to represent a task
class Task:
    def __init__(self, description, priority, status=False):
        self.description = description
        self.priority = priority  # Priority is now a string: "High", "Medium", or "Low"
        self.status = status

    def __str__(self):
        status = "✔" if self.status else "✖"
        return f"{self.description} [Priority: {self.priority}, Completed: {status}]"

# Node class for linked list
class Node:
    def __init__(self, task):
        self.task = task
        self.next = None

# Linked List to store tasks
class LinkedList:
    def __init__(self):
        self.head = None

    def add_task(self, task):
        new_node = Node(task)
        if not self.head:
            self.head = new_node
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = new_node

    def delete_task(self, index):
        if not self.head:
            raise IndexError("Linked list is empty")
        if index == 0:
            self.head = self.head.next
        else:
            current = self.head
            for _ in range(index - 1):
                if not current.next:
                    raise IndexError("Index out of range")
                current = current.next
            if not current.next:
                raise IndexError("Index out of range")
            current.next = current.next.next

    def get_all_tasks(self):
        tasks = []
        current = self.head
        while current:
            tasks.append(current.task)
            current = current.next
        return tasks

# Hash Table for efficient searching by description
class HashTable:
    def __init__(self):
        self.size = 10
        self.table = [[] for _ in range(self.size)]

    def _hash(self, key):
        return hash(key) % self.size

    def insert(self, task):
        key = task.description
        index = self._hash(key)
        self.table[index].append(task)

    def search(self, description):
        index = self._hash(description)
        for task in self.table[index]:
            if task.description.lower() == description.lower():
                return task
        return None

    def remove(self, task):
        index = self._hash(task.description)
        self.table[index] = [t for t in self.table[index] if t.description != task.description]

# Binary Search Tree for managing tasks by priority
class BSTNode:
    def __init__(self, task):
        self.task = task
        self.left = None
        self.right = None

class BinarySearchTree:
    def __init__(self):
        self.root = None

    def insert(self, task):
        if not self.root:
            self.root = BSTNode(task)
        else:
            self._insert(self.root, task)

    def _insert(self, node, task):
        # Priority comparison: High > Medium > Low
        if self._get_priority_value(task.priority) < self._get_priority_value(node.task.priority):
            if node.left is None:
                node.left = BSTNode(task)
            else:
                self._insert(node.left, task)
        else:
            if node.right is None:
                node.right = BSTNode(task)
            else:
                self._insert(node.right, task)

    def _get_priority_value(self, priority):
        # Convert priority string to a numerical value for sorting
        priority_map = {"Low": 1, "Medium": 2, "High": 3}
        return priority_map.get(priority, 0)

    def delete(self, task):
        self.root = self._delete(self.root, task)

    def _delete(self, node, task):
        if node is None:
            return node

        if self._get_priority_value(task.priority) < self._get_priority_value(node.task.priority):
            node.left = self._delete(node.left, task)
        elif self._get_priority_value(task.priority) > self._get_priority_value(node.task.priority):
            node.right = self._delete(node.right, task)
        else:
            if node.task.description == task.description:  # Ensure the correct task is deleted
                if node.left is None:
                    return node.right
                elif node.right is None:
                    return node.left

                temp = self._min_value_node(node.right)
                node.task = temp.task
                node.right = self._delete(node.right, temp.task)
            else:
                node.right = self._delete(node.right, task)  # Continue searching

        return node

    def _min_value_node(self, node):
        current = node
        while current.left is not None:
            current = current.left
        return current

    def in_order_traversal(self, node, result, show_completed):
        if node:
            self.in_order_traversal(node.left, result, show_completed)
            if show_completed or not node.task.status:
                result.append(node.task)
            self.in_order_traversal(node.right, result, show_completed)

    def get_all_tasks_sorted_by_priority(self, show_completed=True):
        result = []
        self.in_order_traversal(self.root, result, show_completed)
        return result

    def update_task_status(self, description, status):
        # Update task status in the BST
        stack = []
        current = self.root
        while stack or current:
            if current:
                stack.append(current)
                current = current.left
            else:
                current = stack.pop()
                if current.task.description == description:
                    current.task.status = status
                    return
                current = current.right

# Main application class
class ToDoAppGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("To-Do List App")
        self.root.geometry("600x600")

        # Initialize data structures
        self.linked_list = LinkedList()
        self.hash_table = HashTable()
        self.bst = BinarySearchTree()

        # Load background image
        try:
            self.bg_image = Image.open("background.jpg")
            self.bg_image = self.bg_image.resize((600, 600), Image.LANCZOS)
            self.bg_photo = ImageTk.PhotoImage(self.bg_image)
        except FileNotFoundError:
            messagebox.showerror("Error", "Background image not found. Please ensure 'background.jpg' is in the correct directory.")
            self.bg_photo = None

        if self.bg_photo:
            self.bg_label = tk.Label(self.root, image=self.bg_photo)
            self.bg_label.place(relwidth=1, relheight=1)

        # Load icons
        self.load_icons()

        # Create GUI widgets
        self.create_widgets()

    def load_icons(self):
        try:
            self.add_icon = ImageTk.PhotoImage(Image.open("add.png").resize((20, 20)))
            self.delete_icon = ImageTk.PhotoImage(Image.open("delete.png").resize((20, 20)))
            self.search_icon = ImageTk.PhotoImage(Image.open("search.png").resize((20, 20)))
            self.show_icon = ImageTk.PhotoImage(Image.open("tasks.png").resize((20, 20)))
        except FileNotFoundError:
            messagebox.showerror("Error", "Icon files not found. Please ensure all icon files are in the correct directory.")

    def create_widgets(self):
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.place(relx=0.5, rely=0.5, anchor="center")

        title_label = ttk.Label(main_frame, text="My To-Do List", font=("Helvetica", 20, "bold"), foreground="#ff6f61")
        title_label.pack(pady=10)

        ttk.Label(main_frame, text="Task Description:", font=("Helvetica", 12), foreground="#6b5b95").pack(pady=5)
        self.description_entry = ttk.Entry(main_frame, width=40, font=("Helvetica", 12))
        self.description_entry.pack(pady=5)

        ttk.Label(main_frame, text="Priority (High/Medium/Low):", font=("Helvetica", 12), foreground="#6b5b95").pack(pady=5)
        self.priority_entry = ttk.Entry(main_frame, width=15, font=("Helvetica", 12))
        self.priority_entry.pack(pady=5)

        # Filter by completion status
        self.show_completed_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(main_frame, text="Show Completed Tasks", variable=self.show_completed_var, command=self.refresh_listbox).pack(pady=5)

        # Sorting options
        ttk.Label(main_frame, text="Sort By:", font=("Helvetica", 12), foreground="#6b5b95").pack(pady=5)
        self.sort_var = tk.StringVar(value="Priority")
        self.sort_options = ttk.Combobox(main_frame, textvariable=self.sort_var, values=["Priority", "Completion Status"], state="readonly")
        self.sort_options.pack(pady=5)
        self.sort_options.bind("<<ComboboxSelected>>", self.refresh_listbox)

        button_frame = ttk.Frame(main_frame)
        button_frame.pack(pady=10)

        self.style = ttk.Style()
        self.style.configure("Pink.TButton",
                             font=("Helvetica", 12),
                             foreground="#ffb6c1",
                             background="#ff6f61",
                             borderwidth=0,
                             padding=10)
        self.style.map("Pink.TButton",
                       background=[("active", "#ff8c7f")],
                       foreground=[("active", "#ffb6c1")])

        ttk.Button(button_frame, text="Add", image=self.add_icon, compound=tk.LEFT, command=self.add_task, style="Pink.TButton").pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Delete", image=self.delete_icon, compound=tk.LEFT, command=self.delete_task, style="Pink.TButton").pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Search", image=self.search_icon, compound=tk.LEFT, command=self.search_task, style="Pink.TButton").pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Show All", image=self.show_icon, compound=tk.LEFT, command=self.display_tasks, style="Pink.TButton").pack(side=tk.LEFT, padx=5)

        self.task_listbox = tk.Listbox(main_frame, width=60, height=10, font=("Helvetica", 12), bg="#ffffff", fg="#6b5b95")
        self.task_listbox.pack(pady=10)

        ttk.Button(main_frame, text="Toggle Completion", command=self.toggle_completion, style="Pink.TButton").pack(pady=5)

    def add_task(self):
        description = self.description_entry.get()
        priority = self.priority_entry.get().capitalize()
        if description and priority in ["High", "Medium", "Low"]:
            task = Task(description, priority)
            self.linked_list.add_task(task)
            self.hash_table.insert(task)
            self.bst.insert(task)
            self.refresh_listbox()
            self.description_entry.delete(0, tk.END)
            self.priority_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Input Error", "Please enter a valid description and priority (High/Medium/Low).")

    def delete_task(self):
        try:
            selected = self.task_listbox.curselection()[0]
            task = self.linked_list.get_all_tasks()[selected]
            self.linked_list.delete_task(selected)
            self.hash_table.remove(task)
            self.bst.delete(task)  # Pass the task object to delete
            self.refresh_listbox()
        except IndexError:
            messagebox.showwarning("Selection Error", "Please select a task to delete.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def search_task(self):
        description = self.description_entry.get()
        if not description:
            messagebox.showwarning("Input Error", "Please enter a task description to search.")
            return
        task = self.hash_table.search(description)
        if task:
            # Highlight the found task in the listbox
            tasks = self.bst.get_all_tasks_sorted_by_priority(show_completed=self.show_completed_var.get())
            for i, t in enumerate(tasks):
                if t.description == task.description:
                    self.task_listbox.selection_clear(0, tk.END)
                    self.task_listbox.selection_set(i)
                    self.task_listbox.see(i)
                    break
            messagebox.showinfo("Search Results", str(task))
        else:
            messagebox.showinfo("Search Results", "No matching tasks found.")

    def display_tasks(self):
        tasks = self.bst.get_all_tasks_sorted_by_priority(show_completed=self.show_completed_var.get())
        if tasks:
            messagebox.showinfo("All Tasks", "\n".join(str(task) for task in tasks))
        else:
            messagebox.showinfo("All Tasks", "No tasks available.")

    def toggle_completion(self):
        try:
            selected = self.task_listbox.curselection()[0]
            task = self.linked_list.get_all_tasks()[selected]
            task.status = not task.status
            self.bst.update_task_status(task.description, task.status)
            self.refresh_listbox()
        except IndexError:
            messagebox.showwarning("Selection Error", "Please select a task to toggle completion status.")

    def refresh_listbox(self, event=None):
        self.task_listbox.delete(0, tk.END)
        tasks = self.bst.get_all_tasks_sorted_by_priority(show_completed=self.show_completed_var.get())
        if self.sort_var.get() == "Completion Status":
            tasks.sort(key=lambda x: x.status)
        for task in tasks:
            self.task_listbox.insert(tk.END, str(task))


if __name__ == "__main__":
    root = tk.Tk()
    app = ToDoAppGUI(root)
    root.mainloop()