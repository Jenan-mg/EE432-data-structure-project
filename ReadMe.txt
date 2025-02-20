# To-Do List Application

## Project Overview
This is a GUI-based To-Do List application built using Python and Tkinter. The application allows users to add, delete, search, and manage tasks with different priority levels and completion statuses. It utilizes a combination of data structures such as linked lists, hash tables, and binary search trees for efficient task management.

## Features
- **Task Management**: Add, delete, and search tasks.
- **Priority Sorting**: Organizes tasks by priority (High, Medium, Low) using a Binary Search Tree.
- **Task Completion Tracking**: Mark tasks as completed or pending.
- **GUI with Tkinter**: User-friendly interface with styled widgets.
- **Hash Table Search**: Enables efficient searching of tasks by description.
- **Linked List for Storage**: Maintains task order dynamically.

## Technologies Used
- **Python** (Programming Language)
- **Tkinter** (GUI Framework)
- **Pillow** (Image Processing for Icons & Background)
- **Data Structures**: Linked List, Hash Table, Binary Search Tree

## Installation
### Prerequisites
Ensure you have Python installed. If not, download and install it from [python.org](https://www.python.org/).

### Required Libraries
Install the necessary dependencies using pip:
```sh
pip install pillow
```

### Running the Application
1. Clone this repository:
   ```sh
   git clone https://github.com/yourusername/todo-app.git
   ```
2. Navigate to the project folder:
   ```sh
   cd todo-app
   ```
3. Run the application:
   ```sh
   python main.py
   ```

## Usage
- Enter a task description and select a priority level.
- Click "Add" to add the task.
- Click "Delete" to remove the selected task.
- Use "Search" to find tasks by description.
- Use "Show All" to list all tasks sorted by priority.
- Toggle task completion with the "Toggle Completion" button.

## File Structure
```
📂 todo-app
 ├── 📜 To-Do_list_project.py            # Main application file
 ├── 📜 README.md          # Project documentation
 ├── 📜 requirements.txt   # List of dependencies
 ├── 📂 assets             # Icons and background images
 │    ├── 📜 background.jpg
 │    ├── 📜 add.png
 │    ├── 📜 delete.png
 │    ├── 📜 search.png
 │    ├── 📜 tasks.png
```

## Troubleshooting
- If images/icons do not load, ensure that the `assets` folder is in the correct directory.
- If you encounter any missing module errors, reinstall dependencies using:
  ```sh
  pip install -r requirements.txt
  ```

## Contribution
Feel free to fork the repository and submit pull requests for enhancements and bug fixes.


