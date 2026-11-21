import json
import os
import tkinter as tk
from tkinter import messagebox, simpledialog

FILE_NAME = "tasks_gui.json"


class TodoApp:

  def __init__(self, root):
    self.root = root
    self.root.title("To-Do List")
    self.root.geometry("400x450")
    self.tasks = self.load_tasks()

    input_frame = tk.Frame(root)
    input_frame.pack(pady=10)

    self.task_entry = tk.Entry(input_frame, width=28, font=("Arial", 12))
    self.task_entry.pack(side=tk.LEFT, padx=5)

    add_btn = tk.Button(input_frame, text="Add Task", command=self.add_task)
    add_btn.pack(side=tk.LEFT)

    self.listbox = tk.Listbox(
        root, width=45, height=15, font=("Arial", 11), selectmode=tk.SINGLE
    )
    self.listbox.pack(pady=10, padx=10)

    btn_frame = tk.Frame(root)
    btn_frame.pack(pady=5)

    tk.Button(btn_frame, text="Mark Done", command=self.complete_task).grid(
        row=0, column=0, padx=5
    )
    tk.Button(btn_frame, text="Edit Task", command=self.update_task).grid(
        row=0, column=1, padx=5
    )
    tk.Button(btn_frame, text="Delete Task", command=self.delete_task).grid(
        row=0, column=2, padx=5
    )

    self.refresh_listbox()

  def load_tasks(self):
    if os.path.exists(FILE_NAME):
      with open(FILE_NAME, "r") as file:
        return json.load(file)
    return []

  def save_tasks(self):
    with open(FILE_NAME, "w") as file:
      json.dump(self.tasks, file, indent=4)

  def refresh_listbox(self):
    self.listbox.delete(0, tk.END)
    for task in self.tasks:
      prefix = "[✓] " if task["completed"] else "[  ] "
      self.listbox.insert(tk.END, prefix + task["title"])

  def add_task(self):
    title = self.task_entry.get().strip()
    if title:
      self.tasks.append({"title": title, "completed": False})
      self.save_tasks()
      self.refresh_listbox()
      self.task_entry.delete(0, tk.END)
    else:
      messagebox.showwarning("Warning", "Please enter a task.")

  def complete_task(self):
    selected = self.listbox.curselection()
    if selected:
      idx = selected[0]
      self.tasks[idx]["completed"] = not self.tasks[idx]["completed"]
      self.save_tasks()
      self.refresh_listbox()

  def update_task(self):
    selected = self.listbox.curselection()
    if selected:
      idx = selected[0]
      new_title = simpledialog.askstring(
          "Edit Task",
          "Update task description:",
          initialvalue=self.tasks[idx]["title"],
      )
      if new_title and new_title.strip():
        self.tasks[idx]["title"] = new_title.strip()
        self.save_tasks()
        self.refresh_listbox()

  def delete_task(self):
    selected = self.listbox.curselection()
    if selected:
      idx = selected[0]
      self.tasks.pop(idx)
      self.save_tasks()
      self.refresh_listbox()


if __name__ == "__main__":
  root = tk.Tk()
  app = TodoApp(root)
  root.mainloop()