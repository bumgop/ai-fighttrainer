#!/usr/bin/env python3

import pandas as pd
import numpy as np
from trend_analyzer import TrendAnalyzer

def create_trend_test_data():
    """Create synthetic session data with known trend patterns"""
    np.random.seed(42)
    
    sessions = []
    
    # Create 6 sessions with different trend patterns
    for i in range(6):
        session_data = {
            'session_id': f'session_{i:03d}',  # Ordered session IDs
        }
        
        # Improving success rate (starts low, gets better)
        base_success = 0.3 + (i * 0.1) + np.random.normal(0, 0.05)
        session_data['anti_air_reaction_test_success_rate'] = max(0, min(1, base_success))
        
        # Improving timing consistency (std decreases over time)
        base_timing_std = 80 - (i * 10) + np.random.normal(0, 5)
        session_data['anti_air_reaction_test_timing_error_std'] = max(10, base_timing_std)
        
        # Regressing false confirm rate (gets worse over time)
        base_false_confirm = 0.1 + (i * 0.05) + np.random.normal(0, 0.02)
        session_data['hit_confirm_test_false_confirm_rate'] = max(0, min(1, base_false_confirm))
        
        # Flat performance (stays roughly the same)
        session_data['whiff_punish_test_correct_rate'] = 0.6 + np.random.normal(0, 0.05)
        
        # Add some noise to other metrics
        session_data['anti_air_reaction_test_early_rate'] = np.random.uniform(0.1, 0.3)
        session_data['whiff_punish_test_late_rate'] = np.random.uniform(0.1, 0.4)
        
        sessions.append(session_data)
    
    return pd.DataFrame(sessions)

def main():
    print("=== Trend Analysis Test ===")
    
    # Create test data with known patterns
    test_df = create_trend_test_data()
    print(f"Created test data with {len(test_df)} sessions")
    
    # Show the data progression
    print("\\nData progression:")
    key_metrics = ['anti_air_reaction_test_success_rate', 'anti_air_reaction_test_timing_error_std', 'hit_confirm_test_false_confirm_rate']
    for metric in key_metrics:
        values = test_df[metric].round(3).tolist()
        print(f"  {metric}: {values}")
    
    # Run trend analysis
    analyzer = TrendAnalyzer()
    results = analyzer.analyze_trends(test_df)
    
    if 'error' in results:
        print(f"\\nError: {results['error']}")
        return
    
    print(f"\\nTrend Analysis Results:")
    print(f"Sessions analyzed: {results['session_count']}")
    print(f"Metrics analyzed: {len(results['metrics_analyzed'])}")
    
    # Show trend classifications
    print(f"\\nTrend Classifications:")
    for metric, trend in results['trend_classifications'].items():
        print(f"  {metric}: {trend}")
    
    # Show overall assessment
    overall = results['trend_summaries']['overall']
    print(f"\\nOverall Assessment: {overall['overall_assessment']}")
    print(f"  Improving: {overall['improving_count']} metrics")
    print(f"  Stable: {overall['flat_count']} metrics")
    print(f"  Regressing: {overall['regressing_count']} metrics")
    
    # Show detailed metric summaries
    print(f"\\nDetailed Metric Summaries:")
    for metric, summary in results['trend_summaries']['per_metric'].items():
        print(f"  {metric}:")
        print(f"    Trend: {summary['trend']}")
        print(f"    Start -> End: {summary['start_value']:.3f} -> {summary['end_value']:.3f}")
        print(f"    Change: {summary['change_magnitude']:.3f}")
        print(f"    Description: {summary['description']}")

if __name__ == "__main__":
    main()