import os
from PyCells import MemorySystem as MemorySystemFileBased
from Pycells2 import MemorySystem as MemorySystemDBBased

class Membrane:
    
    # Initialization
    def __init__(self):
        self.file_based_memory_system = MemorySystemFileBased()
        self.db_based_memory_system = MemorySystemDBBased()

    # Storage Methods

    def store_information(self, sentence, memory_type="general"):
        """Store information in both memory systems."""
        self.file_based_memory_system.store_memory(sentence, memory_type)
        self.db_based_memory_system.store_memory(sentence)

    def store_evolved_memory(self, sentence, memory_type="general"):
        """Store evolved memory in the file-based system."""
        self.file_based_memory_system.evolve_memory(memory_type, sentence)

    # Retrieval Methods

    def retrieve_by_memory_type(self, memory_type):
        """Retrieve information by memory type from the file-based system."""
        return self.file_based_memory_system.retrieve_memory(memory_type)

    def retrieve_by_tag(self, tag):
        """Retrieve information by tag from the SQLite-based system."""
        return self.db_based_memory_system.retrieve_memory_by_tag(tag)

    def retrieve_file_based_directory_tree(self, root_directory="."):
        """Retrieve the entire tree of directories for the file-based system."""
        directory_tree = {}
        for dirpath, dirnames, filenames in os.walk(root_directory):
            current_level = directory_tree
            path_parts = dirpath.split(os.sep)[1:]
            for part in path_parts:
                current_level = current_level.setdefault(part, {})
            current_level["__files__"] = filenames
        return directory_tree

    def print_file_based_directory_tree(self, tree, indent=0):
        """Print the directory tree of the file-based system."""
        for key, value in tree.items():
            if key == "__files__":
                for filename in value:
                    print("  " * indent + f"- {filename}")
            else:
                print("  " * indent + f"+ {key}/")
                self.print_file_based_directory_tree(value, indent + 1)

    def retrieve_db_based_tag_tree(self):
        """Retrieve the hierarchical tag tree for the SQLite-based system."""
        with self.db_based_memory_system.conn:
            tags = self.db_based_memory_system.conn.execute("""
                SELECT id, tag, parent_tag_id FROM tags
            """).fetchall()

        tag_tree = {}
        for tag_id, tag, parent_tag_id in tags:
            if parent_tag_id:
                parent_tag = next(t[1] for t in tags if t[0] == parent_tag_id)
                tag_tree.setdefault(parent_tag, []).append(tag)
            else:
                tag_tree.setdefault(tag, [])

        return tag_tree

    def print_db_based_tag_tree(self, tree, indent=0):
        """Print the tag tree of the SQLite-based system."""
        for key, values in tree.items():
            print("  " * indent + f"+ {key}")
            for value in values:
                print("  " * (indent + 1) + f"- {value}")

# Example Usage

membrane = Membrane()

# Storing information
membrane.store_information("Bats are nocturnal mammals.")
membrane.store_evolved_memory("Bats use echolocation to navigate.", "animals")

# Retrieving information
print(membrane.retrieve_by_memory_type("animals"))
print(membrane.retrieve_by_tag("mammal"))

# Retrieving and printing directory tree for file-based system
print("\nDirectory Tree for PyCells.py (file-based system):")
root_directory = membrane.file_based_memory_system.memory_path
file_based_tree = membrane.retrieve_file_based_directory_tree(root_directory)
membrane.print_file_based_directory_tree(file_based_tree)

# Retrieving and printing tag tree for SQLite-based system
print("\nTag Tree for Pycells2.py (SQLite-based system):")
db_based_tree = membrane.retrieve_db_based_tag_tree()
membrane.print_db_based_tag_tree(db_based_tree)
