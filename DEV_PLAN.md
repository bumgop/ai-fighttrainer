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

✅ Complete

---

## Phase 5 — Analytics & ML Pipeline (Offline)

### Objective

Convert raw telemetry generated by MVP minigames into:
* Structured datasets
* Interpretable features
* Explainable player models
* Actionable weakness signals

All analysis is offline, file-based, and post-session.

This phase proves the telemetry was worth capturing.

---

### Phase 5.1 — Telemetry Aggregation and Validation

#### Objective

Create a Python pipeline that:
* Loads raw telemetry exports
* Validates schema and integrity
* Reconstructs sessions and attempts
* Flags malformed or incomplete data

No feature engineering or modeling yet.

---

#### Deliverables

##### 1. Python Environment Setup
* Isolated environment
* Explicit dependency versions
* Reproducible execution

##### 2. Telemetry Loader
* Loads CSV / JSON files from disk
* Supports multiple sessions
* Preserves raw fields

##### 3. Schema Validation
* Required columns present
* Correct data types
* Valid enum values (event_type, minigame_id, etc.)

##### 4. Structural Validation
* Sessions have:
	* Start
	* Attempts
	* End
* Attempt IDs are consistent
* Timestamps are monotonic per session

##### 5. Validation Report
* Summary counts
* Warnings for anomalies
* Hard failures for invalid files

---

### Non-Goals

* No ML
* No aggregation
* No normalization
* No plots
* No player-facing output

---

### Acceptance Criteria

Phase 5.1 is considered complete when:
* Telemetry files load without manual cleanup
* Invalid files are detected automatically
* Session and attempt structures can be reconstructed deterministically
* The data is trustworthy enough to model on it

---

### Status

✅ Complete

---

### Phase 5.2 — Feature Engineering (Skill-Level Metrics)

#### Objective

Transform validated raw telemetry into structured, interpretable features that represent player skill across minigames.

This phase answers: "What numbers actually represent a player's fundamentals?"

---

#### Deliverables

##### 1. Per-Attempt Feature Extraction
For each minigame attempt, derive:
* Outcome flags (success / failure / partial)
* Timing-relative metrics (e.g., error from optimal window)
* Decision error indicators (e.g., false confirm, wrong block)
These must be derived, not copied.

##### 2. Per-Session Aggregation
Aggregate attempt-level features into session-level metrics:
* Means
* Medians
* Variance / consistency indicators
* Error rates (per category)
Each session becomes one row in a dataset.

##### 3. Per-Minigame Skill Vectors
For each session:
* Producs one feature vector per minigame
* Prefix or namespace features by minigame_id
* Missing minigames are allowed but explicit (NaN)

##### 4. Feature Dictionary
A documented mapping:
* Feature name → description
* Units
* Expected ranges
* Interpretation
This is critical for explainability later.

---

### Non-Goals

* No ML modeling
* No clustering
* No labels like "good" or "bad"
* No normalization across players

---

### Acceptance Criteria

Phase 5.2 is considered complete when:
* A single session can be transformed into a clean feature row
* Features match gameplay intent
* Feature meanings can be explained without referencing code
* Output is suitable for scikit-learn ingestion

---

### Status

✅ Complete

---

### Phase 5.3 — Player Profiling (Unsupervised Clustering)

#### Objective

Identify natural player archetypes using unsupervised learning on engineered features.

This phase answers: "What kinds of players emerge from the data?"

---

#### Deliverables

##### 1. Feature Selection for Clustering
* Subset features that reflect style, not performance ceiling
* Avoid redundant or highly correlated features
* Justify inclusion / exclusion

##### 2. Clustering Models
Implement and compare:
* K-Means
* Gaussian Mixture Models
Evaluate using:
* Silhouette Score
* Cluster stability across runs

##### 3. Cluster Interpretation
For each cluster:
* Compute centroid feature values
* Describe behavioral tendencies
	* E.g., "Cluster 2 reacts quickly but has high timing variance"

##### 4. Cluster Assignment Output
* Each session / player assigned a cluster ID
* Output saved as CSV / JSON

---

### Non-Goals

* No automatic recommendations
* No visualization dashoboards
* No real-time inference
* No deep models

---

### Acceptance Criteria

Phase 5.3 is considered complete when:
* Clusters are reproducible
* Each cluster has a defensible interpretation
* You can explain why a player belongs to a cluster based on features

---

### Status

✅ Complete

---

### Phase 5.4 — Weakness Classification (Supervised, Explainable)

#### Objective

Product specific fundamental weaknesses using supervised, interpretable models.

This phase answers: "Given this player's data, what are they most likely struggling with?"

---

#### Deliverables

##### 1. Weakness Definitions
Define binary or ordinal labels such as:
* "Inconsistent timing"
* "Poor mixup defense"
* "Late punish tendency"
Labels must be derived from thresholds in Phase 5.2 features.

##### 2. Supervised Models
Implement:
* Logistic Regression
* Decision Tree (shallow)
Train per-weakness or multi-label as appropriate.

##### 3. Model Explainability
* Feature weights (logistic)
* Decision paths (trees)
* Clear linkage to gameplay behavior

##### 4. Weakness Prediction Output
* Weakness probabilities or flags
* Confidence scores
* Saved to disk

---

### Non-Goals

* No ensemble methods
* No neural networks
* No optimization for leaderboard-style accuracy
* No automated coaching

---

### Acceptance Criteria

Phase 5.4 is considered complete when:
* Weakness predictions align with intuitive gameplay observations
* Models can be explained line-by-line
* False positives are understandable, not mysterious

---

### Status

✅ Complete

---

### Phase 5.5 — Trend Analysis and Improvement Tracking

#### Objective

Analyze how player skill changes over time, not just static ability.

This phase answers: "Is the player improving, stagnating, or regressing?"

---

#### Deliverables

##### 1. Session Ordering
* Sessions ordered by timestamp
* Gaps allowed
* Multiple sessions per day allowed

##### 2. Metric Smoothing
Apply:
* Rolling averages
* Exponential smoothing
* Simple deltas (early vs late)

##### 3. Trend Classification
For key metrics:
* Improving
* Flat
* Regressing
With thresholds explicitly defined.

##### 4. Trend Output
* Per-metric trend summaries
* Stored in machine-readable format
* Ready for UI consumption in Phase 6

---

### Non-Goals

* No forecasting
* No goal setting
* No player comparison
* No live graphs

---

### Acceptance Criteria

Phase 5.5 is considered complete when:
* Trends are stable across noisy sessions
* Improvement signals are intuitive
* Outputs can directly feed player feedback

---

### Status

✅ Complete

---

## Phase 6 - Player Insight, Feedback, and Explainability

### Objective

Translate analytics and ML outputs into clear, trustworth, player-facing insight that explains:
* What the player struggles with
* Why the system believes so
* How the player can improve

This phase closes the loop from data capture to actionable feedback.

---

### Phase 6.1 — Insight Contract and Vocabulary

#### Objective

Define a shared language between analyticsm ML outputs, and player-facing feedback.

This prevents vague or hand-wavy explanations.

---

#### Deliverables

##### 1. Insight Taxonomy
A fixed set of insight types, for example:
* Timing inconsistency
* Late reactions
* Poor mixup defense
* High variance decision-making
Each insight must map directly to:
* One or more engineered features
* One or more ML outputs

##### 2. Vocabulary Definitions
For each insight type, define:
* Plain-language definitions
* What behavior causes it
* What metrics support it
This vocabulary becomes canonical.

##### 3. Insight Data Structure
Define a structured format (JSON or C# model) such as:
* insight_id
* severity / confidence
* contributing_factors
* explanation_text

---

### Non-Goals

* No UI
* No visuals
* No generation logic
* No prioritization

---

### Acceptance Criteria

Phase 6.1 is considered complete when:
* Every ML output can be expressed as a named insight
* Every insight has a clear definition
* No insight requires guessing to explain

---

### Status

✅ Complete

---

### Phase 6.2 — Insight Generation Logic

#### Objective

Convert ML outputs into concrete insight objects using deterministic logic.

This phase answers: "Given the data and models, what should we say?"

---

#### Deliverables

##### 1. Mapping Logic
Explicit rules that map:
* Cluster assignments
* Weakness probabilities
* Trend classifications
to insight objects defined in Phase 6.1.

##### 2. Confidence and Severity Handling
* Normalize confidence levels
* Avoid binary "good/bad" framing
* Support "emerging weakness" vs "established weakness"

##### 3. Cross-Minigame Attribution
Insights should reference:
* Which minigames contributed
* Which behaviors triggered flags

---

### Non-Goals

* No natural language generation models
* No UI rendering
* No player customization
* No recommendations

---

### Acceptance Criteria

Phase 6.2 is considered complete when:
* Insights are generated reproducibly from analytics outputs
* Each insight is traceable to specific data points
* False positives can be explained

---

### Status

⏳ In Progress

---

### Phase 6.3 — Player-Facing Feedback Presentation

#### Objective

Present insights to the palyer in a minimal, readable, non-overwhelming format.

This phase answers: "How does a human consume this information?"

---

#### Deliverables

##### 1. Feedback Surface
One or more of:
* End-of-session summary screen
* Post-minigame insight panel
* Simple scrollable list
Text-first. Visuals optional.

##### 2. Insight Prioritization
* Limit number of insights shown at once
* Order by severity or confidence
* Avoid overwhelming the player

##### 3. Supporting Context
For each insight:
* Brief explanation
* Referenced minigames or behaviors
* Optional metric values (if helpful)

---

### Non-Goals

* No charts unless strictly necessary
* No historical graphs
* No gamification
* No progress bars

---

### Acceptance Criteria

Phase 6.3 is considered complete when:
* A player can understand their feedback in under 60 seconds
* No insight feels arbitrary
* Feedback aligns with player intuition

---

### Status

❌ Not Started

---

### Phase 6.4 — Actionable Guidance and Framing

#### Objective

Convert insights into clear, bounded next steps without turning the system into a coach simulator.

This phase answers: "What should the player do next?"

---

#### Deliverables

##### 1. Recommendation Templates
For each insight:
* 1-2 actionable suggestions
* Referencing existing minigames only
Example: "Spend time on the Whiff Punish minigame focusing on late recovery windows."

##### 2. Framing and Tone
* Non-judgemental
* Skill-focused
* Improvement-oriented
No scoring or ranking

##### 3. Insight-to-Action Mapping
Explicit link between:
* Insight -> Recommendation
* Metric -> Suggested focus

---

### Non-Goals

* No adaptive training plans
* No scheduling
* No difficulty adjustment
* No personalization beyond insight mapping

---

### Acceptance Criteria

Phase 6.4 is considered complete when:
* Every surfaced insight includes a clear next step
* Recommendations are realistic and bounded
* Players understand why the recommendation exists

---

### Status

❌ Not Started


