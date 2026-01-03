import json
import os
from datetime import datetime

class TodoList:
    """A class to manage to-do list tasks"""
    
    def __init__(self, filename='tasks.json'):
        """Initialize the to-do list with a filename"""
        self.filename = filename
        self.tasks = self.load_tasks()
    
    def load_tasks(self):
        """Load tasks from JSON file"""
        try:
            if os.path.exists(self.filename):
                with open(self.filename, 'r', encoding='utf-8') as file:
                    return json.load(file)
            else:
                return []
        except json.JSONDecodeError:
            print(f"Warning: {self.filename} is corrupted. Starting with empty list.")
            return []
        except Exception as e:
            print(f"Error loading tasks: {e}")
            return []
    
    def save_tasks(self):
        """Save tasks to JSON file"""
        try:
            with open(self.filename, 'w', encoding='utf-8') as file:
                json.dump(self.tasks, file, indent=4)
            return True
        except Exception as e:
            print(f"Error saving tasks: {e}")
            return False
    
    def add_task(self, description):
        """Add a new task to the list"""
        if not description or description.strip() == '':
            print("Error: Task description cannot be empty.")
            return False
        
        task = {
            'id': len(self.tasks) + 1,
            'description': description.strip(),
            'completed': False,
            'created_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        self.tasks.append(task)
        
        if self.save_tasks():
            print(f"\n✓ Task added successfully! (ID: {task['id']})")
            return True
        return False
    
    def view_tasks(self, show_all=True):
        """Display all tasks or only pending tasks"""
        if not self.tasks:
            print("\nNo tasks found. Your to-do list is empty!")
            return
        
        # Filter tasks if needed
        tasks_to_show = self.tasks if show_all else [t for t in self.tasks if not t['completed']]
        
        if not tasks_to_show:
            print("\nNo pending tasks found. Great job!")
            return
        
        print("\n" + "=" * 80)
        print("YOUR TO-DO LIST")
        print("=" * 80)
        
        for task in tasks_to_show:
            status = "✓" if task['completed'] else "○"
            status_text = "DONE" if task['completed'] else "PENDING"
            print(f"\n[{status}] ID: {task['id']} | Status: {status_text}")
            print(f"    Task: {task['description']}")
            print(f"    Created: {task['created_at']}")
        
        print("\n" + "=" * 80)
        
        # Summary
        total = len(self.tasks)
        completed = sum(1 for t in self.tasks if t['completed'])
        pending = total - completed
        print(f"Total: {total} | Completed: {completed} | Pending: {pending}")
        print("=" * 80)
    
    def delete_task(self, task_id):
        """Delete a task by ID"""
        try:
            task_id = int(task_id)
        except ValueError:
            print("Error: Task ID must be a number.")
            return False
        
        # Find task with given ID
        task_index = None
        for i, task in enumerate(self.tasks):
            if task['id'] == task_id:
                task_index = i
                break
        
        if task_index is None:
            print(f"Error: Task with ID {task_id} does not exist.")
            return False
        
        # Confirm deletion
        task_desc = self.tasks[task_index]['description']
        confirm = input(f"\nAre you sure you want to delete '{task_desc}'? (yes/no): ").lower()
        
        if confirm == 'yes':
            self.tasks.pop(task_index)
            if self.save_tasks():
                print(f"\n✓ Task {task_id} deleted successfully!")
                return True
        else:
            print("\nDeletion cancelled.")
        
        return False
    
    def mark_complete(self, task_id):
        """Mark a task as completed"""
        try:
            task_id = int(task_id)
        except ValueError:
            print("Error: Task ID must be a number.")
            return False
        
        # Find task with given ID
        task = None
        for t in self.tasks:
            if t['id'] == task_id:
                task = t
                break
        
        if task is None:
            print(f"Error: Task with ID {task_id} does not exist.")
            return False
        
        if task['completed']:
            print(f"\nTask {task_id} is already marked as completed.")
            return False
        
        task['completed'] = True
        if self.save_tasks():
            print(f"\n✓ Task {task_id} marked as completed!")
            return True
        
        return False
    
    def mark_incomplete(self, task_id):
        """Mark a task as incomplete"""
        try:
            task_id = int(task_id)
        except ValueError:
            print("Error: Task ID must be a number.")
            return False
        
        # Find task with given ID
        task = None
        for t in self.tasks:
            if t['id'] == task_id:
                task = t
                break
        
        if task is None:
            print(f"Error: Task with ID {task_id} does not exist.")
            return False
        
        if not task['completed']:
            print(f"\nTask {task_id} is already marked as incomplete.")
            return False
        
        task['completed'] = False
        if self.save_tasks():
            print(f"\n✓ Task {task_id} marked as incomplete!")
            return True
        
        return False
    
    def clear_completed(self):
        """Delete all completed tasks"""
        completed_tasks = [t for t in self.tasks if t['completed']]
        
        if not completed_tasks:
            print("\nNo completed tasks to clear.")
            return False
        
        confirm = input(f"\nDelete {len(completed_tasks)} completed task(s)? (yes/no): ").lower()
        
        if confirm == 'yes':
            self.tasks = [t for t in self.tasks if not t['completed']]
            if self.save_tasks():
                print(f"\n✓ Cleared {len(completed_tasks)} completed task(s)!")
                return True
        else:
            print("\nOperation cancelled.")
        
        return False

def display_menu():
    """Display the main menu"""
    print("\n" + "=" * 50)
    print("TO-DO LIST APPLICATION")
    print("=" * 50)
    print("1. Add a new task")
    print("2. View all tasks")
    print("3. View pending tasks only")
    print("4. Mark task as complete")
    print("5. Mark task as incomplete")
    print("6. Delete a task")
    print("7. Clear all completed tasks")
    print("8. Exit")
    print("=" * 50)

def main():
    """Main function to run the to-do list application"""
    todo = TodoList()
    
    print("\n" + "=" * 50)
    print("Welcome to Your To-Do List Application!")
    print("=" * 50)
    
    while True:
        display_menu()
        choice = input("\nEnter your choice (1-8): ").strip()
        
        if choice == '1':
            description = input("\nEnter task description: ")
            todo.add_task(description)
        
        elif choice == '2':
            todo.view_tasks(show_all=True)
        
        elif choice == '3':
            todo.view_tasks(show_all=False)
        
        elif choice == '4':
            task_id = input("\nEnter task ID to mark as complete: ")
            todo.mark_complete(task_id)
        
        elif choice == '5':
            task_id = input("\nEnter task ID to mark as incomplete: ")
            todo.mark_incomplete(task_id)
        
        elif choice == '6':
            task_id = input("\nEnter task ID to delete: ")
            todo.delete_task(task_id)
        
        elif choice == '7':
            todo.clear_completed()
        
        elif choice == '8':
            print("\n" + "=" * 50)
            print("Thank you for using To-Do List Application!")
            print("Your tasks have been saved. Goodbye!")
            print("=" * 50 + "\n")
            break
        
        else:
            print("\nInvalid choice! Please enter a number between 1 and 8.")

# Run the application
if __name__ == "__main__":
    main()