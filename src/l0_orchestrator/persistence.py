import json
import os
import time

class SnapshotManager:
    """
    Handles persisting and restoring the state of the Persona Engine.
    """
    def __init__(self, snapshot_dir="snapshots"):
        self.snapshot_dir = snapshot_dir
        os.makedirs(self.snapshot_dir, exist_ok=True)

    def save_snapshot(self, service, label="auto"):
        """
        Captures the current FSM state and Genome from a PersonaService instance.
        """
        timestamp = int(time.time())
        filename = f"snapshot_{label}_{timestamp}.json"
        filepath = os.path.join(self.snapshot_dir, filename)

        snapshot_data = {
            "version": "1.0.0",
            "timestamp": timestamp,
            "label": label,
            "fsm_state": service.fsm.to_dict(),
            "genome": service.genome
        }

        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(snapshot_data, f, indent=2, ensure_ascii=False)

        print(f"📁 Snapshot saved: {filepath}")
        return filepath

    def load_latest_snapshot(self, service):
        """
        Finds the most recent snapshot and applies it to the service.
        """
        import re
        files = [f for f in os.listdir(self.snapshot_dir) if f.endswith(".json")]
        if not files:
            print("📭 No snapshots found.")
            return False

        # Use regex to find timestamp at the end: snapshot_{label}_{timestamp}.json
        def get_timestamp(filename):
            match = re.search(r'_(\d+)\.json$', filename)
            return int(match.group(1)) if match else 0

        files.sort(key=get_timestamp, reverse=True)
        latest_file = os.path.join(self.snapshot_dir, files[0])
        
        return self.load_snapshot(service, latest_file)

    def load_snapshot(self, service, filepath):
        """
        Loads a specific snapshot file and updates the service state.
        """
        if not os.path.exists(filepath):
            print(f"❌ Snapshot file not found: {filepath}")
            return False

        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)

        # Restore FSM
        if "fsm_state" in data:
            service.fsm.from_dict(data["fsm_state"])
        
        # Restore Genome
        if "genome" in data:
            service.genome = data["genome"]
            service.engine.genome = service.genome # Update reference
            # Re-init ArchetypeManager with new genome base
            from src.l2_genome.archetypes import ArchetypeManager
            service.archetype_mgr = ArchetypeManager(service.genome)

        print(f"⏮️ Snapshot restored from: {filepath}")
        return True
