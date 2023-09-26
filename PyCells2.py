import sqlite3
import openai

class HierarchicalTaggingSystem:
    def __init__(self):
        self.tag_hierarchy = {}  # A dictionary to store the hierarchical tags

    def consult_chat_gpt(self, tag):
        # Ask Chat GPT about the overall structure of the tag and potential sub-tags
        response = openai.Completion.create(
            prompt=f"Describe the hierarchical structure and potential sub-categories for the topic '{tag}'",
            max_tokens=150
        )
        return response.choices[0].text.strip()

    def process_memory(self, content):
        # Process a new memory: auto-tag it and adapt the tag hierarchy
        # For simplicity, let's assume we ask Chat GPT for tagging suggestions
        response = openai.Completion.create(
            prompt=f"Suggest hierarchical tags for the following content: '{content}'",
            max_tokens=50
        )
        suggested_tags = response.choices[0].text.strip().split(',')
        for tag in suggested_tags:
            if tag not in self.tag_hierarchy:
                sub_tags = self.consult_chat_gpt(tag)
                self.tag_hierarchy[tag] = sub_tags
        return suggested_tags

class MemorySystem:
    def __init__(self, db_path=":memory:"):
        self.conn = sqlite3.connect(db_path)
        self.tagging_system = HierarchicalTaggingSystem()
        self.create_tables()

    def create_tables(self):
        with self.conn:
            # Memories table
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS memories (
                    id INTEGER PRIMARY KEY,
                    content TEXT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Tags table
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS tags (
                    id INTEGER PRIMARY KEY,
                    tag TEXT UNIQUE,
                    parent_tag_id INTEGER,
                    FOREIGN KEY (parent_tag_id) REFERENCES tags(id)
                )
            """)
            
            # Memory-Tag association table
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS memory_tags (
                    memory_id INTEGER,
                    tag_id INTEGER,
                    PRIMARY KEY (memory_id, tag_id),
                    FOREIGN KEY (memory_id) REFERENCES memories(id),
                    FOREIGN KEY (tag_id) REFERENCES tags(id)
                )
            """)

    def store_memory(self, content):
        with self.conn:
            # Insert the memory
            cur = self.conn.execute("INSERT INTO memories (content) VALUES (?)", (content,))
            memory_id = cur.lastrowid
            
            # Get hierarchical tags for the memory
            tags = self.tagging_system.process_memory(content)
            
            # Insert tags and associate them with the memory
            for tag in tags:
                cur = self.conn.execute("INSERT OR IGNORE INTO tags (tag) VALUES (?)", (tag,))
                tag_id = cur.lastrowid or self.conn.execute("SELECT id FROM tags WHERE tag = ?", (tag,)).fetchone()[0]
                self.conn.execute("INSERT INTO memory_tags (memory_id, tag_id) VALUES (?, ?)", (memory_id, tag_id))

    def retrieve_memory_by_tag(self, tag):
        with self.conn:
            memories = self.conn.execute("""
                SELECT m.content 
                FROM memories m
                JOIN memory_tags mt ON m.id = mt.memory_id
                JOIN tags t ON mt.tag_id = t.id
                WHERE t.tag = ?
            """, (tag,)).fetchall()
        return [memory[0] for memory in memories]

