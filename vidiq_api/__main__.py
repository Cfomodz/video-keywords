"""
Command line interface for vidIQ API.
"""

import sys
import json
from .client import VidiqAPI


def main():
    """Main CLI entry point."""
    if len(sys.argv) < 2:
        print("Usage: python -m vidiq_api <keyword>")
        print("Make sure VIDIQ_TOKEN environment variable is set.")
        sys.exit(1)
    
    keyword = sys.argv[1]
    
    try:
        api = VidiqAPI()
        result = api.analyze_keyword(keyword)
        
        print(json.dumps(result, indent=2))
        
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
