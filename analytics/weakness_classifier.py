import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report
from typing import Dict, List, Tuple
import json

class WeaknessClassifier:
    def __init__(self, random_state=42):
        self.random_state = random_state
        self.scaler = StandardScaler()
        self.models = {}
        self.feature_names = None
        
    def define_weakness_labels(self, df: pd.DataFrame) -> pd.DataFrame:
        """Define binary weakness labels based on feature thresholds"""
        labels_df = df[['session_id']].copy()
        
        # Inconsistent Timing - high variance in timing metrics
        timing_cols = [col for col in df.columns if 'timing_error_std' in col or 'window_offset_std' in col]
        if timing_cols:
            timing_variance = df[timing_cols].mean(axis=1, skipna=True)
            labels_df['inconsistent_timing'] = (timing_variance > timing_variance.quantile(0.7)).astype(int)
        else:
            labels_df['inconsistent_timing'] = 0
            
        # Poor Mixup Defense - high false confirm rate
        if 'hit_confirm_test_false_confirm_rate' in df.columns:
            labels_df['poor_mixup_defense'] = (df['hit_confirm_test_false_confirm_rate'] > 0.3).astype(int)
        else:
            labels_df['poor_mixup_defense'] = 0
            
        # Late Punish Tendency - high late/miss rates in whiff punish
        late_cols = [col for col in df.columns if 'late_rate' in col or 'miss_rate' in col]
        if late_cols:
            late_tendency = df[late_cols].mean(axis=1, skipna=True)
            labels_df['late_punish_tendency'] = (late_tendency > late_tendency.quantile(0.6)).astype(int)
        else:
            labels_df['late_punish_tendency'] = 0
            
        # Impatient Player - high early rates across minigames
        early_cols = [col for col in df.columns if 'early_rate' in col]
        if early_cols:
            early_tendency = df[early_cols].mean(axis=1, skipna=True)
            labels_df['impatient_player'] = (early_tendency > early_tendency.quantile(0.7)).astype(int)
        else:
            labels_df['impatient_player'] = 0
            
        return labels_df
    
    def train_weakness_models(self, feature_df: pd.DataFrame, labels_df: pd.DataFrame) -> Dict:
        """Train logistic regression and decision tree models for each weakness"""
        # Prepare features
        features = feature_df.drop('session_id', axis=1)
        self.feature_names = features.columns.tolist()
        
        # Handle missing values
        features = features.fillna(features.median())
        
        # Scale features
        X_scaled = self.scaler.fit_transform(features)
        
        results = {}
        weakness_types = [col for col in labels_df.columns if col != 'session_id']
        
        for weakness in weakness_types:
            y = labels_df[weakness].values
            
            # Skip if no positive cases
            if y.sum() == 0:
                results[weakness] = {'error': 'No positive cases found'}
                continue
                
            # Train Logistic Regression
            lr_model = LogisticRegression(random_state=self.random_state, max_iter=1000)
            lr_model.fit(X_scaled, y)
            
            # Train Decision Tree (shallow for interpretability)
            dt_model = DecisionTreeClassifier(max_depth=3, random_state=self.random_state)
            dt_model.fit(X_scaled, y)
            
            self.models[weakness] = {
                'logistic': lr_model,
                'decision_tree': dt_model
            }
            
            results[weakness] = {
                'positive_cases': int(y.sum()),
                'total_cases': len(y),
                'prevalence': float(y.mean()),
                'logistic_trained': True,
                'decision_tree_trained': True
            }
            
        return results
    
    def explain_weakness_predictions(self, feature_df: pd.DataFrame, labels_df: pd.DataFrame) -> Dict:
        """Generate explanations for weakness predictions"""
        explanations = {}
        features = feature_df.drop('session_id', axis=1)
        
        for weakness, models in self.models.items():
            if 'logistic' not in models:
                continue
                
            lr_model = models['logistic']
            dt_model = models['decision_tree']
            
            # Logistic regression feature importance
            feature_weights = dict(zip(self.feature_names, lr_model.coef_[0]))
            top_features = sorted(feature_weights.items(), key=lambda x: abs(x[1]), reverse=True)[:5]
            
            # Decision tree rules
            tree_rules = self._extract_tree_rules(dt_model, self.feature_names)
            
            explanations[weakness] = {
                'description': self._get_weakness_description(weakness),
                'key_indicators': [
                    {
                        'feature': feat,
                        'weight': float(weight),
                        'interpretation': 'increases risk' if weight > 0 else 'decreases risk'
                    }
                    for feat, weight in top_features
                ],
                'decision_rules': tree_rules
            }
            
        return explanations
    
    def predict_weaknesses(self, feature_df: pd.DataFrame) -> Dict:
        """Predict weakness probabilities for new sessions"""
        features = feature_df.drop('session_id', axis=1)
        features = features.fillna(features.median())
        X_scaled = self.scaler.transform(features)
        
        predictions = {}
        session_ids = feature_df['session_id'].values
        
        for weakness, models in self.models.items():
            if 'logistic' not in models:
                continue
                
            lr_model = models['logistic']
            probabilities = lr_model.predict_proba(X_scaled)[:, 1]  # Probability of weakness
            
            predictions[weakness] = dict(zip(session_ids, probabilities.astype(float)))
            
        return predictions
    
    def _extract_tree_rules(self, tree_model, feature_names: List[str]) -> List[str]:
        """Extract human-readable rules from decision tree"""
        tree = tree_model.tree_
        rules = []
        
        def recurse(node, depth, condition=""):
            if tree.children_left[node] != tree.children_right[node]:  # Not a leaf
                feature = feature_names[tree.feature[node]]
                threshold = tree.threshold[node]
                
                left_condition = f"{condition} AND {feature} <= {threshold:.3f}" if condition else f"{feature} <= {threshold:.3f}"
                right_condition = f"{condition} AND {feature} > {threshold:.3f}" if condition else f"{feature} > {threshold:.3f}"
                
                recurse(tree.children_left[node], depth + 1, left_condition)
                recurse(tree.children_right[node], depth + 1, right_condition)
            else:  # Leaf node
                value = tree.value[node][0]
                if len(value) > 1 and value[1] > value[0]:  # Positive class
                    rules.append(f"IF {condition} THEN weakness likely")
                    
        recurse(0, 0)
        return rules[:3]  # Return top 3 rules
    
    def _get_weakness_description(self, weakness: str) -> str:
        descriptions = {
            'inconsistent_timing': 'Player shows high variance in timing across attempts',
            'poor_mixup_defense': 'Player tends to autopilot confirm blocked hits',
            'late_punish_tendency': 'Player frequently misses or delays punish opportunities',
            'impatient_player': 'Player tends to input too early across minigames'
        }
        return descriptions.get(weakness, f'Weakness: {weakness}')