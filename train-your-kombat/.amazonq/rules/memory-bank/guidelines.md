# Train Your Kombat - Development Guidelines

## Project Context and Constraints

### Development Workflow
- **Phase-Gated Development**: Work ONLY on currently active phase
- **Ignore Future Phases**: Unless explicitly instructed
- **Ask for Clarification**: If instructions conflict with documentation

### Core Constraints
- **Engine**: Godot 4.x Mono
- **Language**: C#
- **ML Implementation**: Later via Python (file-based exchange)
- **Visual Style**: Minimal and abstract
- **No Multiplayer**: Single-player focused
- **No Scope Expansion**: Without approval

### Execution Rules
1. Follow instructions literally
2. Prefer minimal, clear implementations
3. Avoid speculative abstractions
4. Avoid premature optimization

## Code Quality Standards

### Naming Conventions
- **Classes**: PascalCase (e.g., `AntiAirController`, `TelemetryLogger`)
- **Methods**: PascalCase (e.g., `StartMinigame`, `LogEvent`)
- **Properties**: PascalCase (e.g., `MinigameId`)
- **Private Fields**: camelCase with underscore prefix (e.g., `_threat`, `_sessionId`)
- **Constants**: PascalCase (e.g., `ThreatSpeed`, `WindowDurationMs`)
- **Local Variables**: camelCase (e.g., `timingMs`, `payloadEscaped`)

### Class Structure Patterns
- **Godot Classes**: Always use `public partial class` with Godot inheritance
- **Data Classes**: Use simple `public class` for POCOs (e.g., `TelemetryEvent`)
- **Static Classes**: Use for constants and utility methods (e.g., `TelemetryEventTypes`)
- **Abstract Classes**: Define contracts with protected members for inheritance

### Field Organization
1. Private fields grouped at top of class
2. Constants defined with appropriate access modifiers
3. Properties and methods follow logical grouping
4. Override methods clearly marked with `public override`

## Architectural Patterns

### Dependency Injection Pattern
```csharp
public virtual void Initialize(TelemetryLogger telemetry, TimerService timer, Action requestEnd)
{
    Telemetry = telemetry;
    Timer = timer;
    RequestEnd = requestEnd;
}
```
- Services injected through Initialize method rather than constructor
- Protected fields store injected dependencies for subclass access
- Action delegates used for callback communication

### Abstract Base Class Pattern
```csharp
public abstract partial class MinigameBase : Node
{
    public abstract string MinigameId { get; }
    public abstract void StartMinigame();
    public abstract void EndMinigame();
}
```
- Abstract properties for required implementations
- Virtual methods for optional overrides
- Protected members for shared functionality

### Event-Driven Telemetry
```csharp
Telemetry.LogEvent(new TelemetryEvent
{
    SessionId = _sessionId,
    MinigameId = minigame.MinigameId,
    EventType = TelemetryEventTypes.MinigameStart,
    TimestampMs = _timer.GetElapsedMs(),
    PayloadJson = "{}"
});
```
- Structured event objects with consistent properties
- JSON serialization for complex payload data
- Timestamp-based performance measurement

## Godot-Specific Conventions

### Node Access Pattern
```csharp
_threat = GetNode<ColorRect>("Threat");
_label = GetNode<Label>("Label");
```
- Use generic GetNode<T> for type safety
- Store node references in private fields during _Ready()
- Use string literals for node paths

### Input Handling
```csharp
if (Input.IsActionJustPressed("front_punch"))
{
    // Handle input
}
```
- Use action names defined in project settings
- Check for "JustPressed" for single-frame input detection
- Implement input guards to prevent duplicate processing

### Timer and Physics Integration
```csharp
public override void _Process(double delta)
{
    if (!_active) return;
    // Process logic here
}
```
- Early return pattern for inactive states
- Use delta time for frame-rate independent calculations
- Separate movement and input logic into distinct methods

## Data Management Patterns

### CSV Export Format
```csharp
var line = $"{evt.SessionId},{evt.MinigameId},{evt.EventType},{evt.TimestampMs},\"{payloadEscaped}\"\n";
```
- Comma-separated values with quoted JSON payloads
- Proper CSV escaping for embedded quotes
- Header row definition for data structure

### JSON Serialization
```csharp
PayloadJson = JsonSerializer.Serialize(new
{
    outcome = result,
    timing_ms = timingMs
})
```
- Anonymous objects for simple data structures
- Snake_case property names for consistency
- Nullable types for optional timing data

### File Path Management
```csharp
string relativePath = $"user://telemetry/{sessionId}.csv";
string absolutePath = ProjectSettings.GlobalizePath(relativePath);
```
- Use Godot's user:// protocol for data persistence
- Convert to absolute paths for System.IO operations
- Create directories as needed before file operations

## Error Handling and State Management

### Null Checking Pattern
```csharp
if (_activeMinigame == null)
{
    return;
}
```
- Early return for null state validation
- Guard clauses to prevent invalid operations
- Boolean flags for state management (_active, _inputHandled)

### State Reset Pattern
```csharp
_inputHandled = false;
_active = false;
_windowStartMs = 0;
```
- Explicit state initialization in start methods
- Clear boolean flags for control flow
- Reset timing variables to default values