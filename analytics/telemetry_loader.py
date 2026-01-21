import pandas as pd
import json
from pathlib import Path
from typing import List, Dict, Any

class TelemetryLoader:
    def __init__(self, data_dir: str):
        self.data_dir = Path(data_dir)
    
    def load_session(self, session_file: str) -> pd.DataFrame:
        file_path = self.data_dir / session_file
        return pd.read_csv(file_path)
    
    def load_all_sessions(self) -> pd.DataFrame:
        csv_files = list(self.data_dir.glob("*.csv"))
        if not csv_files:
            return pd.DataFrame()
        
        sessions = []
        for file_path in csv_files:
            df = pd.read_csv(file_path)
            sessions.append(df)
        
        return pd.concat(sessions, ignore_index=True)