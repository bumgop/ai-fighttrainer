#!/usr/bin/env python3

import pandas as pd
import numpy as np
from weakness_classifier import WeaknessClassifier

def create_test_data():
    """Create synthetic session data with known weaknesses"""
    np.random.seed(42)
    
    sessions = []
    for i in range(10):
        session_data = {
            'session_id': f'test_session_{i}',
            'anti_air_reaction_test_success_rate': np.random.uniform(0.3, 0.9),
            'anti_air_reaction_test_early_rate': np.random.uniform(0.0, 0.4),
            'anti_air_reaction_test_late_rate': np.random.uniform(0.0, 0.3),
            'anti_air_reaction_test_timing_error_std': np.random.uniform(10, 80),
            'hit_confirm_test_false_confirm_rate': np.random.uniform(0.0, 0.6),
            'hit_confirm_test_missed_confirm_rate': np.random.uniform(0.0, 0.4),
            'whiff_punish_test_late_rate': np.random.uniform(0.0, 0.5),
            'whiff_punish_test_window_offset_std': np.random.uniform(5, 50)
        }
        
        # Create specific weakness patterns
        if i < 3:  # Inconsistent timing players
            session_data['anti_air_reaction_test_timing_error_std'] = np.random.uniform(60, 100)
            session_data['whiff_punish_test_window_offset_std'] = np.random.uniform(40, 80)
        elif i < 6:  # Poor mixup defense players  
            session_data['hit_confirm_test_false_confirm_rate'] = np.random.uniform(0.4, 0.8)
        elif i < 8:  # Late punish tendency players
            session_data['whiff_punish_test_late_rate'] = np.random.uniform(0.4, 0.7)
        else:  # Impatient players
            session_data['anti_air_reaction_test_early_rate'] = np.random.uniform(0.3, 0.6)
            
        sessions.append(session_data)
    
    return pd.DataFrame(sessions)

def main():
    print("=== Weakness Classification Test ===")
    
    # Create test data
    test_df = create_test_data()
    print(f"Created test data with {len(test_df)} sessions")
    
    # Initialize classifier
    classifier = WeaknessClassifier()
    
    # Define weakness labels
    labels_df = classifier.define_weakness_labels(test_df)
    print(f"\nWeakness label distribution:")
    weakness_cols = [col for col in labels_df.columns if col != 'session_id']
    for weakness in weakness_cols:
        positive_cases = labels_df[weakness].sum()
        print(f"  {weakness}: {positive_cases}/{len(labels_df)} sessions ({positive_cases/len(labels_df)*100:.1f}%)")
    
    # Train models
    training_results = classifier.train_weakness_models(test_df, labels_df)
    print(f"\nModel training results:")
    for weakness, result in training_results.items():
        if 'error' not in result:
            print(f"  {weakness}: {result['positive_cases']} positive cases, prevalence: {result['prevalence']:.2f}")
        else:
            print(f"  {weakness}: {result['error']}")
    
    # Generate explanations
    explanations = classifier.explain_weakness_predictions(test_df, labels_df)
    print(f"\nWeakness explanations generated for {len(explanations)} weaknesses")
    
    for weakness, explanation in explanations.items():
        print(f"\n{weakness.upper()}:")
        print(f"  Description: {explanation['description']}")
        print(f"  Key indicators:")
        for indicator in explanation['key_indicators'][:3]:
            print(f"    - {indicator['feature']}: {indicator['interpretation']} (weight: {indicator['weight']:.3f})")
        if explanation['decision_rules']:
            print(f"  Decision rules:")
            for rule in explanation['decision_rules'][:2]:
                print(f"    - {rule}")
    
    # Make predictions
    predictions = classifier.predict_weaknesses(test_df)
    print(f"\nWeakness predictions:")
    for weakness, session_probs in predictions.items():
        high_risk_sessions = [sid for sid, prob in session_probs.items() if prob > 0.5]
        print(f"  {weakness}: {len(high_risk_sessions)} high-risk sessions")

if __name__ == "__main__":
    main()