#!/usr/bin/env python3

import sys
from pathlib import Path
from telemetry_loader import TelemetryLoader
from validator import TelemetryValidator

def main():
    if len(sys.argv) != 2:
        print("Usage: python analyze.py <telemetry_directory>")
        sys.exit(1)
    
    telemetry_dir = sys.argv[1]
    
    if not Path(telemetry_dir).exists():
        print(f"Error: Directory {telemetry_dir} does not exist")
        sys.exit(1)
    
    print(f"Loading telemetry from: {telemetry_dir}")
    
    loader = TelemetryLoader(telemetry_dir)
    df = loader.load_all_sessions()
    
    if df.empty:
        print("No telemetry data found")
        return
    
    print(f"Loaded {len(df)} events")
    
    validator = TelemetryValidator()
    result = validator.validate(df)
    
    print("\n=== Validation Report ===")
    print(f"Sessions: {result.session_count}")
    print(f"Events: {result.event_count}")
    
    if result.errors:
        print(f"\nErrors ({len(result.errors)}):")
        for error in result.errors:
            print(f"  - {error}")
    
    if result.warnings:
        print(f"\nWarnings ({len(result.warnings)}):")
        for warning in result.warnings:
            print(f"  - {warning}")
    
    if result.is_valid():
        print("\n✅ Validation passed")
    else:
        print("\n❌ Validation failed")
        sys.exit(1)

if __name__ == "__main__":
    main()