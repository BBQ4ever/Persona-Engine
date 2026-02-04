import json
import os
import time

class PersonaReflectionJournal:
    """
    Logs the internal evolution of the persona.
    Used for 'Recursive Self-Observation'.
    """
    def __init__(self, journal_path="logs/persona_journal.jsonl"):
        self.journal_path = journal_path
        os.makedirs(os.path.dirname(self.journal_path), exist_ok=True)

    def log_entry(self, status, user_input=None):
        entry = {
            "timestamp": time.time(),
            "iso_time": time.ctime(),
            "interaction_id": status['interaction_count'],
            "state": status['state'],
            "affect": status['affect'],
            "intimacy": status['intimacy_level'],
            "context_shorthand": user_input[:50] if user_input else "background_process"
        }
        
        with open(self.journal_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")

    def get_recent_insights(self, limit=10):
        """
        Reads the last few entries to provide 'context' for the AI's self-reflection.
        Optimized for large files: Reads from the end.
        """
        if not os.path.exists(self.journal_path):
            return []
            
        results = []
        chunk_size = 1024
        with open(self.journal_path, "rb") as f:
            f.seek(0, 2)
            file_size = f.tell()
            buffer = b""
            pointer = file_size
            
            while len(results) < limit and pointer > 0:
                step = min(chunk_size, pointer)
                pointer -= step
                f.seek(pointer)
                buffer = f.read(step) + buffer
                lines = buffer.split(b"\n")
                
                # Keep the first part in buffer (it might be incomplete)
                buffer = lines[0]
                # Process the rest
                for line in reversed(lines[1:]):
                    if line.strip() and len(results) < limit:
                        results.append(json.loads(line.decode("utf-8")))
        
        return results
