# Train Your Kombat - Technology Stack

## Core Technologies
- **Game Engine**: Godot 4.x Mono with C# support
- **Programming Language**: C# with .NET 8.0 target framework
- **Platform**: Cross-platform (GL Compatibility renderer)
- **ML Analytics**: Python (file-based exchange with Godot)

## Project Configuration
- **Assembly Name**: TrainYourKombat
- **SDK**: Godot.NET.Sdk/4.5.1
- **Dynamic Loading**: Enabled for runtime flexibility
- **Android Support**: .NET 9.0 target when building for Android

## Input System
- **Front Punch**: J key (physical keycode 74)
- **Back Punch**: I key (physical keycode 73)  
- **Front Kick**: K key (physical keycode 75)
- **Back Kick**: L key (physical keycode 76)
- **Deadzone**: 0.2 for all inputs

## Dependencies
- **System.Text.Json**: JSON serialization for telemetry payloads
- **System.IO**: File operations for CSV telemetry logging
- **Godot Core**: Scene management, input handling, and rendering

## Development Commands
- **Build**: Use Godot editor or `dotnet build` in project directory
- **Run**: Launch through Godot editor or export executable
- **Debug**: Godot editor provides integrated debugging for C# scripts

## File Structure Standards
- **Scripts**: `.cs` files with corresponding `.cs.uid` Godot metadata
- **Scenes**: `.tscn` files for Godot scene definitions
- **Data**: Runtime-generated CSV files in `user://telemetry/` directory
- **Configuration**: `.editorconfig` for code formatting standards

## Build Output
- **Debug**: Compiled to `.godot/mono/temp/bin/Debug/`
- **Assembly**: `TrainYourKombat.dll` with PDB debug symbols
- **Runtime Config**: JSON configuration for .NET runtime settings

## Design Constraints
- **Visual Style**: Minimal and abstract
- **No Multiplayer**: Single-player focused
- **No Scope Expansion**: Without approval