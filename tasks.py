import subprocess
import yaml
import sys
import os

def load_tasks(file_path="tasks.yml"):
    """Load tasks from the YAML file."""
    if not os.path.exists(file_path):
        print(f"Error: {file_path} not found!")
        sys.exit(1)
    with open(file_path, "r") as f:
        return yaml.safe_load(f)

def execute_task(task_name, tasks):
    """Execute the command associated with a task."""
    if task_name not in tasks["tasks"]:
        print(f"Task '{task_name}' not found.")
        return
    task = tasks["tasks"][task_name]
    command = task["command"]
    print(f"Running task: {task_name} -> {command}")
    subprocess.run(command, shell=True, check=True)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python tasks.py <task-name>")
        sys.exit(1)

    task_name = sys.argv[1]
    tasks = load_tasks()  # Ensure this loads the tasks.yml
    execute_task(task_name, tasks)


