import time
from typing import List, Dict, Any, Tuple

class ShortTermMemory:
    """
    Manages the active context window for the Persona.
    Uses Saliency Scoring to prune noise instead of simple FIFO.
    """
    def __init__(self, max_entries=10):
        self.max_entries = max_entries
        self.entries = []

    def add(self, entry: Dict[str, Any]) -> List[str]:
        """
        Adds a new memory entry. Prunes if limit exceeded.
        Returns a list of reason codes related to pruning.
        """
        self.entries.append(entry)
        reason_codes = []
        
        if len(self.entries) > self.max_entries:
            pruned_idx, reason = self._prune()
            reason_codes.append(f"MEMORY_PRUNED_{reason}_AT_{pruned_idx}")
            
        return reason_codes

    def _score_entry(self, entry: Dict[str, Any], index: int, total: int) -> float:
        """
        Heuristic Saliency Scoring.
        Score = Intensity * StateWeight * Recency
        """
        # Affect intensity
        affect = entry.get('affect', {'p': 0, 'a': 0, 'd': 0})
        intensity = abs(affect.get('p', 0)) + abs(affect.get('a', 0)) + abs(affect.get('d', 0))
        
        # State importance (Transitions or high-risk states)
        state = entry.get('state', 'STABLE')
        state_weight = 1.5 if state in ['LOCKED', 'DRIFTING', 'FORMING'] else 1.0
        
        # Recency (Linear weight from 0.5 to 1.0)
        recency = 0.5 + (0.5 * (index / total)) if total > 1 else 1.0
        
        return (intensity + 0.1) * state_weight * recency

    def _prune(self) -> Tuple[int, str]:
        """
        Finds the least 'salient' entry and removes it.
        We protect the latest 2 entries from pruning to ensure immediate conversational flow.
        """
        if len(self.entries) <= 2:
            # Should not happen if max_entries > 2
            return -1, "BUFFER_TOO_SMALL"
            
        # Candidates for pruning: all except the last 2
        candidates_end_idx = len(self.entries) - 2
        candidates = self.entries[:candidates_end_idx]
        
        scores = [self._score_entry(e, i, len(self.entries)) for i, e in enumerate(candidates)]
        
        # Find index of minimum score
        min_score_idx = scores.index(min(scores))
        
        # Remove and return info
        self.entries.pop(min_score_idx)
        return min_score_idx, "LOW_SALIENCE"

    def get_summary(self) -> List[Dict[str, Any]]:
        """Returns the current prioritized memory entries."""
        return self.entries
