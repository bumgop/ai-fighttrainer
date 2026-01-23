import pandas as pd
import numpy as np
from typing import Dict, Any

class SessionAggregator:
    def aggregate_session_features(self, attempts_df: pd.DataFrame) -> pd.DataFrame:
        if attempts_df.empty:
            return pd.DataFrame()
        
        sessions = []
        
        for session_id in attempts_df['session_id'].unique():
            session_attempts = attempts_df[attempts_df['session_id'] == session_id]
            session_features = {'session_id': session_id}
            
            for minigame_id in session_attempts['minigame_id'].unique():
                minigame_attempts = session_attempts[session_attempts['minigame_id'] == minigame_id]
                minigame_features = self._aggregate_minigame_session(minigame_attempts, minigame_id)
                session_features.update(minigame_features)
            
            sessions.append(session_features)
        
        return pd.DataFrame(sessions)
    
    def _aggregate_minigame_session(self, df: pd.DataFrame, minigame_id: str) -> Dict[str, Any]:
        prefix = f"{minigame_id}_"
        
        if minigame_id == 'anti_air_reaction_test':
            return self._aggregate_anti_air(df, prefix)
        elif minigame_id == 'hit_confirm_test':
            return self._aggregate_hit_confirm(df, prefix)
        elif minigame_id == 'whiff_punish_test':
            return self._aggregate_whiff_punish(df, prefix)
        elif minigame_id == 'defense_under_pressure_test':
            return self._aggregate_defense(df, prefix)
        return {}
    
    def _aggregate_anti_air(self, df: pd.DataFrame, prefix: str) -> Dict[str, Any]:
        return {
            f"{prefix}success_rate": df['outcome_success'].mean(),
            f"{prefix}early_rate": df['outcome_early'].mean(),
            f"{prefix}late_rate": df['outcome_late'].mean(),
            f"{prefix}miss_rate": df['outcome_missed'].mean(),
            f"{prefix}timing_error_mean": df['timing_error_ms'].mean() if df['timing_error_ms'].notna().any() else np.nan,
            f"{prefix}timing_error_std": df['timing_error_ms'].std() if df['timing_error_ms'].notna().any() else np.nan,
            f"{prefix}attempts": len(df)
        }
    
    def _aggregate_hit_confirm(self, df: pd.DataFrame, prefix: str) -> Dict[str, Any]:
        return {
            f"{prefix}correct_rate": df['outcome_correct'].mean(),
            f"{prefix}false_confirm_rate": df['outcome_false_confirm'].mean(),
            f"{prefix}missed_confirm_rate": df['outcome_missed_confirm'].mean(),
            f"{prefix}decision_error_rate": df['decision_error'].mean(),
            f"{prefix}attempts": len(df)
        }
    
    def _aggregate_whiff_punish(self, df: pd.DataFrame, prefix: str) -> Dict[str, Any]:
        return {
            f"{prefix}correct_rate": df['outcome_correct'].mean(),
            f"{prefix}early_rate": df['outcome_early'].mean(),
            f"{prefix}unsafe_rate": df['outcome_unsafe'].mean(),
            f"{prefix}late_rate": df['outcome_late'].mean(),
            f"{prefix}miss_rate": df['outcome_missed'].mean(),
            f"{prefix}window_offset_mean": df['window_offset_ms'].mean() if df['window_offset_ms'].notna().any() else np.nan,
            f"{prefix}window_offset_std": df['window_offset_ms'].std() if df['window_offset_ms'].notna().any() else np.nan,
            f"{prefix}attempts": len(df)
        }
    
    def _aggregate_defense(self, df: pd.DataFrame, prefix: str) -> Dict[str, Any]:
        return {
            f"{prefix}block_accuracy_mean": df['block_accuracy'].mean(),
            f"{prefix}block_accuracy_std": df['block_accuracy'].std(),
            f"{prefix}error_rate_mean": df['error_rate'].mean(),
            f"{prefix}total_attacks_mean": df['total_attacks'].mean(),
            f"{prefix}string_success_rate": df['string_success'].mean() if 'string_success' in df.columns else np.nan,
            f"{prefix}attempts": len(df)
        }