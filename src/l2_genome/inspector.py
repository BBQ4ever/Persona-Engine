import json
import sys

def print_bar(label, value, length=20):
    filled = int(value * length)
    bar = "█" * filled + "░" * (length - filled)
    print(f"{label:20} [{bar}] {value:.2f}")

def inspect_genome(path):
    with open(path, 'r') as f:
        data = json.load(f)
        
    print(f"\n--- Persona Genome Inspection: {data.get('metadata', {}).get('persona_id', 'Unknown')} ---")
    print(f"Version: {data['version']}")
    print("-" * 50)
    
    for locus in data['loci']:
        print(f"\nID: {locus['id']} ({locus['category']})")
        print(f"Desc: {locus['description']}")
        
        dist = locus['distribution']
        if dist['type'] == 'range':
            vals = dist['values']
            print_bar("  Default Value", vals['default'])
            print(f"  Range: [{vals['min']} - {vals['max']}]")
        elif dist['type'] == 'categorical':
            for cat, prob in dist['values'].items():
                print_bar(f"  {cat}", prob)
        
        print_bar("  Weight", locus.get('weight', 0.5))
        print_bar("  Variability", locus.get('variability', 0.0))

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python inspector.py <genome_json>")
        sys.exit(1)
    inspect_genome(sys.argv[1])
