import pandas as pd
import json
from typing import Dict, Any, Optional

class FeatureExtractor:
    def extract_attempt_features(self, df: pd.DataFrame) -> pd.DataFrame:
        attempts = []
        
        # Handle NaN session_ids by filling them with a placeholder
        df = df.copy()
        df['session_id'] = df['session_id'].fillna('unknown_session')
        
        for session_id in df['session_id'].unique():
            session_df = df[df['session_id'] == session_id].sort_values('timestamp_ms')
            
            for minigame_id in session_df['minigame_id'].unique():
                minigame_df = session_df[session_df['minigame_id'] == minigame_id]
                features = self._extract_minigame_features(minigame_df, session_id, minigame_id)
                if features:
                    attempts.append(features)
        
        return pd.DataFrame(attempts)
    
    def _extract_minigame_features(self, df: pd.DataFrame, session_id: str, minigame_id: str) -> Optional[Dict[str, Any]]:
        if minigame_id == 'anti_air_reaction_test':
            return self._extract_anti_air_features(df, session_id)
        elif minigame_id == 'hit_confirm_test':
            return self._extract_hit_confirm_features(df, session_id)
        elif minigame_id == 'whiff_punish_test':
            return self._extract_whiff_punish_features(df, session_id)
        elif minigame_id == 'defense_under_pressure_test':
            return self._extract_defense_features(df, session_id)
        return None
    
    def _extract_anti_air_features(self, df: pd.DataFrame, session_id: str) -> Dict[str, Any]:
        result_events = df[df['event_type'].isin(['result', 'anti_air_attempt'])]
        if result_events.empty:
            return None
        
        result_event = result_events.iloc[0]
        payload = json.loads(result_event['payload'])
        
        return {
            'session_id': session_id,
            'minigame_id': 'anti_air_reaction_test',
            'outcome_success': 1 if payload.get('outcome') in ['correct', 'success'] else 0,
            'outcome_early': 1 if payload.get('outcome') == 'early' else 0,
            'outcome_late': 1 if payload.get('outcome') == 'late' else 0,
            'outcome_missed': 1 if payload.get('outcome') == 'missed' else 0,
            'timing_error_ms': payload.get('timing_ms', 0) if payload.get('outcome') in ['correct', 'success'] else None,
            'has_timing_data': 1 if payload.get('timing_ms') is not None else 0
        }
    
    def _extract_hit_confirm_features(self, df: pd.DataFrame, session_id: str) -> Dict[str, Any]:
        result_events = df[df['event_type'].isin(['result', 'hit_confirm_attempt'])]
        if result_events.empty:
            return None
        
        result_event = result_events.iloc[0]
        payload = json.loads(result_event['payload'])
        
        outcome = payload.get('outcome', '')
        
        return {
            'session_id': session_id,
            'minigame_id': 'hit_confirm_test',
            'outcome_correct': 1 if outcome in ['correct', 'correct_block', 'correct_confirm'] else 0,
            'outcome_false_confirm': 1 if 'false_confirm' in outcome else 0,
            'outcome_missed_confirm': 1 if 'missed_confirm' in outcome else 0,
            'decision_error': 1 if any(x in outcome for x in ['false_confirm', 'missed_confirm']) else 0,
            'hit_was_confirmed': 1 if payload.get('was_hit_confirmed', False) else 0
        }
    
    def _extract_whiff_punish_features(self, df: pd.DataFrame, session_id: str) -> Dict[str, Any]:
        result_events = df[df['event_type'].str.contains('whiff_punish', na=False)]
        if result_events.empty:
            return None
        
        result_event = result_events.iloc[0]
        payload = json.loads(result_event['payload'])
        
        return {
            'session_id': session_id,
            'minigame_id': 'whiff_punish_test',
            'outcome_correct': 1 if payload.get('outcome') == 'correct_whiff_punish' else 0,
            'outcome_early': 1 if payload.get('outcome') == 'early_whiff_punish' else 0,
            'outcome_unsafe': 1 if payload.get('outcome') == 'unsafe_whiff_punish' else 0,
            'outcome_late': 1 if payload.get('outcome') == 'late_whiff_punish' else 0,
            'outcome_missed': 1 if payload.get('outcome') == 'missed_punish' else 0,
            'window_offset_ms': payload.get('window_offset_ms') if payload.get('outcome') == 'correct_whiff_punish' else None,
            'phase_at_input': payload.get('phase_at_input', 'unknown')
        }
    
    def _extract_defense_features(self, df: pd.DataFrame, session_id: str) -> Dict[str, Any]:
        attack_events = df[df['event_type'] == 'defense_attack_result']
        string_events = df[df['event_type'] == 'defense_string_complete']
        
        if attack_events.empty:
            return None
        
        total_attacks = len(attack_events)
        correct_blocks = len(attack_events[attack_events['payload'].str.contains('correct', na=False)])
        
        features = {
            'session_id': session_id,
            'minigame_id': 'defense_under_pressure_test',
            'total_attacks': total_attacks,
            'correct_blocks': correct_blocks,
            'block_accuracy': correct_blocks / total_attacks if total_attacks > 0 else 0,
            'error_rate': (total_attacks - correct_blocks) / total_attacks if total_attacks > 0 else 0
        }
        
        if not string_events.empty:
            string_payload = json.loads(string_events.iloc[0]['payload'])
            features['string_success'] = 1 if string_payload.get('string_success', False) else 0
        
        return features