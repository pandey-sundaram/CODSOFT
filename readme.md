# Classic To-Do List Application

A comprehensive, classic-themed GUI To-Do List application built with Python's `tkinter` and `ttk` modules. This application provides a robust and user-friendly interface for managing daily tasks with detailed entries and intuitive controls.

## Features

-   **Detailed Task Creation:** Add tasks with a Topic, Description, Date, Time, and Priority (High, Medium, Low).
-   **Interactive Date & Time Selection:**
    -   Click the **"📅"** button to open a pop-up calendar for easy date selection.
    -   Use spinboxes and a dropdown menu to select the exact time in HH:MM AM/PM format.
-   **Structured Task View:** All tasks are displayed in a clean, sortable table, providing a clear overview.
-   **Priority Coloring:** Tasks are automatically color-coded based on their priority level (High, Medium, Low) for quick visual identification.
-   **Powerful Search:** Use the search bar to instantly filter tasks by topic or description. Click "Clear Search" to view the full list again.
-   **Easy Updates:**
    1.  Click any task in the table to load its details into the input fields.
    2.  Modify the information as needed.
    3.  Click **"Update Task"** to save your changes.
-   **Safe Deletion:** Select a task and click **"Delete Task"**. A confirmation dialog prevents accidental deletions.
-   **Track Completion:** Select a task and click **"Toggle Complete"**. The task's status will update, and its text will be greyed out and struck through for clear tracking.
-   **Persistent Storage:** Your entire to-do list, including all details and completion status, is automatically saved to a `tasks.json` file when the application is closed and reloaded on the next launch.

## Requirements

-   Python 3.x

No external libraries are needed, as the application uses only the `tkinter`, `ttk`, `json`, `os`, and `datetime` modules from the Python standard library.

## How to Run the Application

1.  **Save the Code:** Ensure the `todo_app.py` file is saved in its own directory.
2.  **Navigate to the Directory:** Open your computer's terminal or command prompt. Use the `cd` command to navigate to the folder where you saved the file.
    ```sh
    cd path/to/your/project_folder
    ```
3.  **Execute the Script:** Run the application using the following command:
    ```sh
    python todo_app.py
    ```
4.  The To-Do List window will appear. A `tasks.json` file will be automatically created in the same directory to store your tasks as you add them.
