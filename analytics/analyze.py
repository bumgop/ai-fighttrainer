#!/usr/bin/env python3

import sys
from pathlib import Path
from telemetry_loader import TelemetryLoader
from validator import TelemetryValidator
from feature_extractor import FeatureExtractor
from session_aggregator import SessionAggregator
from feature_selector import FeatureSelector
from clustering import PlayerClustering
import json

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
        print("\nValidation failed")
        sys.exit(1)
    
    print("\nValidation passed")
    
    # Feature Engineering
    print("\n=== Feature Engineering ===")
    extractor = FeatureExtractor()
    attempts_df = extractor.extract_attempt_features(df)
    print(f"Extracted features for {len(attempts_df)} attempts")
    
    aggregator = SessionAggregator()
    sessions_df = aggregator.aggregate_session_features(attempts_df)
    print(f"Aggregated features for {len(sessions_df)} sessions")
    
    # Player Clustering
    if len(sessions_df) >= 2:  # Need at least 2 sessions for clustering
        print("\n=== Player Clustering ===")
        selector = FeatureSelector()
        clustering_features = selector.select_clustering_features(sessions_df)
        print(f"Selected {len(clustering_features.columns)-1} features for clustering")
        
        clusterer = PlayerClustering()
        clustering_results = clusterer.fit_clustering_models(clustering_features)
        
        print(f"K-Means best: {clustering_results['kmeans']['best_k']} clusters (silhouette: {clustering_results['kmeans']['best_score']:.3f})")
        print(f"GMM best: {clustering_results['gmm']['best_k']} clusters (silhouette: {clustering_results['gmm']['best_score']:.3f})")
        
        interpretations = clusterer.interpret_clusters(clustering_features, clustering_results)
        
        if interpretations.get('error'):
            print(f"\nClustering failed: {interpretations['error']}")
            clustering_results = None
            interpretations = None
        else:
            print(f"\nUsing {interpretations['method_used']} clustering:")
            for cluster_id, info in interpretations['cluster_interpretations'].items():
                print(f"  {info['description']} ({info['size']} sessions)")
    else:
        print("\nInsufficient data for clustering (need >=2 sessions)")
        clustering_results = None
        interpretations = None
    
    # Save outputs
    output_dir = Path(telemetry_dir).parent / "processed"
    output_dir.mkdir(exist_ok=True)
    
    attempts_df.to_csv(output_dir / "attempt_features.csv", index=False)
    sessions_df.to_csv(output_dir / "session_features.csv", index=False)
    
    if clustering_results and clustering_results.get('kmeans', {}).get('best_k') is not None:
        with open(output_dir / "clustering_results.json", 'w') as f:
            # Convert numpy types to native Python for JSON serialization
            serializable_results = {
                'kmeans': {
                    'best_k': int(clustering_results['kmeans']['best_k']),
                    'best_score': float(clustering_results['kmeans']['best_score'])
                },
                'gmm': {
                    'best_k': int(clustering_results['gmm']['best_k']),
                    'best_score': float(clustering_results['gmm']['best_score'])
                }
            }
            json.dump(serializable_results, f, indent=2)
        
        with open(output_dir / "cluster_interpretations.json", 'w') as f:
            json.dump(interpretations, f, indent=2)
    
    print(f"\nAnalysis complete. Results saved to {output_dir}")
    print("  - attempt_features.csv: Per-attempt metrics")
    print("  - session_features.csv: Per-session aggregated metrics")
    if clustering_results and clustering_results.get('kmeans', {}).get('best_k') is not None:
        print("  - clustering_results.json: Clustering model performance")
        print("  - cluster_interpretations.json: Player archetype descriptions")

if __name__ == "__main__":
    main()