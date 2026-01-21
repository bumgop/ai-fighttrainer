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

* Tooling is set up correctly
* Architectural intent is documented
* Scope is locked
* Future phases can be executed without ambiguity

---

### Deliverables

#### 1. Repository & Tooling

* Git repository initialized
* Godot 4.x Mono (C#) project created
* Project builds and runs successfully in an empty state

#### 2. Core Documentation Files

The following files must exist at repo root:

* `PROJECT_STATE.md` — Living snapshot of the project’s current state
* `ARCHITECTURE.md` — High-level system design and responsibilities
* `DEV_PLAN.md` — This phase-gated development plan

#### 3. Locked Constraints

* Engine: Godot 4.x Mono
* Language: C#
* ML stack: Python (numpy, pandas, scikit-learn)
* Data exchange: File-based (CSV / JSON) for MVP
* Visual style: Minimal / abstract
* Scope limited strictly to MVP minigames and analytics

---

### Non-Goals

* No gameplay implementation
* No minigames
* No ML models
* No UI polish
* No refactoring discussions

---

### Acceptance Criteria

Phase 0 is considered complete when:

* Project opens and runs in Godot without errors
* All documentation files exist and are populated
* Development phases are clearly defined
* The next phase can begin without ambiguity

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

* Centralized input handling in C#
* Discrete actions (confirm / block / attack) abstracted from raw key presses
* Minigames consume input via a shared interface

#### 2. Session & Attempt Lifecycle

* Explicit minigame session start
* Explicit attempt start / end
* Explicit session end

#### 3. Telemetry Core

* Event-based telemetry system
* Standard event structure:

  * timestamp
  * minigame_id
  * attempt_id
  * event_type
  * event_payload

#### 4. File-Based Data Export

* CSV or JSON output per session
* Deterministic file naming
* Human-readable and ML-friendly structure

---

### Non-Goals

* No ML models
* No analytics dashboards
* No performance optimization
* No balancing
* No cross-minigame feedback logic

---

### Acceptance Criteria

Phase 1 is considered complete when:

* A minigame can run using shared systems
* Player input is captured consistently
* Telemetry events are recorded and exported to disk
* Data files can be loaded into pandas without cleanup

---

### Status

✅ Complete

---

## Phase 2 — First MVP Minigame: Anti-Air Reaction & Timing

### Objective

Implement the first representative MVP minigame that validates:

* Shared runtime systems
* Telemetry capture quality
* Timing-based skill measurement (not pure reaction)

This minigame serves as the **reference implementation** for all future minigames.

---

### Deliverables

#### 1. Anti-Air Timing Minigame

* Abstract visual representation (rectangles / shapes)
* Threat entity performs a jump-in arc toward the player
* Clear timing window for valid anti-air input
* Player action evaluated against timing window

#### 2. Metrics Captured

* Reaction latency (jump start → first input)
* Timing accuracy (distance from optimal window)
* Success / failure classification
* Early input detection
* Late input detection
* Missed input detection

#### 3. Telemetry Integration

* All attempts logged via shared telemetry system
* Metrics emitted as structured payloads

---

### Non-Goals

* No difficulty scaling
* No player feedback summaries
* No ML inference
* No visual polish
* No multiple threat types

---

### Acceptance Criteria

Phase 2 is considered complete when:

* The minigame runs start-to-finish without manual intervention
* All defined metrics are recorded correctly
* Session export produces clean, analyzable data
* The minigame reflects both **reaction** and **timing** skill

---

### Status

✅ Complete

---

## Phase 3 — Minigame Implementation (Gameplay + Telemetry)

Phase 3 is broken into strictly ordered sub-phases. Each sub-phase adds **one standalone minigame**, fully wired into the shared input, telemetry, and session systems.

The Reaction & Anti-Air Timing Test was completed in **Phase 2** and is **explicitly excluded** from Phase 3.

No new minigame may begin until the previous sub-phase has passed acceptance.

---

### Phase 3.1 — Hit-Confirm Challenge

#### Objective

Implement a minigame that evaluates:

* Player decision-making under uncertainty
* Input discipline (confirm vs autopilot)
* Ability to withhold action on non-confirmed hits

This minigame establishes how **branching outcomes** are represented in telemetry.

---

#### Deliverables

* Standalone playable scene
* Shared input system integration
* Per-attempt telemetry records
* Automatic minigame completion logic

---

### Non-Goals

* No combo systems
* No variable hit-stun modeling
* No adaptive difficulty

---

### Acceptance Criteria

* Player outcomes are unambiguous and repeatable
* Telemetry cleanly distinguishes decision errors
* Minigame end is reliably triggered

---

### Status

✅ Complete

---

### Phase 3.2 — Whiff Punish Timing

#### Objective

Implement a minigame that evaluates:

* Recognition of whiffed attacks
* Timing a punish during recovery frames
* Avoidance of premature or late punish attempts

This minigame tests **temporal opportunity recognition** rather than pure reaction speed.

---

#### Deliverables

* Standalone playable scene
* Enemy attack with startup, active, and recovery states
* Player attack input window during recovery
* Per-attempt outcome classification
* Shared telemetry integration

---

### Non-Goals

* No hitstun or frame-advantage modeling
* No movement or spacing mechanics
* No adaptive timing windows
* No difficulty scaling
* No UI polish

---

### Acceptance Criteria

* All attempts emit exactly one result event
* Early / correct / late / missed outcomes are distinguishable
* Timing metrics are internally consistent
* No new core systems are introduced

---

### Status

✅ Complete

---

### Phase 3.3 — Defense Under Pressure (Mixup Blocking)

#### Objective

Implement a defensive minigame that evaluates:

* Recognition of attack types
* Correct defensive input selection under time pressure
* Consistency across multi-hit attack strings

This minigame introduces **sequential decision pressure** and defensive fundamentals.

---

#### Deliverables

* Standalone playable scene
* Predefined 2–3 hit attack strings
* Distinct visual indicators for Low / Mid / High / Overhead attacks
* Per-hit and per-string telemetry records

---

### Non-Goals

* No guard meter or stamina
* No chip damage
* No pushback or spacing
* No adaptive mixups
* No difficulty scaling
* No animation or UI polish

---

### Acceptance Criteria

* All attack types are visually distinct and readable
* Defensive outcomes are unambiguous and repeatable
* Multi-hit strings resolve deterministically
* Telemetry cleanly captures per-hit and per-string data

---

### Status

✅ Complete

---

## Phase 4 — Runtime Flow & Menu System

### Objective

Introduce a minimal runtime flow that allows players to:

* Launch the application into a main menu
* Select and start any implemented minigame
* Return to the menu after a minigame completes

This phase improves developer iteration speed and player usability without expanding gameplay scope

---

### Phase 4.1 — Minigame Registry and Metadata

#### Objective

Create a single source of truth describing available minigames that can be queried by runtime systems (menu, launcher, telemetry).

This sub-phase ensures the menu system does not hardcode scenes or logic.

---

#### Deliverables

##### 1. Minigame Descriptor Structure
Define a lightweight data structure containing:
* minigame_id (string, stable)
* display_name (string)
* scene_path (string)
* short_description (string)

##### 2. Central Registry
* A static or singleton registry that:
	* Registers all available minigames at startup
	* Exposes an ordered list for UI cycling
* No dynamic loading or reflection

##### 3. Telemetry Alignment
* Ensure minigame_id used here matches telemetry output exactly
* No renaming or aliasing logic

---

### Non-Goals

* No unlock logic
* No difficulty tiers
* No persistence of player choice
* No runtime discovery

---

### Acceptance Criteria

Phase 4.1 is considered complete when:
* The registry contains all implemented minigames
* Menu code can enumerate minigames without scene knowledge
* Telemetry IDs remain unchanged and valid

---

### Status

✅ Complete

---

### Phase 4.2 — Main Menu Scene (Minigame Selection)

#### Objective

Implement a minimal main menu scene that allows the player to:
* View the currently selected minigame
* Cycle through available minigames
* Launch the selected minigame

This scene is intentionally utilitarian.

---

#### Deliverables

##### 1. Main Menu Scene
* New Godot scene set as project entry point
* Contains:
	* Minigame name label (text only)
	* "Previous" and "Next" buttons to cycle minigames
	* "Start" button to launch selected minigame

##### 2. Selection Logic
* Cycling through registry entries
* Wraparound behavior (last -> first, first -> last)
* No animations or transitions

##### 3. Minigame Launch
* On "Start" button press:
	* Selected minigame scene path is passed to launcher
	* Scene change is initiated

---

### Non-Goals
* No previews beyond text
* No settings menu
* No player profiles
* No mouse/controller rebinding

---

### Acceptance Criteria
Phase 4.2 is considered complete when:
* The player can launch any implemented minigame from the menu
* No editor changes are required to switch minigames
* Scene transitions are stable and repeatable

---

### Status

✅ Complete

---

### Phase 4.3 — Minigame Launch and Return Flow

#### Objective

Standardize how minigames start and end so they can be cleanly embedded in a larger flow

This sub-phase formalizes expectations between:
* Menu
* Minigame
* Session lifecycle

---

#### Deliverables

##### 1. Standardized Minigame Entry
* On scene load:
	* Short delay to give players time to prepare
	* Explicit session start signal
* No reliance on _Ready() timing quirks

##### 2. Minigame Completion Contract
* All minigames must:
	* Signal completion explicitly
	* End their telemetry session clearly

##### 3. Return to Menu
* Post-completion UI:
	* Simple "return to menu" button
* Button triggers scene change back to main menu
* No automatic chaining

---

### Non-Goals

* No score summaries
* No cross-minigame analytics
* No run history
* No auto-restart logic

---

### Acceptance Criteria

Phase 4.3 is considered complete when:
* All minigames start consistently after being launched
* All minigames can return to the main menu
* Telemetry sessions are not cut off or duplicated

---

### Status

⏳ In Progress

---

## Phase 5 — Analytics & ML (Offline)

### Objective

Analyze collected telemetry to produce explainable player insights.

---

### Deliverables

* Data ingestion with pandas
* Feature extraction per minigame
* Player clustering (K-Means or GMM)
* Weakness prediction (logistic regression or decision trees)
* Trend analysis over time

---

### Non-Goals

* No real-time inference
* No online or live services

---

### Acceptance Criteria

* Scripts run end-to-end on exported telemetry
* Outputs are explainable and reproducible

---

### Status

❌ Not Started

---

## Phase 6 — Player Feedback & Reporting

### Objective

Convert analytics output into clear, actionable player-facing feedback.

---

### Deliverables

* Text-based feedback summaries
* Weakness callouts
* Improvement trends over time

---

### Non-Goals

* No real-time inference
* No advanced UI or visualization

---

### Acceptance Criteria

* Feedback is understandable without developer explanation
* Output clearly maps to underlying analytics

---

### Status

❌ Not Started
