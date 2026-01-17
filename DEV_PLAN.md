# Development Plan

This document defines a **phase-gated development plan** for the project:
**Adaptive Fighting Game Training System (WarioWare-Style Minigames)**

Progression through phases requires **explicit approval**.
No phase is entered implicitly.

---

## Phase 0 — Project Initialization & Planning

### Objective
Establish a clean technical foundation, shared understanding, and development structure before writing gameplay or ML code.

This phase ensures:
- Tooling is set up correctly
- Architectural intent is documented
- Scope is locked
- Future phases can be executed without ambiguity

---

### Deliverables

#### 1. Repository & Tooling
- Git repository initialized
- Godot 4.x Mono (C#) project created
- Project builds and runs successfully in an empty state

#### 2. Core Documentation Files
The following files must exist at repo root:

- `PROJECT_STATE.md`
  - Living snapshot of the project’s current state
- `ARCHITECTURE.md`
  - High-level system design and responsibilities
- `DEV_PLAN.md`
  - This phase-gated development plan

#### 3. Locked Constraints
- Engine: Godot 4.x Mono
- Language: C#
- ML stack: Python (numpy, pandas, scikit-learn)
- Data exchange: File-based (CSV / JSON) for MVP
- Visual style: Minimal / abstract
- Scope limited strictly to MVP minigames and analytics

#### 4. Phase Structure Defined
- All major development phases outlined at a high level
- Only Phase 1 is detailed after approval
- Later phases remain summaries only

---

### Non-Goals (Phase 0)
- No gameplay implementation
- No minigames
- No ML models
- No UI polish
- No refactoring discussions

---

### Acceptance Criteria
Phase 0 is considered complete when:
- Project opens and runs in Godot without errors
- All documentation files exist and are populated
- Development phases are clearly defined
- The next phase can begin without ambiguity

---

### Status
✅ Complete

---

## Phase 1 — Core Runtime & Telemetry Foundations

### Objective
Create the minimal runtime systems required for all minigames to function consistently and to generate analyzable data.

This phase establishes the **technical backbone** shared by all gameplay content.

---

### Deliverables

#### 1. Input Abstraction
- Centralized input handling in C#
- Discrete actions (e.g. confirm / block / attack) abstracted from raw key presses
- Minigames consume input via a shared interface

#### 2. Session & Attempt Lifecycle
- Explicit minigame session start
- Explicit attempt start / end
- Explicit session end

#### 3. Telemetry Core
- Event-based telemetry system
- Standard event structure:
  - timestamp
  - minigame_id
  - attempt_id
  - event_type
  - event_payload

#### 4. File-Based Data Export
- CSV or JSON output per session
- Deterministic file naming
- Human-readable and ML-friendly structure

---

### Non-Goals (Phase 1)
- No ML models
- No analytics dashboards
- No performance optimization
- No balancing
- No cross-minigame feedback logic

---

### Acceptance Criteria
Phase 1 is considered complete when:
- A minigame can run using shared systems
- Player input is captured consistently
- Telemetry events are recorded and exported to disk
- Data files can be loaded into pandas without cleanup

---

### Status
✅ Complete

---

## Phase 2 — First MVP Minigame: Anti-Air Reaction & Timing

### Objective
Implement the first representative MVP minigame that validates:
- Shared runtime systems
- Telemetry capture quality
- Timing-based skill measurement (not pure reaction)

This minigame serves as the **reference implementation** for all future minigames.

---

### Deliverables

#### 1. Anti-Air Timing Minigame
- Abstract visual representation (rectangles / shapes)
- Threat entity performs a jump-in arc toward the player
- Clear timing window for valid anti-air input
- Player action evaluated against timing window

#### 2. Metrics Captured
- Reaction latency (jump start → first input)
- Timing accuracy (distance from optimal window)
- Success / failure classification
- Early input detection
- Late input detection
- Missed input detection

#### 3. Telemetry Integration
- All attempts logged via shared telemetry system
- Metrics emitted as structured payloads

---

### Non-Goals (Phase 2)
- No difficulty scaling
- No player feedback summaries
- No ML inference
- No visual polish
- No multiple threat types

---

### Acceptance Criteria
Phase 2 is considered complete when:
- The minigame runs start-to-finish without manual intervention
- All defined metrics are recorded correctly
- Session export produces clean, analyzable data
- The minigame reflects both **reaction** and **timing** skill

---

### Status
✅ Complete

---

## Phase 3 — Minigame Implementation (Gameplay + Telemetry)
Phase 3 is broken into strictly ordered sub-phases. Each sub-phase implements one additional minigame, fully wired into the shared input, telemetry, and session systems.
No new minigame may begin until the previous sub-phase has passed acceptance.

---

### Phase 3.1 — Hit-Confirm Minigame

#### Objective
Implement a minigame that evaluates:
- Player decision-making under uncertainty
- Input discipline (confirm vs autopilot)
- Ability to withhold action on non-confirmed hits

This minigame establishes how branching outcomes are handled in telemetry.

#### Scope
- Visual cue indicating "hit" or "block" state
- Player attack input window
- Distinct outcomes for:
	- Correct hit-confirm
	- False hit-confirm
	- Missed hit-confirm

#### Deliverables
- Standalone playable minigame scene
- Shared input system integration
- Per-attempt telemetry records
- Automatic minigame completion logic

#### Non-Goals
- No combo systems
- No variable hit-stun modeling
- No difficulty scaling

#### Acceptance Criteria
- Player outcomes are unambigious and repeatable
- Telemetry cleanly distinguishes decision errors
- Minigame end is reliably triggered

#### Status
⏳ In Progress

---

### Phase 3.2 - Whiff Punish Minigame
(After Phase 3.1 acceptance))
#### Status
❌ Not Started

---

### Phase 3.3 - Defense Under Pressure Minigame
(After Phase 3.2 acceptance)))
#### Status
❌ Not Started

---

## Phase 4 — Analytics & ML (Offline)

### Objective
Analyze collected telemetry to produce explainable player insights.

---

### Scope Summary
- Data ingestion with pandas
- Feature extraction per minigame
- Player clustering (K-Means / GMM)
- Weakness prediction (logistic regression or decision trees)
- Trend analysis over time

---

### Status
❌ Not Started

---

## Phase 5 — Player Feedback & Reporting

### Objective
Convert analytics output into clear, actionable player-facing feedback.

---

### Scope Summary
- Text-based feedback summaries
- Weakness callouts
- Improvement trends
- No real-time inference (offline only)

---

### Status
❌ Not Started

