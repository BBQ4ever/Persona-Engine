import sys
import argparse
import json
import uuid
from src.app_integration import PersonaService

def main():
    parser = argparse.ArgumentParser(description="Persona Engine: Context Compiler CLI")
    parser.add_argument("user_input", help="The raw user input string")
    parser.add_argument("--format", choices=["text", "json"], default="text", 
                        help="Output format (default: text). Use 'json' for full metadata.")
    parser.add_argument("--session-id", default=f"user_{uuid.uuid4().hex[:8]}", 
                        help="Session ID for stability and history")
    parser.add_argument("--persona-id", default="pioneer_v2", 
                        help="Persona ID to use (default: pioneer_v2)")
    parser.add_argument("--trace", action="store_true", 
                        help="Enable detailed trace output to stderr")
    parser.add_argument("--seed", type=int, help="Optional manual seed for reproducibility")
    parser.add_argument("--genome", help="Path to a specific genome file")

    args = parser.parse_args()

    try:
        service = PersonaService(genome_path=args.genome, persona_id=args.persona_id)
        
        # In a real implementation, we would pass args.seed to SeededSampler 
        # via PersonaService. For now, session_id handles it.
        
        payload = service.get_llm_payload(args.user_input, session_id=args.session_id, manual_seed=args.seed)
        
        if args.trace:
            sys.stderr.write(f"--- Persona Engine CLI Trace ---\n")
            sys.stderr.write(f"Session: {args.session_id}\n")
            sys.stderr.write(f"Trace ID: {payload['metadata']['trace_id']}\n")
            sys.stderr.write(f"Reason Codes: {', '.join(payload['metadata']['reason_codes'])}\n")
            sys.stderr.write(f"Stance: {payload['metadata']['stance']}\n")
            sys.stderr.write(f"--------------------------------\n")

        if args.format == "json":
            # JSON format: Full payload including metadata
            print(json.dumps(payload, indent=2, ensure_ascii=False))
        else:
            # Text format: ONLY the system instruction for piping (stdout discipline)
            print(payload["messages"][0]["content"])

    except Exception as e:
        sys.stderr.write(f"❌ Persona Runtime Error: {str(e)}\n")
        sys.exit(1)

if __name__ == "__main__":
    main()
