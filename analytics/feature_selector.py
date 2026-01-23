import pandas as pd
import numpy as np
from typing import List, Dict

class FeatureSelector:
    def __init__(self):
        # Features that reflect playing style rather than performance ceiling
        self.style_features = [
            # Timing consistency (not accuracy)
            'anti_air_reaction_test_timing_error_std',
            'whiff_punish_test_window_offset_std',
            
            # Decision patterns
            'hit_confirm_test_false_confirm_rate',
            'hit_confirm_test_missed_confirm_rate',
            
            # Defensive tendencies
            'defense_under_pressure_test_block_accuracy_std',
            
            # Error type distributions (style indicators)
            'anti_air_reaction_test_early_rate',
            'anti_air_reaction_test_late_rate',
            'whiff_punish_test_early_rate',
            'whiff_punish_test_unsafe_rate',
            'whiff_punish_test_late_rate'
        ]
    
    def select_clustering_features(self, df: pd.DataFrame) -> pd.DataFrame:
        available_features = [f for f in self.style_features if f in df.columns]
        
        if not available_features:
            raise ValueError("No clustering features available in dataset")
        
        # Select features and handle missing values
        feature_df = df[['session_id'] + available_features].copy()
        
        # Remove features that are all NaN
        features_to_keep = []
        for col in available_features:
            if not feature_df[col].isna().all():
                features_to_keep.append(col)
        
        if not features_to_keep:
            raise ValueError("All clustering features contain only NaN values")
        
        # Keep only valid features
        feature_df = feature_df[['session_id'] + features_to_keep]
        
        # Fill remaining NaN with median, then 0 if median is still NaN
        for col in features_to_keep:
            if feature_df[col].isna().any():
                median_val = feature_df[col].median()
                if pd.isna(median_val):
                    median_val = 0.0
                feature_df[col] = feature_df[col].fillna(median_val)
        
        return feature_df
    
    def get_feature_justification(self) -> Dict[str, str]:
        return {
            'anti_air_reaction_test_timing_error_std': 'Timing consistency - distinguishes precise vs erratic players',
            'whiff_punish_test_window_offset_std': 'Punish timing consistency - execution reliability',
            'hit_confirm_test_false_confirm_rate': 'Autopilot tendency - decision-making discipline',
            'hit_confirm_test_missed_confirm_rate': 'Conservative tendency - risk aversion',
            'defense_under_pressure_test_block_accuracy_std': 'Defensive consistency under pressure',
            'anti_air_reaction_test_early_rate': 'Impatience/anticipation tendency',
            'anti_air_reaction_test_late_rate': 'Slow reaction/hesitation tendency',
            'whiff_punish_test_early_rate': 'Aggressive/impatient punish attempts',
            'whiff_punish_test_unsafe_rate': 'Risky timing errors',
            'whiff_punish_test_late_rate': 'Hesitant/slow punish recognition'
        }