# Train Your Kombat - Project State

## Core Architecture

### Session Management
- **MinigameSession**: Standardized wrapper providing 1-second preparation delay, automatic minigame discovery, telemetry management, and return-to-menu functionality
- **TelemetryLogger**: CSV-based event logging to user://telemetry/ directory with structured JSON payloads
- **TimerService**: Session-relative timing for performance measurement

### Minigame System
- **MinigameBase**: Abstract base class with Initialize/StartMinigame/EndMinigame contract and proper session ID tracking
- **MinigameRegistry**: Singleton registry containing metadata for all minigames (ID, display name, scene path, description)
- **Completion Flow**: Minigames signal completion via RequestEnd callback, triggering return button display
- **Session ID Management**: Consistent session tracking across all telemetry events

### User Interface
- **MainMenuController**: Menu navigation with Previous/Next/Start buttons for minigame selection
- **Return Button**: Standardized bottom-right positioned button appearing after minigame completion

## Implemented Minigames
- **AntiAirController**: Timing-based reaction test with visual threat movement
- **HitConfirmController**: Decision-making under uncertainty with hit/block scenarios
- **WhiffPunishController**: Frame data training with visual progress bar and attack phases
- **DefenseUnderPressureController**: Sequential blocking challenge with mixed attack patterns

## Data Architecture
- **TelemetryEvent**: Structured events with session_id, minigame_id, event_type, timestamp_ms, payload_json
- **CSV Export**: Comma-separated format with quoted JSON payloads for external analysis
- **File-Based Exchange**: Telemetry data prepared for Python ML analytics integration

## Scene Structure
- All minigame scenes use MinigameSession wrapper with consistent node hierarchy
- Automatic minigame discovery eliminates hardcoded scene references
- Standardized entry/exit flow with preparation delay and clean return navigation

## Analytics Pipeline
- **Python Environment**: Isolated venv with scikit-learn/pandas/numpy dependencies
- **TelemetryLoader**: CSV file loading from Godot telemetry output
- **TelemetryValidator**: Schema and structural validation with error/warning reporting
- **FeatureExtractor**: Per-attempt feature extraction from minigame events with outcome classification
- **SessionAggregator**: Per-session skill metrics aggregation (means, rates, consistency measures)
- **FeatureSelector**: Style-based feature selection for clustering (timing consistency, decision patterns)
- **PlayerClustering**: K-Means and Gaussian Mixture Models with silhouette score evaluation
- **Cluster Interpretation**: Automated behavioral archetype descriptions with distinctive feature analysis
- **WeaknessClassifier**: Supervised learning models (Logistic Regression, Decision Trees) for weakness prediction
- **Model Explainability**: Feature importance analysis and decision rule extraction for interpretable predictions
- **TrendAnalyzer**: Longitudinal analysis with session ordering, metric smoothing, and trend classification
- **Improvement Tracking**: Rolling averages, exponential smoothing, and trend assessment (improving/flat/regressing)
- **Robust Error Handling**: Graceful handling of insufficient data diversity cases
- **Feature Dictionary**: Documented feature definitions for ML explainability
- **Integrated Pipeline**: End-to-end analysis from raw telemetry to trends, weaknesses, and cluster assignments

## Player Feedback System
- **InsightContract**: Structured taxonomy of 10 insight types with canonical vocabulary definitions
- **InsightVocabulary**: Plain-language definitions, behavior causes, and supporting metrics for each insight type
- **InsightDataStructure**: Structured format with severity levels, confidence levels, contributing factors, and explanations
- **ML Source Mapping**: Explicit mapping between analytics components and insight types they can generate
- **Validation System**: Ensures insights are traceable to specific data points and have required supporting evidence

## Known Gaps
- Insight generation logic (Phase 6.2)
- Player-facing feedback presentation (Phase 6.3)
- Actionable guidance system (Phase 6.4)