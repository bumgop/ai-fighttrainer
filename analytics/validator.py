import pandas as pd
from typing import List, Dict, Any

class ValidationResult:
    def __init__(self):
        self.errors = []
        self.warnings = []
        self.session_count = 0
        self.event_count = 0
    
    def add_error(self, message: str):
        self.errors.append(message)
    
    def add_warning(self, message: str):
        self.warnings.append(message)
    
    def is_valid(self) -> bool:
        return len(self.errors) == 0

class TelemetryValidator:
    REQUIRED_COLUMNS = ['session_id', 'minigame_id', 'event_type', 'timestamp_ms', 'payload']
    VALID_EVENT_TYPES = ['minigame_start', 'minigame_end', 'input', 'result']
    VALID_MINIGAME_IDS = ['anti_air_reaction_test', 'hit_confirm_test', 'whiff_punish_test', 'defense_under_pressure_test']
    
    def validate(self, df: pd.DataFrame) -> ValidationResult:
        result = ValidationResult()
        
        if df.empty:
            result.add_error("No data to validate")
            return result
        
        self._validate_schema(df, result)
        self._validate_data_types(df, result)
        self._validate_enum_values(df, result)
        self._validate_structure(df, result)
        
        result.session_count = df['session_id'].nunique()
        result.event_count = len(df)
        
        return result
    
    def _validate_schema(self, df: pd.DataFrame, result: ValidationResult):
        missing_cols = [col for col in self.REQUIRED_COLUMNS if col not in df.columns]
        if missing_cols:
            result.add_error(f"Missing required columns: {missing_cols}")
    
    def _validate_data_types(self, df: pd.DataFrame, result: ValidationResult):
        if 'timestamp_ms' in df.columns and not pd.api.types.is_numeric_dtype(df['timestamp_ms']):
            result.add_error("timestamp_ms must be numeric")
    
    def _validate_enum_values(self, df: pd.DataFrame, result: ValidationResult):
        if 'event_type' in df.columns:
            invalid_events = df[~df['event_type'].isin(self.VALID_EVENT_TYPES)]['event_type'].unique()
            if len(invalid_events) > 0:
                result.add_warning(f"Unknown event types: {invalid_events}")
        
        if 'minigame_id' in df.columns:
            invalid_minigames = df[~df['minigame_id'].isin(self.VALID_MINIGAME_IDS)]['minigame_id'].unique()
            if len(invalid_minigames) > 0:
                result.add_warning(f"Unknown minigame IDs: {invalid_minigames}")
    
    def _validate_structure(self, df: pd.DataFrame, result: ValidationResult):
        if 'session_id' not in df.columns or 'timestamp_ms' not in df.columns:
            return
        
        for session_id in df['session_id'].unique():
            session_df = df[df['session_id'] == session_id].sort_values('timestamp_ms')
            
            if not session_df['timestamp_ms'].is_monotonic_increasing:
                result.add_error(f"Session {session_id}: timestamps not monotonic")
            
            has_start = (session_df['event_type'] == 'minigame_start').any()
            has_end = (session_df['event_type'] == 'minigame_end').any()
            
            if not has_start:
                result.add_warning(f"Session {session_id}: missing minigame_start event")
            if not has_end:
                result.add_warning(f"Session {session_id}: missing minigame_end event")