import tkinter as tk
from tkinter import simpledialog, filedialog, scrolledtext, messagebox
import logging
import json
import datetime
import os
import PyCells
import Pycells2

logging.basicConfig(filename='memory_debugger.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

class MemoryDebugger:
    def __init__(self):
        self.pycells_memory = PyCells.MemorySystem()
        self.pycells2_memory = Pycells2.MemorySystem()
        self.gui = self.create_gui()

    def create_gui(self):
        root = tk.Tk()
        root.title("Memory Debugger")

        # Text area for output
        self.output_text = scrolledtext.ScrolledText(root, width=70, height=20)
        self.output_text.pack(pady=20)

        # Buttons for various actions
        store_btn = tk.Button(root, text="Store Memory", command=self.store_memory)
        store_btn.pack()

        retrieve_btn = tk.Button(root, text="Retrieve Memory", command=self.retrieve_memory)
        retrieve_btn.pack()

        search_btn = tk.Button(root, text="Search Memory", command=self.search_memory)
        search_btn.pack()

        edit_btn = tk.Button(root, text="Edit Memory", command=self.edit_memory)
        edit_btn.pack()

        batch_upload_btn = tk.Button(root, text="Batch Upload", command=self.batch_upload)
        batch_upload_btn.pack()

        return root

    def store_memory(self):
        content = simpledialog.askstring("Store Memory", "Enter the memory content:")
        self.pycells_memory.store_memory(content, "general")
        self.pycells2_memory.store_memory(content)
        self.log_operation("Stored Memory", content)

    def retrieve_memory(self):
        memories_pycells = self.pycells_memory.retrieve_memory("general")
        memories_pycells2 = self.pycells2_memory.retrieve_memory_by_tag("general")
        self.output_text.insert(tk.END, "Memories from PyCells:\n")
        for memory in memories_pycells:
            self.output_text.insert(tk.END, memory + "\n")
        self.output_text.insert(tk.END, "\nMemories from Pycells2:\n")
        for memory in memories_pycells2:
            self.output_text.insert(tk.END, memory + "\n")

    def search_memory(self):
        keyword = simpledialog.askstring("Search", "Enter keyword or phrase:")
        results_pycells = [memory for memory in self.pycells_memory.retrieve_memory("general") if keyword in memory]
        results_pycells2 = self.pycells2_memory.retrieve_memory_by_tag(keyword)
        self.output_text.insert(tk.END, "Search Results:\n")
        for memory in results_pycells:
            self.output_text.insert(tk.END, f"From PyCells: {memory}\n")
        for memory in results_pycells2:
            self.output_text.insert(tk.END, f"From Pycells2: {memory}\n")

    def edit_memory(self):
        # Ask the user for the memory they want to edit
        memory_to_edit = simpledialog.askstring("Edit", "Enter a keyword or phrase from the memory you wish to edit:")

        # Search for the memory in both systems
        memories_pycells = [memory for memory in self.pycells_memory.retrieve_memory("general") if memory_to_edit in memory]
        memories_pycells2 = self.pycells2_memory.retrieve_memory_by_tag(memory_to_edit)

        # Combine memories from both systems and display them for the user to select
        all_memories = memories_pycells + memories_pycells2
        if not all_memories:
            messagebox.showinfo("Edit", "No matching memory found.")
            return

        # Let the user select the exact memory they want to edit
        memory_selection = simpledialog.askstring("Edit", f"Select the exact memory you wish to edit from the following:\n\n{'\n'.join(all_memories)}")

        if memory_selection not in all_memories:
            messagebox.showinfo("Edit", "Invalid selection.")
            return

        # Ask the user for the new content
        new_content = simpledialog.askstring("Edit", "Enter the new content:", initialvalue=memory_selection)

        # Update the memory in both systems (for demonstration purposes, we're only updating in PyCells)
        # In a real-world scenario, you'd need to handle updating in both systems and handle cases where the memory might not exist in one of them
        # Here, we're replacing the content in the file for PyCells. For Pycells2, you'd need to update the database entry.
        with open(os.path.join(self.pycells_memory.memory_path, "general.txt"), "r") as file:
            content = file.read()
        content = content.replace(memory_selection, new_content)
        with open(os.path.join(self.pycells_memory.memory_path, "general.txt"), "w") as file:
            file.write(content)

        # Log the editing operation
        self.log_operation("Edited Memory", f"Original: {memory_selection}, New: {new_content}")

    def batch_upload(self):
        file_paths = filedialog.askopenfilenames(filetypes=[("Text files", "*.txt")])
        for file_path in file_paths:
            with open(file_path, 'r') as file:
                content = file.read()
                self.pycells_memory.store_memory(content, "general")
                self.log_operation("Batch Uploaded", file_path)

    def log_operation(self, operation, details="", level="info"):
        log_data = {
            "operation": operation,
            "details": details,
            "timestamp": datetime.datetime.now().isoformat()
        }
        log_message = json.dumps(log_data)
        if level == "info":
            logging.info(log_message)
        elif level == "warning":
            logging.warning(log_message)
        elif level == "error":
            logging.error(log_message)
        elif level == "debug":
            logging.debug(log_message)
        else:
            logging.info(log_message)

    def run(self):
        self.gui.mainloop()

if __name__ == "__main__":
    debugger = MemoryDebugger()
    debugger.run()
