#!/usr/bin/env python3

import sys
from pathlib import Path
from telemetry_loader import TelemetryLoader
from validator import TelemetryValidator
from feature_extractor import FeatureExtractor
from session_aggregator import SessionAggregator

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
    
    if not result.is_valid():
        print("\n❌ Validation failed")
        sys.exit(1)
    
    print("\n✅ Validation passed")
    
    # Feature Engineering
    print("\n=== Feature Engineering ===")
    extractor = FeatureExtractor()
    attempts_df = extractor.extract_attempt_features(df)
    print(f"Extracted features for {len(attempts_df)} attempts")
    
    aggregator = SessionAggregator()
    sessions_df = aggregator.aggregate_session_features(attempts_df)
    print(f"Aggregated features for {len(sessions_df)} sessions")
    
    # Save outputs
    output_dir = Path(telemetry_dir).parent / "processed"
    output_dir.mkdir(exist_ok=True)
    
    attempts_df.to_csv(output_dir / "attempt_features.csv", index=False)
    sessions_df.to_csv(output_dir / "session_features.csv", index=False)
    
    print(f"\n📊 Features saved to {output_dir}")
    print("  - attempt_features.csv: Per-attempt metrics")
    print("  - session_features.csv: Per-session aggregated metrics")

if __name__ == "__main__":
    main()