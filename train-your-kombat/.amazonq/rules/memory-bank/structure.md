# Train Your Kombat - Project Structure

## Directory Organization

### `/Scripts/` - Core Application Logic
- **`Core/`** - Fundamental game systems
  - `GameSession.cs` - Main session orchestrator and minigame lifecycle manager
  - `MinigameBase.cs` - Abstract base class defining minigame interface
  - `TimerService.cs` - Session timing and elapsed time tracking
- **`Minigames/`** - Individual training exercises (WarioWare-style)
  - `AntiAirController.cs` - Anti-air reaction timing minigame implementation
  - `TestMinigame.cs` - Basic minigame template for development
- **`Telemetry/`** - Data collection and logging
  - `TelemetryEvent.cs` - Event data structure definition
  - `TelemetryLogger.cs` - CSV file logging implementation
  - `TelemetrySchema.cs` - Event type constants and schema definitions
- **`UI/`** - User interface components (currently empty)

### `/Scenes/` - Godot Scene Files
- `Main.tscn` - Primary application scene
- `Minigames/AntiAir.tscn` - Anti-air minigame scene layout

### `/Data/` - Runtime Data Storage
- `telemetry/` - CSV files containing session performance data

### External Analytics (Python)
- Located in separate `analytics/` directory at solution level
- File-based exchange with Godot telemetry system
- ML-assisted performance analysis

## Core Architecture Patterns

### Minigame System
- Abstract base class pattern with `MinigameBase`
- WarioWare-style short, focused training exercises
- Dependency injection for telemetry and timer services
- Callback-based lifecycle management through `RequestEnd` action

### Session Management
- Single session per application run with unique GUID identifier
- Centralized service initialization and minigame orchestration
- Automatic telemetry session setup and data directory creation

### Telemetry Architecture
- Event-driven data collection with structured JSON payloads
- CSV export format for external analysis tools
- File-based exchange with Python ML analytics
- Timestamp-based performance measurement using session-relative timing

### Component Relationships
```
GameSession (orchestrator)
├── TelemetryLogger (data collection)
├── TimerService (timing)
└── MinigameBase implementations (WarioWare-style exercises)
    └── AntiAirController (specific minigame)
```

## Development Constraints
- **Phase-Gated**: Work only on currently active phase
- **Minimal Design**: Abstract visual style
- **No Multiplayer**: Single-player focused
- **File-Based ML**: Python analytics via CSV exchange