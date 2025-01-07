import json
import os

class Task:
    def __init__(self, title, description, status='Pending'):
        self.title = title
        self.description = description
        self.status = status

    def __str__(self):
        return f"Title: {self.title}\nDescription: {self.description}\nStatus: {self.status}"

    def to_dict(self):
        return {
            'title': self.title,
            'description': self.description,
            'status': self.status
        }

class TaskManager:
    def __init__(self, filename="tasks.json"):
        self.filename = filename
        self.tasks = self.load_tasks()

    def load_tasks(self):
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as file:
                return json.load(file)
        else:
            return []

    def save_tasks(self):
        with open(self.filename, 'w') as file:
            json.dump([task.to_dict() for task in self.tasks], file, indent=4)

    def add_task(self, title, description):
        task = Task(title, description)
        self.tasks.append(task)
        self.save_tasks()
        print("Task added successfully!")

    def view_tasks(self):
        if not self.tasks:
            print("No tasks found.")
            return
        for i, task in enumerate(self.tasks, 1):
            print(f"Task #{i}")
            print(task)
            print("-" * 20)

    def update_task(self, task_index, new_title=None, new_description=None, new_status=None):
        try:
            task = self.tasks[task_index]
            if new_title:
                task.title = new_title
            if new_description:
                task.description = new_description
            if new_status:
                task.status = new_status
            self.save_tasks()
            print("Task updated successfully!")
        except IndexError:
            print("Invalid task index.")

    def delete_task(self, task_index):
        try:
            del self.tasks[task_index]
            self.save_tasks()
            print("Task deleted successfully!")
        except IndexError:
            print("Invalid task index.")

def main():
    manager = TaskManager()

    while True:
        print("\nTask Manager Menu:")
        print("1. Add Task")
        print("2. View Tasks")
        print("3. Update Task")
        print("4. Delete Task")
        print("5. Exit")

        choice = input("Choose an option: ")

        if choice == '1':
            title = input("Enter task title: ")
            description = input("Enter task description: ")
            manager.add_task(title, description)
        elif choice == '2':
            manager.view_tasks()
        elif choice == '3':
            manager.view_tasks()
            try:
                task_index = int(input("Enter task number to update: ")) - 1
                new_title = input("Enter new title (or leave blank to keep current): ")
                new_description = input("Enter new description (or leave blank to keep current): ")
                new_status = input("Enter new status (or leave blank to keep current): ")
                manager.update_task(task_index, new_title, new_description, new_status)
            except ValueError:
                print("Invalid input.")
        elif choice == '4':
            manager.view_tasks()
            try:
                task_index = int(input("Enter task number to delete: ")) - 1
                manager.delete_task(task_index)
            except ValueError:
                print("Invalid input.")
        elif choice == '5':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == '__main__':
    main()
