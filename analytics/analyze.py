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
    
    # Weakness Classification
    if len(sessions_df) >= 3:  # Need minimum data for supervised learning
        print("\n=== Weakness Classification ===")
        from weakness_classifier import WeaknessClassifier
        
        classifier = WeaknessClassifier()
        labels_df = classifier.define_weakness_labels(sessions_df)
        
        print(f"Defined weakness labels for {len(labels_df)} sessions")
        weakness_cols = [col for col in labels_df.columns if col != 'session_id']
        for weakness in weakness_cols:
            positive_cases = labels_df[weakness].sum()
            print(f"  {weakness}: {positive_cases}/{len(labels_df)} sessions ({positive_cases/len(labels_df)*100:.1f}%)")
        
        training_results = classifier.train_weakness_models(sessions_df, labels_df)
        explanations = classifier.explain_weakness_predictions(sessions_df, labels_df)
        predictions = classifier.predict_weaknesses(sessions_df)
        
        print("\nWeakness model training complete")
        for weakness, result in training_results.items():
            if 'error' not in result:
                print(f"  {weakness}: {result['positive_cases']} positive cases")
    else:
        print("\nInsufficient data for weakness classification (need >=3 sessions)")
        training_results = None
        explanations = None
        predictions = None
    
    # Trend Analysis
    if len(sessions_df) >= 2:  # Need at least 2 sessions for trends
        print("\n=== Trend Analysis ===")
        from trend_analyzer import TrendAnalyzer
        
        analyzer = TrendAnalyzer()
        trend_results = analyzer.analyze_trends(sessions_df)
        
        if 'error' in trend_results:
            print(f"Trend analysis failed: {trend_results['error']}")
            trend_results = None
        else:
            print(f"Analyzed trends across {trend_results['session_count']} sessions")
            print(f"Metrics analyzed: {len(trend_results['metrics_analyzed'])}")
            
            overall = trend_results['trend_summaries']['overall']
            print(f"\nOverall assessment: {overall['overall_assessment']}")
            print(f"  Improving: {overall['improving_count']} metrics")
            print(f"  Stable: {overall['flat_count']} metrics")
            print(f"  Regressing: {overall['regressing_count']} metrics")
    else:
        print("\nInsufficient data for trend analysis (need >=2 sessions)")
        trend_results = None
    
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
    
    if training_results:
        with open(output_dir / "weakness_training_results.json", 'w') as f:
            json.dump(training_results, f, indent=2)
        
        with open(output_dir / "weakness_explanations.json", 'w') as f:
            json.dump(explanations, f, indent=2)
        
        with open(output_dir / "weakness_predictions.json", 'w') as f:
            json.dump(predictions, f, indent=2)
    
    if trend_results:
        with open(output_dir / "trend_analysis.json", 'w') as f:
            json.dump(trend_results, f, indent=2)
    
    print(f"\nAnalysis complete. Results saved to {output_dir}")
    print("  - attempt_features.csv: Per-attempt metrics")
    print("  - session_features.csv: Per-session aggregated metrics")
    if clustering_results and clustering_results.get('kmeans', {}).get('best_k') is not None:
        print("  - clustering_results.json: Clustering model performance")
        print("  - cluster_interpretations.json: Player archetype descriptions")
    if training_results:
        print("  - weakness_training_results.json: Model training statistics")
        print("  - weakness_explanations.json: Feature importance and decision rules")
        print("  - weakness_predictions.json: Per-session weakness probabilities")
    if trend_results:
        print("  - trend_analysis.json: Improvement trends and performance trajectories")

if __name__ == "__main__":
    main()