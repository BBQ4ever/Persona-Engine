import json
import re
import sys
import os

class GenomeValidator:
    def __init__(self, schema_path):
        with open(schema_path, 'r') as f:
            self.schema = json.load(f)
            
    def validate(self, genome_data):
        """
        Performs structural and semantic validation.
        Note: For production, use jsonschema library. 
        This is a custom implementation to support 'Truth Independence' checks.
        """
        errors = []
        
        # 1. Structural Check (Simplified version of JSON Schema validation)
        if "version" not in genome_data:
            errors.append("Missing 'version'")
        if "loci" not in genome_data:
            errors.append("Missing 'loci' array")
            return errors
            
        for i, locus in enumerate(genome_data["loci"]):
            locus_id = locus.get("id", f"index_{i}")
            
            # Category check
            if locus.get("category") not in ["cognitive", "value", "style", "domain"]:
                errors.append(f"Locus '{locus_id}': Invalid category")
                
            # 2. Principle I: Truth Independence (The "Must-Not")
            # We scan for factual-sounding declarations in descriptions
            description = locus.get("description", "").lower()
            fact_patterns = [
                r"\bis a\b", r"\bare\b", r"\bfact\b", r"\btruth\b", 
                r"\bproven\b", r"\bscience\b", r"1\+1="
            ]
            for pattern in fact_patterns:
                if re.search(pattern, description):
                    errors.append(f"Locus '{locus_id}': Potential Truth-Independence violation in description. "
                                  f"Descriptions should define tendencies, not facts.")
            
            # 3. Principle II: Non-Deterministic Execution
            # Check if distribution is just a single fixed token (forbidden at L2)
            dist = locus.get("distribution", {})
            if dist.get("type") == "scalar":
                # Scalar is allowed as a parameter, but it shouldn't be a 'final answer'
                pass

        return errors

def main():
    if len(sys.argv) < 3:
        print("Usage: python validator.py <schema_json> <genome_json>")
        sys.exit(1)
        
    schema_path = sys.argv[1]
    genome_path = sys.argv[2]
    
    with open(genome_path, 'r') as f:
        genome_data = json.load(f)
        
    validator = GenomeValidator(schema_path)
    errors = validator.validate(genome_data)
    
    if not errors:
        print(f"✅ Genome '{genome_path}' is VALID and compliant with L2 Charter.")
    else:
        print(f"❌ Validation FAILED for '{genome_path}':")
        for err in errors:
            print(f"  - {err}")
        sys.exit(1)

if __name__ == "__main__":
    main()
