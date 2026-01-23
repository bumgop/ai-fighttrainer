import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.mixture import GaussianMixture
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score
from typing import Dict, Tuple, List
import json

class PlayerClustering:
    def __init__(self, random_state=42):
        self.random_state = random_state
        self.scaler = StandardScaler()
        self.best_kmeans = None
        self.best_gmm = None
        self.feature_names = None
        
    def fit_clustering_models(self, feature_df: pd.DataFrame) -> Dict:
        # Prepare data
        session_ids = feature_df['session_id'].values
        features = feature_df.drop('session_id', axis=1)
        self.feature_names = features.columns.tolist()
        
        # Check for any remaining NaN values
        if features.isna().any().any():
            print("Warning: NaN values detected, filling with 0")
            features = features.fillna(0)
        
        # Scale features
        X_scaled = self.scaler.fit_transform(features)
        
        # Check for any infinite values after scaling
        if not np.isfinite(X_scaled).all():
            print("Warning: Non-finite values after scaling, replacing with 0")
            X_scaled = np.nan_to_num(X_scaled, nan=0.0, posinf=0.0, neginf=0.0)
        
        results = {
            'kmeans': self._evaluate_kmeans(X_scaled, session_ids),
            'gmm': self._evaluate_gmm(X_scaled, session_ids)
        }
        
        return results
    
    def _evaluate_kmeans(self, X: np.ndarray, session_ids: np.ndarray) -> Dict:
        best_score = -1
        best_k = None
        best_model = None
        
        results = {}
        
        for k in range(2, min(6, len(X))):  # Test 2-5 clusters
            kmeans = KMeans(n_clusters=k, random_state=self.random_state, n_init=10)
            labels = kmeans.fit_predict(X)
            
            if len(np.unique(labels)) > 1:  # Need at least 2 clusters for silhouette
                score = silhouette_score(X, labels)
                results[k] = {
                    'silhouette_score': score,
                    'labels': labels,
                    'centroids': kmeans.cluster_centers_
                }
                
                if score > best_score:
                    best_score = score
                    best_k = k
                    best_model = kmeans
        
        self.best_kmeans = best_model
        
        return {
            'best_k': best_k,
            'best_score': best_score,
            'all_results': results,
            'session_assignments': dict(zip(session_ids, results[best_k]['labels'])) if best_k and best_k in results else {}
        }
    
    def _evaluate_gmm(self, X: np.ndarray, session_ids: np.ndarray) -> Dict:
        best_score = -1
        best_k = None
        best_model = None
        
        results = {}
        
        for k in range(2, min(6, len(X))):
            gmm = GaussianMixture(n_components=k, random_state=self.random_state)
            labels = gmm.fit_predict(X)
            
            if len(np.unique(labels)) > 1:
                score = silhouette_score(X, labels)
                results[k] = {
                    'silhouette_score': score,
                    'labels': labels,
                    'means': gmm.means_
                }
                
                if score > best_score:
                    best_score = score
                    best_k = k
                    best_model = gmm
        
        self.best_gmm = best_model
        
        return {
            'best_k': best_k,
            'best_score': best_score,
            'all_results': results,
            'session_assignments': dict(zip(session_ids, results[best_k]['labels'])) if best_k and best_k in results else {}
        }
    
    def interpret_clusters(self, feature_df: pd.DataFrame, clustering_results: Dict) -> Dict:
        # Check if we have valid clustering results
        kmeans_valid = clustering_results['kmeans']['best_k'] is not None
        gmm_valid = clustering_results['gmm']['best_k'] is not None
        
        if not kmeans_valid and not gmm_valid:
            return {
                'method_used': 'none',
                'cluster_interpretations': {},
                'session_assignments': {},
                'error': 'Insufficient data for clustering - need more diverse sessions'
            }
        
        # Use the better performing model
        kmeans_score = clustering_results['kmeans']['best_score'] if kmeans_valid else -2
        gmm_score = clustering_results['gmm']['best_score'] if gmm_valid else -2
        
        if kmeans_valid and (not gmm_valid or kmeans_score >= gmm_score):
            best_method = 'kmeans'
            best_k = clustering_results['kmeans']['best_k']
            assignments = clustering_results['kmeans']['session_assignments']
            centroids = clustering_results['kmeans']['all_results'][best_k]['centroids']
        else:
            best_method = 'gmm'
            best_k = clustering_results['gmm']['best_k']
            assignments = clustering_results['gmm']['session_assignments']
            centroids = clustering_results['gmm']['all_results'][best_k]['means']
        
        # Create interpretations
        interpretations = {}
        features = feature_df.drop('session_id', axis=1)
        
        for cluster_id in range(len(centroids)):
            cluster_sessions = [sid for sid, cid in assignments.items() if cid == cluster_id]
            cluster_data = features[feature_df['session_id'].isin(cluster_sessions)]
            
            # Compute cluster statistics
            cluster_means = cluster_data.mean()
            overall_means = features.mean()
            
            # Identify distinctive characteristics (features > 1 std dev from overall mean)
            distinctive_features = []
            for feature in self.feature_names:
                if feature in cluster_means.index and feature in overall_means.index:
                    cluster_val = cluster_means[feature]
                    overall_val = overall_means[feature]
                    overall_std = features[feature].std()
                    
                    if abs(cluster_val - overall_val) > overall_std:
                        direction = "high" if cluster_val > overall_val else "low"
                        distinctive_features.append(f"{direction} {feature}")
            
            interpretations[cluster_id] = {
                'size': len(cluster_sessions),
                'distinctive_features': distinctive_features,
                'description': self._generate_cluster_description(cluster_id, distinctive_features)
            }
        
        return {
            'method_used': best_method,
            'cluster_interpretations': interpretations,
            'session_assignments': assignments
        }
    
    def _generate_cluster_description(self, cluster_id: int, distinctive_features: List[str]) -> str:
        # Generate human-readable cluster descriptions
        descriptions = {
            'high anti_air_reaction_test_early_rate': 'impatient/anticipatory',
            'high anti_air_reaction_test_late_rate': 'hesitant/slow reactions',
            'high hit_confirm_test_false_confirm_rate': 'autopilot tendency',
            'high hit_confirm_test_missed_confirm_rate': 'overly conservative',
            'high whiff_punish_test_early_rate': 'aggressive punish attempts',
            'high whiff_punish_test_unsafe_rate': 'risky timing',
            'low anti_air_reaction_test_timing_error_std': 'consistent timing',
            'high anti_air_reaction_test_timing_error_std': 'erratic timing'
        }
        
        traits = []
        for feature in distinctive_features:
            if feature in descriptions:
                traits.append(descriptions[feature])
        
        if not traits:
            return f"Cluster {cluster_id}: Balanced playstyle"
        
        return f"Cluster {cluster_id}: {', '.join(traits)} players"