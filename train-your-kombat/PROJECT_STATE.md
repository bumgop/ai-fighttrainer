# Train Your Kombat - Project State

## Core Architecture

### Session Management
- **MinigameSession**: Standardized wrapper providing 1-second preparation delay, automatic minigame discovery, telemetry management, and return-to-menu functionality
- **TelemetryLogger**: CSV-based event logging to user://telemetry/ directory with structured JSON payloads
- **TimerService**: Session-relative timing for performance measurement

### Minigame System
- **MinigameBase**: Abstract base class with Initialize/StartMinigame/EndMinigame contract
- **MinigameRegistry**: Singleton registry containing metadata for all minigames (ID, display name, scene path, description)
- **Completion Flow**: Minigames signal completion via RequestEnd callback, triggering return button display

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

## Known Gaps
- Python ML analytics system (deferred to later phases)
- Advanced UI polish and visual effects
- Additional minigame types beyond core 4 implementations