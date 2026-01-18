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
✅ Complete

---

### Phase 3.2 - Whiff Punish Minigame

#### Objective
Implement a minigame that evaluates:
- Player ability to recognize and punish whiffed attacks
- Ability to time a punish to land during recovery frames
- Avoidance of premature or late punish attempts

This is not reaction-only and decision-only; it is temporal opportunity recognition.

#### Scope
- Visual cue indicating enemy startup, active, and recovery frames
- Player attack input window during recovery frames
- Distinct outcomes for:
	- Correct whiff punish (attack during recovery)
	- Early whiff punish (attack during startup)
	- Unsafe whiff punish (attack during active)
	- Late whiff punish (attack after recovery)
	- Missed punish (no attack at all)

#### Deliverables

##### 1. Whiff Punish Minigame
- Abstract visual representation (rectangles / shapes)
- Enemy entity performs an attack with clear frame states after a random delay
- Player attack input window during recovery frames
- Player action evaluated against timing windows
- Minigame completion logic

##### 2. Metrics Captured
- outcome (listed above)
- input_time_ms (nullable)
- phase_at_input (startup / active / recovery / post-recovery / no input)
- window_offset_ms (time difference from optimal punish window)
	- Nullable if no input

##### 3. Telemetry Integration
- All attempts logged via shared telemetry system
- Per-attempt telemetry records

#### Non-Goals
- No hitstun/frame advantage modeling
- No movement/spacing mechanics
- No adaptive timing windows
- No difficulty scaling
- No UI polish

#### Acceptance Criteria
- Player outcomes are unambigious and repeatable
- All attempts emit exactly one result event
- Early/correct/late/missed cases are distinguishable in telemetry
- Timing metrics are internally consistent with TimerService
- No new core systems are introduced

#### Status
✅ Complete

---

### Phase 3.3 - Defense Under Pressure Minigame (Mixup Blocking)

#### Objective
Implement a minigame that evaluates:
- Player recognition of attack types
- Correct defensive input selection under time pressure
- Player ability to recognize attack strings and block accordingly

This minigame introduces sequential decision pressure and tests defensive fundamentals rather than reaction speed alone.

#### Deliverables

##### 1. Defense Under Pressure Minigame
- Abstract visual representation of incoming attacks
- Predefined attack strings (2-3 hits per string)
- Randomized selection of attack strings per trial
- Each attack clearly labeled and color-coded:
 	- Low
	- Mid
	- High
	- Overhead

##### 2. Blocking Rules Implemented (MVP)
- Mid: blocked by Stand Block or Crouch Block
- Low: blocked by Crouch Block
- High: blocked by Stand Block or Crouch Block or evaded with crouch
- Overhead: blocked by Stand Block only

##### 3. Timing Model
- Each attack has a startup window before impack
- Startup speeds (fast -> slow):
 	- Low
	- High
	- Mid
	- Overhead
- Player input evaluated only during the active "impact" window
- Failure to input defaults to "no block"

##### 4. Metrics Captured (Per Hit)
- attack_type
- expected_defense
- player_defense_input
- outcome:
	- correct_block
	- incorrect_block
	- correct_evade
	- hit_taken
- input_time_ms (relative to attack start)
- attack_index_in_string 

##### 5. String-Level Metrics
- total_hits (number of attacks in string)
- successful_defenses (number of hits defended correctly)
- string_success (all hits defended correctly)

##### 6. Telemetry Integration
- One telemetry event per attack
- One summary event per string
- Logged via shared telemetry system
- CSV output consistent with prior minigames

#### Non-Goals (Phase 3.3)
- No guard meter or stamina
- No chip damage
- No pushback or spacing
- No adaptive or learning-based mixups
- No difficulty scaling
- No UI or animation polish

#### Acceptance Criteria
Phase 3.3 is considered complete when:
- The minigame runs start-to-finish without manual intervention
- All attack types are visually distinct and readable
- Defensive outcomes are unambiguous and repeatable
- Multi-hit strings resolve deterministically
- Telemetry correctly records per-hit and per-string metrics
- CSV data can clearly distinguish success and failure cases

#### Status
✅ Complete

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

