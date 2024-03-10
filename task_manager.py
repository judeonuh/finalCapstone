"""
This python program provides functionality for task management.
Functionalities include: user registration, task assignment, adding tasks,
viewing tasks, editing tasks, generating task reports, and displaying statistics.
"""

# Notes:
# 1. Use the following username and password to access the admin rights
# username: admin
# password: password
# 2. Ensure you open the whole folder for the task manager in VS Code
# otherwise the program will look in your root directory for the text
# files.

# =====Importing Libraries=====
import os
from datetime import datetime, date


class colors:
    """
    This class comprises a selection of colors and their ASCII codes
    """
    reset = '\033[0m'
    red = '\033[91m'
    green = '\033[92m'
    yellow = '\033[93m'
    blue = '\033[94m'
    purple = '\033[95m'
    cyan = '\033[96m'


def reg_user():
    """
    This function registers a new user by prompting for a unique username and password.
    User information is checked for duplicates, and stores the credentials in a file.
    """

    # Prompt user for new username and check for duplicates
    while True:
        new_username = input("\nNew Username: ")
        if new_username not in username_password:
            break
        print(colors.red)
        print(f"{new_username} is already in use! Please enter a different username.")
        print(colors.reset)

    # Request for new passport and validate this
    while True:
        new_password = input("New Password: ")
        confirm_password = input("Confirm Password: ")
        if new_password == confirm_password:
            print(f"{colors.green}\nSuccess! New user added! {colors.reset}")

            # Add new user credentials to user dictionary and new text file
            username_password[new_username] = new_password
            with open("user.txt", "w", encoding="utf-8") as output_file:
                user_data = []
                for key, value in username_password.items():
                    user_data.append(f"{key};{value}")
                output_file.write("\n".join(user_data))

            break

        print(f"{colors.red}\nSorry! Passwords do not match.{colors.reset}")


def add_task():
    """
    This function prompts the user to enter new task details.
    Entry is validated and added to a list and a text file.
    """

    # Request username of task owner and check if user exists.
    while True:
        task_user = input("Enter Username this task is assigned to: ")
        if task_user in username_password:
            break
        print(f"\n{colors.red}User does not exist. Please enter a valid username.")
        print(f"{colors.reset}")

    # Collect task details
    task_title = input("Enter task title: ")
    task_description = input("Enter brief task description: ")
    curr_date = date.today()

    # Request task due date and check that it is in correct format
    while True:
        try:
            task_due_date = input("Due date of task (YYYY-MM-DD): ")
            due_date_time = datetime.strptime(task_due_date,
                                              DATETIME_STRING_FORMAT)
            break

        except ValueError:
            print(f"\n{colors.red}Invalid date.")
            print("Please enter valid date in the format specified")
            print(colors.reset)

    # Create a dictionary with task details, add to task list and a text file
    new_task = {
        "Username": task_user,
        "Task title": task_title,
        "Task description": task_description,
        "Due date": due_date_time,
        "Assigned date": curr_date,
        "completed": False
    }
    task_list.append(new_task)
    update_task_file()
    print(f"\n{colors.green}Task successfully added.{colors.reset}")


def view_all():
    """
    This function prints all tasks with a unique identier 
    and a message if there are no tasks.
    """
    # Print all tasks with a unique identifier, and return error message if task list is empty
    for task_id, task in enumerate(task_list):
        print_task(task_id, task)
    if not task_list:
        print(f"\n{colors.red}Sorry! There are currently no tasks logged.{colors.reset}")


def view_mine():
    """
    This function allows a user to view and interact with tasks assigned to them.
    They can edit and mark tasks as complete if they are not already completed.
    """
    # Print all user's task, or return appropriate message if they have no assigned task.
    while True:
        my_task_ids = []
        for task_id, task in enumerate(task_list):
            if task["Username"] == curr_user:
                print_task(task_id, task)
                my_task_ids.append(task_id)

        if not my_task_ids:
            print(f"\n{colors.red}No tasks have been assigned to you.{colors.reset}")
            break

        # Allow user to interact with, and/or manipulate their task
        user_task_choice = input("""\nTo select a task, enter the task ID.
Or enter '-1' to return to the main menu.
: """)

        if user_task_choice.isnumeric() and int(user_task_choice) in my_task_ids:
            print_task(user_task_choice, task_list[int(user_task_choice)])
            while True:
                user_choice = input("""\nSelect one of the following options:
c - To mark as complete
e - To Edit task
t - To return to previous menu
What would you like to do? : """).lower().strip()

                if user_choice == "c":

                    # Mark task as complete and update task file
                    task_list[int(user_task_choice)]["completed"] = True
                    update_task_file()
                    print("Task marked as complete.")
                    break

                # Call edit function and update task file when completed
                if user_choice == "e" and not \
                        task_list[int(user_task_choice)]["completed"]:
                    edit_task(task_list[int(user_task_choice)])
                    update_task_file()
                    break

                # If task is completed, return appropriate message
                if user_choice == "e":
                    print(f"\n{colors.green}Task completed - unavailable for editing.")
                    print(colors.reset)
                    break

                if user_choice == "t":
                    break

                print(f"\n{colors.red}Invalid input! Please try again.\n{colors.reset}")

        elif user_task_choice == "-1":
            break

        else:
            print(f"\n{colors.red}Invalid input! Please try again.\n{colors.reset}")


def print_task(task_id, task: dict):
    """
    This function takes a task ID and a dictionary representing a task, 
    then prints formatted information about the task.
    """
    # Build a string which displays all the task information
    disp_str = f"Task: \t\t {task["Task title"]}\n"
    disp_str += f"Assigned to: \t {task["Username"]}\n"
    disp_str += ("Date Assigned: \t "
                 f"{task["Assigned date"].strftime(DATETIME_STRING_FORMAT)}\n")
    disp_str += ("Due Date: \t "
                 f"{task["Due date"].strftime(DATETIME_STRING_FORMAT)}\n")
    disp_str += f"Task Description: \n{task["Task description"]}"

    # Print this information along with corresponding task id
    print("_ " * 30)
    print(f"\n{colors.yellow}Task ID: {task_id}\n" + disp_str)
    print(colors.reset)
    print("_ " * 30)


def edit_task(task: dict):
    """
    This function allows the user to manipulate tasks stored in a dictionary.
    User can either reassign a task to another user or edit the due date of the task.
    """
    while True:
        # Prompt user for input
        edit_choice = input("""\nEDIT TASK MENU:
r - Reassign task
e - Edit due date
What would you like to do?: """).lower()

        if edit_choice == "r":
            # Reassign to new username and update dictionary.
            while True:
                new_user = input("\nEnter username you want to reassign task to: ")
                if new_user in username_password:
                    task["Username"] = new_user
                    print(f"\n{colors.green}Task reassigned to {new_user}.")
                    print(colors.reset)
                    break

                print(f"{colors.red}\n{new_user} does not exist! Please try again.")
                print(colors.reset)
            break

        if edit_choice == "e":
            # Request new due date and ensure it is in correct format
            while True:
                try:
                    new_date = input("\nEnter new task due date (YYYY-MM-DD): ")
                    new_date_time = \
                        datetime.strptime(new_date, DATETIME_STRING_FORMAT)
                    break

                except ValueError:
                    print(f"\n{colors.red}Invalid datetime format."
                          f"Please use the format specified.{colors.reset}")

            # Update dictionary for this task
            task["Due date"] = new_date_time
            print(f"{colors.green}\nDue date successfully updated.{colors.reset}")
            break

        print(f"\n{colors.red}Invalid input - please try again.{colors.reset}")


def update_task_file():
    """
    This function writes task information to a text file in a specific format.
    For each task, attributes lists containing information for the text file
    are created.
    """
    with open("tasks.txt", "w", encoding="utf-8") as file:

        # For each task, create an attributes list containing
        # information for the .txt file
        task_list_to_write = []
        for task in task_list:
            str_attrs = [
                task["Username"],
                task["Task title"],
                task["Task description"],
                task["Due date"].strftime(DATETIME_STRING_FORMAT),
                task["Assigned date"].strftime(DATETIME_STRING_FORMAT),
                "Yes" if task["completed"] else "No"
            ]

            # Join the attributes with semi-colons and add this string
            # to a new list
            task_list_to_write.append(";".join(str_attrs))

        # Write the string for each task on a separate line in the .txt
        # file
        file.write("\n".join(task_list_to_write))


def gen_task_overview():
    """
    This function generates a summary of task completion status
    This is then written to a text file.
    """
    # Declare variables and initialize to 0
    completed_tasks = 0
    uncompleted_tasks = 0
    overdue_tasks = 0

    # For each task, update variables accordingly
    for task in task_list:
        if task["completed"]:
            completed_tasks += 1
        elif datetime.today() > task["Due date"]:
            uncompleted_tasks += 1
            overdue_tasks += 1
        else:
            uncompleted_tasks += 1

    # Calculate percentages for each variable
    total_tasks = len(task_list)
    try:
        percent_complete = (completed_tasks / total_tasks) * 100
        percent_incomplete = (uncompleted_tasks / total_tasks) * 100
        percent_overdue = (overdue_tasks / total_tasks) * 100

    # If there are no tasks at all, set all percentages to 0
    except ZeroDivisionError:
        percent_complete = percent_incomplete = percent_overdue = 0

    # Write information to a text file
    date_time = datetime.today().strftime(DATETIME_STRING_FORMAT + " %H:%M")

    with open("task_overview.txt", "w", encoding="utf-8") as report_file:
        report_file.write("TASK OVERVIEW\n" + date_time + "\n" + "_" * 13 +
                          "\n")
        report_file.write(f"\nTotal number of tasks = {total_tasks}")
        report_file.write("\nTotal number of completed tasks = "
                          f"{completed_tasks} ({percent_complete:.1f}%)")
        report_file.write("\nTotal number of uncompleted tasks = "
                          f"{uncompleted_tasks} ({percent_incomplete:.1f}%)")
        report_file.write(f"\nTotal number of overdue tasks = {overdue_tasks} "
                          f"({percent_overdue:.1f}%)")


def gen_user_overview():
    """
    This function generates an overview of the tasks assigned to each user.
    Information displayed include completion status, overdue tasks, etc.
    This is then written to a text file.
    """

    # Retrieve the total number of users and tasks
    # Write the general information to a text file
    total_users = len(username_password)
    total_tasks = len(task_list)

    date_time = datetime.today().strftime(DATETIME_STRING_FORMAT + " %H:%M")

    with open("user_overview.txt", "w", encoding="utf-8") as report_file:
        report_file.write("USER OVERVIEW\n" + date_time + "\n" + "_" * 13 +
                          "\n")
        report_file.write(f"\nTotal number of users = {total_users}")
        report_file.write(f"\nTotal number of tasks = {total_tasks}")

        # Perform calculations for each user
        for current_user in sorted(username_password):

            # Create a list of tasks assigned to the current user in the
            # loop
            user_task_list = [task for task in task_list if task["Username"]
                              == current_user]

            # Retrieve total number of tasks for that user
            user_total_tasks = len(user_task_list)

            # Set variables to 0
            completed_tasks = 0
            uncompleted_tasks = 0
            overdue_tasks = 0

            # For each task, update variables accordingly
            for user_task in user_task_list:
                if user_task["completed"]:
                    completed_tasks += 1
                elif datetime.today() > user_task["Due date"]:
                    uncompleted_tasks += 1
                    overdue_tasks += 1
                else:
                    uncompleted_tasks += 1

            # Calculate percentages for each variable
            try:
                pc_assigned = (user_total_tasks / total_tasks) * 100
                percent_completed = (completed_tasks / user_total_tasks) * 100
                pc_uncompleted = (uncompleted_tasks / user_total_tasks) * 100
                percent_overdue = (overdue_tasks / user_total_tasks) * 100

            # If user has no tasks assigned, set all percentages to 0
            except ZeroDivisionError:
                pc_assigned = percent_completed = pc_uncompleted = percent_overdue = 0

            # Write specific information for current user in loop to
            # .txt file
            report_file.write(f"\n\n> {current_user}")
            report_file.write("\nNumber of tasks assigned: "
                              f"{user_total_tasks} ({pc_assigned:.1f}%)")
            report_file.write("\nNumber of assigned tasks completed: "
                              f"{completed_tasks} ({percent_completed:.1f}%)")
            report_file.write("\nNumber of assigned tasks uncompleted: "
                              f"{uncompleted_tasks} ({pc_uncompleted:.1f}%)")
            report_file.write("\nNumber of assigned tasks overdue: "
                              f"{overdue_tasks} ({percent_overdue:.1f}%)")


def create_taskfile():
    """
    The function `create_taskfile` creates a new file named "tasks.txt" 
    if it does not already exist.
    """
    if not os.path.exists("tasks.txt"):
        with open("tasks.txt", "w", encoding="utf-8"):
            pass


def create_userfile():
    """
    The function `create_userfile` creates a text file named "user.txt" 
    with default user credentials if the file does not already exist.
    """
    if not os.path.exists("user.txt"):
        with open("user.txt", "w", encoding="utf-8") as default_file:
            default_file.write("admin;password")


def count_lines(file):
    """
    The function `count_lines` takes a file as input and returns the 
    number of non-empty lines in the file.
    
    :param file: The `count_lines` function you provided takes a file 
    object as input and counts the number of non-empty lines in the 
    file. The function iterates over each line in the file and 
    increments the `num_lines` counter if the line is not empty (i.e., 
    not equal to "\n")
    :return: The function `count_lines` returns the number of non-empty
    lines in the file.
    """
    num_lines = 0
    for line in file:
        if line != "\n":
            num_lines += 1
    return num_lines


def display_stats():
    """
    The `display_stats` function reads the number of users and tasks 
    from text files and displays the statistics.
    """
    # Create tasks.txt and user.txt if they don't exist
    create_userfile()
    create_taskfile()

    # Count number of users and tasks listed in the .txt files
    with open("user.txt", "r", encoding="utf-8") as users:
        num_users = count_lines(users)

    with open("tasks.txt", "r", encoding="utf-8") as tasks:
        num_tasks = count_lines(tasks)

    # Display statistics
    print("\n-----------------------------------")
    print(f"Number of users: \t\t {num_users}")
    print(f"Number of tasks: \t\t {num_tasks}")
    print("-----------------------------------")


DATETIME_STRING_FORMAT = "%Y-%m-%d"

# Create tasks.txt if it doesn't exist
create_taskfile()

# Retrieve task information from the .txt file
with open("tasks.txt", 'r', encoding="utf-8") as task_file:
    task_data = task_file.read().split("\n")
    task_data = [t for t in task_data if t != ""]

task_list = []

# Reorganise each task string in the task data list into a dictionary
for t_str in task_data:
    curr_t = {}

    # Split by semicolon and manually add each component
    task_components = t_str.split(";")
    curr_t["Username"] = task_components[0]
    curr_t["Task title"] = task_components[1]
    curr_t["Task description"] = task_components[2]
    curr_t["Due date"] = datetime.strptime(task_components[3],
                                           DATETIME_STRING_FORMAT)
    curr_t["Assigned date"] = datetime.strptime(task_components[4],
                                                DATETIME_STRING_FORMAT)
    curr_t["completed"] = task_components[5] == "Yes"

    # Add dictionary to a task list
    task_list.append(curr_t)

# =====Login Section=====
# This code reads usernames and password from the user.txt file to allow
# a user to login

# If no user.txt file, write one with a default account
create_userfile()

# Read in user data
with open("user.txt", 'r', encoding="utf-8") as user_file:
    login_data = user_file.read().split("\n")

# Convert to a dictionary
username_password = {}
for user in login_data:
    username, password = user.split(';')
    username_password[username] = password

# Request login information from user
LOGGED_IN = False
while not LOGGED_IN:
    print("\nLOGIN")
    curr_user = input("Username: ")
    curr_pass = input("Password: ")

    # Check that username exists
    if curr_user not in username_password:
        print(f"\n{colors.red}User does not exist.{colors.reset}")
        continue

    # Check that password matches
    if username_password[curr_user] != curr_pass:
        print(f"\n{colors.red}Wrong password{colors.reset}")
        continue

    # If checks pass, exit loop
    print(f"\n{colors.green}Login Successful!{colors.reset}")
    LOGGED_IN = True

while True:
    # Present the menu to the user and request selection
    menu = input('''\nTASK MANAGER MENU
r - Register a user
a - Add a task
va - View all tasks
vm - View my tasks
gr - Generate reports
ds - Display statistics
e - Exit
\nWhat would you like to do?: ''').lower().strip()

    if menu == "r":
        reg_user()

    elif menu == "a":
        add_task()

    elif menu == "va":
        view_all()

    elif menu == "vm":
        view_mine()

    elif menu == "gr":
        gen_task_overview()
        gen_user_overview()
        print(f"\n{colors.green}Reports generated in local directory.")
        print(colors.reset)

    elif menu == "ds":
        if curr_user == "admin":
            display_stats()

        else:
            print(f"\n{colors.red}You must be an administrator to access statistics.")
            print(colors.reset)

    elif menu == "e":
        print(f"\n{colors.cyan}Goodbye!\n{colors.reset}")
        break

    else:
        print(f"{colors.red}\nInvalid input - please try again.")
        print(colors.reset)
