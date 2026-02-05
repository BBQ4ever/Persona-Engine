"""
Persona Engine Configuration Hub
-------------------------------
Contains only RUNTIME TUNABLES (thresholds, weights, paths, keywords).
CONSTITUTIONAL RULES (Safety Anchors) remain hardcoded in recombinator.py.
"""

# --- 1. Scenario Analysis (L0) ---
# Keywords for scenario classification
FACT_KEYWORDS = [
    r"calculate", r"compute", r"prove", r"math", r"fact", 
    r"tutorial", r"square root", r"formula", r"definition",
    r"scientific", r"technical", r"review", r"expert", r"logic",
    r"sqrt", r"计算", r"证明", r"平方根", r"solve", r"analyze"
]

SUPPORT_KEYWORDS = [
    r"help", r"feel", r"sad", r"lonely", r"comfort", r"support",
    r"need someone", r"listen", r"tough day",
    r"thank you", r"thanks", r"love", r"friend", r"companion"
]

# --- 2. Governance Thresholds (L2/L4) ---
# Drift tolerance for the Phase 11 Gyroscope
DRIFT_THRESHOLD = 0.3

# Interaction History Window size
HISTORY_WINDOW_SIZE = 20

# --- 3. Default Stances (Archetypes) ---
# Used when specific recommendations are missing
DEFAULT_STANCE = {"rigor": 0.5, "warmth": 0.5, "chaos": 0.5}
FACTUAL_STANCE = {"rigor": 0.9, "warmth": 0.2, "chaos": 0.1}
SUPPORTIVE_STANCE = {"rigor": 0.3, "warmth": 0.9, "chaos": 0.4}

# --- 4. Resource Metadata ---
CONTRACT_VERSION = "1.0.0"
DEFAULT_PERSONA_ID = "pioneer_v2"
GENOME_PATH = "src/l2_genome/sample_genome.json"

# --- 5. Emotional Decay Rates (L1) ---
# (Will be used more extensively in Sprint 3)
PASSIVE_DECAY_RATE = 0.05
LOCKED_DECAY_MULTIPLIER = 0.2
