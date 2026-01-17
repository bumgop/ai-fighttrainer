# PROJECT_STATE.md

## Project Overview

This project is a **WarioWare-style fighting game training and analytics system**. It is **not** a full fighting game. Instead, it consists of short, standalone minigames designed to teach and measure specific fighting game fundamentals.

The primary purpose of the project is to:
- Collect structured player telemetry during gameplay
- Analyze player performance using simple, explainable ML techniques
- Provide actionable feedback on player strengths, weaknesses, and tendencies

The project is being built as a **solo, portfolio-focused MVP** demonstrating:
- Software engineering fundamentals
- Data collection and analytics pipelines
- ML-assisted player modeling

The system is intentionally minimalist in visuals and scope to prioritize correctness, clarity, and analyzability.

---

## Current Goals (Phase-Gated)

**Immediate goal (current phase):**
- Establish a stable, reusable gameplay + telemetry foundation
- Fully implement and validate the first minigame (Reaction & Anti-Air Test)

**Near-term goals (next phases):**
- Rapidly implement remaining MVP minigames using the same pattern
- Ensure all minigames emit clean, comparable telemetry

**Explicitly NOT current goals:**
- ML model training or deployment
- Advanced UI/visual polish
- Player-facing analytics dashboards

---

## Implemented Systems

### 1. Project & Environment Setup
- Godot 4.x Mono project created and verified
- C# (.NET) scripting pipeline confirmed working
- Folder structure established for core systems, minigames, telemetry, and UI

### 2. Core Game Systems (Partial but Functional)

**GameSession**
- Owns session lifecycle
- Generates a unique session ID
- Starts and ends minigames
- Centralizes telemetry emission for lifecycle events

**MinigameBase (Abstract Contract)**
- Enforces a consistent minigame lifecycle
- Injects shared services (TelemetryLogger, TimerService)
- Uses a callback-based `RequestEnd` mechanism to avoid lifecycle ownership conflicts

**TimerService**
- Provides a session-level clock
- All timestamps are derived from a single source

### 3. Telemetry System (MVP-Complete)

**TelemetryEvent (Schema)**
- session_id
- minigame_id
- event_type
- timestamp_ms
- payload_json

**TelemetryLogger**
- File-based CSV logging
- One CSV file per session
- Append-only, human-readable, pandas-friendly format

**TelemetryEventTypes**
- Defined string constants for core lifecycle events

### 4. Reaction & Anti-Air Minigame (Timing-Window MVP)

**Gameplay Logic**
- Threat object approaches on a simple linear path
- Visual state communicates timing (red = too early, green = correct window)
- Player input evaluated relative to a timing window

**Logged Outcomes**
- success
- early
- late
- missed

**Logged Metrics (per trial)**
- result category
- timing_ms (nullable, window-relative)

This minigame serves as a **canonical implementation pattern** for all remaining MVP minigames, alongside the Hit-Confirm minigame which demonstrates decision-making mechanics.

### 5. Hit-Confirm Minigame (Decision-Making MVP)

**Gameplay Logic**
- Visual cue shows either "HIT" (green) or "BLOCK" (red) state
- Player has 500ms window to decide whether to attack with front punch
- Random delay before cue appears to prevent anticipation

**Logged Outcomes**
- correct_hit_confirm (attack on hit state)
- false_hit_confirm (attack on block state)
- missed_hit_confirm (no attack on hit state)
- correct_block (no attack on block state)

**Logged Metrics (per trial)**
- outcome category
- timing_ms (reaction time from cue to input)
- was_hit_state (boolean for analysis)

This minigame validates decision-making under uncertainty and input discipline.

---

## Known Gaps / TODOs

### Gameplay
- Implement remaining MVP minigames:
  - Whiff Punish Timing
  - Defense Under Pressure

### Telemetry
- Standardize event naming across all minigames
- Define a minimal shared schema for "result" events across drills

### Analytics / ML (Not Started Yet)
- Telemetry ingestion scripts (Python)
- Feature extraction per minigame
- Player profiling / clustering
- Weakness classification
- Trend tracking over time

### UI / Feedback
- Results summary UI
- Session-level feedback presentation
- Visualization of trends and weaknesses

---

## Assumptions Made So Far

- All analytics and ML will be **offline** and file-based for MVP
- CSV is sufficient as a primary telemetry format
- Per-session analysis is acceptable for MVP (cross-session aggregation later)
- Simple, explainable ML models are preferred over complex approaches
- Visual fidelity is secondary to data quality

---

## Locked Technical Decisions

These decisions are considered **final for MVP**:

- Engine: Godot 4.x Mono
- Language: C# for gameplay and systems
- Analytics/ML: Python (numpy, pandas, scikit-learn)
- Data exchange: File-based CSV / JSON
- No runtime Python integration
- No multiplayer or online features
- No full fighting game mechanics
- Minigames must:
  - Be standalone
  - Share core systems
  - Emit structured telemetry
