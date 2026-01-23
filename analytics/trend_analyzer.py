import pandas as pd
import numpy as np
from typing import Dict, List, Tuple
from datetime import datetime
import json

class TrendAnalyzer:
    def __init__(self):
        self.trend_thresholds = {
            'improving': 0.1,    # 10% improvement threshold
            'regressing': -0.1,  # 10% regression threshold
            'flat': 0.05         # Within 5% considered flat
        }
        
    def analyze_trends(self, sessions_df: pd.DataFrame) -> Dict:
        """Analyze improvement trends across all sessions"""
        if len(sessions_df) < 2:
            return {'error': 'Need at least 2 sessions for trend analysis'}
            
        # Order sessions by timestamp (using session_id as proxy for now)
        ordered_sessions = self._order_sessions(sessions_df)
        
        # Extract key metrics for trend analysis
        trend_metrics = self._select_trend_metrics(ordered_sessions)
        
        # Apply smoothing techniques
        smoothed_metrics = self._apply_smoothing(trend_metrics)
        
        # Classify trends
        trend_classifications = self._classify_trends(smoothed_metrics)
        
        # Generate trend summaries
        trend_summaries = self._generate_trend_summaries(trend_classifications, smoothed_metrics)
        
        return {
            'session_count': len(ordered_sessions),
            'metrics_analyzed': list(trend_metrics.keys()),
            'trend_classifications': trend_classifications,
            'trend_summaries': trend_summaries,
            'smoothed_data': smoothed_metrics
        }
    
    def _order_sessions(self, df: pd.DataFrame) -> pd.DataFrame:
        """Order sessions chronologically (using session_id as timestamp proxy)"""
        # For now, assume session_id contains timestamp info or use row order
        # In real implementation, would parse actual timestamps
        return df.sort_values('session_id').reset_index(drop=True)
    
    def _select_trend_metrics(self, df: pd.DataFrame) -> Dict[str, List[float]]:
        """Select key metrics for trend analysis"""
        metrics = {}
        
        # Success rates (performance metrics)
        success_cols = [col for col in df.columns if 'success_rate' in col or 'correct_rate' in col]
        for col in success_cols:
            if col in df.columns:
                values = df[col].fillna(0).tolist()
                if any(v > 0 for v in values):  # Only include if has data
                    metrics[col] = values
        
        # Consistency metrics (lower is better)
        consistency_cols = [col for col in df.columns if 'std' in col and 'timing' in col]
        for col in consistency_cols:
            if col in df.columns:
                values = df[col].fillna(df[col].median()).tolist()
                if any(v > 0 for v in values):
                    metrics[col] = values
        
        # Error rates (lower is better)
        error_cols = [col for col in df.columns if any(x in col for x in ['early_rate', 'late_rate', 'false_confirm_rate'])]
        for col in error_cols:
            if col in df.columns:
                values = df[col].fillna(0).tolist()
                if any(v > 0 for v in values):
                    metrics[col] = values
        
        return metrics
    
    def _apply_smoothing(self, metrics: Dict[str, List[float]]) -> Dict[str, Dict]:
        """Apply smoothing techniques to metrics"""
        smoothed = {}
        
        for metric_name, values in metrics.items():
            if len(values) < 2:
                continue
                
            smoothed[metric_name] = {
                'raw_values': values,
                'rolling_average': self._rolling_average(values, window=2),
                'exponential_smoothing': self._exponential_smoothing(values, alpha=0.3),
                'simple_delta': values[-1] - values[0] if len(values) >= 2 else 0
            }
        
        return smoothed
    
    def _rolling_average(self, values: List[float], window: int = 2) -> List[float]:
        """Calculate rolling average"""
        if len(values) < window:
            return values
            
        smoothed = []
        for i in range(len(values)):
            if i < window - 1:
                smoothed.append(values[i])
            else:
                avg = sum(values[i-window+1:i+1]) / window
                smoothed.append(avg)
        return smoothed
    
    def _exponential_smoothing(self, values: List[float], alpha: float = 0.3) -> List[float]:
        """Apply exponential smoothing"""
        if not values:
            return []
            
        smoothed = [values[0]]
        for i in range(1, len(values)):
            smoothed_val = alpha * values[i] + (1 - alpha) * smoothed[i-1]
            smoothed.append(smoothed_val)
        return smoothed
    
    def _classify_trends(self, smoothed_metrics: Dict[str, Dict]) -> Dict[str, str]:
        """Classify trends as improving, flat, or regressing"""
        classifications = {}
        
        for metric_name, data in smoothed_metrics.items():
            if len(data['raw_values']) < 2:
                classifications[metric_name] = 'insufficient_data'
                continue
                
            # Use exponential smoothing for trend classification
            smoothed_values = data['exponential_smoothing']
            start_val = smoothed_values[0]
            end_val = smoothed_values[-1]
            
            # Calculate relative change
            if start_val == 0:
                relative_change = 1.0 if end_val > 0 else 0.0
            else:
                relative_change = (end_val - start_val) / abs(start_val)
            
            # Classify based on metric type and change direction
            is_lower_better = any(x in metric_name for x in ['std', 'error', 'early_rate', 'late_rate', 'false_confirm'])
            
            if is_lower_better:
                # For metrics where lower is better (errors, variance)
                if relative_change <= -self.trend_thresholds['improving']:
                    classifications[metric_name] = 'improving'
                elif relative_change >= self.trend_thresholds['improving']:
                    classifications[metric_name] = 'regressing'
                else:
                    classifications[metric_name] = 'flat'
            else:
                # For metrics where higher is better (success rates)
                if relative_change >= self.trend_thresholds['improving']:
                    classifications[metric_name] = 'improving'
                elif relative_change <= self.trend_thresholds['regressing']:
                    classifications[metric_name] = 'regressing'
                else:
                    classifications[metric_name] = 'flat'
        
        return classifications
    
    def _generate_trend_summaries(self, classifications: Dict[str, str], smoothed_data: Dict[str, Dict]) -> Dict[str, Dict]:
        """Generate human-readable trend summaries"""
        summaries = {}
        
        # Overall trend summary
        trend_counts = {'improving': 0, 'flat': 0, 'regressing': 0, 'insufficient_data': 0}
        for trend in classifications.values():
            trend_counts[trend] += 1
        
        summaries['overall'] = {
            'total_metrics': len(classifications),
            'improving_count': trend_counts['improving'],
            'flat_count': trend_counts['flat'],
            'regressing_count': trend_counts['regressing'],
            'overall_assessment': self._get_overall_assessment(trend_counts)
        }
        
        # Per-metric summaries
        summaries['per_metric'] = {}
        for metric_name, trend in classifications.items():
            if trend == 'insufficient_data':
                continue
                
            data = smoothed_data[metric_name]
            start_val = data['exponential_smoothing'][0]
            end_val = data['exponential_smoothing'][-1]
            
            summaries['per_metric'][metric_name] = {
                'trend': trend,
                'start_value': round(start_val, 3),
                'end_value': round(end_val, 3),
                'change_magnitude': round(abs(end_val - start_val), 3),
                'description': self._get_metric_description(metric_name, trend, start_val, end_val)
            }
        
        return summaries
    
    def _get_overall_assessment(self, trend_counts: Dict[str, int]) -> str:
        """Generate overall player assessment"""
        total = trend_counts['improving'] + trend_counts['flat'] + trend_counts['regressing']
        if total == 0:
            return 'insufficient_data'
            
        improving_pct = trend_counts['improving'] / total
        regressing_pct = trend_counts['regressing'] / total
        
        if improving_pct >= 0.6:
            return 'strong_improvement'
        elif improving_pct >= 0.4:
            return 'moderate_improvement'
        elif regressing_pct >= 0.6:
            return 'concerning_regression'
        elif regressing_pct >= 0.4:
            return 'some_regression'
        else:
            return 'stable_performance'
    
    def _get_metric_description(self, metric_name: str, trend: str, start_val: float, end_val: float) -> str:
        """Generate human-readable metric description"""
        metric_type = self._get_metric_type(metric_name)
        change_direction = 'increased' if end_val > start_val else 'decreased'
        
        if trend == 'improving':
            return f"{metric_type} has {change_direction}, showing improvement"
        elif trend == 'regressing':
            return f"{metric_type} has {change_direction}, showing regression"
        else:
            return f"{metric_type} has remained relatively stable"
    
    def _get_metric_type(self, metric_name: str) -> str:
        """Get human-readable metric type"""
        if 'success_rate' in metric_name or 'correct_rate' in metric_name:
            return 'Success rate'
        elif 'timing_error_std' in metric_name:
            return 'Timing consistency'
        elif 'early_rate' in metric_name:
            return 'Early input tendency'
        elif 'late_rate' in metric_name:
            return 'Late input tendency'
        elif 'false_confirm_rate' in metric_name:
            return 'False confirm rate'
        else:
            return 'Performance metric'